All The Papers
==============
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

[![Chart](https://raw.githubusercontent.com/floft/all-the-papers/master/bar.png)](https://raw.githubusercontent.com/floft/all-the-papers/master/bar.png)
