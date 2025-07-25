
New codespace:
sudo apt update
sudo apt install pandoc


Old codespace:

in docs/
```
weasyprint --base-url _site/ _site/book.html assets/与廖耀湘有关的文字资料合集.pdf -e utf-8
```

```
pandoc _site/book.html -o assets//与廖耀湘有关的文字资料合集.epub --toc
```