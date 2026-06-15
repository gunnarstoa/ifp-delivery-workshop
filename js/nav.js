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

  // ── My Progress link + sidebar status dots ────────────────────────────────
  // Only runs on workshop pages served at /w/<slug>/<page>.html — the Flask
  // backend exposes /w/<slug>/progress (page) and /w/<slug>/progress.json (data).
  // The static GitHub Pages docs site doesn't serve those endpoints, so the
  // injection is a no-op there (the fetch fails silently, the link is hidden).
  (function () {
    var wMatch = window.location.pathname.match(/^\/w\/([a-z0-9-]{1,40})\//);
    if (!wMatch) return;
    var workshopSlug = wMatch[1];
    var navList = document.querySelector('.nav-list');
    var firstSubmenu = navList ? navList.querySelector('.nav-submenu') : null;
    if (!firstSubmenu) return;

    // Inject "My Progress" as the first item in the first nav section
    var progressLi = document.createElement('li');
    progressLi.className = 'nav-progress-item';
    progressLi.innerHTML = '<a class="nav-link nav-link-progress" href="/w/' + workshopSlug + '/progress">' +
      '<span class="nav-link-progress-icon" aria-hidden="true">📊</span>' +
      '<span>My Progress</span>' +
      '<span class="nav-link-progress-percent" data-progress-percent>—</span>' +
      '</a>';
    firstSubmenu.insertBefore(progressLi, firstSubmenu.firstChild);
    // Mark active when we're on the progress page itself
    if (window.location.pathname === '/w/' + workshopSlug + '/progress') {
      progressLi.querySelector('a').classList.add('active');
    }

    // Fetch the per-page status map and paint dots beside each nav-link
    fetch('/w/' + workshopSlug + '/progress.json', { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data) return;
        if (data.overall && typeof data.overall.percent === 'number') {
          var pctEl = progressLi.querySelector('[data-progress-percent]');
          if (pctEl) pctEl.textContent = data.overall.percent + '%';
        }
        var byPage = data.by_page || {};
        document.querySelectorAll('.nav-list .nav-link').forEach(function (link) {
          if (link.classList.contains('nav-link-progress')) return;
          var href = link.getAttribute('href') || '';
          // Resolve relative href ("./05-…html") to absolute /w/<slug>/<file>
          var fileName = href.split('/').pop();
          if (!fileName) return;
          var key = '/w/' + workshopSlug + '/' + fileName;
          var status = byPage[key];
          if (!status) return;
          var dot = document.createElement('span');
          dot.className = 'nav-link-status nav-link-status-' + status;
          dot.setAttribute('aria-hidden', 'true');
          dot.title = status === 'done' ? 'Complete' : status === 'partial' ? 'In progress' : status === 'failed' ? 'Needs retry' : 'Not started';
          link.insertBefore(dot, link.firstChild);
        });
      })
      .catch(function () { /* silent — static-site build won't have this endpoint */ });
  })();

});
