nnoremap <leader><Esc> :noh<CR>

nnoremap : ;
nnoremap ; :
vnoremap : ;
vnoremap ; :

inoremap kk <Esc>
inoremap jj <Esc>
inoremap hh <Esc>
inoremap ll <Esc>

inoremap <C-k> <UP>
inoremap <C-j> <DOWN>
inoremap <C-h> <LEFT>
inoremap <C-l> <RIGHT>
nnoremap <C-k> 5k
nnoremap <C-j> 5j
nnoremap <C-h> 5h
nnoremap <C-l> 5l
vnoremap <C-k> 5k
vnoremap <C-j> 5j
vnoremap <C-h> 5h
vnoremap <C-l> 5l
nnoremap <leader>dw di<leader>w
nnoremap <leader>cw ci<leader>w

nnoremap f <leader><leader>/
inoremap { {}<LEFT>
inoremap [ []<LEFT>
inoremap < <><LEFT>
inoremap ( ()<LEFT>
inoremap " ""<LEFT>
inoremap ' ''<LEFT>

nnoremap <CR> i<CR><Esc>
inoremap <S-CR> <End><CR>
inoremap <C-S-CR> <UP><End><CR>
nnoremap <S-CR> <End><CR>
nnoremap <C-S-CR> <UP><End><CR>

nnoremap <C-w> :w!<CR>

nnoremap n nzz
nnoremap N Nzz
nnoremap s "_s
nnoremap x "_x

nnoremap <leader>P "0P
nnoremap <leader>p "0p
vnoremap p "_dP
vnoremap <leader>p "_d"0P

nnoremap <C-a> ggvG
inoremap <C-a> <Esc>ggvG

vnoremap < <gv
vnoremap > >gv
