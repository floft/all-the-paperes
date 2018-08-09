#!/usr/bin/env python3
"""
From the pdfgrep output data, generate a chart
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def replace(df, replacements):
    """
    If replacements={'s': 'r'} then replace all 's' with 'r' in dataframe df.

    Note: case refers to case-sensitivity, which by default is False, i.e.
    in the above example 'S' would also be replaced with 'r'.
    """
    for s, r in replacements.items():
        df = df.str.lower().replace(s, r)

    return df

def pandasSetPrint():
    """ Make it so we can see the output """
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.expand_frame_repr = False

def pie(fracs, labels=None, save_name=None, pandas=False, figsize=(7,7)):
    """
    Generate and save pie plot

    If pandas=True:
        pie(df, save_name='pie', pandas=True)
    If pandas=False:
        pie(fracs, labels, 'pie')
    """
    if pandas:
        fig = plt.figure()
        df.value_counts().plot.pie(
                figsize=figsize,
                radius=0.7,
                autopct='%.0f%%')
    else:
        fig = plt.figure(figsize=figsize)
        patches, texts, autotexts = plt.pie(fracs,
                labels=labels,
                radius=0.75,
                autopct='%.0f%%')
        #plt.legend(patches, labels, loc="best")

    ax = fig.gca()
    ax.set_title("")
    ax.set_ylabel("")
    ax.set_xlabel("")
    fig = ax.get_figure()

    if save_name is not None:
        fig.savefig(save_name+'.png', bbox_inches='tight')
        fig.savefig(save_name+'.pdf', bbox_inches='tight')

def pieCombined(fracs1, labels1, title1, fracs2, labels2, title2,
        save_name=None, figsize=(10,5)):
    """ Generate and save 2 pie plots together using subplots """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    plt.tight_layout()

    ax1.axis("equal")
    ax2.axis("equal")

    #pie = plt.pie(df, startangle=0, autopct='%1.0f%%', pctdistance=0.9, radius=1.2)
    #labels=df.index.unique()
    #plt.title('Pie Chart Demonstration', weight='bold', size=14)
    #plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10,
    #                   bbox_transform=plt.gcf().transFigure)
    #plt.subplots_adjust(left=0.0, bottom=0.1, right=0.85)

    patches, texts, autotexts = ax1.pie(
            fracs1, radius=1.2, autopct='%.0f%%',
            startangle=90, pctdistance=0.6)
    ax1.set_title(title1, weight='bold', fontsize=16)
    ax1.legend(patches, labels1,
            bbox_to_anchor=(0,0.1), loc="lower left", fontsize=12,
               bbox_transform=fig.transFigure)
    for t in texts:
        t.set_size('smaller')
    for t in autotexts:
        t.set_size('x-large')

    patches, texts, autotexts = ax2.pie(
            fracs2, radius=1.2, autopct='%.0f%%',
            startangle=90)
    ax2.set_title(title2, weight='bold', fontsize=16)
    ax2.legend(patches, labels2,
            bbox_to_anchor=(0.5,0.0), loc="lower left", fontsize=12,
               bbox_transform=fig.transFigure)
    for t in texts:
        t.set_size('smaller')
    for t in autotexts:
        t.set_size('x-large')
        percent = float(t.get_text().replace('%',''))
        if percent < 2:
            t.set_text('')

    if save_name is not None:
        fig.savefig(save_name+'.png', bbox_inches='tight', pad_inches=0)
        fig.savefig(save_name+'.pdf', bbox_inches='tight', pad_inches=0)

def cap(s):
    """
    Capitalize only the first letter of a string
    
    s.capitalize() and s.title() make the non-first letters of words lowercase.
    I don't want to change anything other than the first letter.
    """
    return s[0].upper() + s[1:]

def remzero(num):
    """
    Remove zero at front of float
    """
    s = '%.1f' % num
    s = s.replace(".00", ".0")
    return s[1:] if s[0] == "0" else s

def autolabel(ax, rects, yerr=None):
    """
    Attach a text label above each bar displaying its height
    
    From: https://matplotlib.org/examples/api/barchart_demo.html
    """
    for i, rect in enumerate(rects):
        height = rect.get_height()
        yerrh = 0
        
        if yerr:
            yerrh = yerr[i]
        
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height + yerrh,
                #remzero(height),
                '%.1f' % height,
                ha='center', va='bottom')

def barplot(fracs, labels, save_name=None):
    assert len(fracs) == len(labels)
    colors = ["xkcd:orange", "xkcd:teal", "xkcd:darkgreen", "xkcd:orchid", "xkcd:blue", "xkcd:indigo"]
    
    fig, ax = plt.subplots(1,1,figsize=(8, 4))
    rects = []
    margin = 0.02
    width = 1 - margin - 0.02

    # Plot x values
    i = 0 # We only have one set of bars
    n = len(labels)
    x = np.array(range(n), dtype=np.float)
    rects.append(ax.bar(x + i*width + i*margin, fracs, width))
    autolabel(ax, rects[-1])
    ax.set_ylim([0,max(fracs)+1])
        
    plt.xticks(x, labels, rotation=40, fontsize=12)
    #ax.set_xticks(x + width) # Offset if more than one set
    plt.ylabel("%")
    plt.title("Percent of GAN Papers Including Terms")

    if save_name is not None:
        plt.savefig(save_name+".png", bbox_inches='tight')
        plt.savefig(save_name+".pdf", bbox_inches='tight')

if __name__ == '__main__':
    pandasSetPrint()

    # Paths to pdfgrep output
    grepGAN = 'grep/gan.txt'
    grepTL = 'grep/tl.txt'

    # Where to save lists
    listdir = 'list'

    # Read data
    df_gan = pd.read_csv(grepGAN, sep='\x00', names=['Filename','Match'])
    df_tl = pd.read_csv(grepTL, sep='\x00', names=['Filename','Term'])

    # Pick one set of TL terms
    df_tl['Term'] = replace(df_tl['Term'], {
        'multitask learning':     'multi-task learning',
        'multi task learning':    'multi-task learning',
        'multidomain learning':   'multi-domain learning',
        'multi domain learning':  'multi-domain learning',
        'self taught learning':  'self-taught learning',
        'co-variate shift':       'covariate shift',
        'sample selection bias':  'sample-selection bias',
        'life long learning':     'life-long learning',
        })

    #
    # Get GAN papers that also mention TL terms
    #
    gan = df_gan['Filename'].unique()
    tl = df_tl['Filename'].unique()
    ganCount = len(gan)
    tlCount = len(tl)

    # Pie chart of how many GAN papers include a mention of each of these terms
    both = df_tl.loc[df_tl['Filename'].isin(df_gan['Filename'])].drop_duplicates()
    papers = both['Filename'].unique()
    gantlCount = len(papers)
    terms = both['Term'].unique()

    termCounts = {}
    for t in terms:
        termCounts[t] = 0

    for p in papers:
        for t in both[both['Filename']==p]['Term']:
            termCounts[t] += 1

    fracs = [c/ganCount for c in termCounts.values()]
    labels = termCounts.keys()
    labels = [cap(l) for l in labels]
    fracs, labels = zip(*sorted(zip(fracs, labels), reverse=True)) # Sort
    #pie(fracs, labels, "pie")
    barplot([f*100 for f in fracs], labels, save_name="bar")

    # Print counts of papers
    print("GAN Papers:", ganCount)
    print("TL Papers:", tlCount)
    print("GAN & TL Papers:", gantlCount)

    # Print percentages
    print()
    print("Percent of GAN Papers Including Terms")
    for i in range(len(fracs)):
        print(" ",labels[i],"-","%.1f%%"%(fracs[i]*100))

    # Pie chart showing of the GAN papers how many include any of the TL terms
    includeTermsFracs = [(ganCount-gantlCount)/ganCount, gantlCount/ganCount]
    includeTermsLabels = ['No TL Terms', 'Include TL Term(s)']
    #pie(includeTermsFracs, includeTermsLabels, "pie_terms")

    title1="GAN Papers Mentioning Transfer Learning"
    title2="Transfer Learning Terms"
    pieCombined(
            includeTermsFracs, includeTermsLabels, title1,
            fracs, labels, title2,
            "pie")

    #
    # Output filenames for each of them
    #
    if not os.path.exists(listdir):
        os.makedirs(listdir)

    # When a single PDF (multiple rows) has multiple terms, join them to be
    # like: ("pdfName", "term1, term2, term3")
    grouped = df_tl.drop_duplicates().groupby('Filename').apply(lambda x: pd.Series({
            'Term': ', '.join(x['Term'].sort_values())
        })).reset_index()
    both_grouped = grouped.loc[grouped['Filename'].isin(df_gan['Filename'])].drop_duplicates()
    assert len(both_grouped) == len(papers), "Somehow grouped length different than overlap papers length"

    with open(os.path.join(listdir, 'overlap.txt'), 'w') as f:
        for index, row in both_grouped.iterrows():
            f.write(row['Filename']+'\t'+row['Term']+'\n')
    with open(os.path.join(listdir, 'gan.txt'), 'w') as f:
        for e in gan:
            f.write(e+'\n')
    with open(os.path.join(listdir, 'tl.txt'), 'w') as f:
        for e in tl:
            f.write(e+'\n')

    """
    pie(both['Term'], save_name='pie', pandas=True)

    # Pie chart of what TL terms are included in each GAN paper that mentions at least one
    #
    pie(both['Term'], save_name='pie_set', pandas=True)
    """
