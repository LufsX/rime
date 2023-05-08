-- select_character_processor: 以词定字
-- 详见 `lua/select_character.lua`
select_character = require("select_character")

-- date_translator: 动态日期时间输入
-- 详见 `lua/date_translator.lua`
date_translator = require("date_translator")

-- long_phrase_first: 最长词组和单字在先
-- 详见 `lua/candidate_sorting/long_phrase_first.lua`
long_phrase_first = require("candidate_sorting.long_phrase_first")

-- single_char_first: 单字在先
-- 详见 `lua/candidate_sorting/single_char_first.lua`
single_char_first = require("candidate_sorting.single_char_first")

-- single_char_only: 只显示单字
-- 详见 `lua/candidate_sorting/single_char_only.lua`
single_char_only = require("candidate_sorting.single_char_only")

-- unicode_input: Unicode 输入
-- 详见 `lua/candidate_sorting/unicode_input.lua`
unicode_input = require("unicode_input")
