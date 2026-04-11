---
layout: default
title: 廖耀湘 · Q&A 访谈
permalink: /qa.html
sitemap: false
description: "与廖耀湘相关人士的 Q&A 访谈合集"
---

<style>
  /* ============================================================
     Q&A Editorial Magazine — WSJ / NY Post / Medium inspired
     ============================================================ */

  html { scroll-behavior: smooth; }

  /* --- Reading progress bar --- */
  .qa-progress {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: transparent;
    z-index: 200;
    pointer-events: none;
  }
  .qa-progress-bar {
    height: 100%;
    width: 0%;
    background: var(--color-accent-gold);
    transition: width 0.1s linear;
  }

  /* --- Overall layout: sidebar + article --- */
  .qa-layout {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem 4rem;
    display: grid;
    grid-template-columns: 220px minmax(0, 1fr);
    column-gap: 3.5rem;
  }

  /* --- Sticky sidebar TOC --- */
  .qa-sidebar {
    position: sticky;
    top: 2rem;
    align-self: start;
    max-height: calc(100vh - 3rem);
    overflow-y: auto;
    padding-right: 0.25rem;
    scrollbar-width: thin;
  }
  .qa-sidebar::-webkit-scrollbar { width: 4px; }
  .qa-sidebar::-webkit-scrollbar-thumb { background: var(--color-border-light); }

  .qa-sidebar-label {
    font-family: var(--font-sans);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--color-charcoal);
    border-bottom: 2px solid var(--color-charcoal);
    padding: 0 0 0.8rem;
    margin: 0 0 1.1rem;
  }

  .qa-toc-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .qa-toc-item {
    border-left: 2px solid transparent;
    padding: 0.55rem 0 0.55rem 0.85rem;
    margin-left: -0.85rem;
    transition: border-color 0.2s ease;
  }

  .qa-toc-item.active {
    border-left-color: var(--color-accent-gold);
  }

  .qa-toc-item a {
    display: block;
    font-family: var(--font-serif);
    font-size: 0.82rem;
    line-height: 1.5;
    color: var(--color-gray-600);
    border: none;
  }

  .qa-toc-item.active a {
    color: var(--color-charcoal);
  }

  .qa-toc-item a:hover {
    color: var(--color-accent-gold);
  }

  .qa-toc-num {
    display: block;
    font-family: var(--font-sans);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: var(--color-accent-red);
    margin-bottom: 0.15rem;
  }

  /* --- Main article column --- */
  .qa-main {
    max-width: 720px;
    min-width: 0;
  }

  /* --- Masthead (editorial hero) --- */
  .qa-masthead {
    border-top: 6px double var(--color-charcoal);
    border-bottom: 6px double var(--color-charcoal);
    padding: 3.25rem 0 2.75rem;
    margin-bottom: 4rem;
    text-align: center;
  }

  .qa-kicker {
    display: inline-block;
    font-family: var(--font-sans);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: var(--color-accent-red);
    padding: 0.45rem 1.05rem 0.4rem;
    border: 1px solid var(--color-accent-red);
    margin-bottom: 1.75rem;
  }

  .qa-headline {
    font-family: var(--font-serif);
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1.15;
    color: var(--color-charcoal);
    margin: 0 0 1.15rem;
    letter-spacing: -0.005em;
  }

  .qa-deck {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.12rem;
    line-height: 1.6;
    color: var(--color-charcoal-light);
    max-width: 560px;
    margin: 0 auto 2rem;
    font-weight: 400;
  }

  .qa-stats {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.2rem;
    font-family: var(--font-sans);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-gray-500);
  }

  .qa-stats::before,
  .qa-stats::after {
    content: "";
    flex: 0 0 50px;
    height: 1px;
    background: var(--color-charcoal);
  }

  .qa-stats-sep {
    color: var(--color-accent-gold);
    font-weight: 400;
  }

  /* --- Chapter (one question) --- */
  .qa-chapter {
    margin-bottom: 5rem;
    scroll-margin-top: 1.5rem;
  }

  .qa-chapter-head {
    display: grid;
    grid-template-columns: 88px minmax(0, 1fr);
    gap: 1.75rem;
    align-items: start;
    padding-bottom: 1.75rem;
    margin-bottom: 2.75rem;
    border-bottom: 1px solid var(--color-charcoal);
  }

  .qa-chapter-num {
    font-family: var(--font-serif);
    font-size: 4.8rem;
    font-weight: 700;
    font-style: italic;
    line-height: 0.85;
    color: var(--color-accent-gold);
    letter-spacing: -0.02em;
  }

  .qa-chapter-body { padding-top: 0.4rem; }

  .qa-chapter-label {
    font-family: var(--font-sans);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--color-gray-500);
    margin: 0 0 0.75rem;
  }

  .qa-chapter-label span {
    color: var(--color-accent-red);
  }

  .qa-chapter-question {
    font-family: var(--font-serif);
    font-size: 1.68rem;
    font-weight: 700;
    line-height: 1.38;
    color: var(--color-charcoal);
    margin: 0;
    letter-spacing: -0.005em;
  }

  /* --- Answer list --- */
  .qa-answers {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .qa-answer {
    margin: 0 0 2.5rem;
    padding-bottom: 2.5rem;
    border-bottom: 1px solid var(--color-border-light);
  }

  .qa-answer:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  /* Byline: small rule + label + italic respondent name */
  .qa-byline {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .qa-byline-rule {
    flex: 0 0 42px;
    height: 1px;
    background: var(--color-accent-gold);
  }

  .qa-byline-label {
    font-family: var(--font-sans);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-gray-500);
  }

  .qa-byline-name {
    font-family: var(--font-serif);
    font-size: 1.05rem;
    font-weight: 700;
    font-style: italic;
    color: var(--color-charcoal);
    letter-spacing: 0.01em;
  }

  .qa-answer-text {
    font-family: var(--font-serif);
    font-size: 1.08rem;
    line-height: 1.95;
    color: var(--color-charcoal-light);
    white-space: pre-wrap;
    margin: 0;
  }

  .qa-answer-empty {
    font-style: italic;
    color: var(--color-gray-400);
  }

  /* --- Figures / images --- */
  .qa-figure {
    margin: 1.75rem 0 0.25rem;
  }

  .qa-figure img {
    display: block;
    width: 100%;
    border: 1px solid var(--color-border-light);
    background: #fff;
  }

  .qa-figure figcaption {
    font-family: var(--font-sans);
    font-size: 0.72rem;
    color: var(--color-gray-500);
    margin-top: 0.65rem;
    font-style: italic;
    text-align: center;
  }

  .qa-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 0.5rem;
    margin: 1.5rem 0 0.25rem;
  }

  .qa-gallery img {
    display: block;
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border: 1px solid var(--color-border-light);
    background: #fff;
    cursor: zoom-in;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .qa-gallery img:hover {
    transform: scale(1.015);
    border-color: var(--color-accent-gold);
  }

  /* --- Chapter footer: nav --- */
  .qa-chapter-footer {
    margin-top: 2.75rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--color-border-light);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }

  .qa-chapter-footer a {
    font-family: var(--font-sans);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-gray-500);
    border: none;
  }

  .qa-chapter-footer a:hover { color: var(--color-accent-gold); }

  .qa-next-q { text-align: right; max-width: 60%; }

  .qa-next-q-preview {
    display: block;
    margin-top: 0.4rem;
    font-family: var(--font-serif);
    font-size: 0.92rem;
    font-style: italic;
    font-weight: 400;
    line-height: 1.45;
    color: var(--color-charcoal);
    text-transform: none;
    letter-spacing: 0;
  }

  /* --- Mobile --- */
  @media (max-width: 960px) {
    .qa-layout {
      grid-template-columns: minmax(0, 1fr);
      column-gap: 0;
      padding: 0 1.1rem 3rem;
    }
    .qa-sidebar {
      position: sticky;
      top: 0;
      max-height: none;
      overflow: visible;
      background: var(--color-paper);
      margin: 0 -1.1rem 2rem;
      padding: 0.6rem 1.1rem 0.55rem;
      border-bottom: 1px solid var(--color-border-light);
      z-index: 50;
    }
    .qa-sidebar-label { display: none; }
    .qa-toc-list {
      display: flex;
      gap: 0.4rem;
      overflow-x: auto;
      scrollbar-width: none;
      padding: 0.25rem 0;
    }
    .qa-toc-list::-webkit-scrollbar { display: none; }
    .qa-toc-item {
      flex-shrink: 0;
      border: 1px solid var(--color-border-light);
      border-left-width: 1px;
      padding: 0.4rem 0.75rem;
      margin: 0;
      background: #fff;
      white-space: nowrap;
    }
    .qa-toc-item.active {
      border-color: var(--color-accent-gold);
      border-left-width: 1px;
      background: var(--color-paper);
    }
    .qa-toc-item a {
      font-size: 0.72rem;
      display: flex;
      align-items: baseline;
      gap: 0.4rem;
    }
    .qa-toc-num {
      display: inline;
      font-size: 0.56rem;
      margin: 0;
    }
    .qa-toc-text {
      display: inline;
      max-width: 10em;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .qa-main { max-width: none; }
    .qa-masthead { padding: 2.25rem 0 1.85rem; margin-bottom: 2.5rem; }
    .qa-headline { font-size: 2.1rem; }
    .qa-deck { font-size: 1rem; }
    .qa-stats { font-size: 0.6rem; letter-spacing: 0.18em; gap: 0.75rem; }
    .qa-stats::before, .qa-stats::after { flex-basis: 28px; }
    .qa-chapter { margin-bottom: 3.5rem; }
    .qa-chapter-head {
      grid-template-columns: 60px minmax(0, 1fr);
      gap: 1rem;
      padding-bottom: 1.25rem;
      margin-bottom: 2rem;
    }
    .qa-chapter-num { font-size: 3.2rem; }
    .qa-chapter-question { font-size: 1.28rem; }
    .qa-answer-text { font-size: 1rem; line-height: 1.85; }
  }

  @media (max-width: 600px) {
    .qa-headline { font-size: 1.75rem; }
    .qa-chapter-head { grid-template-columns: 46px minmax(0, 1fr); gap: 0.85rem; }
    .qa-chapter-num { font-size: 2.5rem; }
    .qa-chapter-question { font-size: 1.15rem; }
    .qa-gallery { grid-template-columns: repeat(auto-fill, minmax(105px, 1fr)); }
    .qa-chapter-footer { flex-direction: column; align-items: stretch; }
    .qa-next-q { max-width: none; text-align: left; }
  }
</style>

{% assign total_answers = 0 %}
{% for q in site.data.qa %}
  {% assign _n = q.answers | size %}
  {% assign total_answers = total_answers | plus: _n %}
{% endfor %}
{% assign total_questions = site.data.qa | size %}

<div class="qa-progress" aria-hidden="true">
  <div class="qa-progress-bar" id="qa-progress-bar"></div>
</div>

<div class="qa-layout" id="top">
  <aside class="qa-sidebar" aria-label="问题目录">
    <p class="qa-sidebar-label">题目 / Contents</p>
    <ul class="qa-toc-list" id="qa-toc-list">
      {% for item in site.data.qa %}
      <li class="qa-toc-item{% if forloop.first %} active{% endif %}" data-index="{{ forloop.index }}">
        <a href="#q{{ forloop.index }}">
          <span class="qa-toc-num">{{ forloop.index | prepend: '00' | slice: -2, 2 }} &middot; {{ total_questions | prepend: '00' | slice: -2, 2 }}</span>
          <span class="qa-toc-text">{% if item.question and item.question != "" %}{{ item.question | truncate: 28 }}{% else %}待录入{% endif %}</span>
        </a>
      </li>
      {% endfor %}
    </ul>
  </aside>

  <article class="qa-main">
    <header class="qa-masthead">
      <span class="qa-kicker">Special Interview &middot; 访谈特辑</span>
      <h1 class="qa-headline">{{ page.title }}</h1>
      <p class="qa-deck">九个提问，百家之声——来自天南海北的回答，写给一位久远的将军。A chorus of voices remembering the General: nine questions, answered in many hands.</p>
      <div class="qa-stats">
        <span>{{ total_questions }} Questions</span>
        <span class="qa-stats-sep">&#9672;</span>
        <span>{{ total_answers }} Responses</span>
        <span class="qa-stats-sep">&#9672;</span>
        <span>2026 Issue</span>
      </div>
    </header>

    {% for item in site.data.qa %}
    {% assign chapter_index = forloop.index %}
    {% assign is_last = forloop.last %}
    <section class="qa-chapter" id="q{{ chapter_index }}">
      <header class="qa-chapter-head">
        <div class="qa-chapter-num" aria-hidden="true">{{ chapter_index | prepend: '00' | slice: -2, 2 }}</div>
        <div class="qa-chapter-body">
          <p class="qa-chapter-label">Chapter <span>{{ chapter_index }}</span> of {{ total_questions }} &middot; 第 {{ chapter_index }} 问</p>
          <h2 class="qa-chapter-question">
            {% if item.question and item.question != "" %}
              {{ item.question }}
            {% else %}
              <em class="qa-answer-empty">[问题 {{ chapter_index }} · 待录入]</em>
            {% endif %}
          </h2>
        </div>
      </header>

      <ol class="qa-answers">
        {% for ans in item.answers %}
        <li class="qa-answer">
          <div class="qa-byline">
            <span class="qa-byline-rule" aria-hidden="true"></span>
            <span class="qa-byline-label">By</span>
            <span class="qa-byline-name">{{ ans.respondent }}</span>
          </div>
          {% if ans.text and ans.text != "" %}
            <p class="qa-answer-text">{{ ans.text }}</p>
          {% else %}
            <p class="qa-answer-text qa-answer-empty">[待录入 · Pending]</p>
          {% endif %}
          {% if ans.image %}
          <figure class="qa-figure">
            <img src="{{ ans.image }}" alt="{{ ans.respondent }} 附图" loading="lazy">
            <figcaption>{{ ans.respondent }} &middot; 附图</figcaption>
          </figure>
          {% endif %}
          {% if ans.images %}
          <div class="qa-gallery">
            {% for img in ans.images %}
              <img src="{{ img }}" alt="{{ ans.respondent }} 附图" loading="lazy">
            {% endfor %}
          </div>
          {% endif %}
        </li>
        {% endfor %}
      </ol>

      <footer class="qa-chapter-footer">
        <a href="#top">↑ 返回顶部 / Top</a>
        {% unless is_last %}
        <a href="#q{{ chapter_index | plus: 1 }}" class="qa-next-q">
          下一问 / Next →
          {% for next_item in site.data.qa offset: chapter_index limit: 1 %}
            {% if next_item.question and next_item.question != "" %}
              <span class="qa-next-q-preview">{{ next_item.question | truncate: 42 }}</span>
            {% endif %}
          {% endfor %}
        </a>
        {% endunless %}
      </footer>
    </section>
    {% endfor %}
  </article>
</div>

<script>
(function() {
  const progressBar = document.getElementById('qa-progress-bar');
  const article = document.querySelector('.qa-main');
  const chapters = document.querySelectorAll('.qa-chapter');
  const tocItems = document.querySelectorAll('.qa-toc-item');
  const sidebar = document.querySelector('.qa-sidebar');

  function updateProgress() {
    if (!article || !progressBar) return;
    const rect = article.getBoundingClientRect();
    const viewport = window.innerHeight;
    const scrolled = Math.max(0, -rect.top);
    const total = Math.max(1, rect.height - viewport);
    const pct = Math.min(100, Math.max(0, (scrolled / total) * 100));
    progressBar.style.width = pct + '%';
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const idx = entry.target.id.replace('q', '');
          tocItems.forEach(item => {
            const isActive = item.dataset.index === idx;
            item.classList.toggle('active', isActive);
            if (isActive && window.innerWidth <= 960) {
              item.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
          });
        }
      });
    }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });
    chapters.forEach(c => observer.observe(c));
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();
})();
</script>
