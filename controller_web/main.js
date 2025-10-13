(function () {
  const els = {};
  let ws = null;
  let connected = false;

  function $(id) { return document.getElementById(id); }
  function log(msg, type = 'info') {
    const el = document.createElement('div');
    el.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    if (type === 'error') el.style.color = '#f88';
    els.log.appendChild(el);
    els.log.scrollTop = els.log.scrollHeight;
  }
  function setStatus(text, color) {
    els.status.textContent = text;
    els.status.style.background = color || 'rgba(255,255,255,.08)';
  }
  function getWsUrl() {
    const host = els.host.value.trim() || location.hostname;
    const port = parseInt(els.port.value.trim(), 10) || 8888;
    return `ws://${host}:${port}`;
  }
  function connect() {
    try {
      const url = getWsUrl();
      log(`Connecting to ${url} ...`);
      ws = new WebSocket(url);
      ws.onopen = () => {
        connected = true;
        setStatus('Connected', '#3fb950');
        log('Connected. Sending credentials ...');
        const user = els.username.value || 'admin';
        const pass = els.password.value || '123456';
        ws.send(`${user}:${pass}`);
      };
      ws.onmessage = (ev) => {
        log(`← ${ev.data}`);
        // Try to detect info responses and show them in the Info section
        try {
          const data = JSON.parse(ev.data);
          if (data && typeof data === 'object' && 'status' in data) {
            if (data.title === 'get_info' || data.data?.title === 'get_info') {
              els.info.textContent = JSON.stringify(data, null, 2);
            }
          }
        } catch (_) { /* ignore non-JSON */ }
      };
      ws.onerror = (ev) => {
        log(`WebSocket error`, 'error');
      };
      ws.onclose = () => {
        connected = false;
        setStatus('Disconnected', 'rgba(255,255,255,.08)');
        log('Disconnected');
      };
    } catch (e) {
      log(`Connect error: ${e}`, 'error');
    }
  }
  function disconnect() {
    if (ws) {
      log('Closing connection ...');
      ws.close();
      ws = null;
    }
  }
  function sendCommand(cmd) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      log('Not connected', 'error');
      return;
    }
    log(`→ ${cmd}`);
    ws.send(cmd);
  }
  function sendCommandWithArg(cmd, value) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      log('Not connected', 'error');
      return;
    }
    const msg = `${cmd} ${value}`;
    log(`→ ${msg}`);
    ws.send(msg);
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Cache elements
    els.host = $('host');
    els.port = $('port');
    els.username = $('username');
    els.password = $('password');
    els.btnConnect = $('btnConnect');
    els.status = $('status');
    els.speed = $('speed');
    els.speedVal = $('speedVal');
    els.btnSetSpeed = $('btnSetSpeed');
    els.btnGetInfo = $('btnGetInfo');
    els.log = $('log');
    els.info = $('info');

    // Defaults
    if (!els.host.value) els.host.value = location.hostname || 'raspberrypi.local';

    // Events
    els.btnConnect.addEventListener('click', () => {
      if (!connected) connect(); else disconnect();
    });

    document.querySelectorAll('[data-cmd]').forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.getAttribute('data-cmd');
        sendCommand(cmd);
      });
    });

    els.speed.addEventListener('input', () => {
      els.speedVal.textContent = els.speed.value;
    });

    els.btnSetSpeed.addEventListener('click', () => {
      const val = parseInt(els.speed.value, 10) || 0;
      sendCommandWithArg('wsB', val);
    });

    els.btnGetInfo.addEventListener('click', () => {
      sendCommand('get_info');
    });
  });
})();
