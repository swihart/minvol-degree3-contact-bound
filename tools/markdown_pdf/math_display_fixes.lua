-- Pandoc normally wraps display math in \[ ... \].  The Markdown proof notes
-- contain a few multi-line displays with per-line \tag commands inside an
-- aligned environment.  amsmath forbids \tag inside aligned, but permits the
-- same material in align*.  Convert only those affected displays to raw LaTeX.
function Para(block)
  if #block.content ~= 1 then
    return nil
  end

  local item = block.content[1]
  if item.t ~= 'Math' or item.mathtype ~= 'DisplayMath' then
    return nil
  end

  local text = item.text
  local inner = text:match('\\begin{aligned}%s*(.-)%s*\\end{aligned}')
  if inner ~= nil and inner:match('\\tag%s*{') then
    return pandoc.RawBlock('latex', '\\begin{align*}\n' .. inner .. '\n\\end{align*}')
  end

  return nil
end
