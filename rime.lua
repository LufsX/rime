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

local function utf8_sub(s, i, j)
    i = i or 1
    j = j or -1

    if i < 1 or j < 1 then
        local n = utf8.len(s)
        if not n then
            return nil
        end
        if i < 0 then
            i = n + 1 + i
        end
        if j < 0 then
            j = n + 1 + j
        end
        if i < 0 then
            i = 1
        elseif i > n then
            i = n
        end
        if j < 0 then
            j = 1
        elseif j > n then
            j = n
        end
    end

    if j < i then
        return ""
    end

    i = utf8.offset(s, i)
    j = utf8.offset(s, j + 1)

    if i and j then
        return s:sub(i, j - 1)
    elseif i then
        return s:sub(i)
    else
        return ""
    end
end

local function first_character(s)
    return utf8_sub(s, 1, 1)
end

local function last_character(s)
    return utf8_sub(s, -1, -1)
end

function select_character_processor(key, env)
    local engine = env.engine
    local context = engine.context
    local commit_text = context:get_commit_text()
    local config = engine.schema.config

    local first_key = config:get_string('key_binder/select_first_character') or 'bracketleft'
    local last_key = config:get_string('key_binder/select_last_character') or 'bracketright'

    if (key:repr() == first_key and commit_text ~= "") then
        engine:commit_text(first_character(commit_text))
        context:clear()

        return 1 -- kAccepted
    end

    if (key:repr() == last_key and commit_text ~= "") then
        engine:commit_text(last_character(commit_text))
        context:clear()

        return 1 -- kAccepted
    end

    return 2 -- kNoop
end

-- date_translator: 动态日期时间输入

function date_translator(input, seg)
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
    if (input == "timestamp") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("time", seg.start, seg._end, os.time(), ""))
    end
    if (input == "datetime") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("datetime", seg.start, seg._end, os.date("%Y-%m-%d %H:%M:%S"), ""))
        yield(Candidate("datetime", seg.start, seg._end, os.date("%Y-%m-%dT%H:%M:%S+08:00"), ""))
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
