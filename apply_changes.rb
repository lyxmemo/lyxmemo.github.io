require 'yaml'
require 'date'

# Read original
content = File.read("docs/_data/chronology.yml")
data = YAML.safe_load(content, permitted_classes: [Date])

# Helper to find year
def find_year(data, y)
  data.find { |yd| yd["year"] == y }
end

# Helper to make entry
def make_entry(date, content, source: "", source_url: "", date_display: "", original_text: "", notes: "")
  {
    "date" => date,
    "date_display" => date_display,
    "content" => content,
    "source" => source,
    "source_url" => source_url,
    "original_text" => original_text,
    "notes" => notes
  }
end

# Helper to find entry by date and content substring
def find_entry(entries, date, content_sub = nil)
  entries.each_with_index do |e, i|
    next unless e["date"].to_s == date
    if content_sub.nil? || e["content"].to_s.include?(content_sub)
      return [e, i]
    end
  end
  nil
end

### 1945 changes ###
y1945 = find_year(data, 1945)
es = y1945["entries"]

# Add 1945-08-27 entry
es << make_entry("1945-08-27",
  "新六军副军长舒适存随冷欣中将率前进指挥所一行159人乘七架美军运输机由芷江飞抵南京，新六军被指定接收南京防区。新六军官兵52人随行先遣。",
  source: "申报 1945年08月28日 第1版 第25650期",
  source_url: "/newspapers/前進指揮所主任冷欣中將飛抵京.html")

# Update 1945-09-04 (空运南京) source_url
e, _ = find_entry(es, "1945-09-04", "新六军开始空运南京")
if e
  e["source_url"] = "/newspapers/新六軍健兒一營昨晨自芷江到京.html"
end

# Update 1945-09-04 (芷江庆祝) source_url
e, _ = find_entry(es, "1945-09-04", "芷江各界")
if e
  e["source_url"] = "/newspapers/芷江慶祝勝利大會盛况.html"
end

# Add 1945-09-06
es << make_entry("1945-09-06",
  "美军开始大规模空运八万中国军队至京沪，为军事史上最大规模空运之一。新六军由美第十航空隊自芷江空运南京，往返飞行距离1300英里，预计四十日完成。",
  source: "申报 1945年09月07日 第1版 第25660期",
  source_url: "/newspapers/最大規模空運昨開始實現我八萬大軍分運京滬.html")

# Add 1945-09-07
es << make_entry("1945-09-07",
  "廖耀湘偕十四师师长龙天武等飞抵南京，新六军军司令部设于黄埔路。先遣部队已于6日接收光华门外防务，后续部队自8日起加紧空运。",
  source: "申报 1945年09月09日 第1版 第25662期",
  source_url: "/newspapers/新六軍分批空運到京.html")

# Update 1945-09-09 (谒陵合影)
e, _ = find_entry(es, "1945-09-09", "谒陵")
if e
  e["content"] = "受降签字后七小时，何应钦率陆海军将校约八十人谒陵，廖耀湘随行，舒适存、龙天武分率新六军战士乘车前导。"
  e["source"] = "中缅印战区盟军将帅图志P252; 申报 1945年09月10日 第1版 第25663期"
  e["source_url"] = "/newspapers/受降後七小時何總司令謁陵.html"
end

# Add 1945-09-13
es << make_entry("1945-09-13",
  "新六军开始在南京城郊布防，备受市民热烈欢迎。",
  source: "申报 1945年09月14日 第1版 第25667期",
  source_url: "/newspapers/新六軍在京布防受熱烈歡迎.html")

# Add 1945-09-14
es << make_entry("1945-09-14",
  "南京全体商民推派代表向何应钦献旗致敬，并备大批慰劳物品慰劳总部将士及新六军。",
  source: "申报 1945年09月15日 第1版 第25668期",
  source_url: "/newspapers/京市民代表謁何總司令獻旗致敬.html")

# Add 1945-09-15
es << make_entry("1945-09-15",
  "新六军空运部队到达者骤增，南京警卫除挹江门一隅外均已由新六军接收把守。",
  source: "申报 1945年09月16日 第1版 第25669期",
  source_url: "/newspapers/新六軍續運抵京.html")

# Add 1945-11-26 (慰劳)
es << make_entry("1945-11-26",
  "中华口琴会会长王庆勋率代表队赴新六军第十四师慰劳演奏，龙天武师长简述该师作战经过。",
  source: "申报 1945年11月27日 第3版 第24343期",
  source_url: "/newspapers/慰勞新六軍.html")

