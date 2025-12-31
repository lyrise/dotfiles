# 実行環境を識別
if [ "$(uname)" = 'Darwin' ]; then
    OS='Mac'
elif [ "$(expr substr $(uname -s) 1 5)" = 'Linux' ]; then
    OS='Linux'
fi

if [ "${OS}" = 'Linux' ]; then
    # pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
fi

if [ "${OS}" = 'Mac' ]; then
    export PATH="/opt/homebrew/bin:$PATH"
fi

# common
export PATH="$HOME/bin:$PATH"

# dotenv
eval "$(direnv hook zsh)"

# docker
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# fzf
export PATH="$HOME/.fzf/bin:$PATH"

# rust
export PATH="$HOME/.cargo/bin:$PATH"
export RUSTC_WRAPPER=$(which sccache)
export SCCACHE_CACHE_SIZE="40G"

# goenv
# export GOENV_ROOT="$HOME/.goenv"
# export PATH="$GOENV_ROOT/bin:$PATH"
# export GOENV_DISABLE_GOPATH=1
# eval "$(goenv init -)"

# dotnet
export PATH="$HOME/.dotnet/tools:$PATH"

# go
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# poetry
export PATH="$HOME/.local/bin:$PATH"

# vim
export EDITOR=vim
bindkey -v

# sdkman
source "$HOME/.sdkman/bin/sdkman-init.sh"

# java
export JAVA_HOME=$HOME/.sdkman/candidates/java/current
export PATH=$JAVA_HOME/bin:$PATH

# snap
export PATH=/snap/bin:$PATH

# dotnet
export PATH="$PATH:$HOME/.dotnet/tools"

# 任意の設定を読み込む
if [ -e ~/.zshenv.local ]; then
    . ~/.zshenv.local
fi
