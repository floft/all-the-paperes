#!/usr/bin/env python3
"""
Script to download a whole bunch of ML and AI papers from 2014-2018
"""
import os
import re
import json
import time
import random
import lxml.html
import urllib.request
import urllib.error
from hashlib import md5
from urllib.parse import urlparse, urljoin
from tqdm import tqdm # progress bar

# Conferences with links to .pdf on their webpages
conferences_easy = {
    'ICML': {
        2014: 'http://proceedings.mlr.press/v32/',
        2015: 'http://proceedings.mlr.press/v37/',
        2016: 'http://proceedings.mlr.press/v48/',
        2017: 'http://proceedings.mlr.press/v70/',
        2018: 'http://proceedings.mlr.press/v80/'
    },
    'AISTATS': {
        2014: 'http://proceedings.mlr.press/v33/',
        2015: 'http://proceedings.mlr.press/v38/',
        2016: 'http://proceedings.mlr.press/v51/',
        2017: 'http://proceedings.mlr.press/v54/',
        2018: 'http://proceedings.mlr.press/v84/'
    },
    'ACL': {
        2014: 'http://www.aclweb.org/anthology/P/P14/',
        2015: 'http://www.aclweb.org/anthology/P/P15/',
        2016: 'http://www.aclweb.org/anthology/P/P16/',
        2017: 'http://www.aclweb.org/anthology/P/P17/'
    },
    'CVPR': {
        2014: 'http://openaccess.thecvf.com/CVPR2014.py',
        2015: 'http://openaccess.thecvf.com/CVPR2015.py',
        2016: 'http://openaccess.thecvf.com/CVPR2016.py',
        2017: 'http://openaccess.thecvf.com/CVPR2017.py',
        2018: 'http://openaccess.thecvf.com/CVPR2018.py'
    },
    'IJCAI': {
        2015: 'https://www.ijcai.org/proceedings/2015/',
        2016: 'https://www.ijcai.org/proceedings/2016/',
        2017: 'https://www.ijcai.org/proceedings/2017/',
        2018: 'https://www.ijcai.org/proceedings/2018/'
    },
    'JMLR': {
        2014: 'http://www.jmlr.org/papers/v15/',
        2015: 'http://www.jmlr.org/papers/v16/',
        2016: 'http://www.jmlr.org/papers/v17/',
        2017: 'http://www.jmlr.org/papers/v18/' # and 2018
    },
}

conferences_add_pdf = {
    # grab the URLs and add .pdf
    'NIPS': {
        2014: 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-27-2014',
        2015: 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-28-2015',
        2016: 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-29-2016',
        2017: 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017'
    },
}

conferences_hard = {
    # These will take more work
    'ICLR': {
        2015: 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2015:accepted-main.html', # point to arXiv
        2016: 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2016:accepted-main.html', # point to arXiv
        #2017: 'https://openreview.net/group?id=ICLR.cc/2017/conference',
        #2018: 'https://openreview.net/group?id=ICLR.cc/2018/Conference',
        2017: 'https://openreview.net/notes?invitation=ICLR.cc%2F2017%2Fconference%2F-%2Fpaper.*%2Facceptance', # JSON data
        2018: 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2Fconference%2F-%2Fpaper.*%2Facceptance', # JSON data
    },
    'AAAI': {
        2014: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI14/schedConf/presentations',
        2015: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI15/schedConf/presentations',
        2016: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI16/schedConf/presentations',
        2017: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI17/schedConf/presentations',
        2018: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI18/schedConf/presentations'
    },
    # Not worth it -- ACM requires downloading immediately to not get forbidden and doesn't look like there's GAN papers
    #'KDD': {
    #    2015: 'http://www.kdd.org/kdd2015/toc.html',
    #    2016: 'http://www.kdd.org/kdd2016/program/accepted-papers',
    #    2017: 'http://www.kdd.org/kdd2017/accepted-papers'
    #},
    # Springer ones would be difficult
    #'ECCV': {
    #    2014: 'http://eccv2014.org/proceedings/',
    #    2016: 'http://www.eccv2016.org/proceedings/'
    #},
    #International Journal of Computer Vision (IJCV) 
    #Machine Learning (Springer) https://link.springer.com/journal/10994
}

