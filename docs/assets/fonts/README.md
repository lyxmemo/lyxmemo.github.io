# Fonts

## lxgw-wenkai-chronology.woff2

霞鹜文楷 LXGW WenKai v1.520, subset to the 2,344 characters that appear in
`_data/chronology.yml` plus ASCII and CJK punctuation. Used as the 楷体 face
for 〔关涉〕 entries on `/chronology-cards.html`.

- Source: https://github.com/lxgw/LxgwWenKai (`LXGWWenKai-Regular.ttf`)
- Licence: SIL Open Font License 1.1 — see `lxgw-wenkai-OFL.txt`

The licence reserves the name `LXGW`, but grants an additional permission for
Modified Versions "subsetted or converted to other formats (e.g. WOFF/WOFF2)
solely for web font delivery", which is what this file is. It is served as a
webfont only and is not offered as an installable desktop font.

To rebuild after the chronology grows:

    pyftsubset LXGWWenKai-Regular.ttf --text-file=chars.txt \
      --output-file=lxgw-wenkai-chronology.woff2 --flavor=woff2 \
      --layout-features='' --no-hinting --desubroutinize \
      --name-IDs='0,1,2,3,4,5,6,13,14' --notdef-outline

where `chars.txt` holds every character in the chronology data.
