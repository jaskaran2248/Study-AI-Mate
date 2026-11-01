/**
 * StudyMate AI - Interactive Tiered Quiz & Exam Runner
 */

window.Quiz = {
  currentQuiz: null,
  currentIndex: 0,
  userAnswers: {},
  timerInterval: null,
  timeRemainingSec: 0,
  timeSpentSec: 0,
  lastAttemptResult: null,

  init() {
    this.quizListEl = document.getElementById('quizzes-list-container');
    this.runnerEl = document.getElementById('quiz-runner-container');
    this.resultsEl = document.getElementById('quiz-results-container');
    this.setupListeners();
  },

  setupListeners() {
    const btnNewQuiz = document.getElementById('btn-open-create-quiz');
    const modal = document.getElementById('create-quiz-modal');
    const btnCloseModal = document.getElementById('btn-close-quiz-modal');
    const btnSubmitCreate = document.getElementById('btn-submit-create-quiz');

    if (btnNewQuiz && modal) {
      btnNewQuiz.addEventListener('click', async () => {
        modal.classList.remove('hidden');
        await this.populateDocumentDropdown();
      });
    }

    if (btnCloseModal && modal) {
      btnCloseModal.addEventListener('click', () => modal.classList.add('hidden'));
    }

    if (btnSubmitCreate) {
      btnSubmitCreate.addEventListener('click', () => this.handleCreateQuiz());
    }

    // Runner controls
    const btnPrev = document.getElementById('btn-quiz-prev');
    const btnNext = document.getElementById('btn-quiz-next');
    const btnFinish = document.getElementById('btn-quiz-finish');
    const btnHint = document.getElementById('btn-quiz-hint');

    if (btnPrev) btnPrev.addEventListener('click', () => this.navigateQuestion(-1));
    if (btnNext) btnNext.addEventListener('click', () => this.navigateQuestion(1));
    if (btnFinish) btnFinish.addEventListener('click', () => this.submitQuiz());
    if (btnHint) btnHint.addEventListener('click', () => this.toggleHint());
  },

  async populateDocumentDropdown() {
    const select = document.getElementById('quiz-doc-select');
    if (!select) return;

    try {
      const res = await fetch('/api/documents');
      const data = await res.json();
      const docs = data.documents || [];

      select.innerHTML = '<option value="">-- Choose from Uploaded Materials (or enter custom topic below) --</option>' +
        docs.map(d => `<option value="${d.id}">${d.title} (${d.subject})</option>`).join('');
    } catch (e) {
      console.error(e);
    }
  },

  async handleCreateQuiz() {
    const docId = document.getElementById('quiz-doc-select')?.value;
    const customTopic = document.getElementById('quiz-custom-topic')?.value.trim();
    const tier = document.getElementById('quiz-tier-select')?.value || 'Adaptive Mix';
    const count = parseInt(document.getElementById('quiz-count-select')?.value || '8');
    const timeLimit = parseInt(document.getElementById('quiz-time-select')?.value || '12');

    if (!docId && !customTopic) {
      showToast('Please select a document or enter a custom topic.', 'warning');
      return;
    }

    const payload = {
      difficulty_tier: tier,
      question_count: count,
      time_limit_min: timeLimit
    };
    if (docId) payload.document_id = parseInt(docId);
    if (customTopic) payload.topic = customTopic;

    document.getElementById('create-quiz-modal')?.classList.add('hidden');
    showToast(`Generating ${tier} quiz...`, 'info');

    try {
      const res = await fetch('/api/quiz/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to generate quiz');

      showToast(`Quiz ready! ${data.question_count} questions generated.`, 'success');
      this.startQuiz(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  async loadQuizzesList() {
    try {
      const res = await fetch('/api/quiz');
      const data = await res.json();
      const quizzes = data.quizzes || [];

      if (!this.quizListEl) return;

      if (quizzes.length === 0) {
        this.quizListEl.innerHTML = `
          <div class="p-8 text-center text-slate-400 bg-white dark:bg-slate-900 rounded-xl border border-dashed border-slate-300 dark:border-slate-800">
            No quizzes generated yet. Click "+ Create Custom Quiz" or pick an uploaded document!
          </div>
        `;
        return;
      }

      this.quizListEl.innerHTML = quizzes.map(q => `
        <div class="p-5 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow transition flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 text-xs font-semibold rounded ${
                q.difficulty_tier === 'Mastery' ? 'badge-mastery' :
                (q.difficulty_tier === 'Advanced' ? 'badge-advanced' :
                (q.difficulty_tier === 'Intermediate' ? 'badge-intermediate' : 'badge-basic'))
              }">
                ${q.difficulty_tier}
              </span>
              <span class="text-xs text-slate-400">⏱️ ${q.time_limit_min} mins</span>
            </div>
            <h4 class="font-bold text-slate-800 dark:text-slate-100 text-base mt-2">${q.title}</h4>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">${q.description || q.topic}</p>
          </div>

          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <span class="text-xs text-slate-500 dark:text-slate-400">
              ${q.actual_question_count || q.question_count} Questions
              ${q.best_score != null ? `• Best: <strong class="text-emerald-600">${q.best_score}%</strong>` : ''}
            </span>
            <button onclick="window.Quiz.loadAndStartQuiz(${q.id})" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition shadow-sm">
              Start Quiz →
            </button>
          </div>
        </div>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  async loadAndStartQuiz(quizId) {
    try {
      const res = await fetch(`/api/quiz/${quizId}`);
      if (!res.ok) throw new Error('Quiz not found');
      const quiz = await res.json();
      this.startQuiz(quiz);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  startQuiz(quiz) {
    this.currentQuiz = quiz;
    this.currentIndex = 0;
    this.userAnswers = {};
    this.timeSpentSec = 0;
    this.timeRemainingSec = (quiz.time_limit_min || 15) * 60;

    // Switch view to runner
    document.getElementById('quizzes-overview-view')?.classList.add('hidden');
    document.getElementById('quiz-results-container')?.classList.add('hidden');
    document.getElementById('quiz-runner-container')?.classList.remove('hidden');

    // Title
    document.getElementById('runner-quiz-title').textContent = quiz.title;

    // Start timer
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.updateTimerDisplay();
    this.timerInterval = setInterval(() => {
      this.timeRemainingSec--;
      this.timeSpentSec++;
      this.updateTimerDisplay();
      if (this.timeRemainingSec <= 0) {
        clearInterval(this.timerInterval);
        showToast('Time is up! Submitting quiz...', 'warning');
        this.submitQuiz();
      }
    }, 1000);

    this.renderQuestion();
  },

  updateTimerDisplay() {
    const timerEl = document.getElementById('runner-timer');
    if (!timerEl) return;
    const mins = Math.floor(Math.max(0, this.timeRemainingSec) / 60);
    const secs = Math.max(0, this.timeRemainingSec) % 60;
    timerEl.textContent = `⏱️ ${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  },

  renderQuestion() {
    const questions = this.currentQuiz.questions || [];
    if (questions.length === 0) return;

    const q = questions[this.currentIndex];

    // Progress bar
    const progressPct = ((this.currentIndex + 1) / questions.length) * 100;
    document.getElementById('runner-progress-bar').style.width = `${progressPct}%`;
    document.getElementById('runner-progress-text').textContent = `Question ${this.currentIndex + 1} of ${questions.length}`;

    // Difficulty & Bloom's badge
    const diffBadge = document.getElementById('runner-diff-badge');
    if (diffBadge) {
      const diff = (q.difficulty || 'basic').toLowerCase();
      diffBadge.textContent = `${q.difficulty.toUpperCase()} • Bloom's: ${q.bloom_level || 'Recall'}`;
      diffBadge.className = `px-2.5 py-1 text-xs font-bold rounded-lg ${
        diff === 'mastery' ? 'badge-mastery' :
        (diff === 'advanced' ? 'badge-advanced' :
        (diff === 'intermediate' ? 'badge-intermediate' : 'badge-basic'))
      }`;
    }

    // Points
    document.getElementById('runner-points-badge').textContent = `+${q.points || 10} XP`;

    // Question stem
    document.getElementById('runner-question-text').textContent = q.question_text;

    // Hint element reset
    const hintBox = document.getElementById('runner-hint-box');
    if (hintBox) {
      hintBox.classList.add('hidden');
      document.getElementById('runner-hint-text').textContent = q.hint || 'No specific hint for this question.';
    }

    // Options rendering
    const optionsContainer = document.getElementById('runner-options-container');
    optionsContainer.innerHTML = '';

    const selectedAns = this.userAnswers[q.id.toString()] || '';

    (q.options || []).forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.className = `w-full text-left p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 quiz-opt-btn flex items-center space-x-3 text-sm font-medium ${
        selectedAns === opt ? 'selected' : ''
      }`;
      const letters = ['A', 'B', 'C', 'D', 'E'];
      btn.innerHTML = `
        <span class="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
          ${letters[idx] || (idx + 1)}
        </span>
        <span class="flex-1 text-slate-800 dark:text-slate-200">${opt}</span>
      `;
      btn.addEventListener('click', () => {
        this.userAnswers[q.id.toString()] = opt;
        this.renderQuestion();
      });
      optionsContainer.appendChild(btn);
    });

    // Navigation buttons state
    document.getElementById('btn-quiz-prev').disabled = this.currentIndex === 0;
    const isLast = this.currentIndex === questions.length - 1;
    document.getElementById('btn-quiz-next').classList.toggle('hidden', isLast);
    document.getElementById('btn-quiz-finish').classList.toggle('hidden', !isLast);
  },

  navigateQuestion(delta) {
    const questions = this.currentQuiz.questions || [];
    const nextIdx = this.currentIndex + delta;
    if (nextIdx >= 0 && nextIdx < questions.length) {
      this.currentIndex = nextIdx;
      this.renderQuestion();
    }
  },

  toggleHint() {
    const hintBox = document.getElementById('runner-hint-box');
    if (hintBox) hintBox.classList.toggle('hidden');
  },

  async submitQuiz() {
    if (this.timerInterval) clearInterval(this.timerInterval);

    showToast('Evaluating answers and updating skill mastery...', 'info');

    try {
      const res = await fetch('/api/quiz/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          quiz_id: this.currentQuiz.id,
          time_spent_sec: this.timeSpentSec,
          answers: this.userAnswers
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Submission failed');

      this.lastAttemptResult = data;
      this.showResults(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  showResults(res) {
    document.getElementById('quiz-runner-container')?.classList.add('hidden');
    const container = document.getElementById('quiz-results-container');
    if (!container) return;
    container.classList.remove('hidden');

    // Scorecard Values
    document.getElementById('res-percentage').textContent = `${res.percentage}%`;
    document.getElementById('res-score').textContent = `${res.score} / ${res.max_score} pts`;
    document.getElementById('res-xp').textContent = `+${res.xp_earned} XP`;
    document.getElementById('res-mastery').textContent = res.new_mastery_level || 'Apprentice';
    document.getElementById('res-feedback').textContent = res.ai_feedback;

    // Difficulty Breakdown Bars (Structured & Zero-Overlap)
    const bk = res.difficulty_breakdown || {};
    const renderTierBar = (tierName, barId, labelId) => {
      const t = bk[tierName] || { correct: 0, total: 0 };
      const pct = t.total > 0 ? Math.round((t.correct / t.total) * 100) : 0;
      const barEl = document.getElementById(barId);
      const labelEl = document.getElementById(labelId);
      if (barEl) {
        barEl.style.width = `${pct}%`;
      }
      if (labelEl) {
        labelEl.textContent = `${pct}% (${t.correct}/${t.total})`;
      }
    };
    renderTierBar('basic', 'bar-tier-basic', 'label-tier-basic');
    renderTierBar('intermediate', 'bar-tier-intermediate', 'label-tier-intermediate');
    renderTierBar('advanced', 'bar-tier-advanced', 'label-tier-advanced');
    renderTierBar('mastery', 'bar-tier-mastery', 'label-tier-mastery');

    // Remediation Button Handling
    const remediationBtn = document.getElementById('btn-launch-remediation');
    if (remediationBtn) {
      if (res.remediation_topics && res.remediation_topics.length > 0) {
        remediationBtn.classList.remove('hidden');
        remediationBtn.textContent = `🎯 Practice Missed Topics (${res.remediation_topics.length} Areas)`;
        remediationBtn.onclick = () => this.launchRemediationQuiz(res.remediation_topics);
      } else {
        remediationBtn.classList.add('hidden');
      }
    }

    // Review List
    const reviewList = document.getElementById('res-review-container');
    if (reviewList) {
      reviewList.innerHTML = (res.review || []).map((item, idx) => `
        <div class="p-5 rounded-xl border ${item.is_correct ? 'border-emerald-200 dark:border-emerald-900/40 bg-emerald-50/40 dark:bg-emerald-950/20' : 'border-rose-200 dark:border-rose-900/40 bg-rose-50/40 dark:bg-rose-950/20'}">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold ${item.is_correct ? 'text-emerald-700 dark:text-emerald-400' : 'text-rose-700 dark:text-rose-400'}">
              ${item.is_correct ? '✓ Correct' : '✗ Needs Revision'} • ${item.difficulty.toUpperCase()}
            </span>
            <span class="text-xs text-slate-500">${item.bloom_level}</span>
          </div>
          <h5 class="font-bold text-slate-800 dark:text-slate-100 mt-2">${idx + 1}. ${item.question_text}</h5>
          
          <div class="mt-2 text-xs space-y-1">
            <p><span class="font-semibold text-slate-600 dark:text-slate-400">Your Answer:</span> <span class="${item.is_correct ? 'text-emerald-700 font-semibold' : 'text-rose-700 font-semibold'}">${item.user_answer || '(Unanswered)'}</span></p>
            ${!item.is_correct ? `<p><span class="font-semibold text-slate-600 dark:text-slate-400">Correct Answer:</span> <strong class="text-emerald-700 dark:text-emerald-400">${item.correct_answer}</strong></p>` : ''}
          </div>

          <div class="mt-3 p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-300">
            <span class="font-bold">Explanation:</span> ${item.explanation}
          </div>
        </div>
      `).join('');
    }
  },

  async launchRemediationQuiz(topics) {
    showToast('AI is generating targeted drill on your missed concepts...', 'info');
    try {
      const res = await fetch('/api/quiz/remediation', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(topics)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to generate remediation quiz');

      showToast(`Remediation drill ready!`, 'success');
      this.startQuiz(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  exitQuiz() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    document.getElementById('quiz-runner-container')?.classList.add('hidden');
    document.getElementById('quiz-results-container')?.classList.add('hidden');
    document.getElementById('quizzes-overview-view')?.classList.remove('hidden');
    this.loadQuizzesList();
  }
};

document.addEventListener('DOMContentLoaded', () => window.Quiz.init());
