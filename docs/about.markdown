---
layout: default
title: 关于本站
permalink: /about/
---

<style>
.about-section { margin-bottom: 2em; }
.about-section h2 { border-bottom: 1px solid #ddd; padding-bottom: 0.3em; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1em; margin: 1em 0; }
.stat-card { background: #f9f9f7; border: 1px solid #e0e0e0; border-radius: 4px; padding: 1em; text-align: center; }
.stat-card .number { font-size: 1.8em; font-weight: 700; color: #C5A02F; }
.stat-card .label { font-size: 0.9em; color: #666; margin-top: 0.3em; }
.collection-list { list-style: none; padding-left: 0; }
.collection-list li { padding: 0.4em 0; border-bottom: 1px solid #eee; }
.collection-list li:last-child { border-bottom: none; }
</style>

<div class="about-section">

## 简介

本站是关于**廖耀湘将军**（1906–1968）的历史文献数字档案馆，致力于收集、整理和公开与廖耀湘相关的各类文字资料，包括其个人著述、来往电报、战友回忆、报刊报道、战史研究等，为近现代军事史研究提供参考。

廖耀湘（字俊凌），湖南邵阳人，黄埔六期、法国圣西尔军校毕业，历任新编第二十二师师长、新编第六军军长、第九兵团司令官。先后参加昆仑关战役、中国远征军入缅作战、反攻缅北等重要战役，以孟关大捷闻名中外。1948年辽沈战役中兵败被俘，1961年获特赦。

</div>

<div class="about-section">

## 馆藏概况

<div class="stats-grid">
  <div class="stat-card">
    <div class="number">{{ site.liaos_tele.size }}</div>
    <div class="label">来往电报</div>
  </div>
  <div class="stat-card">
    <div class="number">{{ site.newspapers.size }}</div>
    <div class="label">报刊杂志</div>
  </div>
  <div class="stat-card">
    <div class="number">{{ site.ten_year_memorial.size }}</div>
    <div class="label">故人回忆</div>
  </div>
  <div class="stat-card">
    <div class="number">{{ site.battles_history.size }}</div>
    <div class="label">战史资料</div>
  </div>
  <div class="stat-card">
    <div class="number">{{ site.liaos_writings.size }}</div>
    <div class="label">廖耀湘文集</div>
  </div>
  <div class="stat-card">
    <div class="number">{{ site.data.chronology | size }}</div>
    <div class="label">年谱（年）</div>
  </div>
</div>

<ul class="collection-list">
  <li><strong><a href="/categories/liaos_writings/">文集</a></strong> — 廖耀湘个人著述、军事论文、诗作等</li>
  <li><strong><a href="/categories/liaos_tele/">来往电报</a></strong> — 1937–1948年间军事通信档案，来源以国史馆藏档为主</li>
  <li><strong><a href="/categories/newspapers/">报刊杂志</a></strong> — 当时报刊对廖耀湘及新六军的报道</li>
  <li><strong><a href="/categories/ten_year_memorial/">故人回忆</a></strong> — 战友、部属、亲属的回忆文章</li>
  <li><strong><a href="/categories/battles_history/">战史</a></strong> — 昆仑关、远征军入缅、反攻缅北、辽沈战役等战史资料</li>
  <li><strong><a href="/categories/n6a_memorial/">新六军纪念</a></strong> / <strong><a href="/categories/n22d_memorial/">新二十二师纪念</a></strong> — 部队纪念文集</li>
  <li><strong><a href="/chronology.html">年谱</a></strong> — 廖耀湘生平大事年表（1906–1968），附来源考证</li>
</ul>

</div>

<div class="about-section">

## 资料来源

本站资料主要来源：

- **国史馆**（台北）档案：蒋中正总统文物、军事档案等
- **《廖耀湘将军逝世十周年纪念集》**：战友亲属回忆录合集
- **《新邵文史》第10辑、第20辑**：地方文史资料中的廖耀湘专辑
- **《新编第二十二师出关周年纪念特刊》**
- **《新六军成立三周年纪念册》**
- **各类报刊**：《中央日报》《大公报》《申报》《立报》等
- **战史资料**：《中国远征军》、辽沈战役相关回忆录等
- **个人档案与回忆录**：杜聿明、郑洞国、蒋经国、徐永昌等人相关记述

</div>

<div class="about-section">

## 联系方式

- 邮箱：[{{ site.email }}](mailto:{{ site.email }})
- GitHub：[{{ site.github_username }}](https://github.com/{{ site.github_username }})

如有资料提供、勘误指正或合作意向，欢迎来信。

</div>
