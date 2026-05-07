// T&Q Lab Guide — Navigation & Language Switcher

document.addEventListener('DOMContentLoaded', function () {

  // Mark active nav link based on current page filename
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href').split('/').pop();
    if (href === currentPage) {
      link.classList.add('active');
    }
  });

  // ── Collapsible nav sections ──────────────────────────────────────────────
  // Section titles act as toggles; their submenu is the following <ul class="nav-submenu">
  const sectionTitles = document.querySelectorAll('.nav-section-title');

  sectionTitles.forEach(title => {
    const submenu = title.nextElementSibling;
    if (!submenu || !submenu.classList.contains('nav-submenu')) return;

    // Check if the active page lives in this section
    const hasActive = submenu.querySelector('.nav-link.active');

    // Start expanded if active page is inside, collapsed otherwise
    if (hasActive) {
      title.classList.add('open');
      submenu.style.display = 'block';
    } else {
      title.classList.remove('open');
      submenu.style.display = 'none';
    }

    title.style.cursor = 'pointer';
    title.addEventListener('click', () => {
      const isOpen = title.classList.toggle('open');
      submenu.style.display = isOpen ? 'block' : 'none';
    });
  });

  // Mobile hamburger toggle
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.querySelector('.sidebar');
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => sidebar.classList.toggle('open'));
  }

  // Language switcher
  const langSelect = document.getElementById('lang-select');
  if (langSelect) {
    const pathParts = window.location.pathname.split('/');
    const langIndex = pathParts.indexOf('docs') + 1;
    const currentLang = (langIndex > 0 && pathParts[langIndex] && pathParts[langIndex].length === 2)
      ? pathParts[langIndex]
      : 'en';
    langSelect.value = currentLang;

    langSelect.addEventListener('change', function () {
      const selectedLang = this.value;
      const currentPath = window.location.pathname;

      let newPath;
      if (selectedLang === 'en') {
        newPath = currentPath.replace(/\/docs\/[a-z]{2}\//, '/docs/');
      } else {
        if (currentPath.includes('/docs/') && !currentPath.match(/\/docs\/[a-z]{2}\//)) {
          newPath = currentPath.replace('/docs/', `/docs/${selectedLang}/`);
        } else {
          newPath = currentPath.replace(/\/docs\/[a-z]{2}\//, `/docs/${selectedLang}/`);
        }
      }
      window.location.href = newPath;
    });
  }

});
