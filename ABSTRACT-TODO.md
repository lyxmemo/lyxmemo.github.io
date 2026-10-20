# 英文提要待办清单 / English Abstract To-Do List

The 24 items in `docs/_liaos_writings/` now all carry `title_en`, `english_abstract`
and `keywords_en`. This is the prioritized list of everything else on the site worth
abstracting, in the order I'd do it. Hand this file to whichever AI writes the
abstracts — the spec in section 1 is what makes the output drop straight into the repo
with no rework.

**Scope: 766 files across six collections, of which 581 have transcribed body text.**
The other 185 are `[待录入]` stubs — front matter and a source line only, nothing to
abstract. They're struck through in the lists below; skip them and revisit once the
text is entered. Tiers 1–3 (about 130 files) carry most of the research and SEO value.

---

## 1. Output spec — follow this exactly

Add three keys to each file's YAML front matter, **after the existing keys and before
the closing `---`**. Don't touch `layout`, `title`, `author`, `category`, `tags` or
`date`, and don't touch the Chinese body text.

```yaml
title_en: "English Title Carrying the Campaign, Date or Document Type"
english_abstract: >
  Prose paragraph, 100–220 words, wrapped at 88 columns with two-space indent.
keywords_en: >
  keyword, 关键词, keyword 关键词, ...
  (comma-separated, wrapped at 88 columns with two-space indent)
```

Both `english_abstract` and `keywords_en` are YAML **folded scalars** (`>`): every line
must be indented exactly two spaces and wrapped at word boundaries, since newlines
become single spaces. Never start a wrapped line with extra indentation, and never
leave a blank line inside the block.

These fields are already wired into the site, so nothing else needs changing:

| Surface | File |
| --- | --- |
| Abstract + keyword box on the article page | `docs/_includes/english_abstract.html` |
| `<meta name="keywords">` | `docs/_layouts/default.html` |
| schema.org `ScholarlyArticle` JSON-LD (`abstract`, `keywords`) | `docs/_includes/english_abstract.html` |
| Fuse.js site-search index | `docs/search.json` |
| `/llms.txt` catalog for LLM crawlers | `docs/_plugins/llms_txt.rb` |
| `/en/liaos-writings/` index page | `docs/en/liaos-writings.md` |

The include is rendered by the `post` and `manuscript` layouts, and every file in every
collection below already uses one of those two — so no template work is needed. The
include is guarded by `{% if page.english_abstract %}`, so files without the field
render exactly as they do today.

One thing that *will* need adding as collections get covered: `/en/liaos-writings/`
only lists `site.liaos_writings`. Once a second collection has abstracts, either give
it its own `/en/<collection>/` index page on the same template, or generalize that page
to loop over several collections. `_plugins/llms_txt.rb` likewise only walks
`liaos_writings` and has a hardcoded "Other collections" section near the bottom that
should become a real listing.

### What goes in `english_abstract`

- What the document **is** (memoir, after-action report, telegram, news dispatch, diary
  excerpt, testimony, inscription), who wrote it, when, and where it was published.
- The concrete content: units, places, dates, decisions, named people.
- Its **evidentiary value** — what a researcher can and cannot use it for.
- For 文史资料 (Wenshi Ziliao) memoirs and other PRC-era texts, say so plainly:
  first-person but composed in captivity or under that series' editorial conventions,
  not contemporaneous wartime documents. The 24 existing abstracts model this.
- Don't invent. If a date, name or figure isn't in the source, leave it out. Where the
  archive's own metadata looks wrong, flag it rather than silently correcting — see the
  note at the end of the 辽阳 abstract in `_liaos_writings` for the pattern.

### What goes in `keywords_en`

This is where the search value lives. For every proper noun in the abstract, give the
variants a researcher might actually type:

- **Romanization variants** — pinyin *and* Wade-Giles / postal forms: Chiang Kai-shek
  蒋介石 / Chiang Chieh-shih / Jiang Jieshi; Mukden 沈阳; Chinchow 锦州; Ssupingchieh /
  Szeping 四平街; Liao Yao-hsiang 廖耀湘.
- **Chinese characters beside the English** for every person, place, unit, campaign and
  publication — this site's readers search in Chinese.
- **Unit designations** in both forms: New 22nd Division 新编第二十二师, New Sixth Army
  新六军, Ninth Army Group 第九兵团, Fifth Army 第五军, Chinese Army in India 中国驻印军
  (X Force), Chinese Expeditionary Force 中国远征军.
- **Campaign and battle names** in both forms: Liaoshen campaign 辽沈战役, Battle of
  Siping 四平街战役, Kunlun Pass 昆仑关, Hukawng Valley 胡康河谷, Myitkyina 密支那.
- **Organization and series names**: Kuomintang KMT Guomindang, Wenshi Ziliao 文史资料,
  CPPCC 政协, Academia Historica 国史馆, Central News Agency 中央社.
- End every list with the canonical identity block used in `_liaos_writings`:

```
Liao Yaoxiang 廖耀湘, Liao Yao-hsiang, Liao Yao-siang, Liao Chien-chu 廖建楚,
General Liao Yaoxiang, Kuomintang KMT Guomindang Nationalist army 国民党军,
National Revolutionary Army 国民革命军, Republic of China military history,
primary source 史料 原始文献, liaoyaoxiang.com archive
```

For documents where Liao is a minor figure — much of 报刊 and 来往电报 — lead with the
actual principal instead, and keep Liao's names only where he genuinely appears.

### Verifying before commit

```bash
cd docs && bundle install
bundle exec jekyll build
```

Then confirm `_site/search.json` parses as JSON, every `application/ld+json` block in
`_site/<collection>/*.html` parses, and `_site/llms.txt` lists the new entries. If the
`pages-themes/minimal` remote theme can't be downloaded (a 403 from a restricted
network will do it), build with `remote_theme:` blanked in an override config — the
local `_layouts/` are what these fields depend on.

---

## 2. Priority tiers

**Tier 1 — do first (6 files).** `docs/_n6a_memorial/` and `docs/_n22d_memorial/`, minus
their three stubs. Short, and they anchor the whole archive: `新六军简史` and
`本师成立经过概要` are what an English-language researcher looking for the New Sixth
Army or the New 22nd Division will land on first.

**Tier 2 — battle histories (69 files).** The operational core of the site. Within it,
do `liaoshen/1948` first — the Liaoshen campaign is the most-searched topic here, and
these are the counterpart accounts to Liao's own `辽西战役纪实`, including Du Yuming's
`辽沈战役概述`, Zheng Tingji's `辽西兵团的覆灭`, and the PLA-side pieces on Heishan and
the encirclement. Then `1944` (the northern Burma reconquest, with Zheng Dongguo's
memoirs and the Chinese Army in India), then `1942` (the first Burma campaign, the
Japanese official history excerpt, and the Alexander memoir extract), then
`liaoshen/1946` (Siping and Shaling), then `1939`, `1943`, `1945`, `liaoshen/1947`.

**Tier 3 — the 40 largest 故人回忆 memoirs.** The biographical sources: the Stilwell and
Xu Yongchang diary excerpts, the Chiang Kai-shek chronology extracts, the two
full-length Liao biographies, the family and staff-officer recollections, and
`廖耀湘在新中国的二十年` on his PRC years. High value per file, and almost none of it
exists in English anywhere.

**Tier 4 — remaining 故人回忆 and the 40 largest 报刊 items.** The newspaper pieces are
short; 80–120 words is usually enough, but the keyword list still matters — date,
paper, place, unit.

**Tier 5 — remaining 报刊 and 来往电报.** For the telegrams I would **not** write
individual abstracts for all 352: 169 of them are 待录入 stubs with no text at all, and
the transcribed remainder are mostly a few hundred characters and highly repetitive.
Two better options:

1. Abstract only the 30 largest transcribed ones (listed below) — the Chiang–Stilwell
   conversation records, the Nanjing defence battle report, the Lin Biao / Luo Ronghuan
   campaign summary — and give the series a **collection-level** English overview page
   at `/en/telegrams/`: date range, senders and recipients, archival provenance, and
   what the series is good for.
