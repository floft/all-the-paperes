#!/bin/bash
#
# Open each file in the input list in evince
#
file="$1"

if [[ ! -e $file ]]; then
    echo "Usage: ./open.sh list/overlap.txt"
    exit 1
fi

while IFS= read line; do
    filename="$(cut -d $'\t' -f1 <<< "$line")"
    terms="$(cut -d $'\t' -f2 <<< "$line")"
    firstTerm="$(cut -d ',' -f1 <<< "$terms")"

    if [[ -e "$filename" ]]; then
        [[ ! -z $terms ]] && echo "Terms: $terms"
        
        # Search for the term
        if [[ ! -z $firstTerm ]]; then
            # Note: if for example "co-variate shift" was in the document,
            # it'll mistakingly search for "covariate shift". It picks the one
            # I preferred.
            evince -l "$firstTerm" "$filename"
        # Show page 1 otherwise
        else
            evince -p 1 "$filename"
        fi
    else
        echo "Error: $line does not exist"
    fi
done < "$file"
