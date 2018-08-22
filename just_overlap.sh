#!/bin/bash
#
# Copy just the overlapping GAN and TL papers to a directory so I can delete
# the 25 GiB but still go through all of these overlap papers
#
dir="pdfs_just_overlap/"
mkdir -p "$dir"
cut -d$'\t' -f1 list/overlap.txt | xargs -I{} cp -a {} "$dir"