# Update 1945-11-25 source_url
e, _ = find_entry(es, "1945-11-25", "苏州视察")
if e
  e["source_url"] = "/newspapers/廖耀湘今日返滬.html"
end

# Update 1945-12-20 source_url
e, _ = find_entry(es, "1945-12-20", "马歇尔")
if e
  e["source_url"] = "/newspapers/馬歇爾特使昨抵滬.html"
end

# Add 1945-12-26
es << make_entry("1945-12-26",
  "新六军副军长舒适存抵达北平，全副美式装备之新六军士兵初次出现北平街头。",
  source: "申报 1945年12月31日 第1版 第24377期",
  source_url: "/newspapers/中蘇間橫亘小陰影東北局勢低迷沉悶.html")

### 1946 changes ###
y1946 = find_year(data, 1946)
es6 = y1946["entries"]

# Update 1946-01-02
e, _ = find_entry(es6, "1946-01-02")
if e
  e["content"] = "廖耀湘、龙天武、李澍等出席淞沪军事长官会商，商定六项办法整肃军纪，取消各军师办事处，不得占用民房。"
  e["source"] = "申报 1946年01月03日 第3版 第24380期"
  e["source_url"] = "/newspapers/本巿軍事首長商決各軍師辦事處一律取消.html"
end

# Add 1946-01-09 (东北前线)
es6 << make_entry("1946-01-09",
  "东北前线国军士兵冬服仍未齐备，多手脚冻坏，报道称俟最精锐之新一军新六军等到达后，前线始可稍息仔肩。",
  source: "申报 1946年01月11日 第1版 第24388期",
  source_url: "/newspapers/東北局勢陰霾漸散國軍待接防瀋陽.html")

# Add 1946-01-11
es6 << make_entry("1946-01-11",
  "美军总部宣布：美军船只运输新六军由上海赴东北将于本月16日开始，御寒配备已整筹就绪，并已注射防疫针。",
  source: "申报 1946年01月12日 第1版 第24389期",
  source_url: "/newspapers/美宣布定十六日開始運新六軍赴東北.html")

# Add 1946-01-12
es6 << make_entry("1946-01-12",
  "魏德迈将军招待记者时宣布：新六军将于本月16日开始自沪运往东北，北上者共二万六千人，并备有御寒配备。",
  source: "申报 1946年01月13日 第5版 第24390期",
  source_url: "/newspapers/魏德邁將軍昨招待記者新六軍即由滬開往東北.html")

# Add 1946-01-14
es6 << make_entry("1946-01-14",
  "美陆军部长柏德遜抵沪，检阅新六军派往机场之仪仗队。",
  source: "申报 1946年01月15日 第5版 第24392期",
  source_url: "/newspapers/美國陸軍部長柏德遜昨飛抵滬.html")

# Add 1946-01-16
es6 << make_entry("1946-01-16",
  "新六军开始由上海海运赴东北，上海防务由青年军207师接替。",
  source: "申报 1946年01月17日 第5版 第24394期",
  source_url: "/newspapers/新六軍昨開東北靑年軍來滬接防.html")

# Add 1946-01-17 (军服厂)
es6 << make_entry("1946-01-17",
  "裕鞏军服厂因赶制新六军军服棉被手套失火，焚去楼房十二幢，损失棉被千余条、军服七千余件。",
  source: "申报 1946年01月18日 第5版 第24395期",
  source_url: "/newspapers/裕華軍服廠失愼.html")

# Add 1946-01-17 (二十二师)
es6 << make_entry("1946-01-17",
  "新六军二十二师六千人乘美登陆船六艘由上海启程北上，拟直驶葫芦岛登陆续向沈阳推进。全军官兵二万六千人可于本月22日前后全体首途。",
  source: "申报 1946年01月18日 第5版 第24395期; 申报 1946年01月18日 第1版 第24395期",
  source_url: "/newspapers/新六軍開往東北携帶法幣出關五千元爲度.html")

# Update 1946-01-20 -> 1946-01-19 (白崇禧)
e, _ = find_entry(es6, "1946-01-20")
if e && e["original_text"].to_s.include?("白崇禧")
  e["date"] = "1946-01-19"
  e["content"] = "白崇禧抵沪检阅新六军及青年军207师，廖耀湘陪同白崇禧于虹口公园检阅部队并训话。"
  e["source"] = "申报 1946年01月20日 第5版 第24397期"
  e["source_url"] = "/newspapers/檢閱上海地區駐軍白崇禧將軍蒞滬.html"
