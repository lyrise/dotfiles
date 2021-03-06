let mapleader = ","

nnoremap <leader><Esc> :noh<CR>

inoremap <C-k> <UP>
inoremap <C-j> <DOWN>
inoremap <C-h> <LEFT>
inoremap <C-l> <RIGHT>
nnoremap k gk
nnoremap j gj
nnoremap <C-k> 5k
nnoremap <C-j> 5j
nnoremap <C-h> ^
nnoremap <C-l> $
vnoremap <C-k> 5k
vnoremap <C-j> 5j
vnoremap <C-h> ^
vnoremap <C-l> $

nnoremap t <leader><leader>/
nnoremap m  %
vnoremap m  %

nnoremap <CR> i<CR><Esc>
inoremap <S-CR> <End><CR>
inoremap <C-S-CR> <UP><End><CR>
nnoremap <S-CR> <End><CR>
nnoremap <C-S-CR> <UP><End><CR>

nnoremap <C-w> :w<CR>
nnoremap <C-q> :q<CR>

nnoremap n nzz
nnoremap N Nzz
nnoremap s "_s
vnoremap s "_s
nnoremap x "_x
vnoremap x "_x

nnoremap <leader>P "0P
nnoremap <leader>p "0p
vnoremap p "_s<C-V><ESC>

nnoremap <C-a> ggvG
inoremap <C-a> <Esc>ggvG

vnoremap { S}
vnoremap ( S)
vnoremap [ S]
vnoremap " S"
vnoremap ' S'
vmap < S]<ESC>cs[>

vnoremap $ $<LEFT>
