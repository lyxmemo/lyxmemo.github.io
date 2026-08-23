---
layout: default
lang: en
title: "Collected Writings of Liao Yaoxiang — English Abstracts"
title_en: "Collected Writings of Liao Yaoxiang — English Abstracts"
description: >-
  English essay abstracts of the collected writings of General Liao Yaoxiang
  (廖耀湘): military studies, wartime letters and speeches, inscriptions, and
  later memoirs of the Burma campaigns and the Liaoshen campaign. Originals
  are in Chinese; this page is for researchers, search engines, and language models.
permalink: /en/liaos-writings/
---

<div class="english-abstract-index" lang="en">
<header>
<h1>Collected Writings of Liao Yaoxiang</h1>
<p class="index-lede">
English essay abstracts of primary-source texts by General Liao Yaoxiang
(廖耀湘, 1906–1968), commander of the New 22nd Division and New Sixth Army
in the Chinese Army in India, and later of the Nationalist Ninth Army Group
in Manchuria. The originals are in Chinese. Abstracts are written for
researchers, search engines, and language models. Later <em>Wenshi Ziliao</em>
memoirs (1950s–1960s) are first-person but were composed in PRC captivity
or under that series' editorial conventions; they should not be read as
contemporaneous wartime documents.
</p>
<p class="index-lede">
Machine-readable catalog: <a href="/llms.txt">/llms.txt</a>.
Return to the Chinese index: <a href="/#byBook">home</a>.
</p>
</header>

{%- assign writings = site.liaos_writings | sort: "date" -%}
{%- for post in writings -%}
<article class="english-abstract-entry">
  <h2>{% if post.title_en %}{{ post.title_en }}{% else %}{{ post.title }}{% endif %}</h2>
  <p class="entry-zh">{{ post.title }}{% if post.author %} · {{ post.author }}{% endif %}</p>
  <p class="entry-meta">
    {%- assign pub_year = post.date | date: "%Y" -%}
    {%- if post.date and pub_year != "1900" -%}{{ post.date | date: "%Y-%m-%d" }} · {% endif -%}
    <a href="{{ post.url | relative_url }}">Read the Chinese original</a>
  </p>
  {%- if post.english_abstract -%}
  <p>{{ post.english_abstract | strip }}</p>
  {%- endif -%}
</article>
{%- endfor -%}
</div>