end

# Add 1946-01-22
es6 << make_entry("1946-01-22",
  "十四师师长龙天武招待新闻记者，十四师首批五千余人已上船，分三批开赴东北。二十二师已于16至19日分两批出发并已抵达目的地。",
  source: "申报 1946年01月23日 第4版 第24400期",
  source_url: "/newspapers/新六軍十四師健兒分三批開東北.html")

# Update 1946-01-26
e, _ = find_entry(es6, "1946-01-26")
if e
  e["content"] = "沪市各界于大光明戏院举行欢送新六军、迎接青年军207师盛会，大会代表向廖耀湘献赠「党国干城」锦旗，廖军长致词。"
  e["source"] = "南京晚報 1946.01.25 第1版; 申报 1946年01月27日 第4版 第24404期"
  e["source_url"] = "/newspapers/各界迎送國軍.html"
end

# Update 1946-02-10 source_url
e, _ = find_entry(es6, "1946-02-10", "207师今日开拔")
if e
  e["source_url"] = "/newspapers/靑年軍今日離滬廖耀湘即飛錦.html"
end

### Now sort entries within each year and clear original_text where source_url exists ###
data.each do |yd|
  entries = yd["entries"]

  # Clear original_text where source_url is non-empty
  entries.each do |e|
    if e["source_url"].to_s.length > 0 && e["original_text"].to_s.length > 0
      e["original_text"] = ""
    end
  end

  # Stable sort entries by date
  entries.each_with_index { |e, i| e["_orig_idx"] = i }
  entries.sort_by! do |e|
    d = e["date"].to_s
    sort_key = case d.length
    when 0 then "9999-99-99"  # undated entries go to end
    when 4 then "#{d}-00-00"
    when 7 then "#{d}-00"
    else d
    end
    [sort_key, e["_orig_idx"]]
  end
  entries.each { |e| e.delete("_orig_idx") }
end

### Write back preserving original format ###
lines = []
data.each do |yd|
  lines << "- year: #{yd["year"]}"
  lines << "  entries:"
  yd["entries"].each do |e|
    lines << "    - date: \"#{e["date"]}\""
    lines << "      date_display: \"#{e["date_display"]}\""
    # Content may contain special chars - use double quotes with escaping
    content_val = e["content"].to_s.gsub('"', '\\"')
    lines << "      content: \"#{content_val}\""
    source_val = e["source"].to_s.gsub('"', '\\"')
    lines << "      source: \"#{source_val}\""
    lines << "      source_url: \"#{e["source_url"]}\""
    ot = e["original_text"].to_s
    if ot.length > 0 && !ot.include?('"')
      lines << "      original_text: \"#{ot}\""
    elsif ot.length > 0
      # Use single quotes or escape
      lines << "      original_text: \"#{ot.gsub('"', '\\"')}\""
    else
      lines << "      original_text: \"\""
    end
    notes_val = e["notes"].to_s.gsub('"', '\\"')
    lines << "      notes: \"#{notes_val}\""
  end
end

File.write("docs/_data/chronology.yml", lines.join("\n") + "\n")
puts "All changes applied, sorted, and original_text cleared where links exist."
require 'yaml'
require 'date'

data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date])

def find_year(data, y)
  data.find { |yd| yd["year"] == y }
end

def make_entry(date, content, source: "", source_url: "", date_display: "", original_text: "", notes: "")
  {
    "date" => date,
    "date_display" => date_display,
    "content" => content,
    "source" => source,
    "source_url" => source_url,
    "original_text" => original_text,
    "notes" => notes
  }
end

### 1945 changes ###
y1945 = find_year(data, 1945)
es = y1945["entries"]

# UPDATE 1945-09-09 受降签字 entry (NOT the 谒陵 one) - add 何应钦 report details + 2 sources
es.each do |e|
  if e["date"].to_s == "1945-09-09" && e["content"].to_s.include?("受降签字仪式") && !e["content"].to_s.include?("谒陵")
    e["content"] = "受降签字仪式在南京举行，参加观礼。据何应钦事后报告，受降时南京仅运到新六军五个连，当时城区敌军约七万、伪军一万余。黄埔路上满布空运抵此之宪兵及新六军担任警戒，安保工作全由新6军第14师40团担任。"
    e["source"] = "申报 1945年09月10日 第1版 第25663期; 申报 1946年05月14日 第2版 第24511期"
    e["source_url"] = "/newspapers/中國日軍投降簽字昨在京順利完成.html; /newspapers/何總司令報吿執行任務情形.html"
    puts "Updated 1945-09-09 受降签字"
    break
  end
