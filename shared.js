/* _shared.js — UI_PJEV Documentation */

/* ── Copiar código ── */
function copyCode(blockId, btn) {
  const block = document.getElementById(blockId);
  const pre   = block ? block.querySelector('pre') : null;
  if (!pre) return;
  navigator.clipboard.writeText(pre.innerText).then(() => {
    btn.textContent = '✓ Copiado';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copiar'; btn.classList.remove('copied'); }, 2000);
  });
}

/* ── Marcar link activo en sidebar ── */
function markActiveSidebarLink() {
  const current = location.pathname.split('/').pop();
  document.querySelectorAll('.sidebar-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === current) link.classList.add('active');
  });
}

document.addEventListener('DOMContentLoaded', markActiveSidebarLink);
