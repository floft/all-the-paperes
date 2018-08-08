All The Papers
==============
## Running
First, download a whole bunch of ML and AI papers from 2014-2018 from a
variety of conferences and journals.

    ./download_pdfs.py

Second, `pdfgrep` through the papers to find the ones about GANs and relate
in some way to transfer learning.

    ./grep_pdfs.sh

Finally, make a pie chart about how many papers have overlap between GANs and
various types of transfer learning.

    ./generate_pie_chart.py

Optionally, look through all the overlap papers.

    ./open.sh list/overlap.txt

## Results

| *Papers* | *Number* |
|:---------|:---------
| Total    | 16,644   |
| GAN      | 500      |
| TL       | 1,173    |
| GAN & TL | 91       |

[![Pie Chart](https://raw.githubusercontent.com/floft/all-the-papers/master/pie.png)](https://raw.githubusercontent.com/floft/all-the-papers/master/pie.png)
