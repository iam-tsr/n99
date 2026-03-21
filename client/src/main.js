// ...existing code...
let currentTempKey = null;

// --- Tab Navigation Logic ---
// Set min date for calendar input to tomorrow
document.addEventListener('DOMContentLoaded', () => {
  const dateInput = document.getElementById('date');
  if (dateInput) {
    const today = new Date();
    today.setDate(today.getDate() + 1); // tomorrow
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const minDate = `${yyyy}-${mm}-${dd}`;
    dateInput.setAttribute('min', minDate);
    dateInput.value = minDate;
  }
});
const tabs = document.querySelectorAll('.tab');
const panes = document.querySelectorAll('.tab-pane');

function switchTab(targetId) {
  tabs.forEach(t => t.classList.remove('active'));
  panes.forEach(p => p.classList.remove('active'));
  
  document.querySelector(`.tab[data-target="${targetId}"]`).classList.add('active');
  document.getElementById(targetId).classList.add('active');
}

tabs.forEach(tab => {
  tab.addEventListener('click', () => switchTab(tab.dataset.target));
});

// --- API 1: Movie Selection (Home Tab) ---
document.getElementById('tracking-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const statusEl = document.getElementById('movie-status');
  
  const payload = {
    movie: document.getElementById('movie').value,
    cinema: document.getElementById('cinema').value,
    date: document.getElementById('date').value,
  };

  btn.textContent = 'Starting...';
  statusEl.textContent = '';

  try {
    // ⚠️ Uncomment when backend is ready
    const res = await fetch(`/movie-selection`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    
    // --- Mock Response ---
    // const data = { temp_key: "key_" + Date.now() };

    if (data.temp_key) {
      currentTempKey = data.temp_key;
      statusEl.style.color = '#10B981';
      statusEl.textContent = 'Tracking initiated! Moving to profile...';
      
      setTimeout(() => {
        switchTab('profile');
        btn.textContent = 'Start Tracking';
        statusEl.textContent = '';
      }, 1000);
    }
  } catch (err) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = 'Failed to connect to server.';
    btn.textContent = 'Start Tracking';
  }
});

// --- API 2: User Profile (Profile Tab) ---
document.getElementById('profile-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const statusEl = document.getElementById('profile-status');
  
  if (!currentTempKey) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = 'Please start tracking a movie first.';
    return;
  }

  const payload = {
    temp_key: currentTempKey,
    username: document.getElementById('username').value,
    email: document.getElementById('email').value
  };

  btn.textContent = 'Confirming...';

  try {
    // ⚠️ Uncomment when backend is ready
    await fetch(`/user-profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    statusEl.style.color = '#10B981';
    statusEl.textContent = 'Profile confirmed! Setup complete.';
    
    // Reset the key now that the flow is complete
    currentTempKey = null; 
    
    setTimeout(() => {
      btn.textContent = 'Confirm Profile';
      statusEl.textContent = '';
      e.target.reset(); 
      document.getElementById('tracking-form').reset();
      switchTab('home'); 
    }, 2000);

  } catch (err) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = 'Failed to save profile.';
    btn.textContent = 'Confirm Profile';
  }
});

// --- API 3 & 4: Keep-Alive Schedulers (Using Web Worker) ---
async function startKeepAlive() {
  try {
    fetch('/api/active-scheduler', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      keepalive: true
    });
  } catch (error) {
    console.error('Error triggering active scheduler:', error);
  }

  try {
    fetch('/api/lazy-scheduler', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      keepalive: true
    });
  } catch (error) {
    console.error('Error triggering lazy scheduler:', error);
  }
}