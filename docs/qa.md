---
layout: default
title: 廖耀湘 · Q&A 访谈
permalink: /qa.html
sitemap: false
description: "与廖耀湘相关人士的 Q&A 访谈合集"
---

<style>
  .qa-article {
    max-width: 760px;
    margin: 0 auto;
  }

  .qa-header {
    text-align: center;
    padding-bottom: 1.25rem;
    border-bottom: 3px solid var(--color-charcoal);
    margin-bottom: 2.5rem;
  }

  .qa-header .qa-eyebrow {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    color: var(--color-accent-red);
    margin: 0 0 0.6rem;
  }

  .qa-title {
    font-family: var(--font-serif);
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.35;
    color: var(--color-charcoal);
    margin: 0 0 0.6rem;
  }

  .qa-subtitle {
    font-size: 0.85rem;
    color: var(--color-gray-500);
    margin: 0;
    font-style: italic;
  }

  .qa-toc {
    background: #fff;
    border: 1px solid var(--color-border-light);
    padding: 1.25rem 1.5rem;
    margin-bottom: 2.5rem;
  }

  .qa-toc-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--color-gray-500);
    margin: 0 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--color-border-light);
  }

  .qa-toc ol {
    margin: 0;
    padding-left: 1.4rem;
    font-family: var(--font-serif);
    font-size: 0.95rem;
    line-height: 1.9;
  }

  .qa-toc ol li::marker {
    color: var(--color-accent-gold);
    font-weight: 700;
  }

  .qa-toc a {
    color: var(--color-charcoal);
    border-bottom: 1px dashed transparent;
  }

  .qa-toc a:hover {
    color: var(--color-accent-gold);
    border-bottom-color: var(--color-accent-gold);
  }

  .qa-block {
    margin-bottom: 3.5rem;
    scroll-margin-top: 1.5rem;
  }

  .qa-block + .qa-block {
    border-top: 1px solid var(--color-border-light);
    padding-top: 2.5rem;
  }

  .qa-question {
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    margin-bottom: 1.75rem;
  }

  .qa-q-marker {
    flex-shrink: 0;
    font-family: var(--font-serif);
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.2;
    color: var(--color-accent-red);
    width: 1.8rem;
  }

  .qa-q-text {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.55;
    color: var(--color-charcoal);
    margin: 0;
  }

  .qa-q-placeholder {
    color: var(--color-gray-400);
    font-weight: 400;
    font-style: italic;
  }

  .qa-answers {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .qa-answer {
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    padding: 0.9rem 0;
    border-bottom: 1px dotted var(--color-border-light);
  }

  .qa-answer:last-child {
    border-bottom: none;
  }

  .qa-a-marker {
    flex-shrink: 0;
    font-family: var(--font-serif);
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.7;
    color: var(--color-accent-gold);
    width: 1.8rem;
  }

  .qa-a-body {
    flex: 1;
    font-family: var(--font-serif);
    font-size: 1rem;
    line-height: 1.95;
    color: var(--color-charcoal-light);
  }

  .qa-respondent {
    display: inline-block;
    font-weight: 700;
    color: var(--color-charcoal);
    margin-right: 0.5rem;
  }

  .qa-respondent::after {
    content: "：";
    color: var(--color-gray-500);
    font-weight: 400;
  }

  .qa-a-text {
    white-space: pre-wrap;
  }

  .qa-photo {
    display: block;
    max-width: 100%;
    margin: 1rem 0 0.5rem;
    border: 1px solid var(--color-border-light);
    border-radius: 4px;
  }

  .qa-empty {
    color: var(--color-gray-400);
    font-style: italic;
  }

  .qa-back-top {
    display: block;
    text-align: center;
    margin: 1rem 0 0;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-gray-500);
  }

  .qa-back-top:hover {
    color: var(--color-accent-gold);
  }

  @media (max-width: 600px) {
    .qa-title { font-size: 1.6rem; }
    .qa-q-text { font-size: 1.1rem; }
    .qa-q-marker { font-size: 1.4rem; width: 1.5rem; }
    .qa-a-marker { width: 1.5rem; }
  }
</style>

<article class="qa-article" id="top">
  <header class="qa-header">
    <p class="qa-eyebrow">Interview · 访谈</p>
    <h1 class="qa-title">{{ page.title }}</h1>
    <p class="qa-subtitle">共 {{ site.data.qa | size }} 个问题</p>
  </header>

  <nav class="qa-toc" aria-label="目录">
    <p class="qa-toc-title">目录 / Contents</p>
    <ol>
      {% for item in site.data.qa %}
      <li>
        <a href="#q{{ forloop.index }}">
          {% if item.question and item.question != "" %}{{ item.question }}{% else %}问题 {{ forloop.index }}（待录入）{% endif %}
        </a>
      </li>
      {% endfor %}
    </ol>
  </nav>

  {% for item in site.data.qa %}
  <section class="qa-block" id="q{{ forloop.index }}">
    <div class="qa-question">
      <span class="qa-q-marker" aria-hidden="true">Q{{ forloop.index }}</span>
      <h2 class="qa-q-text">
        {% if item.question and item.question != "" %}
          {{ item.question }}
        {% else %}
          <span class="qa-q-placeholder">[问题 {{ forloop.index }} · 待录入]</span>
        {% endif %}
      </h2>
    </div>

    <ol class="qa-answers">
      {% for ans in item.answers %}
      <li class="qa-answer">
        <span class="qa-a-marker" aria-hidden="true">A{{ forloop.index }}</span>
        <div class="qa-a-body">
          {% if ans.respondent and ans.respondent != "" %}
            <span class="qa-respondent">{{ ans.respondent }}</span>
          {% endif %}
          {% if ans.text and ans.text != "" %}
            <span class="qa-a-text">{{ ans.text }}</span>
          {% else %}
            <span class="qa-empty">[待录入]</span>
          {% endif %}
          {% if ans.image %}
            <img class="qa-photo" src="{{ ans.image }}" alt="{{ ans.respondent }} 附图" loading="lazy">
          {% endif %}
          {% if ans.images %}
            {% for img in ans.images %}
              <img class="qa-photo" src="{{ img }}" alt="{{ ans.respondent }} 附图" loading="lazy">
            {% endfor %}
          {% endif %}
        </div>
      </li>
      {% endfor %}
    </ol>

    <a href="#top" class="qa-back-top">↑ 返回目录 / Back to top</a>
  </section>
  {% endfor %}
</article>
