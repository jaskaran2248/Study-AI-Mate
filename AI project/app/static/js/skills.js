/**
 * StudyMate AI - Skills & Analytics Module
 */

window.Skills = {
  init() {
    this.container = document.getElementById('skills-dashboard-container');
  },

  async loadDashboard() {
    try {
      const res = await fetch('/api/skills/dashboard');
      const data = await res.json();
      this.renderDashboard(data);
    } catch (err) {
      console.error(err);
    }
  },

  renderDashboard(data) {
    // Top Stats Counters
    const xpEl = document.getElementById('stat-total-xp');
    const quizzesEl = document.getElementById('stat-quizzes-taken');
    const accEl = document.getElementById('stat-avg-accuracy');
    const headerXpEl = document.getElementById('header-xp-badge');

    if (xpEl) xpEl.textContent = `${data.total_xp} XP`;
    if (quizzesEl) quizzesEl.textContent = data.quizzes_completed;
    if (accEl) accEl.textContent = `${data.average_accuracy}%`;
    if (headerXpEl) headerXpEl.textContent = `⭐ ${data.total_xp} XP`;

    // Skills Competency Bars
    const skillsListEl = document.getElementById('skills-tree-list');
    if (skillsListEl) {
      const skills = data.skills || [];
      if (skills.length === 0) {
        skillsListEl.innerHTML = `
          <div class="p-6 text-center text-slate-400">
            No skill history yet. Complete your first quiz to calibrate your competencies!
          </div>
        `;
      } else {
        skillsListEl.innerHTML = skills.map(s => `
          <div class="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <div>
                <h5 class="font-bold text-slate-800 dark:text-slate-100 text-sm">${s.skill_name}</h5>
                <span class="text-xs text-slate-400">${s.mastery_level} • ${s.xp} XP</span>
              </div>
              <span class="text-sm font-extrabold text-blue-600 dark:text-blue-400">${s.mastery_percent}%</span>
            </div>

            <!-- Master Bar -->
            <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2 mb-3 overflow-hidden">
              <div class="bg-blue-600 h-2 rounded-full transition-width" style="width: ${Math.min(100, s.mastery_percent)}%"></div>
            </div>

            <!-- 4-Tier Sub-Bar Matrix -->
            <div class="grid grid-cols-4 gap-2 text-center text-xs">
              <div class="p-1.5 rounded bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300">
                <span class="block text-[10px] font-semibold text-slate-400">Basic</span>
                <span class="font-bold">${Math.round(s.basic_score || 0)}%</span>
              </div>
              <div class="p-1.5 rounded bg-amber-50 dark:bg-amber-950/20 text-amber-800 dark:text-amber-300">
                <span class="block text-[10px] font-semibold text-slate-400">Applied</span>
                <span class="font-bold">${Math.round(s.intermediate_score || 0)}%</span>
              </div>
              <div class="p-1.5 rounded bg-indigo-50 dark:bg-indigo-950/20 text-indigo-800 dark:text-indigo-300">
                <span class="block text-[10px] font-semibold text-slate-400">Advanced</span>
                <span class="font-bold">${Math.round(s.advanced_score || 0)}%</span>
              </div>
              <div class="p-1.5 rounded bg-purple-50 dark:bg-purple-950/20 text-purple-800 dark:text-purple-300">
                <span class="block text-[10px] font-semibold text-slate-400">Mastery</span>
                <span class="font-bold">${Math.round(s.mastery_score || 0)}%</span>
              </div>
            </div>
          </div>
        `).join('');
      }
    }

    // Badges Shelf
    const badgesEl = document.getElementById('badges-shelf-container');
    if (badgesEl) {
      badgesEl.innerHTML = (data.badges || []).map(b => `
        <div class="p-4 rounded-xl border ${b.unlocked ? 'border-amber-300/80 dark:border-amber-800/60 bg-amber-50/40 dark:bg-amber-950/20' : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/40 opacity-50'} flex items-center space-x-3">
          <div class="text-3xl">${b.icon}</div>
          <div>
            <div class="flex items-center space-x-1.5">
              <h5 class="font-bold text-xs text-slate-800 dark:text-slate-100">${b.name}</h5>
              ${b.unlocked ? '<span class="text-[10px] font-bold text-amber-600">UNLOCKED</span>' : '<span class="text-[10px] text-slate-400">LOCKED</span>'}
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">${b.desc}</p>
          </div>
        </div>
      `).join('');
    }

    // Recent Attempts Table
    const historyEl = document.getElementById('recent-attempts-list');
    if (historyEl) {
      const attempts = data.recent_attempts || [];
      if (attempts.length === 0) {
        historyEl.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-slate-400 text-xs">No attempts recorded yet.</td></tr>`;
      } else {
        historyEl.innerHTML = attempts.map(a => `
          <tr class="border-b border-slate-100 dark:border-slate-800 text-xs">
            <td class="p-3 font-semibold text-slate-800 dark:text-slate-100">${a.quiz_title}</td>
            <td class="p-3">
              <span class="font-bold ${a.percentage >= 75 ? 'text-emerald-600' : (a.percentage >= 50 ? 'text-amber-600' : 'text-rose-600')}">
                ${a.percentage}%
              </span>
            </td>
            <td class="p-3 text-slate-500">${a.time_spent_sec}s</td>
            <td class="p-3 text-slate-400">${new Date(a.created_at).toLocaleDateString()}</td>
            <td class="p-3">
              <button onclick="window.Quiz.loadAndStartQuiz(${a.quiz_id}); switchTab('quiz');" class="text-blue-600 font-bold hover:underline">
                Retake →
              </button>
            </td>
          </tr>
        `).join('');
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', () => window.Skills.init());
