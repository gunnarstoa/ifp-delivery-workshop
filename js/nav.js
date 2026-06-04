// T&Q Lab Guide — Navigation & Language Switcher

document.addEventListener('DOMContentLoaded', function () {

  // Mark active nav link based on current page filename
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href').split('/').pop();
    if (href === currentPage) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
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

    // All sections start expanded. Only highlight the section with active page.
    title.classList.add('open');
    submenu.style.display = 'block';

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

  // ── Language switcher ─────────────────────────────────────────────────────
  // Handles two URL patterns:
  //   1. Docs pages:  /docs/page.html  ↔  /docs/{lang}/page.html
  //   2. Root index:  /index.html      ↔  /{lang}/index.html
  // GitHub Pages subpath prefixes (e.g. /ifp-delivery-workshop/) are preserved.
  const langSelect = document.getElementById('lang-select');
  if (langSelect) {
    function detectLang(path) {
      const docsMatch = path.match(/\/docs\/([a-z]{2})\//);
      if (docsMatch) return docsMatch[1];
      // Root /{lang}/ — only when NOT under /docs/
      if (!path.includes('/docs/')) {
        const rootMatch = path.match(/\/([a-z]{2})\/(?:index\.html)?$/);
        if (rootMatch) return rootMatch[1];
      }
      return 'en';
    }

    function switchLanguage(currentPath, selectedLang) {
      const isDocsPage = /\/docs\//.test(currentPath);
      const docsLangMatch = currentPath.match(/\/docs\/([a-z]{2})\//);
      const currentDocsLang = docsLangMatch ? docsLangMatch[1] : null;

      if (isDocsPage) {
        if (selectedLang === 'en') {
          return currentDocsLang
            ? currentPath.replace(`/docs/${currentDocsLang}/`, '/docs/')
            : currentPath;
        }
        return currentDocsLang
          ? currentPath.replace(`/docs/${currentDocsLang}/`, `/docs/${selectedLang}/`)
          : currentPath.replace('/docs/', `/docs/${selectedLang}/`);
      }

      // Root-level navigation
      const rootLangMatch = currentPath.match(/^(.*?)\/([a-z]{2})\/(?:index\.html)?$/);
      const basePath = rootLangMatch
        ? (rootLangMatch[1] || '')
        : currentPath.replace(/\/(?:index\.html)?$/, '');

      return selectedLang === 'en'
        ? basePath + '/index.html'
        : basePath + `/${selectedLang}/index.html`;
    }

    langSelect.value = detectLang(window.location.pathname);
    langSelect.addEventListener('change', function () {
      window.location.href = switchLanguage(window.location.pathname, this.value);
    });
  }

});