end

# ADD 1945-09-14 汤恩伯招待记者
es << make_entry("1945-09-14",
  "第三方面军汤恩伯在沪招待记者，称接收南京之工作已委派新六军廖军长代表处理。",
  source: "申报 1945年09月15日 第1版 第25668期",
  source_url: "/newspapers/湯司令官招待記者談接收京滬工作.html")
puts "Added 1945-09-14 汤恩伯"

# UPDATE 1945-12-20 马歇尔 - expand to 4 sources, 2 URLs
es.each do |e|
  if e["date"].to_s == "1945-12-20" && e["content"].to_s.include?("马歇尔")
    e["source"] = "申报 1945年12月21日 第1版; 申报 1945年12月21日 第5版; 建國日報 1945.12.21; 民國日報 1945.12.21"
    e["source_url"] = "/newspapers/馬歇爾特使昨抵滬.html; /newspapers/歡迎馬帥速寫.html"
    puts "Updated 1945-12-20 马歇尔 sources"
    break
  end
end

### 1946 changes ###
y1946 = find_year(data, 1946)
es6 = y1946["entries"]

# UPDATE 1946-01-09 empty entry (宋子文) - fill content
es6.each do |e|
  if e["date"].to_s == "1946-01-09" && e["content"].to_s.empty?
    e["content"] = "廖耀湘往谒行政院长宋子文，宋氏当日接见钱市长、廖耀湘及申新纺织厂荣鸿元等，听取各方报告。"
    e["source"] = "申报 1946年01月10日 第5版 第24387期"
    e["source_url"] = "/newspapers/宋院長處理要公聽取各方報吿錢市長廖耀湘等先後往謁.html"
    e["original_text"] = ""
    puts "Updated 1946-01-09 宋子文"
    break
  end
end

# ADD 1946-01-19 秦皇岛登陆
es6 << make_entry("1946-01-19",
  "新六军首批约两团在秦皇岛登陆，即转车径赴新民。",
  source: "申报 1946年01月21日 第1版 第24398期",
  source_url: "/newspapers/新六軍兩團登陸秦皇島.html")
puts "Added 1946-01-19 秦皇岛"

# ADD 1946-01-20 第二批新六军北运
es6 << make_entry("1946-01-20",
  "第二批新六军由上海北运开始，美军以登陆船六艘运载约六千人及配备车辆，登陆葫芦岛。全军二万六千人共分数次北上，第一次始于16日。",
  source: "申报 1946年01月21日 第5版 第24398期",
  source_url: "/newspapers/第二批新六軍昨日北運.html")
puts "Added 1946-01-20 第二批"

# ADD 1946-01-26 新六军全部开到
es6 << make_entry("1946-01-26",
  "新六军已有二师抵达秦皇岛，一师尚在途中。沈阳国军仍住于营房中，俟新六军全部开到后始正式接防。新民、彰武两地苏军当日上午十时全部撤退。",
  source: "申报 1946年01月27日 第1版 第24404期",
  source_url: "/newspapers/新六軍全部開到後即正式接防瀋陽.html")
puts "Added 1946-01-26 新六军全部开到"

# ADD 1946-01-28 新六军先遣部队
es6 << make_entry("1946-01-28",
  "新六军先遣部队两队已在秦皇岛登陆，正向锦州移动中。沈阳尚未正式接防，入夜沈市仍无行人。",
  source: "申报 1946年01月29日 第1版 第24406期",
  source_url: "/newspapers/熊式輝由錦飛平新六軍兩隊自秦皇島推進.html")
puts "Added 1946-01-28 先遣部队"

# ADD 1946-02-01 军之友社
es6 << make_entry("1946-02-01",
  "军之友社在沪举行联欢大会，欢迎魏德迈就任名誉理事及青年军207师师长罗又伦来沪，同时欢送廖耀湘北上。",
  source: "申报 1946年02月01日 第4版 第24409期",
  source_url: "/newspapers/軍之友社舉行軍友聯歡大會.html")
puts "Added 1946-02-01 军之友社"

