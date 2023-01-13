local function date_translator(input, seg)
    if (input == "date") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("date", seg.start, seg._end, os.date("%Y-%m-%d"), ""))
        yield(Candidate("date", seg.start, seg._end, os.date("%Y年%m月%d日"), ""))
        yield(Candidate("date", seg.start, seg._end, os.date("%Y%m%d"), ""))
    end
    if (input == "time") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("time", seg.start, seg._end, os.date("%H:%M:%S"), ""))
        yield(Candidate("time", seg.start, seg._end, os.date("%H时%M分%S秒"), ""))
        yield(Candidate("time", seg.start, seg._end, os.date("%H%M%S"), ""))
    end
    if (input == "datetime") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("datetime", seg.start, seg._end, os.date("%Y-%m-%d %H:%M:%S"), ""))
        yield(Candidate("datetime", seg.start, seg._end, os.date("%Y%m%d%H%M"), ""))
    end

    -- 输入星期
    -- -- @JiandanDream
    -- -- https://github.com/KyleBing/rime-wubi86-jidian/issues/54
    if (input == "week") then
        local weekTab = {'日', '一', '二', '三', '四', '五', '六', '七'}
        yield(Candidate("week", seg.start, seg._end, "周" .. weekTab[tonumber(os.date("%w") + 1)], ""))
        yield(Candidate("week", seg.start, seg._end, "星期" .. weekTab[tonumber(os.date("%w") + 1)], ""))
        yield(Candidate("week", seg.start, seg._end, os.date("%A"), ""))
        yield(Candidate("week", seg.start, seg._end, os.date("%a"), ""))
        yield(Candidate("week", seg.start, seg._end, os.date("%W"), "周数"))
    end

    -- 输入月份英文
    if (input == "month") then
        yield(Candidate("month", seg.start, seg._end, os.date("%B"), ""))
        yield(Candidate("month", seg.start, seg._end, os.date("%b"), ""))
    end
end

return date_translator