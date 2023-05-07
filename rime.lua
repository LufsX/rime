--- 过滤器：最长词组和单字在先
function long_phrase_first(input)
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

--- 过滤器：单字在先
function single_char_first(input)
    local l = {}
    for cand in input:iter() do
        if (utf8.len(cand.text) == 1) then
            yield(cand)
        else
            table.insert(l, cand)
        end
    end
    for i, cand in ipairs(l) do
        yield(cand)
    end
end

--- 过滤器：只显示单字
function single_char_only(input)
    for cand in input:iter() do
        if (utf8.len(cand.text) == 1) then
            yield(cand)
        end
    end
end

-- select_character_processor: 以词定字
-- 详见 `lua/select_character.lua`
select_character_processor = require("select_character")

-- date_translator: 动态日期时间输入
-- 详见 `lua/date_translator.lua`
date_translator = require("date_translator")
