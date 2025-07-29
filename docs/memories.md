---
layout: default
title: 分类
---

<style>
/* === Tab 样式 (背景填充) === */
.tab {
  overflow: hidden;
  border-bottom: 1px solid #ddd;
}
.tab button {
  background-color: transparent;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: background-color 0.3s;
  font-size: 17px;
}
.tab button:hover:not(.active) {
  background-color: #f1f1f1;
}
.tab button.active {
  background-color: #e9e9e9;
  font-weight: bold;
}

/* === 内容区域通用样式 === */
.tabcontent { display: none; padding: 0px 0; animation: fadeEffect 0.5s; }
@keyframes fadeEffect { from {opacity: 0;} to {opacity: 1;} }

/* === 可折叠列表样式 === */
.collapsible-book {
  border-bottom: 1px solid #e0e0e0;
}
.collapsible-book:first-of-type {
  border-top: 1px solid #e0e0e0;
}
summary {
  font-size: 1.2em;
  font-weight: 600;
  padding: 5px 0px;
  cursor: pointer;
  list-style: none;
  outline: none;
  margin-bottom:0!important;
  transition: background-color 0.2s;
  color: #504949ff;
}
summary:hover {
  background-color: #f7f7f7;
}
summary::-webkit-details-marker {
  display: none;
}
summary::before {
  content: '+';
  font-family: monospace;
  font-weight: bold;
  font-size: 1.2em;
  margin-right: 12px;
  color: #888;
  display: inline-block;
  width: 20px;
  text-align: center;
}
details[open] > summary::before {
  content: '−';
}
.collapsible-book ul {
  list-style-type: none;
  padding: 10px 0 15px 42px;
  margin: 0;
}
.collapsible-book li {
  padding: 6px 0;
  border: none;
}

/* === 时间线视图的样式 (保持不变) === */
.timeline-list { list-style-type: none; padding-left: 0; }
.timeline-list li, .timeline-list-no-date li {
  display: flex;
  align-items: baseline;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}
