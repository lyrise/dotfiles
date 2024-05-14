local wezterm = require 'wezterm'
wezterm.on('window-config-reloaded', function()
    wezterm.log_info 'the config was reloaded for this window!'
end)

local config = {}
if wezterm.target_triple == 'x86_64-pc-windows-msvc' then
    config.default_prog = { 'pwsh' }
    config.launch_menu = {}
    table.insert(config.launch_menu, {
        label = 'PowerShell',
        args = { 'pwsh.exe', '-NoLogo' },
    })
end

config.audible_bell = "Disabled"
config.color_scheme = "Vs Code Dark+ (Gogh)"
config.font = wezterm.font('HackGen Console NF')
config.keys = {
    -- 次のタブに移動
    { key = "l", mods = "CTRL|ALT",   action = wezterm.action { ActivateTabRelative = 1 } },

    -- 前のタブに移動
    { key = "h", mods = "CTRL|ALT",   action = wezterm.action { ActivateTabRelative = -1 } },

    -- 新しいタブを開く
    { key = "n", mods = "CTRL|SHIFT", action = wezterm.action { SpawnTab = "CurrentPaneDomain" } },

    -- タブを閉じる
    { key = "w", mods = "CTRL|SHIFT", action = wezterm.action { CloseCurrentTab = { confirm = true } } },

    -- コピー
    { key = "c", mods = "CTRL|SHIFT", action = wezterm.action { CopyTo = "Clipboard" } },

    -- 貼り付け
    { key = "v", mods = "CTRL|SHIFT", action = wezterm.action { PasteFrom = "Clipboard" } },

    -- ActivateCopyMode
    { key = 'x', mods = 'CTRL|SHIFT', action = wezterm.action.ActivateCopyMode },
}

return config
