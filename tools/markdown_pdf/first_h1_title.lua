-- Promote the first level-1 heading to document metadata so each PDF has a
-- proper title page without repeating the heading in the body.
function Pandoc(doc)
  if doc.meta.title == nil then
    for i, block in ipairs(doc.blocks) do
      if block.t == 'Header' and block.level == 1 then
        doc.meta.title = pandoc.MetaInlines(block.content)
        table.remove(doc.blocks, i)
        break
      end
    end
  end
  return doc
end
