# Force UTF-8 encoding on all document content to prevent
# "incompatible character encodings: UTF-8 and ASCII-8BIT" errors
# when building on platforms where the default encoding is not UTF-8.

Jekyll::Hooks.register [:documents, :pages], :pre_render do |doc|
  if doc.content.encoding != Encoding::UTF_8
    doc.content = doc.content.force_encoding('UTF-8')
  end
end
