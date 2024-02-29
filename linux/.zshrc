# デバッグ用環境変数
DEBUG=

# zshベンチマーク
# zmodload zsh/zprof && zprof

# zcompileを実施
if [ ! -f ~/.zshrc.zwc -o ~/.zshrc -nt ~/.zshrc.zwc ]; then
    zcompile ~/.zshrc
fi

# wslの設定を読み込む
# https://stackoverflow.com/questions/60922620/shell-script-to-check-if-running-in-windows-when-using-wsl
if [ $(uname -r | sed -n 's/.*\( *Microsoft *\).*/\1/ip') ]; then
    . ~/.zshrc.wsl
fi

# 実行環境を識別
if [ "$(uname)" = 'Darwin' ]; then
    OS='Mac'
elif [ "$(expr substr $(uname -s) 1 5)" = 'Linux' ]; then
    OS='Linux'
fi

if [ "${OS}" = 'Mac' ]; then
    export PATH="/opt/homebrew/bin:$PATH"
fi

# common
export PATH="$HOME/bin:$PATH"

# docker
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# fzf
export PATH="$HOME/.fzf/bin:$PATH"

# rust
export PATH="$HOME/.cargo/bin:$PATH"

# goenv
export GOENV_ROOT="$HOME/.goenv"
export PATH="$GOENV_ROOT/bin:$PATH"
eval "$(goenv init -)"

# go
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# pyenv
eval "$(pyenv init -)"

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

# Google Cloud SDK.
if [ -f ~/google-cloud-sdk/path.zsh.inc ]; then
    . ~/google-cloud-sdk/path.zsh.inc;
fi
if [ -f ~/google-cloud-sdk/completion.zsh.inc ]; then
    . ~/google-cloud-sdk/completion.zsh.inc;
fi

# 任意の設定を読み込む
if [ -e ~/.zshrc.include ]; then
    . ~/.zshrc.include
fi

# エイリアス集
alias ll='lsd -al --date "+%F %T"'
alias k='kubectl'
alias d='docker'
alias dc='docker compose'
alias g='git'
alias g-pr='git pull-request'

if [ $OS = 'Linux' ]; then
    alias pbcopy='xclip -selection clipboard'
    alias pbpaste='xclip -selection clipboard -o'
fi

# 履歴の保存先
HISTFILE=$HOME/.zsh-history
# メモリに展開する履歴の数
HISTSIZE=100000
# 保存する履歴の数
SAVEHIST=100000

# コアダンプサイズを制限
limit coredumpsize 102400
# 出力の文字列末尾に改行コードが無い場合でも表示
unsetopt promptcr

