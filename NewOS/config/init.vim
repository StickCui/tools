set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

if !empty(glob("/path1/bin/python3"))
    let g:python3_host_prog = '/path1/bin/python3'
else
    let g:python3_host_prog = '/path2/bin/python3'
endif
let g:loaded_ruby_provider = 0
let g:loaded_node_provider = 0
let g:loaded_perl_provider = 0

set clipboard+=unnamedplus

autocmd TermOpen * startinsert
