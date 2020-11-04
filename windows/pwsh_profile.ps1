$env:FZF_DEFAULT_OPTS="--height 80% --layout=reverse --border --inline-info --exact --no-sort"
$env:FZF_COMPLETION_TRIGGER=","

Set-PSReadLineKeyHandler -Chord "Ctrl+r" -BriefDescription "fzf" -LongDescription "history-search-by-fzf" -ScriptBlock {
    $historyFile = (Get-PSReadLineOption).HistorySavePath
    $historyList = new-object 'System.Collections.Generic.List[string]'
    $historyList.AddRange((Get-Content -Encoding utf8 $historyFile) -as[string[]])
    $historyList.Reverse()

    $uniqueHistoryList = new-object 'System.Collections.Generic.List[string]'
    $hashSet = new-object 'System.Collections.Generic.HashSet[string]'

    foreach ($a in $historyList) {
        if ($hashSet.Add($a)) {
            $uniqueHistoryList.Add($a)
        }
    }

    $command = $uniqueHistoryList | Invoke-Fzf

    [Microsoft.PowerShell.PSConsoleReadLine]::Insert($command)
}
