
New codespace:
sudo apt update
sudo apt install pandoc


Old codespace:

bundle exec jekyll serve

in docs/
1. 
bundle exec jekyll serve

2. 
```
weasyprint --base-url _site/ _site/book.html assets/与廖耀湘有关的文字资料合集.pdf -e utf-8
```

3. 
```
pandoc _site/book.html -o assets//与廖耀湘有关的文字资料合集.epub --toc
```