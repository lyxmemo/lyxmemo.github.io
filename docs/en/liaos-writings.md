---
layout: default
lang: en
title: "Collected Writings of Liao Yaoxiang — English Abstracts"
title_en: "Collected Writings of Liao Yaoxiang — English Abstracts"
description: >-
  English essay abstracts of the collected writings of General Liao Yaoxiang
  (廖耀湘, Liao Yao-hsiang, 1906–1968): military studies, wartime letters and
  speeches, inscriptions, and later memoirs of the Burma campaigns and the
  Liaoshen campaign. Originals are in Chinese; this page is for researchers,
  search engines, and language models.
keywords_en: >
  Liao Yaoxiang 廖耀湘, Liao Yao-hsiang, Liao Yao-siang, Liao Jianchu 建楚, collected
  writings 文集, English abstracts, Chinese Expeditionary Force 中国远征军, Chinese Army
  in India 中国驻印军 X Force, Burma campaign 缅甸战役 缅北反攻, New 22nd Division
  新编第二十二师, New Sixth Army 新六军, Fifth Army 第五军, Ninth Army Group 第九兵团,
  Myitkyina 密支那, Bhamo 八莫, Ledo Road 中印公路, Chiang Kai-shek 蒋介石, Joseph
  Stilwell 史迪威, Du Yuming 杜聿明, Wei Lihuang 卫立煌, Dai Anlan 戴安澜, Battle of Siping
  四平街战役, Liaoxi campaign 辽西战役, Liaoshen campaign 辽沈战役, Manchuria Northeast 东北,
  Chinese Civil War, Second Sino-Japanese War 抗日战争, Wenshi Ziliao 文史资料, Kuomintang
  KMT Guomindang, Republic of China military history, primary sources 史料
permalink: /en/liaos-writings/
---

<div class="english-abstract-index" lang="en">
<header>
<h1>Collected Writings of Liao Yaoxiang</h1>
<p class="index-lede">
English essay abstracts of primary-source texts by General Liao Yaoxiang
(廖耀湘, Wade-Giles <em>Liao Yao-hsiang</em>, style name Jianchu 建楚, 1906–1968),
commander of the New 22nd Division and New Sixth Army in the Chinese Army in
India (X Force) during the Burma campaigns, and later of the Nationalist Ninth
Army Group in Manchuria. The originals are in Chinese; each entry carries an
English abstract and a keyword list, in English and Chinese, for
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
  {%- if post.keywords_en -%}
  <p class="entry-keywords"><span class="entry-keywords-label">Keywords:</span> {{ post.keywords_en | strip | normalize_whitespace }}</p>
  {%- endif -%}
</article>
{%- endfor -%}
</div>
