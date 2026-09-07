"""
WGI HTTP Server and REST API Backend.
Uses built-in http.server and socketserver for zero external dependencies.
"""

import http.server
import socketserver
import json
import os
import sys
import threading
import subprocess
import pty
import select
import signal
import socket
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional, List

from core.banner import VERSION, WGI_VERSION
from core.registry import registry
from services.config import load_config

PROJECT_ROOT = Path(os.getcwd()).resolve()

# Terminal session storage
TERMINAL_SESSIONS: Dict[str, Dict[str, Any]] = {}
TERMINAL_LOCK = threading.Lock()


class WGIRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP Handler serving REST endpoints and WGI static files."""

    def __init__(self, *args, **kwargs):
        static_dir = Path(__file__).parent / "static"
        super().__init__(*args, directory=str(static_dir), **kwargs)

    def log_message(self, format, *args):
        """Suppress default stdout HTTP access logging to keep terminal clean."""
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/"):
            self.handle_api_get(path, urllib.parse.parse_qs(parsed.query))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body_data = self.rfile.read(length) if length > 0 else b"{}"
        try:
            body = json.loads(body_data.decode("utf-8"))
        except Exception:
            body = {}

        if path.startswith("/api/"):
            self.handle_api_post(path, body)
        else:
            self.send_error(404, "Not Found")

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # Security: Do not allow wildcard cross-origin access
        origin = self.headers.get("Origin", "")
        if origin and ("localhost" in origin or "127.0.0.1" in origin):
            self.send_header("Access-Control-Allow-Origin", origin)
        self.end_headers()
        self.wfile.write(body)

    def handle_api_get(self, path: str, query: Dict[str, List[str]]):
        if path == "/api/status":
            self._send_json({
                "status": "ok",
                "cli_version": VERSION,
                "wgi_version": WGI_VERSION,
                "project_root": str(PROJECT_ROOT)
            })

        elif path == "/api/files":
            files = self.get_project_files()
            self._send_json({"files": files})

        elif path == "/api/file-content":
            rel_path = query.get("path", [""])[0]
            if not rel_path:
                self._send_json({"error": "Path parameter required"}, 400)
                return

            safe_p = self.get_safe_path(rel_path)
            if not safe_p or not safe_p.is_file():
                self._send_json({"error": "File not found or access denied"}, 404)
                return

            if safe_p.suffix.lower() == ".py":
                self._send_json({"error": "Python source files cannot be viewed in WGI viewer"}, 403)
                return

            try:
                content = safe_p.read_text(encoding="utf-8", errors="replace")
                self._send_json({"path": rel_path, "content": content})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        elif path == "/api/commands":
            q = query.get("q", [""])[0]
            cmds = registry.search(q)
            # Make handlers serializable
            res = []
            for c in cmds:
                res.append({
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "category": c.get("category"),
                    "description": c.get("description"),
                    "keywords": c.get("keywords")
                })
            self._send_json({"commands": res})

        elif path == "/api/terminal/output":
            term_id = query.get("id", [""])[0]
            if not term_id or term_id not in TERMINAL_SESSIONS:
                self._send_json({"error": "Invalid terminal ID"}, 404)
                return

            session = TERMINAL_SESSIONS[term_id]
            master_fd = session["master_fd"]
            output = ""

            try:
                while True:
                    r, _, _ = select.select([master_fd], [], [], 0.05)
                    if not r:
                        break
                    data = os.read(master_fd, 4096)
                    if not data:
                        break
                    output += data.decode("utf-8", errors="replace")
            except OSError:
                pass

            self._send_json({"id": term_id, "output": output})

        else:
            self._send_json({"error": "API Endpoint Not Found"}, 404)

    def handle_api_post(self, path: str, body: Dict[str, Any]):
        if path == "/api/terminal/create":
            command = body.get("command", "bash")
            term_id = f"term_{os.urandom(4).hex()}"

            try:
                master_fd, slave_fd = pty.openpty()
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=slave_fd,
                    stdout=slave_fd,
                    stderr=slave_fd,
                    close_fds=True,
                    preexec_fn=os.setsid,
                    cwd=str(PROJECT_ROOT)
                )
                os.close(slave_fd)

                with TERMINAL_LOCK:
                    TERMINAL_SESSIONS[term_id] = {
                        "proc": proc,
                        "master_fd": master_fd
                    }

                self._send_json({"id": term_id, "status": "created"})
            except Exception as e:
                self._send_json({"error": f"Failed to spawn terminal: {e}"}, 500)

        elif path == "/api/terminal/input":
            term_id = body.get("id")
            input_data = body.get("data", "")
            if not term_id or term_id not in TERMINAL_SESSIONS:
                self._send_json({"error": "Invalid terminal ID"}, 404)
                return

            session = TERMINAL_SESSIONS[term_id]
            master_fd = session["master_fd"]
            try:
                os.write(master_fd, input_data.encode("utf-8"))
                self._send_json({"status": "ok"})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        elif path == "/api/terminal/close":
            term_id = body.get("id")
            if term_id in TERMINAL_SESSIONS:
                close_terminal_session(term_id)
            self._send_json({"status": "closed"})

        else:
            self._send_json({"error": "API Endpoint Not Found"}, 404)

    def get_safe_path(self, rel_path: str) -> Optional[Path]:
        p = (PROJECT_ROOT / rel_path).resolve()
        if p == PROJECT_ROOT or PROJECT_ROOT in p.parents:
            return p
        return None

    def get_project_files(self) -> List[Dict[str, Any]]:
        file_tree = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            rel_root = os.path.relpath(root, PROJECT_ROOT)
            if rel_root.startswith(".") and rel_root != ".":
                if rel_root != ".dev":
                    dirs.clear()
                    continue

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in (".md", ".py"):
                    full_p = Path(root) / f
                    rel_p = os.path.relpath(full_p, PROJECT_ROOT)
                    file_tree.append({
                        "name": f,
                        "path": rel_p,
                        "extension": ext,
                        "type": "markdown" if ext == ".md" else "python"
                    })
        return sorted(file_tree, key=lambda x: x["path"])


def close_terminal_session(term_id: str):
    with TERMINAL_LOCK:
        if term_id in TERMINAL_SESSIONS:
            session = TERMINAL_SESSIONS.pop(term_id)
            try:
                os.close(session["master_fd"])
            except OSError:
                pass
            try:
                os.killpg(os.getpgid(session["proc"].pid), signal.SIGTERM)
            except Exception:
                pass


def cleanup_all_terminals():
    with TERMINAL_LOCK:
        term_ids = list(TERMINAL_SESSIONS.keys())
    for tid in term_ids:
        close_terminal_session(tid)


class WGIServer:
    """WGI HTTP Server Manager."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self, auto_open: bool = False):
        # Auto select available port if occupied
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((self.host, self.port))
            sock.close()
        except OSError:
            # Pick auto port
            sock.bind((self.host, 0))
            self.port = sock.getsockname()[1]
            sock.close()

        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            allow_reuse_address = True

        self.httpd = ThreadedTCPServer((self.host, self.port), WGIRequestHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

        url = f"http://{self.host}:{self.port}"
        print(f"\n[WGI] Workstation Graphical Interface started at: {url}")

        if auto_open:
            try:
                import webbrowser
                webbrowser.open(url)
            except Exception:
                pass

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        cleanup_all_terminals()
        print("\n[WGI] Server stopped.")
