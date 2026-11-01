/**
 * StudyMate AI - Global Application Controller
 * Manages tabs, theme, accessibility, speech synthesis, and toast notifications.
 */

const AppState = {
  currentTab: 'upload',
  activeDocumentId: null,
  activeNotesId: null,
  activeQuizId: null,
  totalXp: 0,
  theme: localStorage.getItem('studymate_theme') || 'light',
  fontSize: 'normal',
  isSpeaking: false
};

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initAccessibility();
  initSpeechSynthesis();
  initSettingsModal();
  
  // Load initial view
  switchTab('upload');
  window.Uploader?.loadDocuments();
  window.Skills?.loadDashboard();
});

// ==================== NAVIGATION ====================

function initNavigation() {
  const navButtons = document.querySelectorAll('[data-tab-target]');
  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-tab-target');
      switchTab(target);
    });
  });
}

function switchTab(tabName) {
  AppState.currentTab = tabName;
  
  // Update nav buttons
  document.querySelectorAll('[data-tab-target]').forEach(btn => {
    const isTarget = btn.getAttribute('data-tab-target') === tabName;
    btn.classList.toggle('bg-blue-600', isTarget);
    btn.classList.toggle('text-white', isTarget);
    btn.classList.toggle('text-slate-600', !isTarget);
    btn.classList.toggle('dark:text-slate-300', !isTarget);
    btn.classList.toggle('hover:bg-slate-100', !isTarget);
    btn.classList.toggle('dark:hover:bg-slate-800', !isTarget);
  });

  // Update tab content containers
  document.querySelectorAll('.tab-content').forEach(section => {
    section.classList.add('hidden');
  });

  const targetEl = document.getElementById(`tab-${tabName}`);
  if (targetEl) {
    targetEl.classList.remove('hidden');
  }

  // Trigger tab-specific refresh
  if (tabName === 'upload') {
    window.Uploader?.loadDocuments();
  } else if (tabName === 'notes') {
    window.Notes?.loadNotesList();
  } else if (tabName === 'quiz') {
    window.Quiz?.loadQuizzesList();
  } else if (tabName === 'skills') {
    window.Skills?.loadDashboard();
  }
}

// ==================== THEME & ACCESSIBILITY ====================

function initTheme() {
  document.documentElement.setAttribute('data-theme', AppState.theme);
  const themeToggle = document.getElementById('btn-toggle-theme');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('studymate_theme', AppState.theme);
      document.documentElement.setAttribute('data-theme', AppState.theme);
      showToast(`Switched to ${AppState.theme} mode`, 'info');
    });
  }
}

function initAccessibility() {
  const fontBtn = document.getElementById('btn-font-size');
  if (fontBtn) {
    fontBtn.addEventListener('click', () => {
      if (document.body.classList.contains('font-xl')) {
        document.body.classList.remove('font-xl', 'font-lg');
        AppState.fontSize = 'normal';
        showToast('Standard text size', 'info');
      } else if (document.body.classList.contains('font-lg')) {
        document.body.classList.remove('font-lg');
        document.body.classList.add('font-xl');
        AppState.fontSize = 'xl';
        showToast('Extra large text size', 'info');
      } else {
        document.body.classList.add('font-lg');
        AppState.fontSize = 'lg';
        showToast('Large text size', 'info');
      }
    });
  }

  const contrastBtn = document.getElementById('btn-high-contrast');
  if (contrastBtn) {
    contrastBtn.addEventListener('click', () => {
      const isHigh = document.documentElement.getAttribute('data-high-contrast') === 'true';
      document.documentElement.setAttribute('data-high-contrast', (!isHigh).toString());
      showToast(isHigh ? 'High contrast disabled' : 'High contrast mode enabled', 'info');
    });
  }
}

// ==================== TEXT TO SPEECH (TTS) ====================

function initSpeechSynthesis() {
  window.speakText = (text) => {
    if (!('speechSynthesis' in window)) {
      showToast('Text-to-speech is not supported in this browser.', 'warning');
      return;
    }

    if (AppState.isSpeaking) {
      window.speechSynthesis.cancel();
      AppState.isSpeaking = false;
      showToast('Audio paused', 'info');
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onend = () => {
      AppState.isSpeaking = false;
    };
    utterance.onerror = () => {
      AppState.isSpeaking = false;
    };

    AppState.isSpeaking = true;
    window.speechSynthesis.speak(utterance);
    showToast('Reading aloud...', 'info');
  };
}

// ==================== SETTINGS MODAL ====================

function initSettingsModal() {
  const modal = document.getElementById('settings-modal');
  const openBtn = document.getElementById('btn-open-settings');
  const closeBtn = document.getElementById('btn-close-settings');
  const saveBtn = document.getElementById('btn-save-settings');

  if (openBtn && modal) {
    openBtn.addEventListener('click', async () => {
      modal.classList.remove('hidden');
      try {
        const res = await fetch('/api/settings');
        const data = await res.json();
        document.getElementById('setting-provider').value = data.ai_provider || 'local';
        const keyInput = document.getElementById('setting-api-key');
        keyInput.placeholder = data.api_key_configured ? `Key configured (${data.api_key_masked})` : 'Paste optional API key';
      } catch (e) {
        console.error(e);
      }
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
  }

  if (saveBtn) {
    saveBtn.addEventListener('click', async () => {
      const provider = document.getElementById('setting-provider').value;
      const apiKey = document.getElementById('setting-api-key').value;
      try {
        const res = await fetch('/api/settings', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ ai_provider: provider, api_key: apiKey })
        });
        const data = await res.json();
        modal.classList.add('hidden');
        showToast(`AI Engine updated: ${provider.toUpperCase()}`, 'success');
      } catch (err) {
        showToast('Failed to save settings', 'error');
      }
    });
  }
}

// ==================== TOAST NOTIFICATIONS ====================

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const colors = {
    success: 'bg-emerald-600 text-white',
    error: 'bg-rose-600 text-white',
    warning: 'bg-amber-600 text-white',
    info: 'bg-slate-900 text-white dark:bg-slate-800'
  };

  toast.className = `px-4 py-3 rounded-lg shadow-lg text-sm font-medium transition-all duration-300 transform translate-y-2 opacity-0 flex items-center space-x-2 ${colors[type] || colors.info}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

window.showToast = showToast;
window.switchTab = switchTab;
