## New codespace:

sudo apt update

<s>sudo apt install pandoc</s>

sudo apt install weasyprint


## Old codespace:
```
bundle exec jekyll serve
```


in docs/
1. 
bundle exec jekyll serve

2. 
```
weasyprint --base-url _site/ _site/book.html assets/与廖耀湘有关的文字资料合集.pdf -e utf-8
```

3. <deprecated> epub is no longer served

```
pandoc _site/book.html -o assets//与廖耀湘有关的文字资料合集.epub --toc
```

4.
```
python3 -c "import re; html = open('_site/book.html').read(); clean = re.sub('<[^<]+?>', '', html); print('\n'.join(line.strip() for line in clean.splitlines() if line.strip()))" > assets/与廖耀湘有关的文字资料合集.txt
```