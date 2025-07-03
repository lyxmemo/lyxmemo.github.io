---
layout: page
title: 资料下载区
permalink: /resources/
---

<ul>
  {% for file in site.static_files %}
    {% if file.path contains 'resources' %}
      <li><a href="https://github.com/lyxmemo/lyxmemo.github.io/raw/refs/heads/main/docs/resources/{{ file.basename | uri_escape }}">{{ file.basename }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
