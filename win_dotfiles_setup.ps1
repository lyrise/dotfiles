Remove-Item -Path $PROFILE -Force
New-Item -Type SymbolicLink $PROFILE -Value $PSScriptRoot\windows\pwsh_profile.ps1

Remove-Item -Path $HOME\.vimrc -Force
New-Item -Type SymbolicLink $HOME\.vimrc -Value $PSScriptRoot\linux\.vimrc

Remove-Item -Path $HOME\.ideavimrc -Force
New-Item -Type SymbolicLink $HOME\.ideavimrc -Value $PSScriptRoot\linux\.ideavimrc