2. Or generate `title_en` only (no abstract) for all transcribed telegrams, which is
   cheap and still makes them findable by date and correspondent.

---

## 3. File lists

Ordered by tier. Struck-through entries are `[待录入]` stubs — skip them.

### _n6a_memorial — 2 to abstract (+1 待录入 stub, skip)

- [ ] `docs/_n6a_memorial/廖军长传略.md` — 3.8 KB
- ~~`docs/_n6a_memorial/新六军战斗经验.md`~~ — 待录入 stub, skip
- [ ] `docs/_n6a_memorial/新六军简史.md` — 19.9 KB

### _n22d_memorial — 4 to abstract (+2 待录入 stubs, skip)

- [ ] `docs/_n22d_memorial/二二师打胜仗是偶然的吗？（何玉书）.md` — 16.2 KB
- [ ] `docs/_n22d_memorial/太子河畔的工兵（卢荫权）.md` — 5.9 KB
- [ ] `docs/_n22d_memorial/新二二师出关周年纪念册序（周霁光）.md` — 12.6 KB
- [ ] `docs/_n22d_memorial/本师成立经过概要（魏书文）.md` — 9.7 KB
- ~~`docs/_n22d_memorial/神炮兵之由来（金廷才）.md`~~ — 待录入 stub, skip
- ~~`docs/_n22d_memorial/陆军第五军新编第二十二师桂南抗战阵亡官兵题名录.md`~~ — 待录入 stub, skip

### _battles_history/liaoshen/1948 — 20 to abstract (+1 待录入 stub, skip)

- [ ] `docs/_battles_history/liaoshen/1948/会战辽西（段苏权）.md` — 10.3 KB
- [ ] `docs/_battles_history/liaoshen/1948/关键的一仗（杨迪）.md` — 16.6 KB
- [ ] `docs/_battles_history/liaoshen/1948/四平街战役侧记（高青山）.md` — 5.0 KB
- [ ] `docs/_battles_history/liaoshen/1948/围歼廖耀湘兵团（肖剑飞）.md` — 21.2 KB
- [ ] `docs/_battles_history/liaoshen/1948/廖耀湘被擒记（张世伟、崔井和）.md` — 8.0 KB
- ~~`docs/_battles_history/liaoshen/1948/扼住廖耀湘兵团西进的咽喉（刘转连）.md`~~ — 待录入 stub, skip
- [ ] `docs/_battles_history/liaoshen/1948/新编第一军在辽西（陈时杰）.md` — 34.1 KB
- [ ] `docs/_battles_history/liaoshen/1948/新编第三军辽沈战役被歼记（黄福荫）.md` — 20.7 KB
- [ ] `docs/_battles_history/liaoshen/1948/新编第三军辽西被歼情况片段（郭树人）.md` — 6.2 KB
- [ ] `docs/_battles_history/liaoshen/1948/新编第三军黑山被歼记（李定陆）.md` — 7.8 KB
- [ ] `docs/_battles_history/liaoshen/1948/第七⼗⼀军辽西作战和被歼经过（胡锻夫）.md` — 20.5 KB
- [ ] `docs/_battles_history/liaoshen/1948/第七十一军第八十八师在四平被歼侧记（郑殿起）.md` — 15.7 KB
- [ ] `docs/_battles_history/liaoshen/1948/第五十三军第一三○师沈阳起义经过（谷振寰）.md` — 22.6 KB
- [ ] `docs/_battles_history/liaoshen/1948/血肉筑起的长城（蒋克诚）.md` — 4.0 KB
- [ ] `docs/_battles_history/liaoshen/1948/辽沈战役概述（杜聿明）.md` — 104.0 KB
- [ ] `docs/_battles_history/liaoshen/1948/辽西兵团的覆灭（郑庭笈）.md` — 24.2 KB
- [ ] `docs/_battles_history/liaoshen/1948/辽西战役补述（杨琨）.md` — 9.6 KB
- [ ] `docs/_battles_history/liaoshen/1948/辽西灭“虎”（董占林）.md` — 12.1 KB
- [ ] `docs/_battles_history/liaoshen/1948/辽阳、鞍山国民党军被歼经过（张干樵 郑经纬）.md` — 11.8 KB
- [ ] `docs/_battles_history/liaoshen/1948/郑洞国回忆录——解放战争（郑洞国）.md` — 42.2 KB
- [ ] `docs/_battles_history/liaoshen/1948/黑山阻击战（贺庆积）.md` — 54.5 KB

### _battles_history/liaoshen/1946 — 12 to abstract (+1 待录入 stub, skip)

- [ ] `docs/_battles_history/liaoshen/1946/一九四六年四月至五月新一军在四平街作战经过（节选）（史说）.md` — 8.2 KB
- [ ] `docs/_battles_history/liaoshen/1946/七台子之战（吴显臣）.md` — 9.1 KB
- ~~`docs/_battles_history/liaoshen/1946/东北保安司令长官司令部接收东北周年纪念册(1947年版).md`~~ — 待录入 stub, skip
- [ ] `docs/_battles_history/liaoshen/1946/从辽河扫荡到鸭绿江畔（大可）.md` — 10.5 KB
- [ ] `docs/_battles_history/liaoshen/1946/保卫四平之战（陈沂）.md` — 14.3 KB
- [ ] `docs/_battles_history/liaoshen/1946/出关一年以来的回忆（方哲岳）.md` — 34.9 KB
- [ ] `docs/_battles_history/liaoshen/1946/国民党破坏和平进攻东北始末（杜聿明）.md` — 109.8 KB
- [ ] `docs/_battles_history/liaoshen/1946/在东北接收一年的六十四团（李振华）.md` — 15.4 KB
- [ ] `docs/_battles_history/liaoshen/1946/沙岭之战（刘梓皋）.md` — 14.8 KB
- [ ] `docs/_battles_history/liaoshen/1946/沙岭作战始末（邱中岳）.md` — 8.7 KB
- [ ] `docs/_battles_history/liaoshen/1946/沙岭战斗（罗英）.md` — 10.7 KB
- [ ] `docs/_battles_history/liaoshen/1946/滇军第一八四师海城起义回忆（节选）（马逸飞）.md` — 5.9 KB
- [ ] `docs/_battles_history/liaoshen/1946/陈明仁在东北（节选）（应起鹤）.md` — 7.9 KB

### _battles_history/liaoshen/1947 — 3 to abstract (+1 待录入 stub, skip)

- [ ] `docs/_battles_history/liaoshen/1947/东北保安司令长官部侵占安东战役纪要（杜聿明）.md` — 62.6 KB
- [ ] `docs/_battles_history/liaoshen/1947/第五十三军增援四平街作战经过（节选）（谷振寰 李连仲）.md` — 3.6 KB
- ~~`docs/_battles_history/liaoshen/1947/第四十九军主力在锦西杨家杖子被歼经过（于泽霖）.md`~~ — 待录入 stub, skip
- [ ] `docs/_battles_history/liaoshen/1947/蒋军四平街解围战役中的八棵树争夺战（郑庭笈）.md` — 26.2 KB

### _battles_history/1944 — 13 to abstract (+2 待录入 stubs, skip)

- ~~`docs/_battles_history/1944/与廖耀湘将军一席谈.md`~~ — 待录入 stub, skip
- [ ] `docs/_battles_history/1944/中国驻印军始末（郑洞国 覃异之）.md` — 24.8 KB
- [ ] `docs/_battles_history/1944/从八莫之役到凯旋回国（史说）.md` — 9.9 KB
- [ ] `docs/_battles_history/1944/国军印缅作战回忆录（李珍）.md` — 37.4 KB
- [ ] `docs/_battles_history/1944/国军装甲兵口述历史访问记录.md` — 56.0 KB
- [ ] `docs/_battles_history/1944/在孟拱河谷前线访问孙廖两将军（乐恕人）.md` — 3.3 KB
- [ ] `docs/_battles_history/1944/廖耀湘师长会见记（中央日报记者）.md` — 5.5 KB
- ~~`docs/_battles_history/1944/第五十师赴缅抗日经过（王大中）.md`~~ — 待录入 stub, skip
- [ ] `docs/_battles_history/1944/索卡道之役之作战经过概要（邱中岳）.md` — 10.3 KB
- [ ] `docs/_battles_history/1944/缅北百贼河之役（邱中岳）.md` — 13.6 KB
- [ ] `docs/_battles_history/1944/记廖耀湘将军.md` — 7.4 KB
- [ ] `docs/_battles_history/1944/远征军的将星群（吕德涧）.md` — 1.7 KB
- [ ] `docs/_battles_history/1944/郑洞国回忆录：缅北反攻（上）（郑洞国）.md` — 82.5 KB
- [ ] `docs/_battles_history/1944/郑洞国回忆录：缅北反攻（下）（郑洞国）.md` — 28.7 KB
- [ ] `docs/_battles_history/1944/驻印抗日远征军译员生活回忆.md` — 23.8 KB

