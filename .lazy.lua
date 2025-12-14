return {
	{
		"stevearc/conform.nvim",
		opts = {
			formatters_by_ft = {
				["python"] = { "ruff" },
				["markdown"] = { "mdformat" },
			},
			default_format_opts = {
				lsp_format = "fallback",
			},
		},
	},
}
