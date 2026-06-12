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

/* ── Inyectar Botones de Herramientas ── */
function injectToolbar() {
  if (window.self !== window.top && !document.querySelector('.topbar')) {
    const toolbar = document.createElement('div');
    toolbar.style.position = 'fixed';
    toolbar.style.top = '20px';
    toolbar.style.right = '40px';
    toolbar.style.display = 'flex';
    toolbar.style.gap = '10px';
    toolbar.style.zIndex = '9999';

    const btnStyle = "padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid #D4C9B5; border-radius: 6px; background: #fff; color: #1B3A2D; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: background 0.2s;";

    const btnRefresh = document.createElement('button');
    btnRefresh.innerText = '⟳ Refrescar';
    btnRefresh.style.cssText = btnStyle;
    btnRefresh.onmouseover = () => btnRefresh.style.background = '#f5f5f5';
    btnRefresh.onmouseout = () => btnRefresh.style.background = '#fff';
    btnRefresh.onclick = () => location.reload();

    const btnPrint = document.createElement('button');
    btnPrint.innerText = '🖨 Imprimir';
    btnPrint.style.cssText = btnStyle;
    btnPrint.onmouseover = () => btnPrint.style.background = '#f5f5f5';
    btnPrint.onmouseout = () => btnPrint.style.background = '#fff';
    btnPrint.onclick = () => window.print();

    toolbar.appendChild(btnRefresh);
    toolbar.appendChild(btnPrint);
    
    // Si la página tiene un diagrama de flujo oculto, agregamos el botón
    const flowchartContainer = document.getElementById('module-flowchart');
    if (flowchartContainer) {
      const btnDiagram = document.createElement('button');
      btnDiagram.innerText = '📊 Ver Diagrama';
      btnDiagram.style.cssText = btnStyle + " background: #1B3A2D; color: #fff; border-color: #1B3A2D;";
      btnDiagram.onmouseover = () => btnDiagram.style.background = '#142a20';
      btnDiagram.onmouseout = () => btnDiagram.style.background = '#1B3A2D';
      
      btnDiagram.onclick = () => showModal('Diagrama Interfuncional del Procedimiento', flowchartContainer.innerHTML);
      toolbar.insertBefore(btnDiagram, btnRefresh);
    }

    // Si la página tiene la tabla de procesos, agregamos el botón
    const processTableContainer = document.getElementById('module-process-table');
    if (processTableContainer) {
      const btnProcess = document.createElement('button');
      btnProcess.innerText = '📋 Proceso Funcional';
      btnProcess.style.cssText = btnStyle + " background: #991b1b; color: #fff; border-color: #991b1b;";
      btnProcess.onmouseover = () => btnProcess.style.background = '#7f1d1d';
      btnProcess.onmouseout = () => btnProcess.style.background = '#991b1b';
      
      btnProcess.onclick = () => showModal('Flujograma de Procesos y Descripción', processTableContainer.innerHTML);
      toolbar.insertBefore(btnProcess, btnRefresh);
    }

    // Si la página tiene el anexo de conceptos sugeridos, agregamos el botón
    const conceptsContainer = document.getElementById('module-suggested-concepts');
    if (conceptsContainer) {
      const btnConcepts = document.createElement('button');
      btnConcepts.innerText = '💡 Conceptos Sugeridos';
      btnConcepts.style.cssText = btnStyle + " background: #0284c7; color: #fff; border-color: #0284c7;";
      btnConcepts.onmouseover = () => btnConcepts.style.background = '#0369a1';
      btnConcepts.onmouseout = () => btnConcepts.style.background = '#0284c7';
      
      btnConcepts.onclick = () => showModal('Anexo: Conceptos de Ingreso Sugeridos', conceptsContainer.innerHTML);
      toolbar.insertBefore(btnConcepts, btnRefresh);
    }

    function showModal(titleText, contentHTML) {
      const modal = document.createElement('div');
      modal.style.position = 'fixed';
      modal.style.top = '0'; modal.style.left = '0';
      modal.style.width = '100vw'; modal.style.height = '100vh';
      modal.style.background = 'rgba(0,0,0,0.6)';
      modal.style.display = 'flex';
      modal.style.alignItems = 'center';
      modal.style.justifyContent = 'center';
      modal.style.zIndex = '10000';
      modal.style.backdropFilter = 'blur(3px)';
      
      const modalBox = document.createElement('div');
      modalBox.style.background = '#fff';
      modalBox.style.padding = '30px';
      modalBox.style.borderRadius = '12px';
      modalBox.style.width = '90%';
      modalBox.style.maxWidth = '1000px';
      modalBox.style.maxHeight = '90vh';
      modalBox.style.overflowY = 'auto';
      modalBox.style.boxShadow = '0 10px 40px rgba(0,0,0,0.2)';
      modalBox.style.position = 'relative';
      
      const btnClose = document.createElement('button');
      btnClose.innerText = '✖ Cerrar';
      btnClose.style.position = 'absolute';
      btnClose.style.top = '15px';
      btnClose.style.right = '15px';
      btnClose.style.padding = '6px 12px';
      btnClose.style.background = '#dc2626';
      btnClose.style.color = '#fff';
      btnClose.style.border = 'none';
      btnClose.style.borderRadius = '6px';
      btnClose.style.cursor = 'pointer';
      btnClose.style.fontWeight = 'bold';
      btnClose.onclick = () => document.body.removeChild(modal);
      
      const diagramTitle = document.createElement('h3');
      diagramTitle.innerText = titleText;
      diagramTitle.style.marginTop = '0';
      diagramTitle.style.color = '#1B3A2D';
      
      const diagramContent = document.createElement('div');
      diagramContent.innerHTML = contentHTML;
      diagramContent.style.marginTop = '20px';
      diagramContent.style.textAlign = 'center';
      
      modalBox.appendChild(btnClose);
      modalBox.appendChild(diagramTitle);
      modalBox.appendChild(diagramContent);
      modal.appendChild(modalBox);
      document.body.appendChild(modal);
    }

    document.body.appendChild(toolbar);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  markActiveSidebarLink();
  injectToolbar();
});
