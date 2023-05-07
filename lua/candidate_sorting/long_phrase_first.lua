--- 过滤器：最长词组和单字在先
local function long_phrase_first(input)
    local l = {}
    local s = {}
    local c = {}
    local max = 1
    for cand in input:iter() do
        if (utf8.len(cand.text) > max) then
            max = utf8.len(cand.text)
        end
        if (utf8.len(cand.text) == 1) then
            table.insert(c, cand)
        elseif (utf8.len(cand.text) < max) then
            table.insert(s, cand)
        else
            table.insert(l, cand)
        end
    end
    for i, cand in ipairs(l) do
        yield(cand)
    end
    for i, cand in ipairs(c) do
        yield(cand)
    end
    for i, cand in ipairs(s) do
        yield(cand)
    end
end

return long_phrase_first
