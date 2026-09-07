/* Workstation Graphical Interface (WGI) Frontend Script */

let activeZIndex = 100;
let windowCounter = 0;
let openWindows = {};

document.addEventListener('DOMContentLoaded', () => {
  initUI();
  loadProjectFiles();
  restoreUIState();
});

function initUI() {
  // Command Palette trigger
  document.getElementById('btn-command-palette').addEventListener('click', openCommandPalette);

  // New Terminal trigger
  document.getElementById('btn-new-terminal').addEventListener('click', () => {
    createTerminalWindow('Terminal Session');
  });

  // Keybindings (Ctrl+K)
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openCommandPalette();
    }
  });

  // Command Palette input listener
  const searchInput = document.getElementById('palette-search-input');
  searchInput.addEventListener('input', (e) => {
    searchCommands(e.target.value);
  });

  // Modal overlay dismiss
  const modal = document.getElementById('modal-command-palette');
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });
}

/* Load File Tree */
async function loadProjectFiles() {
  const treeContainer = document.getElementById('file-tree');
  try {
    const res = await fetch('/api/files');
    const data = await res.json();

    if (!data.files || data.files.length === 0) {
      treeContainer.innerHTML = '<div class="tree-loading">No supported files found.</div>';
      return;
    }

    treeContainer.innerHTML = '';
    data.files.forEach(file => {
      const item = document.createElement('div');
      item.className = 'tree-item';

      const icon = file.type === 'markdown' ? '📄' : '🐍';
      item.innerHTML = `<span class="tree-icon">${icon}</span> <span>${file.path}</span>`;

      let clickTimer = null;
      item.addEventListener('click', () => {
        if (clickTimer) {
          clearTimeout(clickTimer);
          clickTimer = null;
          // Double click handler
          handleFileAction(file, 'dblclick');
        } else {
          clickTimer = setTimeout(() => {
            clickTimer = null;
            // Single click handler
            document.querySelectorAll('.tree-item').forEach(el => el.classList.remove('selected'));
            item.classList.add('selected');
            handleFileAction(file, 'click');
          }, 250);
        }
      });

      treeContainer.appendChild(item);
    });
  } catch (err) {
    treeContainer.innerHTML = `<div class="tree-loading">Failed to load files: ${err}</div>`;
  }
}

/* Handle File Clicks */
function handleFileAction(file, eventType) {
  if (file.type === 'markdown') {
    openMarkdownWindow(file.path);
  } else if (file.type === 'python') {
    if (eventType === 'dblclick') {
      openPythonLauncherWindow(file.path);
    }
  }
}

/* Window Manager */
function createWindow({ title, width = 640, height = 400, x = 80, y = 60 }) {
  windowCounter++;
  const winId = `win_${windowCounter}_${Date.now()}`;

  // Offset cascaded window position
  const winCount = Object.keys(openWindows).length;
  const winX = x + (winCount * 25) % 200;
  const winY = y + (winCount * 25) % 200;

  const win = document.createElement('div');
  win.id = winId;
  win.className = 'wgi-window active';
  win.style.width = `${width}px`;
  win.style.height = `${height}px`;
  win.style.left = `${winX}px`;
  win.style.top = `${winY}px`;
  win.style.zIndex = ++activeZIndex;

  win.innerHTML = `
    <div class="window-header">
      <span class="window-title">${title}</span>
      <div class="window-controls">
        <button class="win-btn min">—</button>
        <button class="win-btn max">□</button>
        <button class="win-btn close">×</button>
      </div>
    </div>
    <div class="window-body"></div>
  `;

  document.getElementById('windows-container').appendChild(win);

  // Bring to front on click
  win.addEventListener('mousedown', () => bringToFront(winId));

  // Controls listeners
  const header = win.querySelector('.window-header');
  setupDraggable(win, header);

  win.querySelector('.win-btn.min').addEventListener('click', (e) => {
    e.stopPropagation();
    win.classList.toggle('minimized');
    saveUIState();
  });

  win.querySelector('.win-btn.max').addEventListener('click', (e) => {
    e.stopPropagation();
    win.classList.toggle('maximized');
    saveUIState();
  });

  win.querySelector('.win-btn.close').addEventListener('click', (e) => {
    e.stopPropagation();
    closeWindow(winId);
  });

  openWindows[winId] = { id: winId, element: win, title };
  bringToFront(winId);
  saveUIState();

  return { id: winId, body: win.querySelector('.window-body') };
}

function bringToFront(winId) {
  Object.values(openWindows).forEach(w => {
    w.element.classList.remove('active');
  });
  if (openWindows[winId]) {
    openWindows[winId].element.classList.add('active');
    openWindows[winId].element.style.zIndex = ++activeZIndex;
  }
}

function closeWindow(winId) {
  if (openWindows[winId]) {
    // If terminal session inside window, notify backend
    if (openWindows[winId].termId) {
      fetch('/api/terminal/close', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: openWindows[winId].termId })
      });
    }
    openWindows[winId].element.remove();
    delete openWindows[winId];
    saveUIState();
  }
}

/* Draggable Windows Utility */
function setupDraggable(win, header) {
  let isDragging = false;
  let offsetX = 0, offsetY = 0;

  header.addEventListener('mousedown', (e) => {
    if (e.target.classList.contains('win-btn')) return;
    isDragging = true;
    offsetX = e.clientX - win.offsetLeft;
    offsetY = e.clientY - win.offsetTop;
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging || win.classList.contains('maximized')) return;
    win.style.left = `${e.clientX - offsetX}px`;
    win.style.top = `${e.clientY - offsetY}px`;
  });

  document.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      saveUIState();
    }
  });
}

