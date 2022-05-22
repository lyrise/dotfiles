Remove-Item -Path $PROFILE -Force
New-Item -Type SymbolicLink $PROFILE -Value $PSScriptRoot\windows\pwsh_profile.ps1

Remove-Item -Path $HOME\.vimrc -Force
New-Item -Type SymbolicLink $HOME\.vimrc -Value $PSScriptRoot\linux\.vimrc
