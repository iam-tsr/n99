let currentTempKey = null;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Page Navigation
function showPage(pageId) {
  const sections = document.querySelectorAll('.page-section');
  sections.forEach(s => s.classList.remove('active'));
  document.getElementById(pageId).classList.add('active');
}

// Custom Select Dropdown Logic
class CustomSelect {
  constructor(containerId, hiddenInputId) {
    this.container = document.getElementById(containerId);
    this.hiddenInput = document.getElementById(hiddenInputId);
    this.trigger = this.container.querySelector('.select-trigger');
    this.valueSpan = this.container.querySelector('.select-value');
    this.optionsContainer = this.container.querySelector('.select-options');
    this.searchInput = this.container.querySelector('.select-search');
    this.optionsList = this.container.querySelector('.options-list');
    this.allOptions = [];
    this.isOpen = false;

    this.init();
  }

  init() {
    // Toggle dropdown
    this.trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggle();
    });

    // Search filtering
    this.searchInput.addEventListener('input', (e) => {
      this.filter(e.target.value);
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.container.contains(e.target)) {
        this.close();
      }
    });

    // Prevent search input from closing dropdown
    this.searchInput.addEventListener('click', (e) => e.stopPropagation());
  }

  setOptions(options) {
    this.allOptions = options;
    this.renderOptions(options);
  }

  renderOptions(options) {
    this.optionsList.innerHTML = '';
    if (options.length === 0) {
      this.optionsList.innerHTML = '<div class="option-item no-results">No results found</div>';
      return;
    }
    options.forEach(opt => {
      const div = document.createElement('div');
      div.className = 'option-item';
      div.textContent = opt;
      div.addEventListener('click', () => this.select(opt));
      this.optionsList.appendChild(div);
    });
  }

  filter(query) {
    const filtered = this.allOptions.filter(opt =>
      opt.toLowerCase().includes(query.toLowerCase())
    );
    this.renderOptions(filtered);
  }

  select(value) {
    this.hiddenInput.value = value;
    this.valueSpan.textContent = value;
    this.valueSpan.classList.remove('placeholder');
    this.close();

    // Update selected state
    this.optionsList.querySelectorAll('.option-item').forEach(item => {
      item.classList.toggle('selected', item.textContent === value);
    });
  }

  toggle() {
    this.isOpen ? this.close() : this.open();
  }

  open() {
    this.isOpen = true;
    this.trigger.classList.add('active');
    this.optionsContainer.classList.add('open');
    this.searchInput.value = '';
    this.filter('');
    this.searchInput.focus();
  }

  close() {
    this.isOpen = false;
    this.trigger.classList.remove('active');
    this.optionsContainer.classList.remove('open');
  }
}

let movieSelect, cinemaSelect;

// Populate Dropdowns from API
async function populateDropdowns() {
  movieSelect = new CustomSelect('movie-dropdown', 'movie');
  cinemaSelect = new CustomSelect('cinema-dropdown', 'cinema');

  try {
    const moviesRes = await fetch(`${API_BASE_URL}/api/listed-movies`, { method: 'GET' });
    const moviesData = await moviesRes.json();
    movieSelect.setOptions(moviesData.movies || []);
  } catch (error) {
    console.error('Error loading movies:', error);
  }

  try {
    const cinemasRes = await fetch(`${API_BASE_URL}/api/listed-cinemas`, { method: 'GET' });
    const cinemasData = await cinemasRes.json();
    cinemaSelect.setOptions(cinemasData.cinemas || []);
  } catch (error) {
    console.error('Error loading cinemas:', error);
  }
}

// Set min date for calendar input to tomorrow
document.addEventListener('DOMContentLoaded', () => {
  populateDropdowns();

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

// Check session status
async function checkSession() {
  try {
    const res = await fetch(`${API_BASE_URL}/check-session`, {
      method: 'GET',
      credentials: 'include'
    });
    const data = await res.json();
    return data.has_session;
  } catch (error) {
    console.error('Error checking session:', error);
    return false;
  }
}

// Submit profile with or without username/email
async function submitProfile(skipForm = false) {
  const btn = document.querySelector('#profile-form button');
  const statusEl = document.getElementById('profile-status');

  if (!currentTempKey) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = 'Please start tracking a movie first.';
    return;
  }

  const payload = {
    temp_key: currentTempKey
  };

  // Only add username/email if form is visible and has values
  if (!skipForm) {
    payload.username = document.getElementById('username').value;
    payload.email = document.getElementById('email').value;
  }

  if (btn) btn.textContent = 'Confirming...';

  try {
    const res = await fetch(`${API_BASE_URL}/user-profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Failed to save profile');
    }

    await res.json();
    showPage('success');

    setTimeout(() => {
      currentTempKey = null;
      document.getElementById('profile-form').reset();
      document.getElementById('tracking-form').reset();
      if (btn) btn.textContent = 'Save Profile';
      statusEl.textContent = '';
      showPage('tracking');
    }, 2000);

  } catch (err) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = err.message || 'Failed to save profile.';
    if (btn) btn.textContent = 'Save Profile';
  }
}

// Movie Selection - modified to check session before showing profile
document.getElementById('tracking-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const statusEl = document.getElementById('movie-status');

  const movie = document.getElementById('movie').value;
  const cinema = document.getElementById('cinema').value;

  if (!movie || !cinema) {
    statusEl.style.color = '#DA0B37';
    statusEl.textContent = 'Please select both a movie and cinema.';
    return;
  }

  const payload = {
    movie: movie,
    cinema: cinema,
    date: document.getElementById('date').value,
  };

  btn.textContent = 'Starting...';
  statusEl.textContent = '';

  try {
    const res = await fetch(`${API_BASE_URL}/movie-selection`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const tempKey = data.temp_key;

    if (tempKey) {
      currentTempKey = tempKey;
      statusEl.style.color = '#10B981';
      statusEl.textContent = 'Tracking initiated! Moving to profile...';

      setTimeout(async () => {
        // Check session before showing profile
        const hasSession = await checkSession();
        if (hasSession) {
          // Auto-submit without showing form
          submitProfile(true);
        } else {
          // Show profile form for new users
          showPage('profile');
        }
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

// User Profile - manual submission for new users
document.getElementById('profile-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  await submitProfile(false);
});