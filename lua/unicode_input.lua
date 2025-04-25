-- Unicode 输入支持
-- -- @shewer
-- -- https://github.com/shewer/librime-lua-script/blob/main/lua/component/unicode.lua
local MAX_UNICODE = 0x10FFFF -- Unicode 最大编码
local TRIGGER_PREFIX = "U" -- 触发前缀

local function unicode_input(input, seg, env)
    -- 快速检查有效性
    if not seg:has_tag("unicode") or input == '' then
        return
    end

    -- 匹配 Unicode 编码
    local ucodestr = input:match(TRIGGER_PREFIX .. "(%x+)")

    -- 转换为数值并检查范围
    local code = tonumber(ucodestr, 16)
    if not code then
        return
    end

    if code > MAX_UNICODE then
        yield(Candidate("unicode", seg.start, seg._end, "undefined", "超出范围"))
        return
    end

    -- 生成主候选项
    local text = utf8.char(code)
    yield(Candidate("unicode", seg.start, seg._end, text, string.format("U%x", code)))

    -- 对于较小的编码，生成附加候选项
    if code < 0x10000 then
        for i = 0, 15 do
            local extended_code = code * 16 + i
            if extended_code <= MAX_UNICODE then
                local extended_text = utf8.char(extended_code)
                yield(Candidate("unicode", seg.start, seg._end, extended_text, string.format("U%x~%x", code, i)))
            end
        end
    end
end

return unicode_input