/* Markdown Viewer Application */
async function openMarkdownWindow(filePath) {
  const { id, body } = createWindow({ title: `📄 ${filePath}`, width: 680, height: 480 });
  body.innerHTML = '<div class="tree-loading">Loading content...</div>';

  try {
    const res = await fetch(`/api/file-content?path=${encodeURIComponent(filePath)}`);
    const data = await res.json();

    if (data.error) {
      body.innerHTML = `<div style="color:#ef4444; padding:16px;">${data.error}</div>`;
      return;
    }

    const htmlContent = window.marked ? marked.parse(data.content) : `<pre>${data.content}</pre>`;
    body.innerHTML = `<div class="markdown-body">${htmlContent}</div>`;
  } catch (err) {
    body.innerHTML = `<div style="color:#ef4444; padding:16px;">Failed to render document: ${err}</div>`;
  }
}

/* Python Launcher Window Application */
function openPythonLauncherWindow(filePath) {
  const cmd = `python3 ${filePath}`;
  createTerminalWindow(`🐍 Run ${filePath}`, cmd);
}

/* Terminal Window Application */
async function createTerminalWindow(title, command = 'bash') {
  const { id, body } = createWindow({ title: `💻 ${title}`, width: 720, height: 420 });
  body.style.padding = '0';

  body.innerHTML = `
    <div class="terminal-body">
      <div class="terminal-output" id="term-out-${id}">Connecting terminal process...</div>
      <div class="terminal-input-line">
        <span class="terminal-prompt">$</span>
        <input type="text" class="terminal-input" id="term-in-${id}" placeholder="Type command..." autofocus>
      </div>
    </div>
  `;

  const outElem = document.getElementById(`term-out-${id}`);
  const inElem = document.getElementById(`term-in-${id}`);

  try {
    const res = await fetch('/api/terminal/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    });
    const data = await res.json();

    if (data.error) {
      outElem.textContent = `Error launching terminal: ${data.error}`;
      return;
    }

    const termId = data.id;
    openWindows[id].termId = termId;
    outElem.textContent = '';

    // Poll terminal output
    const pollInterval = setInterval(async () => {
      if (!openWindows[id]) {
        clearInterval(pollInterval);
        return;
      }
      try {
        const outRes = await fetch(`/api/terminal/output?id=${termId}`);
        const outData = await outRes.json();
        if (outData.output) {
          // Strip raw ANSI escape codes for cleaner output
          const cleanOutput = outData.output.replace(/\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])/g, '');
          outElem.textContent += cleanOutput;
          outElem.scrollTop = outElem.scrollHeight;
        }
      } catch (e) {}
    }, 200);

    // Terminal Input
    inElem.addEventListener('keydown', async (e) => {
      if (e.key === 'Enter') {
        const val = inElem.value + '\n';
        inElem.value = '';
        await fetch('/api/terminal/input', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: termId, data: val })
        });
      }
    });
  } catch (err) {
    outElem.textContent = `Failed to connect terminal session: ${err}`;
  }
}

/* Command Palette Modal */
async function openCommandPalette() {
  const modal = document.getElementById('modal-command-palette');
  const input = document.getElementById('palette-search-input');
  modal.classList.remove('hidden');
  input.value = '';
  input.focus();
  await searchCommands('');
}

async function searchCommands(query) {
  const container = document.getElementById('palette-results');
  try {
    const res = await fetch(`/api/commands?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    if (!data.commands || data.commands.length === 0) {
      container.innerHTML = '<div style="padding:16px; color:#94a3b8;">No matching commands found</div>';
      return;
    }

    container.innerHTML = '';
    data.commands.forEach(cmd => {
      const item = document.createElement('div');
      item.className = 'palette-item';
      item.innerHTML = `
        <div>
          <div style="font-weight:600; color:#f8fafc;">${cmd.name}</div>
          <div style="font-size:12px; color:#94a3b8;">${cmd.description || ''}</div>
        </div>
        <span class="palette-cat">${cmd.category}</span>
      `;

      item.addEventListener('click', () => {
        document.getElementById('modal-command-palette').classList.add('hidden');
        if (cmd.name.toLowerCase().includes('terminal')) {
          createTerminalWindow('Terminal');
        } else {
          // Launch default tool in terminal
          createTerminalWindow(cmd.name, `python3 workstation.py`);
        }
      });

      container.appendChild(item);
    });
  } catch (err) {
    container.innerHTML = `<div style="padding:16px; color:#ef4444;">Error fetching commands: ${err}</div>`;
  }
}

/* LocalStorage State Persistence */
function saveUIState() {
  const state = {
    layout: Object.values(openWindows).map(w => ({
      title: w.title,
      width: w.element.offsetWidth,
      height: w.element.offsetHeight,
      left: w.element.offsetLeft,
      top: w.element.offsetTop
    }))
  };
  localStorage.setItem('wgi_ui_state', JSON.stringify(state));
}

function restoreUIState() {
  try {
    const saved = localStorage.getItem('wgi_ui_state');
    if (!saved) return;
    // UI state available for restore if needed
  } catch (e) {}
}
