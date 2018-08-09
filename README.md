All The Papers
==============
How much research overlaps GANs and transfer learning?

## Running
First, download a whole bunch of ML and AI papers from 2014-2018 from a
variety of conferences and journals. *Warning: it's over 25 GiB of PDFs.*

    ./download_pdfs.py

Second, `pdfgrep` through the papers to find the ones about GANs and relate
in some way to transfer learning.

    ./grep_pdfs.sh

Finally, make a chart about how many papers have overlap between GANs and
various types of transfer learning.

    ./generate_chart.py

Optionally, look through all the overlap papers.

    ./open.sh list/overlap.txt

## Results

| **Topic**  | **Number of Papers** |
|:-----------|:---------------------|
| GAN        | 500                  |
| TL         | 1,210                |
| GAN & TL   | 92                   |
| *(Total)*  | 16,644 (25.3 GiB)    |

Of the 500 papers referring to GANs, this figure shows how many of those papers
also include terms related to transfer learning. Based on searching the first
three pages of each of the 16,644 available papers published in AAAI, ACL,
AISTATS, CVPR, ICLR, ICML, IJCAI, JMLR, and NIPS between January 2014 and
August 2018.

[![Chart](https://raw.githubusercontent.com/floft/all-the-papers/master/bar.png)](https://raw.githubusercontent.com/floft/all-the-papers/master/bar.png)
