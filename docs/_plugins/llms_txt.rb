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
  lines << 'Original documents are in Chinese. English essay abstracts are provided on each writings page and listed here for researchers, search engines, and language models.'
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
    if abs.empty?
      lines << "- [#{title}](#{url})"
    else
      lines << "- [#{title}](#{url}): #{abs}"
    end
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
