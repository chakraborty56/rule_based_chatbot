const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('msg');

function addMessage(role, text) {
  const row = document.createElement('div');
  row.className = `msg ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

addMessage('bot', "Hello! I'm NovaMobiles' rule‑based support bot. Ask me about orders, warranty, hours, pickup location, or how to contact support.");

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage('user', text);
  input.value = '';
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    addMessage('bot', data.reply || 'Hmm, something went wrong.');
  } catch (err) {
    addMessage('bot', 'Network error. Is the Flask server running?');
  }
});
