/* Public portfolio assistant. All model output is rendered as text, never HTML. */
(() => {
  'use strict';
  const API = ((['localhost', '127.0.0.1'].includes(location.hostname) && location.port === '5000')
    || location.hostname === 'cattle-scratch-parlor.ngrok-free.dev')
    ? location.origin : 'https://cattle-scratch-parlor.ngrok-free.dev';
  const BOOKING = 'https://calendar.app.google/bNG7fkvhgRykj2Ba7';
  let sessionId = null;
  let pending = false;
  let controller = null;
  let previousFocus = null;

  const widget = document.createElement('div');
  widget.id = 'portfolio-chat';
  // This template is static. Visitor and model content is added only via textContent.
  widget.innerHTML = `
    <button class="chat-launcher" type="button" aria-controls="chat-panel" aria-expanded="false">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z"/></svg>
      Ask about Nafiz <span class="chat-launcher-dot" aria-hidden="true"></span>
    </button>
    <section id="chat-panel" role="dialog" aria-modal="false" aria-labelledby="chat-title" hidden>
      <header class="chat-header">
        <div><div class="chat-eyebrow">THE CONVERSATIONAL PORTFOLIO</div><h2 id="chat-title">Get to know Nafiz.</h2><p id="chat-status" role="status">Research, experience & a time to talk.</p></div>
        <button type="button" class="chat-close" aria-label="Close conversation">×</button>
      </header>
      <div class="chat-transcript" role="log" aria-label="Conversation" aria-live="polite" aria-relevant="additions text">
        <div class="chat-message chat-assistant"><span class="chat-speaker">NAFIZ'S ASSISTANT</span><p>Hi! I can help you explore Nafiz’s research, projects, and experience—or find a time to meet.</p></div>
      </div>
      <div class="chat-suggestions" aria-label="Suggested questions">
        <button type="button">What does Nafiz research?</button>
        <button type="button">Tell me about AngioVision</button>
      </div>
      <div class="chat-tools"><a class="chat-booking-link" href="${BOOKING}" target="_blank" rel="noopener noreferrer">Schedule a meeting ↗</a><button class="chat-reset" type="button">New chat</button></div>
      <form class="chat-form"><label class="chat-sr-only" for="chat-input">Your message</label><textarea id="chat-input" rows="2" maxlength="2000" placeholder="What would you like to know?" required></textarea><button class="chat-send" type="submit" aria-label="Send message"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m5 12 7-7 7 7M12 5v14"/></svg></button></form>
      <p class="chat-footnote">AI answers from the portfolio. Check sources for details.<br>Messages and responses are saved by Nafiz for review. Avoid sharing sensitive information. Booking opens Google Calendar.</p>
    </section>`;
  document.body.appendChild(widget);
  const panel = widget.querySelector('#chat-panel');
  const launcher = widget.querySelector('.chat-launcher');
  const input = widget.querySelector('#chat-input');
  const log = widget.querySelector('.chat-transcript');
  const status = widget.querySelector('#chat-status');
  const send = widget.querySelector('.chat-send');
  const suggestions = widget.querySelector('.chat-suggestions');

  function auditEvent(event) {
    fetch(API + '/api/events', {
      method: 'POST', keepalive: true,
      headers: { 'Content-Type': 'application/json', 'ngrok-skip-browser-warning': '1' },
      body: JSON.stringify({ event, session_id: sessionId }),
    }).catch(() => {});
  }
  widget.addEventListener('click', event => {
    if (event.target.closest('.chat-booking-link, .chat-booking-button')) auditEvent('booking_opened');
  });

  function setOpen(open) {
    panel.hidden = !open;
    launcher.setAttribute('aria-expanded', String(open));
    if (open) {
      previousFocus = document.activeElement;
      input.focus();
      checkHealth();
    } else if (previousFocus) previousFocus.focus();
  }
  launcher.addEventListener('click', () => setOpen(panel.hidden));
  widget.querySelector('.chat-close').addEventListener('click', () => setOpen(false));
  panel.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); setOpen(false); }
  });

  async function request(path, data, signal) {
    const response = await fetch(API + path, {
      method: data ? 'POST' : 'GET',
      headers: { 'ngrok-skip-browser-warning': '1', ...(data ? { 'Content-Type': 'application/json' } : {}) },
      ...(data ? { body: JSON.stringify(data) } : {}), signal,
    });
    if (!(response.headers.get('content-type') || '').includes('application/json')) {
      throw new Error('The assistant is offline right now. Please try later, or schedule a meeting below.');
    }
    const result = await response.json();
    if (!response.ok) throw new Error(typeof result.detail === 'string' ? result.detail : 'Please try a shorter message.');
    return result;
  }
  async function checkHealth() {
    if (pending) return;
    try {
      const result = await request('/api/health', null, AbortSignal.timeout(6000));
      if (!pending) status.textContent = result.model_ready ? 'Ready to chat · Grounded in the portfolio' : 'Assistant offline · Meeting booking is available';
    } catch (_) {
      if (!pending) status.textContent = 'Assistant offline · Meeting booking is available';
    }
  }
  function message(role, text) {
    const element = document.createElement('div');
    element.className = 'chat-message chat-' + role;
    const label = document.createElement('span');
    label.className = 'chat-speaker';
    label.textContent = role === 'user' ? 'YOU' : "NAFIZ'S ASSISTANT";
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    element.append(label, paragraph);
    log.append(element);
    log.scrollTop = log.scrollHeight;
    return element;
  }
  function safeLink(label, href, className) {
    try {
      if (new URL(href).protocol !== 'https:') return null;
    } catch (_) { return null; }
    const link = document.createElement('a');
    link.href = href; link.textContent = label; link.className = className;
    link.target = '_blank'; link.rel = 'noopener noreferrer';
    return link;
  }
  async function submit(text) {
    text = text.trim();
    if (!text || pending) return;
    pending = true;
    send.disabled = true;
    widget.querySelector('.chat-reset').disabled = true;
    suggestions.hidden = true;
    input.value = '';
    message('user', text);
    const waiting = message('assistant', 'Looking through the portfolio…');
    waiting.classList.add('chat-waiting');
    status.textContent = 'Thinking…';
    controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 110000);
    try {
      const result = await request('/api/chat', { message: text, session_id: sessionId }, controller.signal);
      waiting.remove();
      sessionId = result.session_id;
      const answer = message('assistant', result.answer);
      if (result.sources && result.sources.length) {
        const sources = document.createElement('div');
        sources.className = 'chat-sources';
        const title = document.createElement('span'); title.textContent = 'SOURCES';
        sources.append(title);
        for (const source of result.sources) {
          const link = safeLink(source.title, source.url, 'chat-source');
          if (link) sources.append(link);
        }
        answer.append(sources);
      }
      for (const action of result.actions || []) {
        if (action.type === 'booking') {
          const link = safeLink(action.label + ' ↗', action.url, 'chat-booking-button');
          if (link) answer.append(link);
        }
      }
      status.textContent = 'Ready to chat · Grounded in the portfolio';
    } catch (error) {
      waiting.classList.remove('chat-waiting');
      waiting.querySelector('p').textContent = error.name === 'AbortError'
        ? 'That took longer than expected. Please try again in a moment. You can still schedule a meeting below.'
        : error.message === 'Failed to fetch' ? 'Unable to reach the assistant. Please try later, or schedule a meeting below.' : error.message;
      const retry = document.createElement('button');
      retry.type = 'button'; retry.className = 'chat-retry'; retry.textContent = 'Try again';
      retry.addEventListener('click', () => { if (!pending) { retry.remove(); submit(text); } });
      waiting.append(retry);
      status.textContent = 'Could not complete that message';
    } finally {
      clearTimeout(timeout);
      pending = false; send.disabled = false;
      widget.querySelector('.chat-reset').disabled = false;
      log.scrollTop = log.scrollHeight;
      if (!panel.hidden) input.focus();
    }
  }
  widget.querySelector('.chat-form').addEventListener('submit', event => {
    event.preventDefault(); submit(input.value);
  });
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault(); submit(input.value);
    }
  });
  for (const button of suggestions.querySelectorAll('button')) {
    button.addEventListener('click', () => submit(button.textContent));
  }
  widget.querySelector('.chat-reset').addEventListener('click', () => {
    if (pending) return;
    auditEvent('new_chat');
    sessionId = null;
    log.replaceChildren();
    message('assistant', 'A fresh conversation. What would you like to know about Nafiz?');
    suggestions.hidden = false; input.focus();
  });
})();
