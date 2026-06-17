// IFP Delivery Workshop — Sidebar Navigation
//
// Single source of truth for the workshop sidebar. The HTML is built
// from SIDEBAR_TRANSLATIONS below and injected at page load. Pages
// should carry only an empty <nav class="sidebar"></nav> placeholder.
//
// Behaviors:
//   - Sections collapse by default; the section containing the active
//     page opens automatically (mirrors the rpm-apps-workshop pattern).
//   - Language switcher detects /docs/ifp/ (English) and /docs/<2-char>/
//     (translated) paths and rewrites accordingly.
//   - When served at /w/<slug>/..., injects the My Progress link and
//     pulls per-page status dots from the workshop backend.

const SIDEBAR_TRANSLATIONS = {
  en: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 Language',
    sign_out: 'Sign out',
    sections: [
      { title: 'Getting Started', links: [
        { href: '01-overview.html', text: 'Workshop Overview' },
        { href: '02-tenant-access.html', text: 'Tenant Access' },
        { href: '03-ifp-overview.html', text: 'IFP Overview' },
        { href: '04-anaplan-way.html', text: 'Anaplan Way for Applications' },
      ]},
      { title: 'Configuration', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: 'Configuration Exercise 1' },
        { href: '06-exercise-2.html', text: 'Configuration Exercise 2' },
        { href: '06-exercise-3.html', text: 'Configuration Exercise 3' },
        { href: '07-generation.html', text: 'Model Generation' },
        { href: '08-post-gen.html', text: 'Post-Generation Steps' },
        { href: '09-error-logs.html', text: 'Error Log Review' },
      ]},
      { title: 'Extensions', links: [
        { href: '10-extensions-overview.html', text: 'Extensions Overview' },
        { href: '11-extension-exercise-1.html', text: 'Exercise 1' },
        { href: '12-extension-exercise-2.html', text: 'Exercise 2' },
      ]},
      { title: 'Reference', links: [
        { href: '13-whats-coming.html', text: "What's Coming" },
        { href: '14-qanda.html', text: 'Q&A from Sessions' },
        { href: '15-workshop-wrap-up.html', text: 'Workshop Wrap-up' },
      ]},
    ],
  },
  de: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 Sprache',
    sign_out: 'Abmelden',
    sections: [
      { title: 'Erste Schritte', links: [
        { href: '01-overview.html', text: 'Workshop-Übersicht' },
        { href: '02-tenant-access.html', text: 'Tenant-Zugang' },
        { href: '03-ifp-overview.html', text: 'IFP-Übersicht' },
        { href: '04-anaplan-way.html', text: 'Anaplan Way für Applikationen' },
      ]},
      { title: 'Konfiguration', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: 'Konfigurationsübung 1' },
        { href: '06-exercise-2.html', text: 'Konfigurationsübung 2' },
        { href: '06-exercise-3.html', text: 'Konfigurationsübung 3' },
        { href: '07-generation.html', text: 'Modellgenerierung' },
        { href: '08-post-gen.html', text: 'Schritte nach der Generierung' },
        { href: '09-error-logs.html', text: 'Error Log Überprüfung' },
      ]},
      { title: 'Erweiterungen', links: [
        { href: '10-extensions-overview.html', text: 'Erweiterungsübersicht' },
        { href: '11-extension-exercise-1.html', text: 'Übung 1' },
        { href: '12-extension-exercise-2.html', text: 'Übung 2' },
      ]},
      { title: 'Referenz', links: [
        { href: '13-whats-coming.html', text: 'Was kommt als Nächstes' },
        { href: '14-qanda.html', text: 'Fragen & Antworten' },
        { href: '15-workshop-wrap-up.html', text: 'Workshop-Abschluss' },
      ]},
    ],
  },
  es: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 Idioma',
    sign_out: 'Cerrar sesión',
    sections: [
      { title: 'Primeros pasos', links: [
        { href: '01-overview.html', text: 'Resumen del taller' },
        { href: '02-tenant-access.html', text: 'Acceso al tenant' },
        { href: '03-ifp-overview.html', text: 'Resumen de IFP' },
        { href: '04-anaplan-way.html', text: 'Anaplan Way for Applications' },
      ]},
      { title: 'Configuración', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: 'Ejercicio de configuración 1' },
        { href: '06-exercise-2.html', text: 'Ejercicio de configuración 2' },
        { href: '06-exercise-3.html', text: 'Ejercicio de configuración 3' },
        { href: '07-generation.html', text: 'Generación de modelo' },
        { href: '08-post-gen.html', text: 'Pasos posteriores a la generación' },
        { href: '09-error-logs.html', text: 'Revisión de registros de errores' },
      ]},
      { title: 'Extensiones', links: [
        { href: '10-extensions-overview.html', text: 'Resumen de extensiones' },
        { href: '11-extension-exercise-1.html', text: 'Ejercicio 1' },
        { href: '12-extension-exercise-2.html', text: 'Ejercicio 2' },
      ]},
      { title: 'Referencia', links: [
        { href: '13-whats-coming.html', text: 'Lo que viene' },
        { href: '14-qanda.html', text: 'Preguntas y respuestas' },
        { href: '15-workshop-wrap-up.html', text: 'Cierre del taller' },
      ]},
    ],
  },
  fr: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 Langue',
    sign_out: 'Déconnexion',
    sections: [
      { title: 'Pour commencer', links: [
        { href: '01-overview.html', text: "Vue d'ensemble de l'atelier" },
        { href: '02-tenant-access.html', text: "Accès au tenant" },
        { href: '03-ifp-overview.html', text: "Vue d'ensemble d'IFP" },
        { href: '04-anaplan-way.html', text: 'Anaplan Way for Applications' },
      ]},
      { title: 'Configuration', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: 'Exercice de configuration 1' },
        { href: '06-exercise-2.html', text: 'Exercice de configuration 2' },
        { href: '06-exercise-3.html', text: 'Exercice de configuration 3' },
        { href: '07-generation.html', text: 'Génération du modèle' },
        { href: '08-post-gen.html', text: 'Étapes post-génération' },
        { href: "09-error-logs.html", text: "Examen des journaux d'erreurs" },
      ]},
      { title: 'Extensions', links: [
        { href: '10-extensions-overview.html', text: "Vue d'ensemble des extensions" },
        { href: '11-extension-exercise-1.html', text: 'Exercice 1' },
        { href: '12-extension-exercise-2.html', text: 'Exercice 2' },
      ]},
      { title: 'Référence', links: [
        { href: '13-whats-coming.html', text: 'À venir' },
        { href: '14-qanda.html', text: 'Questions & réponses' },
        { href: '15-workshop-wrap-up.html', text: 'Clôture de l\'atelier' },
      ]},
    ],
  },
  ja: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 言語',
    sign_out: 'ログアウト',
    sections: [
      { title: 'はじめに', links: [
        { href: '01-overview.html', text: 'ワークショップ概要' },
        { href: '02-tenant-access.html', text: 'テナントアクセス' },
        { href: '03-ifp-overview.html', text: 'IFP 概要' },
        { href: '04-anaplan-way.html', text: 'Anaplan Way for Applications' },
      ]},
      { title: '設定', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: '設定演習 1' },
        { href: '06-exercise-2.html', text: '設定演習 2' },
        { href: '06-exercise-3.html', text: '設定演習 3' },
        { href: '07-generation.html', text: 'モデル生成' },
        { href: '08-post-gen.html', text: '生成後の手順' },
        { href: '09-error-logs.html', text: 'エラーログ確認' },
      ]},
      { title: '拡張', links: [
        { href: '10-extensions-overview.html', text: '拡張概要' },
        { href: '11-extension-exercise-1.html', text: '演習 1' },
        { href: '12-extension-exercise-2.html', text: '演習 2' },
      ]},
      { title: 'リファレンス', links: [
        { href: '13-whats-coming.html', text: '今後の予定' },
        { href: '14-qanda.html', text: 'セッションからの Q&A' },
        { href: '15-workshop-wrap-up.html', text: 'ワークショップ総括' },
      ]},
    ],
  },
  pt: {
    sidebar_title: 'IFP Delivery Partner Workshop',
    lang_label: '🌐 Idioma',
    sign_out: 'Sair',
    sections: [
      { title: 'Primeiros passos', links: [
        { href: '01-overview.html', text: 'Visão geral do workshop' },
        { href: '02-tenant-access.html', text: 'Acesso ao tenant' },
        { href: '03-ifp-overview.html', text: 'Visão geral do IFP' },
        { href: '04-anaplan-way.html', text: 'Anaplan Way for Applications' },
      ]},
      { title: 'Configuração', links: [
        { href: '05-configurator-walkthrough.html', text: 'Application Framework Configurator' },
        { href: '06-exercise-1.html', text: 'Exercício de configuração 1' },
        { href: '06-exercise-2.html', text: 'Exercício de configuração 2' },
        { href: '06-exercise-3.html', text: 'Exercício de configuração 3' },
        { href: '07-generation.html', text: 'Geração do modelo' },
        { href: '08-post-gen.html', text: 'Etapas pós-geração' },
        { href: '09-error-logs.html', text: 'Revisão de logs de erros' },
      ]},
      { title: 'Extensões', links: [
        { href: '10-extensions-overview.html', text: 'Visão geral de extensões' },
        { href: '11-extension-exercise-1.html', text: 'Exercício 1' },
        { href: '12-extension-exercise-2.html', text: 'Exercício 2' },
      ]},
      { title: 'Referência', links: [
        { href: '13-whats-coming.html', text: 'O que vem a seguir' },
        { href: '14-qanda.html', text: 'Perguntas e respostas' },
        { href: '15-workshop-wrap-up.html', text: 'Encerramento do workshop' },
      ]},
    ],
  },
};