# 色を使う
setopt prompt_subst
# ビープを鳴らさない
setopt nobeep
# 内部コマンド jobs の出力をデフォルトで jobs -l にする
setopt long_list_jobs
# 補完候補一覧でファイルの種別をマーク表示
setopt list_types
# サスペンド中のプロセスと同じコマンド名を実行した場合はリジューム
setopt auto_resume
# 補完候補を一覧表示
setopt auto_list
# 直前と同じコマンドをヒストリに追加しない
setopt hist_ignore_dups
# cd 時に自動で push
setopt auto_pushd
# 同じディレクトリを pushd しない
setopt pushd_ignore_dups
# ファイル名で #, ~, ^ の 3 文字を正規表現として扱う
setopt extended_glob
# TAB で順に補完候補を切り替える
setopt auto_menu
# zsh の開始, 終了時刻をヒストリファイルに書き込む
setopt extended_history
# =command を command のパス名に展開する
setopt equals
# --prefix=/usr などの = 以降も補完
setopt magic_equal_subst
# ヒストリを呼び出してから実行する間に一旦編集
setopt hist_verify
# ファイル名の展開で辞書順ではなく数値的にソート
setopt numeric_glob_sort
# 出力時8ビットを通す
setopt print_eight_bit
# ヒストリを共有
setopt share_history
# 補完候補のカーソル選択を有効に
zstyle ':completion:*:default' menu select=2
# 補完候補の色づけ
#eval `dircolors`
export ZLS_COLORS=$LS_COLORS
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
# ディレクトリ名だけでcd
setopt auto_cd
# カッコの対応などを自動的に補完
setopt auto_param_keys
# ディレクトリ名の補完で末尾の / を自動的に付加し、次の補完に備える
setopt auto_param_slash
# スペルチェック
setopt correct
# {a-c} を a b c に展開する機能を使えるようにする
setopt brace_ccl
# Ctrl+S/Ctrl+Q によるフロー制御を使わないようにする
setopt NO_flow_control
# コマンドラインの先頭がスペースで始まる場合ヒストリに追加しない
setopt hist_ignore_space
# コマンドラインでも # 以降をコメントと見なす
setopt interactive_comments
# ファイル名の展開でディレクトリにマッチした場合末尾に / を付加する
setopt mark_dirs
# history (fc -l) コマンドをヒストリリストから取り除く。
setopt hist_no_store
# 補完候補を詰めて表示
setopt list_packed
# 最後のスラッシュを自動的に削除しない
setopt noautoremoveslash
# ヒストリーに重複を表示しない
setopt histignorealldups
# 履歴をインクリメンタルに追加
setopt inc_append_history
# 余分な空白は詰めて記録
setopt hist_reduce_blanks
# cdrコマンドで履歴にないディレクトリにも移動可能に
# zstyle ":chpwd:*" recent-dirs-default true
# cdrコマンドを有効 ログアウトしても有効なディレクトリ履歴
# cdrタブでリストを表示
autoload -Uz add-zsh-hook
autoload -Uz chpwd_recent_dirs cdr
add-zsh-hook chpwd chpwd_recent_dirs
# 区切り文字の設定
autoload -Uz select-word-style
select-word-style default
zstyle ':zle:*' word-chars "_-./;@"
zstyle ':zle:*' word-style unspecified

# zplugのセットアップ
source ~/.zinit/bin/zinit.zsh

# cdの強化
zinit ice pick'init.sh'
zinit light 'b4b4r07/enhancd'
# fzfのセットアップ
zinit ice multisrc='shell/{completion,key-bindings}.zsh'
zinit light 'junegunn/fzf'
# コマンド補完
zinit wait lucid atload"zicompinit; zicdreplay" blockf for \
    'zsh-users/zsh-completions'
zinit light 'zsh-users/zsh-autosuggestions'
zinit light 'zsh-users/zsh-history-substring-search'
zinit light 'zsh-users/zsh-syntax-highlighting'
zinit light 'chrissicool/zsh-256color'
zinit light 'kwhrtsk/docker-fzf-completion'
# zinit ice pick'contrib/completion/zsh/_docker'
# zinit light 'docker/cli'
# zinit ice pick'contrib/completion/zsh/_docker-compose'
# zinit light 'docker/compose'
# gitのショートカット
forgit_log="g-log"
forgit_diff="g-diff"
forgit_add="g-add"
forgit_reset_head="g-reset-hard"
forgit_ignore="g-ignore"
forgit_restore="g-restore"
forgit_clean="g-clean"
forgit_stash_show="g-stash-show"
zinit light 'wfxr/forgit'
# zのセットアップ
zinit ice pick'z.sh'
zinit light 'rupa/z'
# コマンドの実行時間を表示
zinit light 'popstas/zsh-command-time'
# kube-ps1のセットアップ
KUBE_PS1_SYMBOL_ENABLE='false'
KUBE_PS1_PREFIX='['
KUBE_PS1_SUFFIX=']'
KUBE_PS1_DIVIDER=':'
KUBE_PS1_CTX_COLOR=red
KUBE_PS1_NS_COLOR=cyan
zinit ice pick'kube-ps1.sh'
zinit light 'jonmosco/kube-ps1'

# 補完機能の強化
autoload -Uz compinit
compinit

# git
autoload -Uz vcs_info
setopt prompt_subst
zstyle ':vcs_info:git:*' check-for-changes true
zstyle ':vcs_info:git:*' stagedstr "%F{yellow}!"
zstyle ':vcs_info:git:*' unstagedstr "%F{red}+"
zstyle ':vcs_info:*' formats "%F{blue}%c%u[%b]%f"
zstyle ':vcs_info:*' actionformats '[%b|%a]'

precmd() {
    vcs_info
}

