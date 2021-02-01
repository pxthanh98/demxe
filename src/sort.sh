ls | cat -n | while read n f; do mv "$f" `printf "%06d.jpg" $n`; done