// Order of options in the language dropdown.
const LANG_OPTIONS = [
  { value: 'en', label: '🇺🇸 English' },
  { value: 'ja', label: '🇯🇵 日本語' },
  { value: 'es', label: '🇪🇸 Español' },
  { value: 'fr', label: '🇫🇷 Français' },
  { value: 'de', label: '🇩🇪 Deutsch' },
  { value: 'pt', label: '🇧🇷 Português' },
];

document.addEventListener('DOMContentLoaded', function () {

  // ── Language detection ──
  // English IFP content lives under /docs/ifp/ (a 3-letter slug).
  // Translations live under /docs/<2-letter-lang>/.
  function detectLang(path) {
    if (/\/docs\/ifp\//.test(path)) return 'en';
    const m = path.match(/\/docs\/([a-z]{2})\//);
    return (m && SIDEBAR_TRANSLATIONS[m[1]]) ? m[1] : 'en';
  }

  const currentLang = detectLang(window.location.pathname);
  const t = SIDEBAR_TRANSLATIONS[currentLang] || SIDEBAR_TRANSLATIONS.en;

  // ── Build & inject sidebar HTML ──
  function buildSidebarHTML() {
    const sectionsHTML = t.sections.map(section => {
      const linksHTML = section.links.map(link =>
        `<li><a class="nav-link" href="./${link.href}">${link.text}</a></li>`
      ).join('');
      return `<li class="nav-section-title">${section.title}</li>
        <ul class="nav-submenu">${linksHTML}</ul>`;
    }).join('');

    const langOptionsHTML = LANG_OPTIONS.map(opt =>
      `<option value="${opt.value}">${opt.label}</option>`
    ).join('');

    return `
      <div class="sidebar-header">
        <div class="sidebar-title">${t.sidebar_title}</div>
      </div>
      <ul class="nav-list">${sectionsHTML}</ul>
      <div class="lang-switcher">
        <span class="lang-switcher-label">${t.lang_label}</span>
        <select id="lang-select" class="lang-select">${langOptionsHTML}</select>
      </div>
      <div style="padding: 0.75rem 1rem; border-top: 1px solid rgba(255,255,255,0.1); margin-top: auto;">
        <form method="post" action="https://anaplan-workshops.com/logout" style="margin: 0;">
          <button type="submit" style="background: transparent; border: 1px solid rgba(255,255,255,0.2); color: white; padding: 0.5rem 0.75rem; border-radius: 4px; cursor: pointer; font-size: 0.85rem; width: 100%; font-family: inherit;">${t.sign_out}</button>
        </form>
      </div>`;
  }

  const sidebarEl = document.querySelector('nav.sidebar');
  if (sidebarEl && sidebarEl.children.length === 0) {
    sidebarEl.innerHTML = buildSidebarHTML();
  }

  // ── Mark active nav link based on current page filename ──
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href').split('/').pop();
    if (href === currentPage) {
      link.classList.add('active');
    }
  });

  // ── Collapsible nav sections (default closed; auto-open active) ──
  document.querySelectorAll('.nav-section-title').forEach(title => {
    const submenu = title.nextElementSibling;
    if (!submenu || !submenu.classList.contains('nav-submenu')) return;
    const hasActive = submenu.querySelector('.nav-link.active');
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

  // ── Mobile hamburger toggle ──
  const hamburger = document.getElementById('hamburger');
  if (hamburger && sidebarEl) {
    hamburger.addEventListener('click', () => sidebarEl.classList.toggle('open'));
  }

  // ── Language switcher ──
  // Handles /docs/ifp/page.html (English) ↔ /docs/<lang>/page.html.
  const langSelect = document.getElementById('lang-select');
  if (langSelect) {
    langSelect.value = currentLang;
    langSelect.addEventListener('change', function () {
      const selectedLang = this.value;
      const currentPath = window.location.pathname;
      // Normalize: replace whatever /docs/<segment>/ is present with the target.
      const targetSegment = selectedLang === 'en' ? 'ifp' : selectedLang;
      const newPath = currentPath.replace(/\/docs\/[a-z]{2,3}\//, `/docs/${targetSegment}/`);
      window.location.href = newPath;
    });
  }

  // ── My Progress link + sidebar status dots ──
  // Only runs on workshop pages served at /w/<slug>/... — the workshop
  // backend exposes /w/<slug>/progress and /w/<slug>/progress.json. The
  // static GitHub Pages site doesn't, so the fetch fails silently there.
  (function () {
    const wMatch = window.location.pathname.match(/^\/w\/([a-z0-9-]{1,40})\//);
    if (!wMatch) return;
    const workshopSlug = wMatch[1];
    const navList = document.querySelector('.nav-list');
    const firstSubmenu = navList ? navList.querySelector('.nav-submenu') : null;
    if (!firstSubmenu) return;

    const progressLi = document.createElement('li');
    progressLi.className = 'nav-progress-item';
    progressLi.innerHTML = '<a class="nav-link nav-link-progress" href="/w/' + workshopSlug + '/progress">' +
      '<span class="nav-link-progress-icon" aria-hidden="true">📊</span>' +
      '<span>My Progress</span>' +
      '<span class="nav-link-progress-percent" data-progress-percent>—</span>' +
      '</a>';
    firstSubmenu.insertBefore(progressLi, firstSubmenu.firstChild);
    if (window.location.pathname === '/w/' + workshopSlug + '/progress') {
      progressLi.querySelector('a').classList.add('active');
    }

    fetch('/w/' + workshopSlug + '/progress.json', { credentials: 'same-origin' })
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (!data) return;
        if (data.overall && typeof data.overall.percent === 'number') {
          const pctEl = progressLi.querySelector('[data-progress-percent]');
          if (pctEl) pctEl.textContent = data.overall.percent + '%';
        }
        const byPage = data.by_page || {};
        document.querySelectorAll('.nav-list .nav-link').forEach(link => {
          if (link.classList.contains('nav-link-progress')) return;
          const href = link.getAttribute('href') || '';
          const fileName = href.split('/').pop();
          if (!fileName) return;
          const key = '/w/' + workshopSlug + '/' + fileName;
          const status = byPage[key];
          if (!status) return;
          const dot = document.createElement('span');
          dot.className = 'nav-link-status nav-link-status-' + status;
          dot.setAttribute('aria-hidden', 'true');
          dot.title = status === 'done' ? 'Complete' : status === 'partial' ? 'In progress' : status === 'failed' ? 'Needs retry' : 'Not started';
          link.insertBefore(dot, link.firstChild);
        });
      })
      .catch(() => { /* static-site build, no endpoint */ });
  })();

});