# UPDATE 1946-02-02 -> 1946-02-01 date correction (魏德迈视察)
es6.each do |e|
  if e["original_text"].to_s.include?("魏德邁將軍")
    e["date"] = "1946-02-01"
    e["content"] = "廖耀湘陪同魏德迈视察上海各地，巡视美军需处、美海防司令部及虬江码头。新六军第三批约五千人由登陆舰六艘北上，至此已运北上者达万人左右。廖耀湘预定四五日内乘机北上。"
    e["source"] = "申报 1946年02月02日 第3版 第24410期"
    e["source_url"] = "/newspapers/魏德邁將軍視察巿區.html"
    e["original_text"] = ""
    puts "Updated 1946-02-02->02-01 魏德迈视察"
    break
  end
end

# ADD 1946-02-02 新六军已全部登陆
es6 << make_entry("1946-02-02",
  "新六军已全部登陆完毕，正向沟帮子挺进中，不日或可入驻沈长。苏军撤退延缓，东北接收工作呈停顿状态。",
  source: "申报 1946年02月04日 第1版 第24412期",
  source_url: "/newspapers/東北蘇軍延緩撤退接收工作仍呈停頓.html")
puts "Added 1946-02-02 全部登陆"

# UPDATE 1946-02-04 青年军入伍周年
es6.each do |e|
  if e["date"].to_s == "1946-02-04" && e["original_text"].to_s.include?("靑年軍入伍周年")
    e["content"] = "青年军207师入伍一周年，在中正公园举行阅兵典礼，廖耀湘陪同钱大钧、罗又伦等检阅部队并致词。"
    e["source"] = "申报 1946年02月05日 第3版 第24413期"
    e["source_url"] = "/newspapers/靑年軍入伍周年觀光雄師受檢.html"
    e["original_text"] = ""
    puts "Updated 1946-02-04 青年军入伍周年"
    break
  end
end

# ADD 1946-02-04 新六军进至沟帮子
es6 << make_entry("1946-02-04",
  "新六军进至沟帮子、新民后已暂停前进，静待大局开展。东北中共军队约三四十万，苏军撤退延期，局势混沌。",
  source: "申报 1946年02月06日 第1版 第24414期",
  source_url: "/newspapers/東九省經濟接收工作新六軍行止靜待大局開展.html")
puts "Added 1946-02-04 沟帮子"

# UPDATE 1946-02-12 extend content + add second source
es6.each do |e|
  if e["date"].to_s == "1946-02-12" && e["content"].to_s.include?("李宗仁")
    e["content"] = "晨偕东北长官部留守处长李诚毅，分谒东北行营主任熊式辉、北平行营主任李宗仁、第十一战区长官孙xx（连仲？）。并嘱记者前往秦皇岛拍摄新六军罗又伦207师登陆影。新六军二十二师接防盘山后续开入台安、辽中两县接防；207师乘美运输舰八艘由沪抵秦皇岛。"
    e["source"] = "華北日報 1946.02.13; 申报 1946年02月16日 第1版 第24424期"
    e["source_url"] = "https://gpa.eastview.com/crl/lqrcn/newspapers/hbrb19460213-01.1.1; /newspapers/新六軍接防台安遼中廖耀湘即飛錦晤杜聿明.html"
    puts "Updated 1946-02-12 extended content"
    break
  end
end

# ADD 1946-02-13 207师开入锦州
es6 << make_entry("1946-02-13",
  "207师开入锦州，因杜聿明卧病，由参谋长赵家骧代表阅兵。",
  source: "申报 1946年02月16日 第1版 第24424期",
  source_url: "/newspapers/新六軍接防台安遼中廖耀湘即飛錦晤杜聿明.html")
puts "Added 1946-02-13 207师"

# UPDATE 1946-02-14 + DELETE duplicate
es6.each do |e|
  if e["date"].to_s == "1946-02-14" && e["content"].to_s.include?("李宗仁")
    e["content"] = "廖耀湘抵达北平，稍事联络即将飞锦晤杜聿明。杜氏卧病，已有三名大夫同机飞锦医疗。据悉新六军已至沈阳西方九十华里处。"
    e["source"] = "時事新報 1946.02.15; 申报 1946年02月16日 第1版 第24424期"
    e["source_url"] = "https://gpa.eastview.com/crl/lqrcn/newspapers/ssxb19460215-01.1.1; /newspapers/新六軍接防台安遼中廖耀湘即飛錦晤杜聿明.html"
    puts "Updated 1946-02-14 content"
    break
  end
