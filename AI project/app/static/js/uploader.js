/**
 * StudyMate AI - Uploader & Document Management Module
 */

window.Uploader = {
  init() {
    this.dropZone = document.getElementById('drop-zone');
    this.fileInput = document.getElementById('file-upload-input');
    this.btnUploadFile = document.getElementById('btn-submit-file');
    this.btnPasteSubmit = document.getElementById('btn-submit-paste');

    if (this.dropZone && this.fileInput) {
      this.dropZone.addEventListener('click', () => this.fileInput.click());

      this.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        this.dropZone.classList.add('border-blue-500', 'bg-blue-50', 'dark:bg-blue-950/20');
      });

      this.dropZone.addEventListener('dragleave', () => {
        this.dropZone.classList.remove('border-blue-500', 'bg-blue-50', 'dark:bg-blue-950/20');
      });

      this.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        this.dropZone.classList.remove('border-blue-500', 'bg-blue-50', 'dark:bg-blue-950/20');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          this.fileInput.files = e.dataTransfer.files;
          this.handleFileSelected();
        }
      });

      this.fileInput.addEventListener('change', () => this.handleFileSelected());
    }

    if (this.btnPasteSubmit) {
      this.btnPasteSubmit.addEventListener('click', () => this.submitPastedText());
    }
  },

  handleFileSelected() {
    const file = this.fileInput.files[0];
    if (!file) return;

    const fileStatus = document.getElementById('selected-file-name');
    if (fileStatus) {
      fileStatus.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
      fileStatus.classList.remove('hidden');
    }

    // Auto-upload file
    this.uploadSelectedFile(file);
  },

  async uploadSelectedFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const subject = document.getElementById('upload-subject')?.value || 'General Studies';
    const focus = document.getElementById('upload-focus')?.value || 'Comprehensive Core Mastery';
    formData.append('subject', subject);
    formData.append('sdg_target', focus);

    showToast(`Uploading and analyzing ${file.name}...`, 'info');

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Upload failed');

      showToast(`Success! Extracted ${data.word_count} words from ${file.name}`, 'success');
      this.fileInput.value = '';
      const fileStatus = document.getElementById('selected-file-name');
      if (fileStatus) fileStatus.classList.add('hidden');
      
      this.loadDocuments();
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  async submitPastedText() {
    const title = document.getElementById('paste-title')?.value.trim();
    const content = document.getElementById('paste-content')?.value.trim();
    const subject = document.getElementById('paste-subject')?.value || 'General Studies';

    if (!content) {
      showToast('Please paste or write your study notes or syllabus text.', 'warning');
      return;
    }

    const formData = new FormData();
    formData.append('title', title || 'Custom Notes');
    formData.append('custom_text', content);
    formData.append('subject', subject);
    formData.append('sdg_target', 'Core Curriculum');

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Submission failed');

      showToast(`Syllabus ingested! (${data.word_count} words)`, 'success');
      document.getElementById('paste-title').value = '';
      document.getElementById('paste-content').value = '';
      this.loadDocuments();
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  async loadDocuments() {
    const container = document.getElementById('documents-list');
    if (!container) return;

    try {
      const res = await fetch('/api/documents');
      const data = await res.json();
      const docs = data.documents || [];

      if (docs.length === 0) {
        container.innerHTML = `
          <div class="p-8 text-center text-slate-400 bg-white dark:bg-slate-900 rounded-xl border border-dashed border-slate-300 dark:border-slate-800">
            <p class="text-sm">No study materials uploaded yet. Upload a document or select a sample module below!</p>
          </div>
        `;
        return;
      }

      container.innerHTML = docs.map(d => `
        <div class="p-5 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow transition">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 text-xs font-semibold rounded uppercase bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
                  ${d.file_type || 'txt'}
                </span>
                <h4 class="font-bold text-slate-800 dark:text-slate-100">${d.title}</h4>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                ${d.subject} • ${d.word_count} words • ~${d.reading_time_min} min read
              </p>
              <div class="flex flex-wrap gap-1 mt-2">
                <span class="px-2 py-0.5 text-xs rounded-full bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-300 font-medium border border-blue-200 dark:border-blue-900/40">
                  ${d.sdg_target || 'Core Curriculum'}
                </span>
                ${(d.tags || '').split(',').slice(0, 3).map(tag => tag.trim() ? `
                  <span class="px-2 py-0.5 text-xs rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                    #${tag.trim()}
                  </span>
                ` : '').join('')}
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <button onclick="window.Uploader.quickGenerateNotes(${d.id})" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition flex items-center space-x-1 shadow-sm">
                <span>📘 Study Notes</span>
              </button>
              <button onclick="window.Uploader.quickGenerateQuiz(${d.id})" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition flex items-center space-x-1 shadow-sm">
                <span>🎯 Adaptive Quiz</span>
              </button>
              <button onclick="window.Uploader.deleteDoc(${d.id})" class="p-1.5 text-slate-400 hover:text-red-500 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition" title="Delete">
                🗑️
              </button>
            </div>
          </div>
        </div>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  async quickGenerateNotes(docId) {
    showToast('AI is generating comprehensive study notes...', 'info');
    try {
      const res = await fetch('/api/notes/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ document_id: docId })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Note generation failed');

      showToast('Notes generated successfully!', 'success');
      switchTab('notes');
      window.Notes?.displayNote(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  async quickGenerateQuiz(docId) {
    showToast('AI is generating tiered quiz (Basic -> Advanced)...', 'info');
    try {
      const res = await fetch('/api/quiz/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          document_id: docId,
          difficulty_tier: 'Adaptive Mix',
          question_count: 8,
          time_limit_min: 12
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Quiz generation failed');

      showToast(`Generated ${data.question_count} tiered questions!`, 'success');
      switchTab('quiz');
      window.Quiz?.startQuiz(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  async deleteDoc(docId) {
    if (!confirm('Are you sure you want to delete this study document?')) return;
    try {
      const res = await fetch(`/api/documents/${docId}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('Document removed', 'info');
        this.loadDocuments();
      }
    } catch (err) {
      showToast('Failed to delete document', 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => window.Uploader.init());
