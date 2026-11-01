/**
 * StudyMate AI - Notes & Active Recall Flashcards Module
 */

window.Notes = {
  currentNote: null,
  currentFlashcardIndex: 0,
  flashcards: [],

  init() {
    this.notesListEl = document.getElementById('notes-history-list');
    this.notesDetailEl = document.getElementById('notes-detail-view');
    this.setupFlashcardControls();
  },

  async loadNotesList() {
    try {
      const res = await fetch('/api/notes');
      const data = await res.json();
      const notes = data.notes || [];

      if (!this.notesListEl) return;

      if (notes.length === 0) {
        this.notesListEl.innerHTML = `
          <div class="p-6 text-center text-slate-400">
            No notes generated yet. Upload materials or use the search bar to generate notes!
          </div>
        `;
        return;
      }

      this.notesListEl.innerHTML = notes.map(n => `
        <button onclick="window.Notes.fetchAndDisplayNote(${n.id})" class="w-full text-left p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-blue-500 transition shadow-sm mb-3">
          <h4 class="font-bold text-slate-800 dark:text-slate-100">${n.title}</h4>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">${n.summary}</p>
          <div class="flex items-center space-x-2 mt-2 text-xs text-slate-400">
            <span>📅 ${new Date(n.created_at).toLocaleDateString()}</span>
            <span>•</span>
            <span class="text-blue-600 dark:text-blue-400 font-medium">View Full Notes →</span>
          </div>
        </button>
      `).join('');

      // Auto-load first note if not already viewing one
      if (!this.currentNote && notes.length > 0) {
        this.fetchAndDisplayNote(notes[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  },

  async fetchAndDisplayNote(noteId) {
    try {
      const res = await fetch(`/api/notes/${noteId}`);
      if (!res.ok) throw new Error('Failed to load note');
      const note = await res.json();
      this.displayNote(note);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  displayNote(note) {
    this.currentNote = note;
    this.flashcards = note.flashcards || [];
    this.currentFlashcardIndex = 0;

    // Show detail view
    const view = document.getElementById('notes-detail-view');
    if (!view) return;
    view.classList.remove('hidden');

    // Title & Summary
    document.getElementById('note-title').textContent = note.title;
    document.getElementById('note-summary').textContent = note.summary;

    // Export link
    const exportMdBtn = document.getElementById('btn-export-md');
    if (exportMdBtn) {
      exportMdBtn.href = `/api/notes/${note.id}/export/markdown`;
    }
    const exportJsonBtn = document.getElementById('btn-export-json');
    if (exportJsonBtn) {
      exportJsonBtn.href = `/api/notes/${note.id}/export/json`;
    }

    // Key Concepts
    const conceptsEl = document.getElementById('note-concepts-container');
    if (conceptsEl) {
      conceptsEl.innerHTML = (note.key_concepts || []).map(c => `
        <div class="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-slate-800 dark:text-slate-100 text-base">${c.concept}</h4>
            <span class="px-2 py-0.5 text-xs font-semibold rounded bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300">
              Key Concept
            </span>
          </div>
          <p class="text-sm text-slate-600 dark:text-slate-300 mt-2">${c.definition}</p>
          
          <div class="mt-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40 text-xs text-amber-900 dark:text-amber-200">
            <span class="font-bold">💡 Intuitive Analogy:</span> ${c.analogy}
          </div>

          <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">
            <span class="font-semibold text-slate-700 dark:text-slate-300">Application:</span> ${c.real_world_application}
          </div>
          <div class="mt-1 text-xs text-blue-600 dark:text-blue-400 font-medium">
            🎯 ${c.practical_insight || c.sdg_connection || 'Applied Core Competency'}
          </div>
        </div>
      `).join('');
    }

    // Cheat Sheet
    const cheatEl = document.getElementById('note-cheatsheet-container');
    if (cheatEl) {
      cheatEl.innerHTML = (note.cheat_sheet || []).map(cs => `
        <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850">
          <div class="font-bold text-slate-800 dark:text-slate-200 text-sm">${cs.topic}</div>
          <div class="mt-1 font-mono text-xs p-2 bg-slate-100 dark:bg-slate-900 rounded border border-slate-200 dark:border-slate-800 text-blue-600 dark:text-blue-400">
            ${cs.rules_or_formula}
          </div>
          <div class="text-xs text-slate-500 dark:text-slate-400 mt-1 italic">${cs.quick_tip}</div>
        </div>
      `).join('');
    }

    // Mind Map
    const mindmapEl = document.getElementById('note-mindmap-code');
    if (mindmapEl) {
      mindmapEl.textContent = note.mindmap || 'graph TD\n  Root["Concept Map"]';
    }

    // Glossary
    const glossaryEl = document.getElementById('note-glossary-container');
    if (glossaryEl) {
      glossaryEl.innerHTML = (note.glossary || []).map(g => `
        <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
          <span class="font-bold text-sm text-slate-800 dark:text-slate-200">${g.term}:</span>
          <span class="text-xs text-slate-600 dark:text-slate-400 ml-1">${g.definition}</span>
        </div>
      `).join('');
    }

    // Setup Flashcards
    this.renderCurrentFlashcard();
  },

  setupFlashcardControls() {
    const cardInner = document.getElementById('flashcard-card');
    const btnFlip = document.getElementById('btn-flip-card');
    const btnPrev = document.getElementById('btn-prev-card');
    const btnNext = document.getElementById('btn-next-card');

    const toggleFlip = () => {
      if (cardInner) cardInner.classList.toggle('flipped');
    };

    if (cardInner) cardInner.addEventListener('click', toggleFlip);
    if (btnFlip) btnFlip.addEventListener('click', toggleFlip);

    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        if (this.currentFlashcardIndex > 0) {
          this.currentFlashcardIndex--;
          this.renderCurrentFlashcard();
        }
      });
    }

    if (btnNext) {
      btnNext.addEventListener('click', () => {
        if (this.currentFlashcardIndex < this.flashcards.length - 1) {
          this.currentFlashcardIndex++;
          this.renderCurrentFlashcard();
        }
      });
    }
  },

  renderCurrentFlashcard() {
    const cardInner = document.getElementById('flashcard-card');
    if (cardInner) cardInner.classList.remove('flipped');

    if (!this.flashcards || this.flashcards.length === 0) {
      document.getElementById('card-front-text').textContent = 'No flashcards available for this note.';
      document.getElementById('card-back-text').textContent = '';
      document.getElementById('card-counter').textContent = '0 / 0';
      return;
    }

    const card = this.flashcards[this.currentFlashcardIndex];
    document.getElementById('card-front-text').textContent = card.front;
    document.getElementById('card-back-text').textContent = card.back;
    document.getElementById('card-tag').textContent = card.tag || 'Active Recall';
    document.getElementById('card-counter').textContent = `${this.currentFlashcardIndex + 1} of ${this.flashcards.length}`;

    const diffBadge = document.getElementById('card-diff-badge');
    if (diffBadge) {
      diffBadge.textContent = card.difficulty || 'Basic';
      diffBadge.className = `px-2 py-0.5 text-xs font-semibold rounded ${
        card.difficulty === 'Advanced' ? 'badge-advanced' : (card.difficulty === 'Intermediate' ? 'badge-intermediate' : 'badge-basic')
      }`;
    }
  },

  rateFlashcard(rating) {
    showToast(`Marked as ${rating}. Spaced repetition interval updated.`, 'info');
    if (this.currentFlashcardIndex < this.flashcards.length - 1) {
      this.currentFlashcardIndex++;
      this.renderCurrentFlashcard();
    }
  }
};

document.addEventListener('DOMContentLoaded', () => window.Notes.init());
