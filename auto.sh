#!/bin/bash

for d in */ ; do
    for f in "$d"*.py; 
        do autopep8 -i "$f"; 
        echo "Formatting $f";
    done
done

for d in */ ; do
    echo "$d"
done