def md5sum(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def get_filename(s):
    """ https://stackoverflow.com/a/18727481/2698494 """
    return os.path.basename(urlparse(s).path)

def downloadFile(url,
        filename,
        referer=None,
        useragent='Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'):
    if not os.path.exists(filename):
        print("Downloading", url, "to", filename)

        headers = { 'User-Agent': useragent }

        if referer is not None:
            headers["Referer"] = referer

        req = urllib.request.Request(url, data=None, headers=headers)

        connection = urllib.request.urlopen(req)
        data = connection.read()

        # Save to the cache file so we don't have to load next time
        with open(filename, 'wb') as f:
            f.write(data)
    else:
        print("Skipping", url, ". Exists: ", filename)

def getLinks(url, cachedir='cache', search='//a/@href', referer=None, raw=False):
    """
    Get all the links on a page
    Also return raw content if desired

    Note: caches webpage
    """
    # Create cache directory
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # Cache filename
    cache = os.path.join(cachedir, md5sum(url) + '.txt')

    # Download from web it cache doesn't exist
    if not os.path.exists(cache):
        downloadFile(url, cache, referer)

    assert os.path.exists(cache), "Tried to download file and failed."

    # Now load from the cache file
    with open(cache, 'rb') as f: 
        data = f.read()

    # Get URLs
    dom = lxml.html.fromstring(data)
    links = []

    for link in dom.xpath(search):
        links.append(link)

    if raw:
        return links, data
    else:
        return links

if __name__ == '__main__':
    prepend="" # e.g. ICML_2015_
    downloaddir='pdfs'
    errors="error.txt"

    # Create download directory
    if not os.path.exists(downloaddir):
        os.makedirs(downloaddir)

    # List of files to download
    toDownload = []

    # Easy-to-download PDFs
    for conf, years in conferences_easy.items():
        for year, url in years.items():
            prepend = conf+"_"+str(year)+"_"
            links = getLinks(url)

            # Only download PDFs that are not supplementary material
            for link in links:
                # -supp -- PMLR supplementary material
                # supplemental/ -- CVPR supplemental material
                # AbsBook -- CVPR extracted abstracts from PDFs
                # poster/ -- CVPR posters
                # erratum. -- IJCAI erratum for papers
                # frontmatter -- IJCAI front matter
                # appendix -- JMLR appendices
                # attachments/ -- ACL has some datasets, notes, presentations, etc. files
                if ".pdf" in link \
                        and "-supp" not in link \
                        and "supplemental/" not in link \
                        and "AbsBook" not in link \
                        and "poster/" not in link \
                        and "erratum." not in link \
                        and "frontmatter" not in link \
                        and "appendix" not in link \
                        and "attachments/" not in link:
                    abspath = urljoin(url.strip(), link.strip()) # some links are relative, some have newlines at the end
                    fname = prepend + get_filename(abspath)
                    toDownload.append((abspath, os.path.join(downloaddir, fname)))

    # Some require adding .pdf to the filename
    for conf, years in conferences_add_pdf.items():
        for year, url in years.items():
            prepend = conf+"_"+str(year)+"_"
            links = getLinks(url)

            # Only download PDFs that are not supplementary material
            for link in links:
                if "/paper" in link:
                    abspath = urljoin(url.strip(), link.strip()) + '.pdf' # NIPS links are relative and have .pdf at end
                    fname = prepend + get_filename(abspath)
                    toDownload.append((abspath, os.path.join(downloaddir, fname)))
    
    # The ones that require some effort
    acmMatch = re.compile(r"window\.location\.replace\('(.*)'\);")

    for conf, years in conferences_hard.items():
        for year, url in years.items():
            prepend = conf+"_"+str(year)+"_"

            # OpenReview papers (e.g. ICLR)
            if "openreview.net/notes" in url:
                _, rawData = getLinks(url, raw=True)
                j = json.loads(rawData.decode('utf-8'))

                for entry in j["notes"]:
                    if "Accept" in entry["content"]["decision"]:
                        # Looks like replyto and forum link to the ID of the actual PDF
                        toDownload.append(("https://openreview.net/pdf?id="+entry["replyto"],
                            os.path.join(downloaddir, prepend+entry["replyto"]+".pdf")))

            elif "AAAI" in conf:
                links = getLinks(url, search="//a[contains(@class, 'file')]/@href")

                for link in links:
                    # For AAAI papers, make a substitution in the link
                    if "paper/view" in link:
                        abspath = urljoin(url.strip(), link.strip().replace("paper/view","paper/download")) # get download URL
                        fname = prepend + get_filename(abspath) + ".pdf"
                        toDownload.append((abspath, os.path.join(downloaddir, fname)))
            else:
                links = getLinks(url)

                for link in links:
                    # If it links to arXiv, then download the PDF on arXiv
                    # Note: this doesn't download it if the latest arXiv version doesn't provide a PDF
                    if "arxiv.org" in link:
                        arXivLinks = getLinks(link)

                        for arXivLink in arXivLinks:
                            if "pdf/" in arXivLink:
                                abspath = urljoin(link.strip(), arXivLink.strip()) # make PDF link relative to arXiv URL
                                fname = prepend + get_filename(abspath) + ".pdf"
                                toDownload.append((abspath, os.path.join(downloaddir, fname)))
                    # For KDD papers that link to ACM
                    """
                    elif "KDD" in conf and "dl.acm.org" in link:
                        pass
                        _, acmData = getLinks(link, raw=True, referer=url) # Gives different page without referer
                        match = acmMatch.search(acmData.decode('utf-8')) # PDF link is in Javascript code
                        if match is not None:
                            pdf = match.group(1)
                            abspath = urljoin(url.strip(), pdf.strip())
                            fname = prepend + get_filename(abspath)
                            downloadFile(abspath, os.path.join(downloaddir, fname))
                    """


    # Get the list of ones that errored
    error_files = []
    if os.path.exists(errors):
        with open(errors, 'r') as f:
            for line in f:
                error_files.append(line.strip())

    # Throw out all that were already downloaded
    notDownloaded = []

    for link, fname in toDownload:
        if not os.path.exists(fname) and link not in error_files:
            notDownloaded.append((link, fname))

    # Now shuffle and then download. This supposedly will make it so we don't
    # download everything from the same site at the same time. Hopefully make
    # me not get blocked.
    random.shuffle(notDownloaded)

    for link, fname in tqdm(notDownloaded):
        try:
            downloadFile(link, fname)
        except urllib.error.HTTPError:
            print("Error downloading", fname)
            with open(errors, 'a') as f:
                f.write(link+'\n')
            time.sleep(0.5)
