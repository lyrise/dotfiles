$env:FZF_DEFAULT_OPTS = "--height 80% --layout=reverse --border --inline-info --exact --no-sort"
$env:FZF_COMPLETION_TRIGGER = ","

Set-PSReadLineOption -PredictionSource History
Set-PSReadlineOption -HistoryNoDuplicates
Set-PSReadlineOption -BellStyle None
Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'
