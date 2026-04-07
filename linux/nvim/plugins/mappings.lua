local function focus_editing_window()
    if vim.bo.filetype ~= "neo-tree" then return end
    vim.cmd.wincmd "p"
end

return {
    "AstroNvim/astrocore",
    ---@type AstroCoreOpts
    opts = {
        mappings = {
            n = {
                ["<C-M-g>"] = { "<cmd>ToggleTerm size=20 direction=horizontal<cr>", desc = "Toggle horizontal terminal" },
                ["<C-M-b>"] = { "<cmd>Neotree toggle<cr>", desc = "Toggle explorer" },
                ["<C-M-e>"] = { "<cmd>Neotree focus<cr>", desc = "Focus explorer" },
                ["<C-M-i>"] = { focus_editing_window, desc = "Focus editing window" },
            },
            i = {
                ["<C-M-g>"] = { "<cmd>ToggleTerm size=20 direction=horizontal<cr>", desc = "Toggle horizontal terminal" },
                ["<C-M-b>"] = { "<cmd>Neotree toggle<cr>", desc = "Toggle explorer" },
                ["<C-M-e>"] = { "<cmd>Neotree focus<cr>", desc = "Focus explorer" },
                ["<C-M-i>"] = { focus_editing_window, desc = "Focus editing window" },
            },
            t = {
                ["<C-M-g>"] = { "<cmd>ToggleTerm size=20 direction=horizontal<cr>", desc = "Toggle horizontal terminal" },
            },
        },
    },
}
