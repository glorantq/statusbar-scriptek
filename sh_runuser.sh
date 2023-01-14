#!/usr/bin/bash

# ezen a fileon 700
# fifo 600
while true ; do
    while IFS='' read command ; do
        $command
    done < ~/.local/scripts/.runuser_execute.fifo
done