# プロンプトの設定
function zle-line-pre-redraw zle-keymap-select zle-line-init {
    PS1=""

    ## ユーザー名とホスト名
    PS1=$PS1$'%{\e[38;5;246m%}%n@%m%{%f%} '

    ## カレントディレクトリパスの表示
    PS1=$PS1$'%{\e[38;5;2m%}%~%{%f%} '

    ## Gitのブランチ名の表示
    PS1=$PS1'${vcs_info_msg_0_} '

    ## kubernetes情報の表示
    PS1=$PS1'$(kube_ps1)'

    ## 改行
    PS1=$PS1'
'

    ## vimのモードの表示
    VIM_NORMAL="%F{208}NORMAL%f"
    VIM_INSERT="%F{075}INSERT%f"
    PS1=$PS1"${${KEYMAP/vicmd/$VIM_NORMAL}/(main|viins)/$VIM_INSERT} "

    ## ">"の表示
    PS1=$PS1"> "

    zle reset-prompt
}

zle -N zle-line-init
zle -N zle-keymap-select
zle -N zle-line-pre-redraw

# プロンプトの設定 (2行目以降)
PS2="> "

# コマンド実行前に時刻を表示
preexec() {
    echo -e "Execution start: $(date +"%Y/%m/%d %H:%M:%S")"
}

# zsh-command-timeの設定
ZSH_COMMAND_TIME_MIN_SECONDS=1
ZSH_COMMAND_TIME_MSG="Execution time: %s"

# fzfの設定
export FZF_DEFAULT_OPTS="--height 80% --layout=reverse --border --inline-info --exact --no-sort"
export FZF_COMPLETION_TRIGGER=','

# Ctrl-Zを割り込みキーとする
stty intr "^Z"

# ヒストリーをfzfで検索
history-fzf() {
    local tac=${commands[tac]:-"tail -r"}
    print -z $( ([ -n "$ZSH_NAME" ] && fc -l 1 || history) | sed 's/ *[0-9]* *//' | eval $tac | awk '!a[$0]++' | fzf +s)
    zle accept-line
}
zle -N history-fzf
bindkey '^r' history-fzf

# killするプロセスをfzfで検索
kill-fzf() {
    if [ $OS = 'Mac' ]; then
        local list=$(ps auxwl)
        local head=$(echo $list | head -n 1)
        local pid=$(echo $list | sed 1d | fzf -m --header="$head" | awk '{print $2}')

        if [ "$pid" != "" ]
        then
            echo $pid | xargs sudo kill -${1:-9}
        fi
    elif [ $OS = 'Linux' ]; then
        local list=$(ps all)
        local head=$(echo $list | head -n 1)
        local pid=$(echo $list | sed 1d | fzf -m --header="$head" | awk '{print $3}')

        if [ "$pid" != "" ]
        then
            echo $pid | xargs sudo kill -${1:-9}
        fi
    fi
    zle accept-line
}
zle -N kill-fzf
bindkey '^x' kill-fzf

# ファイルをfzfで検索
rg-file() {
    if [ ! "$#" -gt 0 ]; then echo "Need a string to search for!"; return 1; fi
    rg --files-with-matches --no-messages "$1" | fzf --preview "highlight -O ansi -l {} 2> /dev/null | rg --colors 'match:bg:yellow' --ignore-case --pretty --context 10 '$1' || rg --ignore-case --pretty --context 10 '$1' {}"
}
zle -N rg-file

# アタッチするDockerコンテナをfzfで検索
d-attach() {
    local cid
    cid=$(docker ps -a | sed 1d | fzf -1 -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker start "$cid" && docker attach "$cid"
}

# 停止するDockerコンテナをfzfで検索
d-stop() {
    local cid
    cid=$(docker ps | sed 1d | fzf -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker stop "$cid"
}

# 削除するDockerコンテナをfzfで検索
d-rm() {
    local cid
    cid=$(docker ps -a | sed 1d | fzf -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker rm -f "$cid"
}

# すべてのDockerコンテナを削除
d-rm-all() {
    docker container rm $(docker ps -aq) -f
}

# if (which zprof > /dev/null 2>&1) ;then
#   zprof
# fi
