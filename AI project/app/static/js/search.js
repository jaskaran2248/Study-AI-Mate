/**
 * StudyMate AI - Search & Discovery Module
 * Searches materials & dynamically generates study packs and tiered quizzes for any topic.
 */

window.SearchEngine = {
  currentQuery: '',
  difficultyFilter: 'all',
  categoryFilter: 'all',

  init() {
    this.input = document.getElementById('search-input');
    this.btnSearch = document.getElementById('btn-execute-search');
    this.btnGenTopic = document.getElementById('btn-gen-from-search');
    this.resultsContainer = document.getElementById('search-results-container');
    this.quickChips = document.querySelectorAll('.search-chip');

    if (this.input) {
      this.input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.executeSearch();
      });
      this.input.addEventListener('input', () => {
        const val = this.input.value.trim();
        if (this.btnGenTopic) {
          if (val.length > 2) {
            this.btnGenTopic.classList.remove('hidden');
            this.btnGenTopic.textContent = `⚡ Generate AI Study Pack on "${val}"`;
          } else {
            this.btnGenTopic.classList.add('hidden');
          }
        }
      });
    }

    if (this.btnSearch) {
      this.btnSearch.addEventListener('click', () => this.executeSearch());
    }

    if (this.btnGenTopic) {
      this.btnGenTopic.addEventListener('click', () => this.generateFromQuery());
    }

    // Quick topic suggestion chips
    this.quickChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const topic = chip.getAttribute('data-topic');
        if (this.input) {
          this.input.value = topic;
          this.executeSearch();
        }
      });
    });

    // Difficulty filter buttons
    document.querySelectorAll('.search-diff-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.search-diff-filter').forEach(b => b.classList.remove('bg-blue-600', 'text-white'));
        btn.classList.add('bg-blue-600', 'text-white');
        this.difficultyFilter = btn.getAttribute('data-diff');
        this.executeSearch();
      });
    });
  },

  async executeSearch() {
    const q = this.input ? this.input.value.trim() : '';
    this.currentQuery = q;

    try {
      const url = `/api/search?q=${encodeURIComponent(q)}&difficulty=${this.difficultyFilter}&category=${this.categoryFilter}`;
      const res = await fetch(url);
      const data = await res.json();
      this.renderResults(data);
    } catch (err) {
      console.error(err);
    }
  },

  renderResults(data) {
    if (!this.resultsContainer) return;

    const { results, query, total_matches } = data;
    const docs = results.documents || [];
    const notes = results.notes || [];
    const quizzes = results.quizzes || [];
    const questions = results.questions || [];

    if (total_matches === 0) {
      this.resultsContainer.innerHTML = `
        <div class="p-8 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
          <p class="text-slate-500 text-sm">No existing items found for "<strong>${query}</strong>".</p>
          <button onclick="window.SearchEngine.generateFromQuery()" class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg transition shadow-sm">
            ⚡ Generate Study Notes & Tiered Quiz for "${query}" Now →
          </button>
        </div>
      `;
      return;
    }

    let html = `
      <div class="mb-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">
        Found ${total_matches} results ${query ? `for "${query}"` : ''}
      </div>
      <div class="space-y-6">
    `;

    // Quizzes Matches
    if (quizzes.length > 0) {
      html += `
        <div>
          <h4 class="font-bold text-slate-800 dark:text-slate-200 text-sm flex items-center space-x-2 mb-3">
            <span>🎯 Quizzes (${quizzes.length})</span>
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            ${quizzes.map(q => `
              <div class="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between">
                <div>
                  <span class="px-2 py-0.5 text-xs font-semibold rounded ${
                    q.difficulty_tier === 'Mastery' ? 'badge-mastery' : (q.difficulty_tier === 'Advanced' ? 'badge-advanced' : 'badge-basic')
                  }">${q.difficulty_tier}</span>
                  <h5 class="font-bold text-sm text-slate-800 dark:text-slate-100 mt-1">${q.title}</h5>
                  <p class="text-xs text-slate-500">${q.question_count} Questions</p>
                </div>
                <button onclick="window.Quiz.loadAndStartQuiz(${q.id}); switchTab('quiz');" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white hover:bg-blue-700">
                  Take Quiz →
                </button>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Questions Matches
    if (questions.length > 0) {
      html += `
        <div>
          <h4 class="font-bold text-slate-800 dark:text-slate-200 text-sm flex items-center space-x-2 mb-3">
            <span>❓ Question Bank Matches (${questions.length})</span>
          </h4>
          <div class="space-y-2">
            ${questions.map(q => `
              <div class="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 text-sm">
                <div class="flex items-center justify-between">
                  <span class="px-2 py-0.5 text-xs font-semibold rounded ${
                    q.difficulty === 'mastery' ? 'badge-mastery' : (q.difficulty === 'advanced' ? 'badge-advanced' : (q.difficulty === 'intermediate' ? 'badge-intermediate' : 'badge-basic'))
                  }">${q.difficulty.toUpperCase()} • ${q.bloom_level}</span>
                  <span class="text-xs text-slate-400">From: ${q.quiz_title}</span>
                </div>
                <p class="font-medium text-slate-800 dark:text-slate-200 mt-2">${q.question_text}</p>
                <div class="mt-2 text-right">
                  <button onclick="window.Quiz.loadAndStartQuiz(${q.quiz_id}); switchTab('quiz');" class="text-xs text-blue-600 font-semibold hover:underline">
                    Practice In Quiz →
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Notes Matches
    if (notes.length > 0) {
      html += `
        <div>
          <h4 class="font-bold text-slate-800 dark:text-slate-200 text-sm flex items-center space-x-2 mb-3">
            <span>📘 Study Notes (${notes.length})</span>
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            ${notes.map(n => `
              <div class="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between">
                <div>
                  <h5 class="font-bold text-sm text-slate-800 dark:text-slate-100">${n.title}</h5>
                  <p class="text-xs text-slate-500 line-clamp-1 mt-1">${n.summary}</p>
                </div>
                <button onclick="window.Notes.fetchAndDisplayNote(${n.id}); switchTab('notes');" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700">
                  Open Notes →
                </button>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Documents Matches
    if (docs.length > 0) {
      html += `
        <div>
          <h4 class="font-bold text-slate-800 dark:text-slate-200 text-sm flex items-center space-x-2 mb-3">
            <span>📄 Uploaded Documents (${docs.length})</span>
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            ${docs.map(d => `
              <div class="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between">
                <div>
                  <span class="px-2 py-0.5 text-xs font-semibold rounded uppercase bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300">${d.file_type}</span>
                  <h5 class="font-bold text-sm text-slate-800 dark:text-slate-100 mt-1">${d.title}</h5>
                  <p class="text-xs text-slate-500">${d.subject} • ${d.word_count} words</p>
                </div>
                <button onclick="window.Uploader.quickGenerateQuiz(${d.id})" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white hover:bg-blue-700">
                  Generate Quiz →
                </button>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    html += `</div>`;
    this.resultsContainer.innerHTML = html;
  },

  async generateFromQuery() {
    const topic = this.input ? this.input.value.trim() : '';
    if (!topic) {
      showToast('Please enter a search topic first.', 'warning');
      return;
    }

    showToast(`AI is generating complete Study Pack for "${topic}"...`, 'info');

    try {
      const res = await fetch('/api/search/generate-from-topic', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          topic: topic,
          difficulty_tier: 'Adaptive Mix',
          subject: 'STEM & Quality Education'
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Generation failed');

      showToast(`Study Pack created for "${topic}"!`, 'success');
      
      // Prompt user whether to view notes or start quiz
      if (confirm(`Study Pack generated for "${topic}"!\n\nClick OK to take the Tiered Quiz, or Cancel to review the Study Notes.`)) {
        switchTab('quiz');
        window.Quiz.startQuiz(data.quiz);
      } else {
        switchTab('notes');
        window.Notes.displayNote(data.notes);
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => window.SearchEngine.init());
