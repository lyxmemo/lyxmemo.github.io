# Force UTF-8 encoding on all string content to prevent
# "incompatible character encodings: UTF-8 and ASCII-8BIT" errors
# when building on platforms where the default encoding is not UTF-8
# (e.g., Cloudflare Pages).

def force_utf8(str)
  return str unless str.is_a?(String)
  return str if str.encoding == Encoding::UTF_8
  str.encode('UTF-8', invalid: :replace, undef: :replace, replace: '?')
rescue
  str.force_encoding('UTF-8')
end

# Fix document and page content before rendering
Jekyll::Hooks.register [:documents, :pages], :pre_render do |doc|
  doc.content = force_utf8(doc.content) if doc.content
  if doc.data
    doc.data.each do |key, value|
      doc.data[key] = force_utf8(value) if value.is_a?(String)
    end
  end
end

# Fix site data after it's read
Jekyll::Hooks.register :site, :post_read do |site|
  # Fix all collection documents
  site.collections.each do |_, collection|
    collection.docs.each do |doc|
      doc.content = force_utf8(doc.content) if doc.content
      if doc.data
        doc.data.each do |key, value|
          doc.data[key] = force_utf8(value) if value.is_a?(String)
        end
      end
    end
  end

  # Fix all pages
  site.pages.each do |page|
    page.content = force_utf8(page.content) if page.content
    if page.data
      page.data.each do |key, value|
        page.data[key] = force_utf8(value) if value.is_a?(String)
      end
    end
  end

  # Fix layouts
  site.layouts.each do |_, layout|
    layout.content = force_utf8(layout.content) if layout.content
  end
end
