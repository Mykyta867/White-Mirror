// ─── MODALS ───────────────────────────────────────
function openModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// Close on overlay click
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
    document.body.style.overflow = '';
  }
});

// Close on Escape key
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(m => {
      m.classList.remove('open');
      document.body.style.overflow = '';
    });
  }
});

// ─── AUTO-DISMISS ALERTS ──────────────────────────
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(20px)';
    alert.style.transition = 'all 0.3s ease';
    setTimeout(() => alert.remove(), 300);
  }, 4000);
});

// ─── CONFIRM DELETE ───────────────────────────────
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', function (e) {
    const msg = this.dataset.confirm || 'Ви впевнені?';
    if (!confirm(msg)) e.preventDefault();
  });
});

// ─── ACTIVE NAV ───────────────────────────────────
// Already handled server-side via active_page context
