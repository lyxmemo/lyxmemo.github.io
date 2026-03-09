require 'yaml'
require 'date'

content = File.read("docs/_data/chronology.yml")
data = YAML.safe_load(content, permitted_classes: [Date])

data.each do |yd|
  es = yd["entries"]

  # Clear original_text where source_url exists
  es.each do |e|
    if e["source_url"].to_s.length > 0 && e["original_text"].to_s.length > 0
      e["original_text"] = ""
    end
  end

  # Sort entries by date
  es.sort_by! do |e|
    d = e["date"].to_s
    case d.length
    when 0 then "0000-00-00"
    when 4 then "#{d}-00-00"
    when 7 then "#{d}-00"
    else d
    end
  end
end

File.write("docs/_data/chronology.yml", YAML.dump(data).sub(/\A---\n/, ""))
puts "Done: sorted entries and cleared redundant original_text"
