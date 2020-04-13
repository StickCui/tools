-- 将 Windows 默认的反斜杠路径分隔符修改为posix的斜杠
local function force_fwd_slashes(text, first, last)
    clink.slash_translation(1)
    return false
end
clink.register_match_generator(force_fwd_slashes, -1)

-- 修改提示符
local function verbatim(s)
    s = string.gsub(s, "%%", "%%%%")
    return s
end

function my_prompt_filter()
    -- get_cwd() is differently encoded than the clink.prompt.value, so everything other than
    -- pure ASCII will get garbled. So try to parse the current directory from the original prompt
    -- and only if that doesn't work, use get_cwd() directly.
    -- The matching relies on the default prompt which ends in X:\PATH\PATH>
    -- (no network path possible here!)
    local old_prompt = clink.prompt.value
    local cwd = old_prompt:match('.*(.:[^>]*)>')
    if cwd == nil then cwd = clink.get_cwd() end

    -- environment systems like pythons virtualenv change the PROMPT and usually
    -- set some variable. But the variables are differently named and we would never
    -- get them all, so try to parse the env name out of the PROMPT.
    -- envs are usually put in round or square parentheses and before the old prompt
    local env = old_prompt:match('.*%(([^%)]+)%).+:')
    -- also check for square brackets
    if env == nil then env = old_prompt:match('.*%[([^%]]+)%].+:') end

    -- build our own prompt
    -- orig: $E[1;32;40m$P$S{git}{hg}$S$_$E[1;30;40m{lamb}$S$E[0m
    -- color codes: "\x1b[1;37;40m"
    local cmder_prompt = "\x1b[1;32;40m{cwd} {git}{hg}{svn} \n\x1b[1;39;40m{lamb} \x1b[0m"
    local lambda = "$"
    cmder_prompt = string.gsub(cmder_prompt, "{cwd}", verbatim(cwd))

    if env ~= nil then
        lambda = "("..env..") "..lambda
    end
    clink.prompt.value = string.gsub(cmder_prompt, "{lamb}", verbatim(lambda))
end

clink.prompt.register_filter(my_prompt_filter, 1)