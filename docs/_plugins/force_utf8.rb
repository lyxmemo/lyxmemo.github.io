# Force UTF-8 encoding on all strings to prevent
# "incompatible character encodings: UTF-8 and ASCII-8BIT" errors
# when building on platforms where the default encoding is not UTF-8
# (e.g. Cloudflare Pages).

# Patch Jekyll::URL.unescape_path which calls String#encode('utf-8')
# on paths that are already UTF-8 bytes but tagged as ASCII-8BIT.
module Jekyll
  module URL
    class << self
      alias_method :original_unescape_path, :unescape_path

      def unescape_path(path)
        if path.encoding == Encoding::ASCII_8BIT
          path = path.force_encoding('UTF-8')
        end
        original_unescape_path(path)
      end
    end
  end
end

# Also fix document/page content and static file paths
Jekyll::Hooks.register [:documents, :pages], :pre_render do |doc|
  if doc.content.encoding != Encoding::UTF_8
    doc.content = doc.content.force_encoding('UTF-8')
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  site.static_files.each do |sf|
    %i[@relative_path @name @extname].each do |ivar|
      val = sf.instance_variable_get(ivar)
      if val.is_a?(String) && val.encoding == Encoding::ASCII_8BIT
        sf.instance_variable_set(ivar, val.force_encoding('UTF-8'))
      end
    end
  end
end
