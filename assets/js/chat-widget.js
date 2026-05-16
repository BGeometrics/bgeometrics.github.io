/* BGeometrics AI Chat Widget — vanilla JS, no dependencies */
(function () {
  'use strict';

  // ── Configuration ─────────────────────────────────────────────────────────────
  var cfg = window.BG_CHAT_CONFIG || {};
  var ENDPOINT = cfg.endpoint || 'https://mcp.bitcoin-data.com/chat';
  var TOKEN    = cfg.token    || null;

  // ── Theme detection ───────────────────────────────────────────────────────────
  // Astro site adds html.dark; charts.bgeometrics.com uses data-theme on body
  function isDark() {
    if (document.documentElement.classList.contains('dark')) return true;
    if (document.body && document.body.getAttribute('data-theme') === 'dark') return true;
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }

  // ── Minimal markdown renderer ─────────────────────────────────────────────────
  function renderMarkdown(text) {
    // Escape HTML first
    var safe = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // **bold**
    safe = safe.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // [label](url) → link; chart links get special button style
    safe = safe.replace(
      /\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,
      function (_, label, url) {
        var isChart = url.indexOf('charts.bgeometrics.com') !== -1;
        var cls = isChart ? ' class="bgcw-chart-link"' : '';
        return '<a href="' + url + '"' + cls + ' target="_blank" rel="noopener noreferrer">' + label + '</a>';
      }
    );

    // Bare chart URLs (not already linked)
    safe = safe.replace(
      /(?<!['"=])(https?:\/\/charts\.bgeometrics\.com\/[^\s<"]+)/g,
      function (url) {
        return '<a class="bgcw-chart-link" href="' + url + '" target="_blank" rel="noopener noreferrer">Ver gráfico →</a>';
      }
    );

    // Newlines → <br>
    safe = safe.replace(/\n/g, '<br>');

    return safe;
  }

  // ── DOM helpers ───────────────────────────────────────────────────────────────
  function el(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        e.setAttribute(k, attrs[k]);
      });
    }
    return e;
  }

  // ── Build widget DOM ──────────────────────────────────────────────────────────
  function createWidget() {
    // ── Floating button
    var btn = el('button', {
      id: 'bgcw-btn',
      title: 'BGeometrics AI',
      'aria-label': 'Open BGeometrics AI assistant',
    });
    btn.innerHTML =
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';

    // ── Panel
    var panel = el('div', {
      id: 'bgcw-panel',
      role: 'dialog',
      'aria-label': 'BGeometrics AI chat',
      'aria-hidden': 'true',
    });

    // Apply dark theme class if needed
    if (isDark()) panel.classList.add('bgcw--dark');

    // Header
    var header = el('div', { class: 'bgcw-header' });
    var headerTitle = el('span', { class: 'bgcw-title' });
    headerTitle.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="opacity:.9">' +
      '<circle cx="12" cy="12" r="10"/>' +
      '<text x="12" y="17" text-anchor="middle" fill="#f7931a" font-size="13" font-weight="bold" font-family="Arial">₿</text>' +
      '</svg>' +
      'BGeometrics AI <span class="bgcw-beta">beta</span>';
    var closeBtn = el('button', { class: 'bgcw-close', 'aria-label': 'Close chat', title: 'Close' });
    closeBtn.textContent = '✕';
    header.append(headerTitle, closeBtn);

    // Messages area
    var messages = el('div', {
      id: 'bgcw-messages',
      role: 'log',
      'aria-live': 'polite',
      'aria-atomic': 'false',
    });

    // Welcome message
    var welcome = el('div', { class: 'bgcw-msg bgcw-msg--assistant' });
    var welcomeBubble = el('div', { class: 'bgcw-bubble' });
    welcomeBubble.innerHTML =
      '¡Hola! Soy el asistente de <strong>BGeometrics</strong>. ' +
      'Pregúntame sobre métricas on-chain de Bitcoin como MVRV, SOPR, hashrate, etc.<br><br>' +
      '<em style="font-size:12px;opacity:.75">Hello! Ask me about Bitcoin on-chain metrics like MVRV, SOPR, hashrate, and more.</em>';
    welcome.appendChild(welcomeBubble);
    messages.appendChild(welcome);

    // Suggested questions (quick chips)
    var suggestions = el('div', { class: 'bgcw-msg bgcw-msg--assistant' });
    var sugBubble = el('div', { class: 'bgcw-bubble' });
    var chips = ['What is the current MVRV?', 'Bitcoin market overview', 'What is the hashrate?'];
    sugBubble.innerHTML = '<span style="font-size:12px;opacity:.7">Try:</span><br>';
    chips.forEach(function (chip) {
      var chipEl = el('button', { class: 'bgcw-chip' });
      chipEl.style.cssText =
        'display:inline-block;margin:3px 3px 0 0;padding:3px 9px;border-radius:12px;' +
        'border:1px solid var(--bgcw-accent);background:transparent;color:var(--bgcw-accent);' +
        'font-size:11px;cursor:pointer;font-family:inherit;';
      chipEl.textContent = chip;
      chipEl.addEventListener('click', function () { submitQuery(chip); });
      sugBubble.appendChild(chipEl);
    });
    suggestions.appendChild(sugBubble);
    messages.appendChild(suggestions);

    // Input area
    var inputArea = el('div', { class: 'bgcw-input-area' });
    var textarea = el('textarea', {
      id: 'bgcw-input',
      placeholder: 'Ask about Bitcoin on-chain metrics...',
      rows: '1',
      maxlength: '500',
      'aria-label': 'Your question',
    });
    var sendBtn = el('button', { id: 'bgcw-send', 'aria-label': 'Send', title: 'Send (Enter)' });
    sendBtn.innerHTML =
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">' +
      '<path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>';
    inputArea.append(textarea, sendBtn);

    // Footer
    var footer = el('div', { class: 'bgcw-footer' });
    footer.innerHTML =
      'Powered by <a href="https://charts.bgeometrics.com" target="_blank" rel="noopener">BGeometrics</a>' +
      ' &middot; <a href="https://bitcoin-data.com" target="_blank" rel="noopener">BGapi</a>';

    panel.append(header, messages, inputArea, footer);
    document.body.append(btn, panel);

    // ── Panel open/close ───────────────────────────────────────────────────────
    var isOpen = false;

    function openPanel() {
      isOpen = true;
      panel.classList.add('bgcw-panel--open');
      panel.setAttribute('aria-hidden', 'false');
      btn.classList.add('bgcw-btn--open');
      btn.setAttribute('aria-label', 'Close BGeometrics AI assistant');
      setTimeout(function () { textarea.focus(); }, 50);
    }

    function closePanel() {
      isOpen = false;
      panel.classList.remove('bgcw-panel--open');
      panel.setAttribute('aria-hidden', 'true');
      btn.classList.remove('bgcw-btn--open');
      btn.setAttribute('aria-label', 'Open BGeometrics AI assistant');
      btn.focus();
    }

    btn.addEventListener('click', function () {
      isOpen ? closePanel() : openPanel();
    });
    closeBtn.addEventListener('click', closePanel);

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen) closePanel();
    });

    // ── Textarea auto-resize + Enter key ──────────────────────────────────────
    textarea.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    textarea.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 110) + 'px';
    });
    sendBtn.addEventListener('click', sendMessage);

    // ── Message send ───────────────────────────────────────────────────────────
    var isBusy = false;

    function submitQuery(query) {
      if (isBusy) return;
      textarea.value = query;
      sendMessage();
    }

    function sendMessage() {
      var query = textarea.value.trim();
      if (!query || isBusy) return;

      isBusy = true;
      sendBtn.disabled = true;
      textarea.value = '';
      textarea.style.height = 'auto';

      appendMessage('user', renderMarkdown(query));

      var assistantDiv = appendMessage('assistant', '');
      var bubble = assistantDiv.querySelector('.bgcw-bubble');
      bubble.innerHTML = '<span class="bgcw-thinking">Pensando…</span>';

      var accumulated = '';

      var headers = { 'Content-Type': 'application/json' };
      if (TOKEN) headers['x-bgapi-token'] = TOKEN;

      fetch(ENDPOINT, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ query: query }),
      })
        .then(function (response) {
          if (!response.ok) {
            return response.json().then(function (d) {
              throw new Error(d.error || 'HTTP ' + response.status);
            });
          }

          var reader = response.body.getReader();
          var decoder = new TextDecoder();
          var sseBuffer = '';
          var currentEvent = '';

          function readChunk() {
            reader
              .read()
              .then(function (result) {
                if (result.done) { finish(); return; }

                sseBuffer += decoder.decode(result.value, { stream: true });
                var lines = sseBuffer.split('\n');
                sseBuffer = lines.pop(); // keep incomplete line

                lines.forEach(function (line) {
                  if (line.startsWith('event: ')) {
                    currentEvent = line.slice(7).trim();
                  } else if (line.startsWith('data: ')) {
                    try {
                      var data = JSON.parse(line.slice(6));
                      handleEvent(currentEvent, data);
                    } catch (_) { /* ignore parse errors */ }
                    currentEvent = '';
                  }
                });

                readChunk();
              })
              .catch(function (err) {
                bubble.innerHTML = '<span class="bgcw-error">Connection error: ' + escapeHtml(err.message) + '</span>';
                finish();
              });
          }

          function handleEvent(name, data) {
            switch (name) {
              case 'start':
                bubble.innerHTML = '<span class="bgcw-thinking">Pensando…</span>';
                break;
              case 'tool_call':
                var tools = data.tools || [];
                var label =
                  tools.some(function (t) {
                    return t === 'get_latest_values' || t === 'get_market_overview';
                  })
                    ? 'Obteniendo datos en tiempo real…'
                    : 'Buscando métricas…';
                bubble.innerHTML = '<span class="bgcw-thinking">' + escapeHtml(label) + '</span>';
                break;
              case 'chunk':
                if (!accumulated && data.text) {
                  bubble.innerHTML = ''; // clear thinking indicator on first chunk
                }
                accumulated += data.text || '';
                bubble.innerHTML = renderMarkdown(accumulated);
                scrollBottom();
                break;
              case 'done':
                if (!accumulated) {
                  bubble.innerHTML = '<em style="opacity:.6">No response received.</em>';
                }
                finish();
                break;
              case 'error':
                bubble.innerHTML =
                  '<span class="bgcw-error">' + escapeHtml(data.message || 'Unknown error') + '</span>';
                finish();
                break;
            }
          }

          readChunk();
        })
        .catch(function (err) {
          bubble.innerHTML =
            '<span class="bgcw-error">Could not connect to AI service. ' + escapeHtml(err.message) + '</span>';
          finish();
        });

      function finish() {
        isBusy = false;
        sendBtn.disabled = false;
        textarea.focus();
        scrollBottom();
      }
    }

    // ── DOM helpers ────────────────────────────────────────────────────────────
    function appendMessage(role, html) {
      var wrapper = el('div', { class: 'bgcw-msg bgcw-msg--' + role });
      var bubble  = el('div', { class: 'bgcw-bubble' });
      if (html) bubble.innerHTML = html;
      wrapper.appendChild(bubble);
      messages.appendChild(wrapper);
      scrollBottom();
      return wrapper;
    }

    function scrollBottom() {
      messages.scrollTop = messages.scrollHeight;
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    }
  }

  // ── Boot ──────────────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }

})();
