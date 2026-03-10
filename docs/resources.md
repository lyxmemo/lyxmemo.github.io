---
layout: page
title: 资料下载区
permalink: /resources/
---

<ul>
  {% for name in site.data.resources %}
    <li><a href="https://github.com/lyxmemo/lyxmemo.github.io/raw/refs/heads/main/docs/resources/{{ name | uri_escape }}.pdf">{{ name }}</a></li>
  {% endfor %}
</ul>
