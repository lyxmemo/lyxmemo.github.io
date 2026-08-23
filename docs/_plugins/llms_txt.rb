# Write /llms.txt at build time: a markdown catalog of English abstracts
# so LLM crawlers can ingest the archive without parsing Chinese originals.

Jekyll::Hooks.register :site, :post_write do |site|
  writings = site.collections['liaos_writings']&.docs || []
  writings = writings.sort_by do |d|
    [d.data['date'] || Time.utc(1900, 1, 1), d.data['title_en'] || d.data['title'] || '']
  end

  lines = []
  lines << '# Liao Yaoxiang Archive'
  lines << ''
  lines << '> Digital archive of primary sources on General Liao Yaoxiang (廖耀湘, 1906–1968), commander of the New 22nd Division and New Sixth Army in the Chinese Army in India, and later of the Nationalist Ninth Army Group in Manchuria.'
  lines << ''
  lines << 'Original documents are in Chinese. English essay abstracts and keyword lists are provided on each writings page and listed here for researchers, search engines, and language models.'
  lines << ''
  lines << 'Name variants: Liao Yaoxiang, 廖耀湘, Liao Yao-hsiang (Wade-Giles), Liao Yao-siang, style name Jianchu 建楚. Subject keywords across the archive: Second Sino-Japanese War 抗日战争, Chinese Expeditionary Force 中国远征军, Chinese Army in India 中国驻印军 (X Force), Burma campaigns 缅甸战役 1942 and 1944-1945 (Hukawng Valley, Maingkwan, Walawbum, Kamaing, Mogaung, Myitkyina, Bhamo, Ledo Road), New 22nd Division 新编第二十二师, New Sixth Army 新六军, Fifth Army 第五军, Ninth Army Group 第九兵团, Chinese Civil War in Manchuria 东北 1946-1948 (Siping, Faku, Jinzhou, Heishan, Liaoxi, Liaoshen campaign), Chiang Kai-shek 蒋介石, Joseph Stilwell 史迪威, Du Yuming 杜聿明, Wei Lihuang 卫立煌, Sun Liren 孙立人, Dai Anlan 戴安澜, Wenshi Ziliao 文史资料 memoirs, Cultural Revolution 文化大革命.'
  lines << ''
  lines << "- Site: #{site.config['url']}"
  lines << '- English abstracts index: https://liaoyaoxiang.com/en/liaos-writings/'
  lines << '- Source: https://github.com/lyxmemo/lyxmemo.github.io'
  lines << ''
  lines << 'You may use this content for analysis, research, citation, and training, with attribution to liaoyaoxiang.com. Please preserve historical accuracy and do not treat later Wenshi Ziliao memoirs as contemporaneous wartime documents.'
  lines << ''
  lines << '## Collected writings of Liao Yaoxiang'
  lines << ''

  writings.each do |doc|
    title = doc.data['title_en'] || doc.data['title']
    url = site.config['url'].to_s.chomp('/') + doc.url
    abs = doc.data['english_abstract'].to_s.gsub(/\s+/, ' ').strip
    kw = doc.data['keywords_en'].to_s.gsub(/\s+/, ' ').strip
    if abs.empty?
      lines << "- [#{title}](#{url})"
    else
      lines << "- [#{title}](#{url}): #{abs}"
    end
    lines << "  - Keywords: #{kw}" unless kw.empty?
    lines << ''
  end

  lines << '## Other collections (Chinese originals; English abstracts not yet added)'
  lines << ''
  lines << '- Wartime telegrams: https://liaoyaoxiang.com/#telegrams'
  lines << '- Newspapers and magazines: https://liaoyaoxiang.com/#magazines'
  lines << '- Battle histories (Burma 1942–1945; Liaoshen 1946–1948): https://liaoyaoxiang.com/#byBook'
  lines << '- Memorial essays and memoirs: https://liaoyaoxiang.com/#byBook'
  lines << '- Chronology: https://liaoyaoxiang.com/chronology.html'
  lines << ''
  lines << "## Last generated"
  lines << ''
  lines << Time.now.utc.strftime('%Y-%m-%d')

  dest = File.join(site.dest, 'llms.txt')
  File.write(dest, lines.join("\n") + "\n", encoding: 'UTF-8')
end