.timeline-date { font-family: monospace; color: #777; margin-right: 15px; flex-shrink: 0; }
.unknown-date-header { margin-top: 40px; padding-top: 20px; border-top: 2px solid #ccc; font-size: 1.1em; color: #555; }
</style>

{%- comment -%}
  ===============================================================
  全新数据收集逻辑：
  1. 遍历所有相关集合。
  2. 如果文章的 category 是 'Liao's Tele'，则归入“电报”。
  3. 否则，归入“故人回忆”。
  ===============================================================
{%- endcomment -%}
{%- assign memorial_posts_raw = "" | split: "" -%}
{%- assign telegrams_raw = "" | split: "" -%}
{%- assign collections_to_search = "liaos_writings,ten_year_memorial,n6a_memorial,n22d_memorial,battles_history,liaos_tele" | split: "," -%}

{%- for collection_name in collections_to_search -%}
  {%- for post in site[collection_name] -%}
    {%- if post.category == "Liao's Tele" -%}
      {%- assign telegrams_raw = telegrams_raw | push: post -%}
    {%- else -%}
      {%- assign memorial_posts_raw = memorial_posts_raw | push: post -%}
    {%- endif -%}
  {%- endfor -%}
{%- endfor -%}


<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'byBook')" id="defaultOpen">按书籍出处排列</button>
  <button class="tablinks" onclick="openTab(event, 'byTime')">按时间线排列</button>
  <button class="tablinks" onclick="openTab(event, 'telegrams')">电报</button>
</div>

<div id="byBook" class="tabcontent">
  {%- if memorial_posts_raw and memorial_posts_raw.size > 0 -%}
    {%- assign posts_by_book = memorial_posts_raw | group_by: "category" -%}
    {%- for book in posts_by_book -%}
      <details class="collapsible-book">
        <summary>《{{ book.name }}》</summary>
        <ul>
          {%- assign items_sorted_by_title = book.items | sort: 'title' -%}
          {%- for post in items_sorted_by_title -%}
            <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a>{%- if post.author -%}（{{ post.author }}）{%- endif -%}</li>
          {%- endfor -%}
        </ul>
      </details>
    {%- endfor -%}
  {%- else -%}
    <p>未能生成列表。</p>
  {%- endif -%}
</div>

<div id="byTime" class="tabcontent">
  {%- if memorial_posts_raw and memorial_posts_raw.size > 0 -%}
    {%- assign dated_posts = "" | split: "" -%}
    {%- assign undated_posts = "" | split: "" -%}
    {%- for post in memorial_posts_raw -%}
      {%- assign formatted_date = post.date | date: "%Y-%m-%d" -%}
      {%- if formatted_date == "1900-01-01" or post.date == nil -%}
        {%- assign undated_posts = undated_posts | push: post -%}
      {%- else -%}
        {%- assign dated_posts = dated_posts | push: post -%}
      {%- endif -%}
    {%- endfor -%}
    {%- if dated_posts.size > 0 -%}
      {%- assign posts_by_year = dated_posts | group_by_exp: "post", "post.date | date: '%Y'" | sort: "name" | reverse -%}
      {%- for year_group in posts_by_year -%}
        <details class="collapsible-book" {% if forloop.first %}open{% endif %}>
          <summary>{{ year_group.name }} 年</summary>
          <ul class="timeline-list-no-date">
            {%- assign posts_in_year = year_group.items | sort: 'date' | reverse -%}
            {%- for post in posts_in_year -%}
              <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a>{%- if post.author -%}（{{ post.author }}）{%- endif -%}</li>
            {%- endfor -%}
          </ul>
        </details>
      {%- endfor -%}
    {%- endif -%}
    {%- if undated_posts.size > 0 -%}
      <h3 class="unknown-date-header">暂无时间</h3>
      <ul>
        {%- assign undated_posts_sorted = undated_posts | sort: 'title' -%}
        {%- for post in undated_posts_sorted -%}
          <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a>{%- if post.author -%}（{{ post.author }}）{%- endif -%}</li>
        {%- endfor -%}
      </ul>
    {%- endif -%}
  {%- else -%}
    <p>未能生成列表。</p>
  {%- endif -%}
</div>

<div id="telegrams" class="tabcontent">
  {%- assign telegrams = site.liaos_tele | sort: 'date' -%}
  {%- if telegrams.size > 0 -%}
    <ul class="timeline-list">
      {%- for post in telegrams -%}
        <li>
          <span class="timeline-date">{{ post.date | date: "%Y-%m-%d" }}</span>
          <div>
            {%- comment -%}
              全新的标题处理逻辑：
              直接分析标题字符串，不再依赖 post.date。
            {%- endcomment -%}
            {%- assign title_parts = post.title | split: ']' -%}
            {%- if title_parts.size > 1 -%}
              {%- comment -%} 情况一：标题包含 [前缀] {%- endcomment -%}
              {%- assign bracket_prefix = title_parts[0] | append: ']' -%}
              {%- assign rest_of_title = title_parts[1] | slice: 10, 999 -%}
              {%- assign title_to_display = bracket_prefix | append: rest_of_title -%}
            {%- else -%}
              {%- comment -%} 情况二：标题不含前缀，直接从开头移除10位日期 {%- endcomment -%}
              {%- assign title_to_display = post.title | slice: 10, 999 -%}
            {%- endif -%}

            <a href="{{ post.url | relative_url }}">{{ title_to_display }}</a>
          </div>
        </li>
      {%- endfor -%}
    </ul>
  {%- else -%}
    <p>未能生成列表。请检查 `_liaos_tele` 文件夹中是否有内容。</p>
  {%- endif -%}
</div>
<script>
  function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    if (evt) {
      evt.currentTarget.className += " active";
    }
  }
  document.getElementById("defaultOpen").click();
</script>