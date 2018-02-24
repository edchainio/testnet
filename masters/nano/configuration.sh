#!/usr/bin/env bash

sh -c 'echo "include /usr/share/nano/*.nanorc" >> .nanorc'

sh -c 'echo "set const" >> .nanorc'

sh -c 'echo "set tabsize 4" >> .nanorc'

sh -c 'echo "set tabstospaces" >> .nanorc'

cp .nanorc /home/<username>/