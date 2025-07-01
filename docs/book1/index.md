---
# book1/index.md
layout: default
title: Title of the First Book
---
# {{ page.title }}

## Chapters
<ul>
  {% for post in site.posts %}
    {% if post.path contains 'book1/_posts' %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% endif %}
  {% endfor %}
</ul>