### _battles_history/1942 — 10 to abstract

- [ ] `docs/_battles_history/1942/1942年缅甸作战回忆（邓军林）.md` — 16.7 KB
- [ ] `docs/_battles_history/1942/中国远征军在缅甸（黄翔）.md` — 18.8 KB
- [ ] `docs/_battles_history/1942/亚历山大元帅战争回忆录（节选）（Field Marshal Harold Alexander, edited by military historian John North）.md` — 32.7 KB
- [ ] `docs/_battles_history/1942/挫辱而归的第一次远征（余韶）.md` — 49.9 KB
- [ ] `docs/_battles_history/1942/新一军的成立及其抗战概述（王大中）.md` — 7.4 KB
- [ ] `docs/_battles_history/1942/新二十二师缅南作战纪要（郭修甲）.md` — 5.0 KB
- [ ] `docs/_battles_history/1942/新编第二十二师六十四团出国抗战纪实（祝能）.md` — 33.4 KB
- [ ] `docs/_battles_history/1942/第一次入缅参战之回忆（李涛）.md` — 5.3 KB
- [ ] `docs/_battles_history/1942/第五军攻略昆仑关作战经过检讨.md` — 16.5 KB
- [ ] `docs/_battles_history/1942/缅甸作战（节选）（日本防卫厅防卫研究所战史研究室）.md` — 122.6 KB

### _battles_history/1939 — 4 to abstract

- [ ] `docs/_battles_history/1939/关于昆仑关战役的回忆（黄翔）.md` — 5.2 KB
- [ ] `docs/_battles_history/1939/昆仑关战役（邓军林）.md` — 29.5 KB
- [ ] `docs/_battles_history/1939/昆仑关攻坚战亲历记（郑洞国 郑庭笈）.md` — 9.5 KB
- [ ] `docs/_battles_history/1939/第四战区关于南宁各役战斗经过概要.md` — 1.5 KB

### _battles_history/1943 — 1 to abstract (+1 待录入 stub, skip)

- [ ] `docs/_battles_history/1943/兰姆珈训练营地与筹划反攻（郑洞国）.md` — 44.0 KB
- ~~`docs/_battles_history/1943/听李（涛）少将谈敌情.md`~~ — 待录入 stub, skip

### _battles_history/1945 — 6 to abstract

- [ ] `docs/_battles_history/1945/中华民国驻印军缅北会战经过概要.md` — 31.4 KB
- [ ] `docs/_battles_history/1945/从印度缅甸到中国（魏书文）.md` — 24.5 KB
- [ ] `docs/_battles_history/1945/参与芷江“日本洽降”经过.md` — 5.2 KB
- [ ] `docs/_battles_history/1945/国民党受降和何应钦的“锦囊妙计”（节选）.md` — 1.6 KB
- [ ] `docs/_battles_history/1945/廖耀湘在芷江的二三事.md` — 8.9 KB
- [ ] `docs/_battles_history/1945/我对湘西“雪峰山会战”的回忆（节选）.md` — 9.9 KB

### _ten_year_memorial — 40 largest (all 40 to abstract)

- [ ] `docs/_ten_year_memorial/史迪威日记（节选其中与第五军、新二二师相关部分）.md` — 97.3 KB
- [ ] `docs/_ten_year_memorial/总统蒋公大事长编（节选与廖耀湘相关片段）.md` — 74.5 KB
- [ ] `docs/_ten_year_memorial/中华复兴社的内幕（廖耀湘等）.md` — 72.5 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军传（刘建章 李珍）.md` — 71.8 KB
- [ ] `docs/_ten_year_memorial/廖耀湘在新中国的二十年（黄双喜）.md` — 71.6 KB
- [ ] `docs/_ten_year_memorial/徐永昌日记（节选与廖耀湘有关片段）.md` — 39.0 KB
- [ ] `docs/_ten_year_memorial/浴血昆仑关（李诚毅）.md` — 38.0 KB
- [ ] `docs/_ten_year_memorial/转战异域扬国威（刘建章）.md` — 37.4 KB
- [ ] `docs/_ten_year_memorial/杜聿明在东北的功与过（陈嘉骥）.md` — 33.7 KB
- [ ] `docs/_ten_year_memorial/忆往事·话湘西（刘征鸿）.md` — 33.1 KB
- [ ] `docs/_ten_year_memorial/我毕生所敬仰的廖耀湘将军（李珍：新22师连、营、团长）.md` — 32.9 KB
- [ ] `docs/_ten_year_memorial/沈醉回忆录（沈醉）.md` — 32.6 KB
- [ ] `docs/_ten_year_memorial/八十自述（罗泽闿）.md` — 32.2 KB
- [ ] `docs/_ten_year_memorial/从军记——印缅战区见闻杂忆（盛渊）.md` — 31.8 KB
- [ ] `docs/_ten_year_memorial/我所知道的教导总队（郭白涛）.md` — 31.3 KB
- [ ] `docs/_ten_year_memorial/廖耀湘事略（禹靖寰）.md` — 31.2 KB
- [ ] `docs/_ten_year_memorial/新一军的少校译员（梁家佑）.md` — 30.7 KB
- [ ] `docs/_ten_year_memorial/沦陷中的栖霞寺（高怀珠）.md` — 30.2 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军与我（蔡贤俊：第九兵团高参、第五军政治部主任）.md` — 28.6 KB
- [ ] `docs/_ten_year_memorial/南京大屠杀幸存者调查口述（和允龙 等）.md` — 28.6 KB
- [ ] `docs/_ten_year_memorial/参加缅印战场抗日回忆（师临先）.md` — 28.3 KB
- [ ] `docs/_ten_year_memorial/廖耀湘之治军与论兵（向华超）.md` — 28.1 KB
- [ ] `docs/_ten_year_memorial/追随廖公耀湘十年记（蒋继志：新二二师、新六军军需处长、主任）.md` — 27.6 KB
- [ ] `docs/_ten_year_memorial/追述辽南、公主屯、辽西诸战役之作战经过及是非曲直（邱中岳：新22师连、营、团长）.md` — 27.3 KB
- [ ] `docs/_ten_year_memorial/我毕生最崇敬的长官廖耀湘将军（何福祥：曾任新22师连、营长，207师团长）.md` — 27.2 KB
- [ ] `docs/_ten_year_memorial/追怀慧眼将军——廖公耀湘之德泽（文中侠：N22D与N38D联络参谋、后一直任廖的联络官）.md` — 26.4 KB
- [ ] `docs/_ten_year_memorial/我所知道的廖耀湘和他的夫人（金咸宗根据其母陈氏口述记录整理）.md` — 25.4 KB
- [ ] `docs/_ten_year_memorial/我所知道的廖耀湘（李以劻）.md` — 23.7 KB
- [ ] `docs/_ten_year_memorial/编后赘言——我怎样写廖耀湘将军传（李珍）.md` — 23.1 KB
- [ ] `docs/_ten_year_memorial/驻印军三年工作漫忆（李则夷）.md` — 22.9 KB
- [ ] `docs/_ten_year_memorial/廖耀湘在野人山行军中（廖谷生）.md` — 21.4 KB
- [ ] `docs/_ten_year_memorial/蒋介石的铁卫队——教导总队（周振强）.md` — 20.9 KB
- [ ] `docs/_ten_year_memorial/我与廖耀湘（文强）.md` — 20.9 KB
- [ ] `docs/_ten_year_memorial/蒋中正日记（节选与廖耀湘有关片段）.md` — 19.7 KB
- [ ] `docs/_ten_year_memorial/悼耀公忆往事（张志良：曾任新22师参谋、营长、团长）.md` — 18.9 KB
- [ ] `docs/_ten_year_memorial/追思总统 蒋公（王铁汉）.md` — 18.9 KB
- [ ] `docs/_ten_year_memorial/追随湘公十年略述（周璞：新22师连、营、团、副师长）.md` — 18.4 KB
- [ ] `docs/_ten_year_memorial/刘建章将军访问纪录（邱中岳）.md` — 18.1 KB
- [ ] `docs/_ten_year_memorial/我参加青年远征军赴缅抗日（黄义方）.md` — 17.5 KB
- [ ] `docs/_ten_year_memorial/在南京保卫战中的教导总队（吴幼元）.md` — 17.3 KB

