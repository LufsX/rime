-- select_character: 以词定字
-- 详见: https://github.com/BlindingDark/rime-lua-select-character
-- 2025-04-25: 优化单字提取逻辑，处理无候选的情况
-- 2025-04-27: 修正无法直接输入对应键的符号
local function extract_character(s, is_first)
    -- 单字不处理
    if utf8.len(s) == 1 then
        return s
    end
    return is_first and s:sub(1, utf8.offset(s, 2) - 1) -- 首字
    or s:sub(utf8.offset(s, -1)) -- 尾字
end

local function select_character(key, env)
    local engine = env.engine
    local context = engine.context
    local config = engine.schema.config
    local candidate = context:get_selected_candidate()

    -- 检查是否处于输入状态
    if key:release() or (not context:is_composing() and not context:has_menu()) then
        return 2 -- kNoop
    end

    -- 获取按键
    local first_key = config:get_string('key_binder/select_first_character')
    local last_key = config:get_string('key_binder/select_last_character')
    local key_repr = key:repr()

    -- 检查按键并给予 is_first 标记
    local is_first = (key_repr == first_key)
    if not (is_first or key_repr == last_key) then
        return 2 -- kNoop
    end

    -- 如果没有已选的词，直接上屏当前输入
    if not candidate then
        engine:commit_text(context:get_commit_text())
        context:clear()
        return 1 -- kAccepted
    end

    -- 提取候选并提交
    local selected_char = extract_character(candidate.text, is_first)
    context:clear_previous_segment()
    engine:commit_text(context:get_commit_text() .. selected_char)
    context:clear()
    return 1 -- kAccepted
end

return select_character