end
# Delete duplicate 1946-02-14 with empty content
before = es6.length
es6.reject! do |e|
  e["date"].to_s == "1946-02-14" && e["content"].to_s.empty? && e["original_text"].to_s.length > 0
end
puts "Deleted #{before - es6.length} duplicate 1946-02-14 entry" if before != es6.length

# UPDATE 1946-06-21 白鲁德合影
es6.each do |e|
  if e["date"].to_s == "1946-06-21" && (e["content"].to_s.include?("白魯德") || e["content"].to_s.include?("白鲁德"))
    e["content"] = "军事调处执行部东北前进小组美代表白鲁德将军抵长春与东北军事当局合影。自右至左：廖耀湘，白鲁德，郑洞国，关邦杰，尚传道。"
    e["source"] = "申报 1946年06月21日 第1版 第24549期"
    e["source_url"] = "/newspapers/銅圖說明廖耀湘白魯德鄭洞國合影.html"
    e["original_text"] = ""
    puts "Updated 1946-06-21 白鲁德"
    break
  end
end

# UPDATE 1946-06-22 慰劳国军
es6.each do |e|
  if e["date"].to_s == "1946-06-22" && (e["content"].to_s.include?("慰勞") || e["content"].to_s.include?("慰劳"))
    e["content"] = "长春市民举行慰劳国军大会，郑洞国、廖耀湘接受献花。"
    e["source"] = "申报 1946年06月22日 第1版 第24550期"
    e["source_url"] = "/newspapers/長春巿民慰勞國軍大會.html"
    e["original_text"] = ""
    puts "Updated 1946-06-22 慰劳国军"
    break
  end
end

# UPDATE 1946-05-28 source_url (may already be done by apply_changes.rb, but ensure)
es6.each do |e|
  if e["date"].to_s == "1946-05-28" && e["content"].to_s.include?("警备司令廖耀湘")
    e["source_url"] = "/newspapers/刧後長春在甦生中.html"
    e["original_text"] = ""
    puts "Ensured 1946-05-28 source_url"
    break
  end
end

### 1947 changes ###
y1947 = find_year(data, 1947)
es7 = y1947["entries"]

# UPDATE 1947-04-06 旅大接收
es7.each do |e|
  if e["original_text"].to_s.include?("旅大接收") || (e["date"].to_s == "1947-04-06" && e["content"].to_s.empty?)
    e["content"] = "普兰店中苏第一线将领会谈，为接收旅大先声。廖耀湘定当夜由鞍山赴沈阳，报告会谈情形。苏方允我先接收洼子店。"
    e["source"] = "申报 1947年04月07日 第2版 第24834期"
    e["source_url"] = "/newspapers/接收旅大益趨具體中蘇將領舉行會談.html"
    e["original_text"] = ""
    puts "Updated 1947-04-06 旅大接收"
    break
  end
end

### Sort and clear original_text where source_url exists ###
data.each do |yd|
  entries = yd["entries"]
  entries.each do |e|
    if e["source_url"].to_s.length > 0 && e["original_text"].to_s.length > 0
      e["original_text"] = ""
    end
  end
  entries.each_with_index { |e, i| e["_orig_idx"] = i }
  entries.sort_by! do |e|
    d = e["date"].to_s
    sort_key = case d.length
    when 0 then "9999-99-99"
    when 4 then "#{d}-00-00"
    when 7 then "#{d}-00"
    else d
    end
    [sort_key, e["_orig_idx"]]
  end
  entries.each { |e| e.delete("_orig_idx") }
end

### Write back preserving format ###
lines = []
data.each do |yd|
  lines << "- year: #{yd["year"]}"
  lines << "  entries:"
  yd["entries"].each do |e|
    lines << "    - date: \"#{e["date"]}\""
    lines << "      date_display: \"#{e["date_display"]}\""
    content_val = e["content"].to_s.gsub('"', '\\"')
    lines << "      content: \"#{content_val}\""
    source_val = e["source"].to_s.gsub('"', '\\"')
    lines << "      source: \"#{source_val}\""
    lines << "      source_url: \"#{e["source_url"]}\""
    ot = e["original_text"].to_s
    if ot.length > 0
      lines << "      original_text: \"#{ot.gsub('"', '\\"')}\""
    else
      lines << "      original_text: \"\""
    end
    notes_val = e["notes"].to_s.gsub('"', '\\"')
    lines << "      notes: \"#{notes_val}\""
  end
end

File.write("docs/_data/chronology.yml", lines.join("\n") + "\n")
puts "\nAll session changes applied successfully."
