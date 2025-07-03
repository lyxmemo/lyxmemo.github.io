---
layout: page
title: 资料下载区
permalink: /resources/
---

<ul>
  {% for file in site.static_files %}
    {% if file.path contains 'resources' %}
      <li><a href="{{ file.path | relative_url }}">{{ file.basename }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