### _ten_year_memorial — remaining: 94 to abstract (+7 待录入 stubs, skip)

- [ ] `docs/_ten_year_memorial/接收东北宣传业务的回忆（陈鎭）.md` — 16.8 KB
- [ ] `docs/_ten_year_memorial/熊式辉东北去来（陈嘉骥）.md` — 16.4 KB
- [ ] `docs/_ten_year_memorial/东北接收与沦陷纪痛（金戎）.md` — 16.0 KB
- [ ] `docs/_ten_year_memorial/抗战胜利后接收东北的回忆（吴焕章）.md` — 15.1 KB
- [ ] `docs/_ten_year_memorial/赵家骧将军传（赵尺子）.md` — 14.8 KB
- [ ] `docs/_ten_year_memorial/我所敬的廖耀湘将军（刘梓皋：曾任新六军暂62师师长，新22师营、团长，教导总队排长）.md` — 14.4 KB
- [ ] `docs/_ten_year_memorial/我所认识的廖耀湘先生（龙天武：第九兵团新三军军长、新六军第14师师长）.md` — 13.7 KB
- [ ] `docs/_ten_year_memorial/印缅抗战亲历记——夏开祥回忆录.md` — 13.4 KB
- [ ] `docs/_ten_year_memorial/航委会驻仰光、印度六年见闻（节选）（罗惠侨）.md` — 13.0 KB
- [ ] `docs/_ten_year_memorial/追随廖耀湘将军远征印缅抗日（师临先）.md` — 12.8 KB
- [ ] `docs/_ten_year_memorial/回忆1942年国民党远征军（前期）赴缅作战片断（刘家茂）.md` — 12.5 KB
- [ ] `docs/_ten_year_memorial/抗日报国扬威异邦——我所经历的“印缅战役”.md` — 12.3 KB
- [ ] `docs/_ten_year_memorial/征战印缅忆语（李奇）.md` — 12.0 KB
- [ ] `docs/_ten_year_memorial/廖先生的“伤兵第一”观念（陆以仁：新22师军医）.md` — 11.8 KB
- [ ] `docs/_ten_year_memorial/关于中国驻印军（刘措宜）.md` — 11.3 KB
- [ ] `docs/_ten_year_memorial/廖耀湘传略（孙武臣 季夫）.md` — 10.8 KB
- [ ] `docs/_ten_year_memorial/记廖耀湘（赵烈安）.md` — 10.8 KB
- [ ] `docs/_ten_year_memorial/怀念廖耀湘将军（郭温）.md` — 10.8 KB
- [ ] `docs/_ten_year_memorial/回忆在芷江接待今井武夫.md` — 10.6 KB
- [ ] `docs/_ten_year_memorial/陕西知识青年从军记（张逸智）.md` — 10.5 KB
- [ ] `docs/_ten_year_memorial/我所知远征军入缅初期抗日作战概况（赵德树）.md` — 10.3 KB
- [ ] `docs/_ten_year_memorial/在驻印缅远征军的几件事（李思恭）.md` — 9.9 KB
- [ ] `docs/_ten_year_memorial/黄埔军校“清党”前后纪实（卞稚珊）.md` — 9.8 KB
- [ ] `docs/_ten_year_memorial/接收东北时军统特务活动种种（文强）.md` — 9.7 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军领导与指挥的特性（舒传煜：新22师参谋、后任第九兵团特务营营长）.md` — 8.7 KB
- [ ] `docs/_ten_year_memorial/复兴社与欧美军事留学生（节选）（蔡仁清）.md` — 8.3 KB
- [ ] `docs/_ten_year_memorial/怀念故友廖耀湘（潘鑑）.md` — 8.2 KB
- [ ] `docs/_ten_year_memorial/烽火中的知音（罗安）.md` — 7.8 KB
- [ ] `docs/_ten_year_memorial/中国战区受降始末（南京市委员会文史资料委员会编）.md` — 7.7 KB
- [ ] `docs/_ten_year_memorial/廖先生的丰功伟绩（马荣相）.md` — 7.7 KB
- [ ] `docs/_ten_year_memorial/抗日战争时期陈诚系军事集团的扩充情况.md` — 7.7 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军评传（姜汉卿：东北行辕参谋处长）.md` — 7.6 KB
- [ ] `docs/_ten_year_memorial/溥仪等人在黄陂横店参观情况回忆（张怡如）.md` — 7.6 KB
- [ ] `docs/_ten_year_memorial/我所知道的廖耀湘将军（黄锦华：曾任新22师营长）.md` — 7.4 KB
- [ ] `docs/_ten_year_memorial/还俗记（钮先铭）.md` — 7.1 KB
- [ ] `docs/_ten_year_memorial/黄埔军校第七期始末（兰守青）.md` — 7.0 KB
- [ ] `docs/_ten_year_memorial/记廖耀湘将军（祝能）.md` — 6.7 KB
- [ ] `docs/_ten_year_memorial/远征军中当译员（潘侨南）.md` — 6.6 KB
- [ ] `docs/_ten_year_memorial/廖公耀湘事略（赵霞：曾任新六军参谋长）.md` — 6.6 KB
- [ ] `docs/_ten_year_memorial/东北地区接收点滴（张干樵）.md` — 6.5 KB
- [ ] `docs/_ten_year_memorial/蒋介石派遣欧美军事留学生纪略（杨中平）.md` — 6.5 KB
- [ ] `docs/_ten_year_memorial/记先夫二、三事（廖黄伯溶）.md` — 6.0 KB
- [ ] `docs/_ten_year_memorial/中国驻印军反攻缅北首战大捷（罗春林 李鸿萱）.md` — 6.0 KB
- [ ] `docs/_ten_year_memorial/长忆廖耀湘（肖自成）.md` — 5.9 KB
- [ ] `docs/_ten_year_memorial/随远征军入缅抗日回忆录（刘天庆 袁启俊）.md` — 5.9 KB
- [ ] `docs/_ten_year_memorial/廖耀湘率部血战缅北（李羽立）.md` — 5.8 KB
- [ ] `docs/_ten_year_memorial/我对中国远征军赴缅作战的回忆（徐继光）.md` — 5.7 KB
- [ ] `docs/_ten_year_memorial/创造历史的伟人（俞济时口述 钱先莲笔录）.md` — 5.6 KB
- [ ] `docs/_ten_year_memorial/中华民国史事日志（节选与廖耀湘有关片段）.md` — 5.5 KB
- [ ] `docs/_ten_year_memorial/记缅北百贼河之役（廖耀汉）.md` — 5.5 KB
- [ ] `docs/_ten_year_memorial/芷江受降侧记.md` — 5.2 KB
- [ ] `docs/_ten_year_memorial/父亲与我——我记忆中的父亲（廖定一）.md` — 5.2 KB
- [ ] `docs/_ten_year_memorial/怀念第五届全国政协委员廖耀湘（李以劻）.md` — 5.0 KB
- [ ] `docs/_ten_year_memorial/《特别公民》节选（周吉平）.md` — 5.0 KB
- [ ] `docs/_ten_year_memorial/回忆廖将军两件小事（易占中）.md` — 4.9 KB
- [ ] `docs/_ten_year_memorial/湘公小传（沈成志）.md` — 4.8 KB
- [ ] `docs/_ten_year_memorial/廖将军是服从命令的楷模（黄友蘅）.md` — 4.8 KB
- [ ] `docs/_ten_year_memorial/刘建章《九十自述》中涉及廖耀湘的几处回忆.md` — 4.7 KB
- [ ] `docs/_ten_year_memorial/辽西恨（舒适存：曾任新六军副军长）.md` — 4.6 KB
- [ ] `docs/_ten_year_memorial/追怀廖耀湘将军（罗林芳：新22师连、营长）.md` — 4.6 KB
- [ ] `docs/_ten_year_memorial/中国陆军总司令部概况（节选）（朱才樑）.md` — 4.6 KB
- [ ] `docs/_ten_year_memorial/处理日本投降文件汇编.md` — 4.6 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军轶事（罗友伦：曾任第五军参谋长）.md` — 4.4 KB
- [ ] `docs/_ten_year_memorial/忆列多，从缅北到辽西（黄超然：曾任驻印军高炮营营长）.md` — 4.4 KB
- [ ] `docs/_ten_year_memorial/悼“乡长”廖耀湘先生（王筠）.md` — 4.3 KB
- [ ] `docs/_ten_year_memorial/从参加抗战到目睹日军投降（节选）（冷欣）.md` — 4.2 KB
- [ ] `docs/_ten_year_memorial/在廖将军指挥下中国战史上最辉煌的两个战役（李定一：曾任新22师营、团长）.md` — 4.1 KB
- [ ] `docs/_ten_year_memorial/不以成败论英雄（王康）.md` — 4.1 KB
- [ ] `docs/_ten_year_memorial/刘伯承请廖耀湘讲军事课（木青）.md` — 3.9 KB
- [ ] `docs/_ten_year_memorial/我所了解的卫立煌（节选）（陈铁）.md` — 3.9 KB
- [ ] `docs/_ten_year_memorial/黄寿仁先生赠廖耀湘诗屏.md` — 3.8 KB
- [ ] `docs/_ten_year_memorial/廖公耀湘先生与我（贾维録）.md` — 3.8 KB
- [ ] `docs/_ten_year_memorial/刘建章先生传略（季夫）.md` — 3.5 KB
- [ ] `docs/_ten_year_memorial/乡亲传颂二三事（陈希桥）.md` — 3.5 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军追思纪念（萧赞育：军委会侍从、秘书长、立法委员）.md` — 3.4 KB
- [ ] `docs/_ten_year_memorial/难忘的回忆：怀念刘建章先生（杜坚）.md` — 3.3 KB
- [ ] `docs/_ten_year_memorial/浩气长存的——廖耀湘将军（谢冰莹）.md` — 3.2 KB
- [ ] `docs/_ten_year_memorial/日本投降和中国陆军总部受降内幕.md` — 3.2 KB
- [ ] `docs/_ten_year_memorial/缅北抗日见闻（祝寿嵩）.md` — 3.2 KB
- [ ] `docs/_ten_year_memorial/怀廖公琐忆二三事（余汝干：新二二师营长、团长）.md` — 3.2 KB
- [ ] `docs/_ten_year_memorial/缅先贤，悼廖公（张绍曾）.md` — 3.1 KB
- [ ] `docs/_ten_year_memorial/我素敬仰的廖先生（罗先致：曾任新22师营长）.md` — 2.9 KB
- [ ] `docs/_ten_year_memorial/怀念廖耀湘（宁秉衡）.md` — 2.7 KB
- [ ] `docs/_ten_year_memorial/《四进长春》节选（尚传道）.md` — 2.4 KB
- [ ] `docs/_ten_year_memorial/抗日名将廖耀湘（许文彬）.md` — 2.2 KB
- [ ] `docs/_ten_year_memorial/廖耀湘在启蒙馆（廖昌仕 廖鹏程）.md` — 2.1 KB
- [ ] `docs/_ten_year_memorial/廖耀湘幼年轶闻（廖昌仕 廖鹏程）.md` — 2.1 KB
- [ ] `docs/_ten_year_memorial/廖耀湘战功点滴（罗林芳 刘万廷）.md` — 1.9 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军殉国十周年纪念（黄振华 陈维纶）.md` — 1.8 KB
- [ ] `docs/_ten_year_memorial/读廖将军传（舒彦文）.md` — 1.8 KB
- [ ] `docs/_ten_year_memorial/抗日胜利时的片断回忆.md` — 1.7 KB
- [ ] `docs/_ten_year_memorial/敬悼 廖耀湘将军（舒适存：曾任新六军副军长）.md` — 1.6 KB
- [ ] `docs/_ten_year_memorial/廖耀湘将军对部队之训练（陈廷元）.md` — 1.4 KB
- [ ] `docs/_ten_year_memorial/陈明仁二三事（罗召南）.md` — 1.3 KB
- ~~`docs/_ten_year_memorial/廖耀湘后人访谈录.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/廖欧阳蘅女士口述：我所知道的廖耀湘.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/爱新觉罗溥仪、王耀武、廖耀湘追悼会在京举行（人民日报）.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/我所知道的廖耀湘（王文通）.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/将军关怀铭胸臆（孙海浪）.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/我对廖先生部队训练的体认（许敬威）.md`~~ — 待录入 stub, skip
- ~~`docs/_ten_year_memorial/我对廖将军之敬仰（席代瑜）.md`~~ — 待录入 stub, skip

### _newspapers — 40 largest (all 40 to abstract)

- [ ] `docs/_newspapers/20170201中国远征军军粮筹办补给经过节略.md` — 38.7 KB
- [ ] `docs/_newspapers/忆说廖耀湘（乔家才）.md` — 17.5 KB
- [ ] `docs/_newspapers/19681125廖耀湘谈话记录.md` — 16.9 KB
- [ ] `docs/_newspapers/东北接收与沦陷纪痛.md` — 16.1 KB
- [ ] `docs/_newspapers/中國日軍投降簽字昨在京順利完成.md` — 15.4 KB
- [ ] `docs/_newspapers/新六军的诞生 廖耀湘军长一夕谈.md` — 12.6 KB
- [ ] `docs/_newspapers/回忆参加中日洽降会议之后勤工作.md` — 11.7 KB
- [ ] `docs/_newspapers/廖耀湘及其卫星（南京通讯）.md` — 11.7 KB
- [ ] `docs/_newspapers/遼陽之春在共軍的手裏溜走.md` — 11.1 KB
- [ ] `docs/_newspapers/保卫上海的新六军.md` — 10.2 KB
- [ ] `docs/_newspapers/踏雪聽砲聲.md` — 9.3 KB
- [ ] `docs/_newspapers/瀋陽的痙攣.md` — 8.3 KB
- [ ] `docs/_newspapers/何總司令報吿執行任務情形.md` — 7.9 KB
- [ ] `docs/_newspapers/向廖耀湘要饷粮（韩宝兴）.md` — 6.4 KB
- [ ] `docs/_newspapers/孟拱河谷之战——记廖耀湘将军的谈话.md` — 6.1 KB
- [ ] `docs/_newspapers/辽沈战役中的电子情报战.md` — 6.1 KB
- [ ] `docs/_newspapers/上海到秦皇島隨軍北征海上六日記.md` — 5.8 KB
- [ ] `docs/_newspapers/廖耀湘与新六军.md` — 5.6 KB
- [ ] `docs/_newspapers/東北烽火圖解.md` — 5.1 KB
- [ ] `docs/_newspapers/”战犯楼“里的廖耀湘（高皋）.md` — 5.1 KB
- [ ] `docs/_newspapers/迎送新旧警备司令.md` — 4.6 KB
- [ ] `docs/_newspapers/20050907栖霞寺1937——中国版“辛德勒名单”.md` — 4.2 KB
- [ ] `docs/_newspapers/國軍出關一年間.md` — 4.1 KB
- [ ] `docs/_newspapers/國軍勁旅開抵吉林.md` — 3.8 KB
- [ ] `docs/_newspapers/新六軍十四師健兒分三批開東北.md` — 3.8 KB
- [ ] `docs/_newspapers/從瀋陽到遼東半島.md` — 3.6 KB
- [ ] `docs/_newspapers/东北怎样失守的？ 主要是由于人谋不臧 卫立煌不该弃职逃走 廖耀湘援锦指挥失当.md` — 3.6 KB
- [ ] `docs/_newspapers/遣送東北日人返國美軍同樣負責.md` — 3.6 KB
- [ ] `docs/_newspapers/歡迎馬帥速寫.md` — 3.6 KB
- [ ] `docs/_newspapers/開原烏拉街收復.md` — 3.6 KB
- [ ] `docs/_newspapers/國軍昨晨收復長春.md` — 3.6 KB
- [ ] `docs/_newspapers/東北局勢益趨緊張四平市郊展開砲戰.md` — 3.5 KB
- [ ] `docs/_newspapers/新中國的干城靑年軍到上海.md` — 3.5 KB
- [ ] `docs/_newspapers/东北将星检阅（和平日报）.md` — 3.5 KB
- [ ] `docs/_newspapers/新六军开拨东北声中 访廖耀湘军长.md` — 3.4 KB
- [ ] `docs/_newspapers/前進指揮所主任冷欣中將飛抵京.md` — 3.3 KB
- [ ] `docs/_newspapers/馬歇爾特使昨抵滬.md` — 3.3 KB
- [ ] `docs/_newspapers/總統決暫坐鎮北平.md` — 3.2 KB
- [ ] `docs/_newspapers/中蘇間橫亘小陰影東北局勢低迷沉悶.md` — 3.2 KB
- [ ] `docs/_newspapers/最大規模空運昨開始實現我八萬大軍分運京滬.md` — 3.2 KB

### _newspapers — remaining: 149 to abstract

- [ ] `docs/_newspapers/廖耀湘怀恩报德.md` — 3.2 KB
- [ ] `docs/_newspapers/廖耀湘捐资助学（周后平）.md` — 3.1 KB
- [ ] `docs/_newspapers/湯司令官招待記者談接收京滬工作.md` — 3.1 KB
- [ ] `docs/_newspapers/國軍深入東北平原.md` — 3.0 KB
- [ ] `docs/_newspapers/國軍抵哈巿近郊.md` — 3.0 KB
- [ ] `docs/_newspapers/多英勇事迹.md` — 2.9 KB
- [ ] `docs/_newspapers/東北將星離平返防.md` — 2.9 KB
- [ ] `docs/_newspapers/廖耀湘對記者談話.md` — 2.8 KB
- [ ] `docs/_newspapers/國軍出擊節節推進.md` — 2.8 KB
- [ ] `docs/_newspapers/國軍越雙廟子北進.md` — 2.8 KB
- [ ] `docs/_newspapers/20050820栖霞寺佛门弟子南京大屠杀保护24000百姓.md` — 2.8 KB
- [ ] `docs/_newspapers/熱國軍進入承德.md` — 2.7 KB
- [ ] `docs/_newspapers/陸空配合固守吉長遼北收復昌圖縣城.md` — 2.7 KB
- [ ] `docs/_newspapers/周恩來對東北衝突主張由軍事調處.md` — 2.6 KB
- [ ] `docs/_newspapers/東九省經濟接收工作新六軍行止靜待大局開展.md` — 2.6 KB
- [ ] `docs/_newspapers/肩披麻袋的南方商人 廖耀湘就擒记.md` — 2.6 KB
- [ ] `docs/_newspapers/刧後長春在甦生中.md` — 2.6 KB
- [ ] `docs/_newspapers/哈里曼由渝抵滬魏德邁解答記者問話.md` — 2.6 KB
- [ ] `docs/_newspapers/靑年軍入伍周年觀光雄師受檢.md` — 2.6 KB
- [ ] `docs/_newspapers/檢閱上海地區駐軍白崇禧將軍蒞滬.md` — 2.5 KB
- [ ] `docs/_newspapers/東北蘇軍延緩撤退接收工作仍呈停頓.md` — 2.4 KB
- [ ] `docs/_newspapers/四平會戰有功人員授勳典禮.md` — 2.4 KB
- [ ] `docs/_newspapers/東北將領會議.md` — 2.3 KB
- [ ] `docs/_newspapers/19451014京畿敌械收缴完毕各地散匪即可肃清.md` — 2.3 KB
- [ ] `docs/_newspapers/美國陸軍部長柏德遜昨飛抵滬.md` — 2.3 KB
- [ ] `docs/_newspapers/長春外圍激戰兩日.md` — 2.2 KB
- [ ] `docs/_newspapers/魏特使視察撫順.md` — 2.2 KB
- [ ] `docs/_newspapers/長春蘇軍續撤退.md` — 2.2 KB
- [ ] `docs/_newspapers/國軍正向吉林推進.md` — 2.2 KB
- [ ] `docs/_newspapers/曲靖劳军盛会.md` — 2.1 KB
- [ ] `docs/_newspapers/電話電燈曾中斷國軍正兼程增防.md` — 2.1 KB
- [ ] `docs/_newspapers/何應欽飛抵長春.md` — 2.1 KB
- [ ] `docs/_newspapers/魏德邁謁馬歇爾美考慮協助遣送東北日人.md` — 2.1 KB
- [ ] `docs/_newspapers/國軍沿中長路掃蕩.md` — 2.1 KB
- [ ] `docs/_newspapers/杜长官没有来 廖军长在跳舞.md` — 2.1 KB
- [ ] `docs/_newspapers/新六軍昨開東北靑年軍來滬接防.md` — 2.1 KB
- [ ] `docs/_newspapers/军事史上最大空运：新六军八万健儿飞京（良友画册）.md` — 2.1 KB
- [ ] `docs/_newspapers/新立屯陷入混戰.md` — 2.1 KB
- [ ] `docs/_newspapers/血汗铺成的史迪威路.md` — 2.1 KB
- [ ] `docs/_newspapers/東北行轅開緊急會議.md` — 2.0 KB
- [ ] `docs/_newspapers/本巿軍事首長商決　各軍師辦事處一律取消（无）.md` — 2.0 KB
- [ ] `docs/_newspapers/東北局勢陰霾漸散國軍待接防瀋陽.md` — 1.9 KB
- [ ] `docs/_newspapers/魏特使離瀋陽前曾與陳總長晤談.md` — 1.9 KB
- [ ] `docs/_newspapers/東北大戰又揭開.md` — 1.9 KB
- [ ] `docs/_newspapers/公主嶺戰事激烈.md` — 1.9 KB
- [ ] `docs/_newspapers/忆廖耀湘将军（王新）.md` — 1.9 KB
- [ ] `docs/_newspapers/打開東北現狀方案.md` — 1.9 KB
- [ ] `docs/_newspapers/通辽前日收复.md` — 1.8 KB
- [ ] `docs/_newspapers/本巿軍事首長商決各軍師辦事處一律取消.md` — 1.8 KB
- [ ] `docs/_newspapers/東北戰局之轉捩點.md` — 1.8 KB
- [ ] `docs/_newspapers/美宣布定十六日開始運新六軍赴東北.md` — 1.7 KB
- [ ] `docs/_newspapers/孫立人將軍談東北軍事近况.md` — 1.7 KB
- [ ] `docs/_newspapers/白崇禧在瀋檢軍.md` — 1.7 KB
- [ ] `docs/_newspapers/空運部隊首批抵長春.md` — 1.7 KB
- [ ] `docs/_newspapers/劫后辽阳疮痕满目 百业萧际粮食奇缺 法币两百万元难购高梁米一斤 廖耀湘谈收复辽阳意义.md` — 1.7 KB
- [ ] `docs/_newspapers/私刻廖耀湘印章 一退役军人被拘（工商报）.md` — 1.6 KB
- [ ] `docs/_newspapers/沈开始撤退 北上劲旅克塔山高桥 铁岭新民新立屯易手 杜聿明廖耀湘失联络.md` — 1.6 KB
- [ ] `docs/_newspapers/廖耀湘等由京返沈有重大决定 东北国军将取攻势 承德平泉外围益紧 大凌河白旗堡一带残共开始窜扰.md` — 1.6 KB
- [ ] `docs/_newspapers/接收人員離長返錦.md` — 1.6 KB
- [ ] `docs/_newspapers/将军音息杳 夫人泪沾襟 ——廖耀湘夫人访问记.md` — 1.6 KB
- [ ] `docs/_newspapers/藩錦國軍三面推進.md` — 1.6 KB
- [ ] `docs/_newspapers/杨宏光等脱险抵青 周福成廖耀湘等仍被囚哈埠 郑洞国亦受监禁惟待遇较优.md` — 1.6 KB
- [ ] `docs/_newspapers/鐵嶺形勢險要天成.md` — 1.6 KB
- [ ] `docs/_newspapers/新六軍全部開到後即正式接防瀋陽.md` — 1.5 KB
- [ ] `docs/_newspapers/接收旅大益趨具體中蘇將領舉行會談.md` — 1.5 KB
- [ ] `docs/_newspapers/新六军接防南京中央社通讯三则.md` — 1.5 KB
- [ ] `docs/_newspapers/松花江北劃緩衝地帶.md` — 1.4 KB
- [ ] `docs/_newspapers/新六軍分批空運到京.md` — 1.4 KB
- [ ] `docs/_newspapers/20050814《栖霞寺1937》再现日军屠城铁证.md` — 1.4 KB
- [ ] `docs/_newspapers/廖耀湘检讨四平之战.md` — 1.4 KB
- [ ] `docs/_newspapers/旅大接收尚有待.md` — 1.4 KB
- [ ] `docs/_newspapers/熊式輝由錦飛平新六軍兩隊自秦皇島推進.md` — 1.3 KB
- [ ] `docs/_newspapers/新六軍開往東北携帶法幣出關五千元爲度.md` — 1.3 KB
- [ ] `docs/_newspapers/廖耀湘谈攻沈共军绝难获得进展（中央社）.md` — 1.3 KB
- [ ] `docs/_newspapers/19480309四平战火向南蔓延 铁岭外围酝酿大战 廖耀湘部到达指定地点严阵以待 李弥将调赴东北负责确保北宁路.md` — 1.3 KB
- [ ] `docs/_newspapers/廖耀湘對記者談話共匪計劃全毀滅.md` — 1.3 KB
- [ ] `docs/_newspapers/19480509对东北有办法 蒋主席在官邸会报中表示 赵家骧廖耀湘等昨飞抵平.md` — 1.3 KB
- [ ] `docs/_newspapers/受降後七小時何總司令謁陵.md` — 1.3 KB
- [ ] `docs/_newspapers/我打虎山战役战果：歼敌五个军十二整师 活捉廖耀湘等八万七千多人.md` — 1.2 KB
- [ ] `docs/_newspapers/傳共軍撤離哈市司令部移佳木斯.md` — 1.2 KB
- [ ] `docs/_newspapers/古北口外圍戰况激烈.md` — 1.1 KB
- [ ] `docs/_newspapers/新六軍接防台安遼中廖耀湘即飛錦晤杜聿明.md` — 1.1 KB
- [ ] `docs/_newspapers/共軍中九名日兵經俘獲由瀋解京.md` — 1.1 KB
- [ ] `docs/_newspapers/四平受創戰士抵滬轉蘇療養.md` — 1.1 KB
- [ ] `docs/_newspapers/中蘇第一綫上將領二度晤談.md` — 1.0 KB
- [ ] `docs/_newspapers/19480312廖耀湘部 北上驰援四平 国军云集北宁路关外段.md` — 1.0 KB
- [ ] `docs/_newspapers/祝贺辽南大捷 政委作欢宴作战有功将领 廖耀湘今天举行作战报告(东北公报) copy.md` — 1.0 KB
- [ ] `docs/_newspapers/廖耀湘谈接收大连 认阻力不太大.md` — 1.0 KB
- [ ] `docs/_newspapers/京高院昨整日偵訊周佛海等.md` — 1.0 KB
- [ ] `docs/_newspapers/廖耀湘等电复申谢 湘省端节各项慰劳.md` — 1.0 KB
- [ ] `docs/_newspapers/廖耀湘谈目前东北局势.md` — 0.9 KB
- [ ] `docs/_newspapers/新六軍健兒一營昨晨自芷江到京.md` — 0.9 KB
- [ ] `docs/_newspapers/19480508廖耀湘赵家骧 再谒主席请示军机 东北共匪意图进犯长沈.md` — 0.9 KB
- [ ] `docs/_newspapers/廖军长谈湘西胜利原因.md` — 0.9 KB
- [ ] `docs/_newspapers/靑年軍今日離滬廖耀湘即飛錦.md` — 0.9 KB
- [ ] `docs/_newspapers/東北華北將領在平開聯席會.md` — 0.9 KB
- [ ] `docs/_newspapers/石觉曾泽生等飞平转京受训.md` — 0.9 KB
- [ ] `docs/_newspapers/魏德邁將軍視察巿區.md` — 0.9 KB
- [ ] `docs/_newspapers/孫立人在長就任兩新職.md` — 0.9 KB
- [ ] `docs/_newspapers/裕華軍服廠失愼.md` — 0.9 KB
- [ ] `docs/_newspapers/19460618廖司令关怀哈市民生.md` — 0.8 KB
- [ ] `docs/_newspapers/宋院长处理要公  听取各方报吿 钱市长廖耀湘等先后往谒.md` — 0.8 KB
- [ ] `docs/_newspapers/廖耀湘今日返滬.md` — 0.8 KB
- [ ] `docs/_newspapers/新六军军长兼长春警备.md` — 0.8 KB
- [ ] `docs/_newspapers/芷江慶祝勝利大會盛况.md` — 0.8 KB
- [ ] `docs/_newspapers/新六军长廖耀湘汽车失踪 一军官驶去私自卖出.md` — 0.8 KB
- [ ] `docs/_newspapers/张主委马将军等 今来沈履新 赵家骧廖耀湘等归任.md` — 0.8 KB
- [ ] `docs/_newspapers/魏德邁將軍昨招待記者新六軍即由滬開往東北.md` — 0.7 KB
- [ ] `docs/_newspapers/传廖耀湘 有脱险说.md` — 0.7 KB
- [ ] `docs/_newspapers/廖军长耀湘关怀儿童.md` — 0.7 KB
- [ ] `docs/_newspapers/廖耀湘巴黎得妻.md` — 0.7 KB
- [ ] `docs/_newspapers/207师今日开拔 廖耀湘明日北飞（无）.md` — 0.7 KB
- [ ] `docs/_newspapers/廖耀湘分析东北战局（中央社）.md` — 0.7 KB
- [ ] `docs/_newspapers/各界迎送國軍.md` — 0.7 KB
- [ ] `docs/_newspapers/张作相马占山 将联袂返东北 廖耀湘等返东北.md` — 0.7 KB
- [ ] `docs/_newspapers/廖耀湘视察辽南 在普兰店饱受民众欢迎.md` — 0.7 KB
- [ ] `docs/_newspapers/孫連仲抵瀋.md` — 0.7 KB
- [ ] `docs/_newspapers/鄭洞國返瀋飛平陳繼承視察唐山.md` — 0.6 KB
- [ ] `docs/_newspapers/新六軍調防昨晨北上.md` — 0.6 KB
- [ ] `docs/_newspapers/廖耀湘等抵瀋陽.md` — 0.6 KB
- [ ] `docs/_newspapers/吴瀚涛昨表示 廖耀湘确被俘 流亡省府结束问题 王铁汉等交换意见.md` — 0.6 KB
- [ ] `docs/_newspapers/东北剿匪总部扩大 行辕大部人员均转入 沈防守司令廖耀湘代（西湖日报）.md` — 0.6 KB
- [ ] `docs/_newspapers/廖耀湘沪寓 汽车被人盗卖（新闻报）.md` — 0.6 KB
- [ ] `docs/_newspapers/宋院長處理要公聽取各方報吿錢市長廖耀湘等先後往謁.md` — 0.6 KB
- [ ] `docs/_newspapers/鄭洞國返瀋.md` — 0.6 KB
- [ ] `docs/_newspapers/新六軍一師長李濤被俘說係謠傳.md` — 0.6 KB
- [ ] `docs/_newspapers/第二批新六軍昨日北運.md` — 0.6 KB
- [ ] `docs/_newspapers/慰勞新六軍.md` — 0.5 KB
- [ ] `docs/_newspapers/辽西战役中国民党大将廖耀湘被活捉（淮海报）.md` — 0.5 KB
- [ ] `docs/_newspapers/軍之友社舉行軍友聯歡大會.md` — 0.5 KB
- [ ] `docs/_newspapers/廖耀湘飞平 昨邀报界宴别.md` — 0.5 KB
- [ ] `docs/_newspapers/张作相马占山赵家骧 今日联袂飞沈 王铁汉董彦平廖耀湘罗右伦偕行.md` — 0.5 KB
- [ ] `docs/_newspapers/銅圖說明廖耀湘白魯德鄭洞國合影.md` — 0.5 KB
- [ ] `docs/_newspapers/廖耀湘将兼军粮局局长.md` — 0.5 KB
- [ ] `docs/_newspapers/新六軍續運抵京.md` — 0.5 KB
- [ ] `docs/_newspapers/赵家骧廖耀湘 飞平晤傅作义 宋子文抵沪将转京.md` — 0.5 KB
- [ ] `docs/_newspapers/京市民代表謁何總司令獻旗致敬.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘（国华报）.md` — 0.4 KB
- [ ] `docs/_newspapers/關麟徵在瀋.md` — 0.4 KB
- [ ] `docs/_newspapers/新六軍兩團登陸秦皇島.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘在長閱兵.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘阅兵 市民争先出睹.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘获美勋章.md` — 0.4 KB
- [ ] `docs/_newspapers/瀋陽防守司令官將由廖耀湘繼任.md` — 0.4 KB
- [ ] `docs/_newspapers/新六軍在京布防受熱烈歡迎.md` — 0.4 KB
- [ ] `docs/_newspapers/長春巿民慰勞國軍大會.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘飛京.md` — 0.4 KB
- [ ] `docs/_newspapers/廖耀湘等就職.md` — 0.4 KB
- [ ] `docs/_newspapers/沈阳防守司令官 将由廖耀湘继任（新生报）.md` — 0.4 KB

### _liaos_tele — 30 largest transcribed (all 30 to abstract)

- [ ] `docs/_liaos_tele/1937-12-31南京保卫战战斗详报.md` — 17.8 KB
- [ ] `docs/_liaos_tele/1942-03-06蒋委员长在重庆接见中国战区参谋长史迪威听其报告来华所负之任务及美方对印、缅军事部署之一般情况谈话记录.md` — 12.8 KB
- [ ] `docs/_liaos_tele/1948-11-08林彪、罗荣桓、刘亚楼、谭政关于九、十两月作战总结致毛泽东等电.md` — 11.9 KB
- [ ] `docs/_liaos_tele/1943-04-01军令部编《缅战概要稿》.md` — 11.5 KB
- [ ] `docs/_liaos_tele/1942-06-15蒋委员长在重庆接见中国战区参谋长史迪威商谈关于如何安顿我国在印军队、组织中国战区参谋本部、中印空航、中国战区组织空军之计划与恢复缅甸等问题谈话记录.md` — 10.7 KB
- [ ] `docs/_liaos_tele/1942-04-01蒋委员长在重庆接见中国战区参谋长史迪威听其报告我军在缅甸作战情况及讨论改编美国空军志愿队等问题谈话记录.md` — 10.0 KB
- [ ] `docs/_liaos_tele/1942-03-10蒋委员长在重庆接见中国战区参谋长史迪威告知其赴缅应注意之给养、联络参谋等问题谈话记录.md` — 9.5 KB
- [ ] `docs/_liaos_tele/1942-03-19蒋委员长在重庆接见中国战区参谋长史迪威讨论缅甸作战方针及统一指挥等问题谈话记录.md` — 8.0 KB
- [ ] `docs/_liaos_tele/1942-06-24蒋委员长在重庆接见中国战区参谋长史迪威商谈关于组织中国战区参谋本部及拟具中国战区整个作战计划等问题谈话记录.md` — 6.9 KB
- [ ] `docs/_liaos_tele/1940-02-19苏联军事顾问加略诺夫关于昆仑关宾阳等役战斗经过及经验教训的报告.md` — 6.6 KB
- [ ] `docs/_liaos_tele/1942-04-02蒋委员长在重庆接见中国战区参谋长史迪威讨论派罗卓英指挥在缅作战之军队及调英游击队入缅作战等问题谈话记录.md` — 5.4 KB
- [ ] `docs/_liaos_tele/1948-10-20林彪、罗荣桓、刘亚楼关于围歼廖耀湘兵团部署致各纵队等电.md` — 5.4 KB
- [ ] `docs/_liaos_tele/1942-03-14林蔚电何应钦徐永昌200师位于同古N22D与96D位于芒市暂不移动及其他军情.md` — 5.3 KB
- [ ] `docs/_liaos_tele/1944-03-01美国驻中缅印军总部请即调一师赴印备忘录及军令部拟复签呈稿.md` — 5.3 KB
- [ ] `docs/_liaos_tele/1942-03-31肖（萧）毅肃致何应钦徐永昌3月28日至4月1日战况.md` — 5.2 KB
- [ ] `docs/_liaos_tele/1948-10-17中央军委关于下一步宜打锦西、葫芦岛致林彪、罗荣桓、刘亚楼、谭政等电.md` — 4.5 KB
- [ ] `docs/_liaos_tele/1942-03-26萧毅肃致何应钦徐永昌同古200师激战新22师加速输送中.md` — 4.4 KB
- [ ] `docs/_liaos_tele/1937-04-29蒋方震等电蒋中正请准拨予旅费俾利史丹发尼赴各驻区视察指导等文电日报表等二则.md` — 4.3 KB
- [ ] `docs/_liaos_tele/1942-03-20蒋委员长在重庆接见中国战区参谋长史迪威讨论缅甸作战统一指挥等问题谈话记录.md` — 4.3 KB
- [ ] `docs/_liaos_tele/1940-01-24白崇禧关于昆仑关龙州等役战斗经过概要代电.md` — 4.2 KB
- [ ] `docs/_liaos_tele/1948-12-01叶锟呈蒋中正辽西战役概要.md` — 4.1 KB
- [ ] `docs/_liaos_tele/1937-12-31第三战区南京会战经过概要.md` — 3.8 KB
- [ ] `docs/_liaos_tele/1951-04-04蒋中正电蒋经国研究保密局报称廖耀湘被俘后攻讦总统任用私人同乡及四大家族把持中国政治等事之对策以驳斥其攻讦.md` — 3.7 KB
- [ ] `docs/_liaos_tele/1948-04-11廖耀湘电呈国民政府主席蒋中正为愿亲往南京面报东北军情.md` — 3.2 KB
- [ ] `docs/_liaos_tele/1948-10-10中央军委关于尽快攻克锦州致林彪、罗荣桓、刘亚楼电.md` — 3.1 KB
- [ ] `docs/_liaos_tele/1939-10-17戴笠呈蒋中正考察驻外武官人选拟荐新廿二师副师长廖耀湘为驻法武官.md` — 2.9 KB
- [ ] `docs/_liaos_tele/1948-10-20中央军委关于全歼廖耀湘兵团致林彪、罗荣桓、刘亚楼电.md` — 2.9 KB
- [ ] `docs/_liaos_tele/1945-04-14何应钦致蒋介石拟第四方面军及王敬久集团协同作战要领.md` — 2.9 KB
- [ ] `docs/_liaos_tele/1942-03-11蒋委员长在重庆接见中国战区参谋长史迪威讨论缅甸总部组织之规划及在缅之指挥权等问题谈话记录.md` — 2.8 KB
- [ ] `docs/_liaos_tele/1942-03-24杜聿明三月二十四日函呈报告入缅情形.md` — 2.7 KB

Remaining transcribed telegrams: 153 files, 192 KB total. A further 169 telegram files are 待录入 stubs with no body text.

