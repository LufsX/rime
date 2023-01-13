--- 过滤器：单字在先
function single_char_first_filter(input)
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

-- select_character_processor: 以词定字
-- 详见 `lua/select_character.lua`
select_character_processor = require("select_character")

-- date_translator: 动态日期时间输入
-- 详见 `lua/date_translator.lua`
date_translator = require("date_translator")
