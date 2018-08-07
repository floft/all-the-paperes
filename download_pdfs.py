"""
Script to download a whole bunch of ML and AI papers from 2014-2018
"""
import os
import random
import lxml.html
import urllib.request
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
    # These will take work
    'ICLR': {
        2015: 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2015:accepted-main.html', # point to arXiv
        2016: 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2016:accepted-main.html', # point to arXiv
        2017: 'https://openreview.net/group?id=ICLR.cc/2017/conference',
        2018: 'https://openreview.net/group?id=ICLR.cc/2018/Conference'
    },
    'AAAI': {
        2014: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI14/schedConf/presentations',
        2015: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI15/schedConf/presentations',
        2016: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI16/schedConf/presentations',
        2017: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI17/schedConf/presentations',
        2018: 'https://www.aaai.org/ocs/index.php/AAAI/AAAI18/schedConf/presentations'
    },
    'KDD': {
        2015: 'http://www.kdd.org/kdd2015/toc.html',
        2016: 'http://www.kdd.org/kdd2016/program/accepted-papers',
        2017: 'http://www.kdd.org/kdd2017/accepted-papers'
    },
    'ECCV': {
        2014: 'http://eccv2014.org/proceedings/',
        2016: 'http://www.eccv2016.org/proceedings/'
    },
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
        useragent='Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'):
    if not os.path.exists(filename):
        print("Downloading", url, "to", filename)

        req = urllib.request.Request(
            url, data=None, headers={
                'User-Agent': useragent
            })

        connection = urllib.request.urlopen(req)
        data = connection.read()

        # Save to the cache file so we don't have to load next time
        with open(filename, 'wb') as f:
            f.write(data)
    else:
        print("Skipping", url, ". Exists: ", filename)

def getLinks(url, cachedir='cache'):
    """
    Get all the links on a page

    Note: caches webpage
    """
    # Create cache directory
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # Cache filename
    cache = os.path.join(cachedir, md5sum(url) + '.txt')

    # Download from web it cache doesn't exist
    if not os.path.exists(cache):
        downloadFile(url, cache)

    assert os.path.exists(cache), "Tried to download file and failed."

    # Now load from the cache file
    with open(cache, 'rb') as f: 
        data = f.read()

    # Get URLs
    dom = lxml.html.fromstring(data.decode('utf-8'))
    links = []

    for link in dom.xpath('//a/@href'):
        links.append(link)

    return links

if __name__ == '__main__':
    prepend="" # e.g. ICML_2015_
    downloaddir='pdfs'

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
    
    # TODO the ones that require some effort

    # Now shuffle and then download. This supposedly will make it so we don't
    # download everything from the same site at the same time. Hopefully make
    # me not get blocked.
    random.shuffle(toDownload)

    for link, fname in tqdm(toDownload):
        downloadFile(link, fname)
