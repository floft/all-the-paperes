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

def barplot(fracs, labels, colors=None, save_name=None):
    assert len(fracs) == len(labels)
    #colors = ["xkcd:orange", "xkcd:teal", "xkcd:darkgreen", "xkcd:orchid", "xkcd:blue", "xkcd:indigo"]
    
    fig, ax = plt.subplots(1,1,figsize=(8, 4))
    rects = []
    margin = 0.02
    width = 1 - margin - 0.02

    # Plot x values
    i = 0 # We only have one set of bars
    n = len(labels)
    x = np.array(range(n), dtype=np.float)
    if colors is not None:
        rects.append(ax.bar(x + i*width + i*margin, fracs, width, color=colors))
    else:
        rects.append(ax.bar(x + i*width + i*margin, fracs, width))
    autolabel(ax, rects[-1])
    ax.set_ylim([0,max(fracs)+5])
        
    plt.xticks(x, labels, rotation=50, fontsize=12)
    ax.set_xticks(x - width/2)
    plt.ylabel("%")
    plt.title("Percent of GAN Papers Including Terms")

    # Assuming highest is generative and lowest is TL
    ax.legend((rects[-1][0], rects[-1][-1]), ('Generation', 'Related to Transfer Learning'))

    if save_name is not None:
        plt.savefig(save_name+".png", bbox_inches='tight')
        plt.savefig(save_name+".pdf", bbox_inches='tight')

if __name__ == '__main__':
    pandasSetPrint()

    # Paths to pdfgrep output
    grepGAN = 'grep/gan.txt'
    grepTL = 'grep/tl.txt'
    grepGen = 'grep/generative.txt'

    # Where to save lists
    listdir = 'list'

    # Read data
    df_gan = pd.read_csv(grepGAN, sep='\x00', names=['Filename','Match'])
    df_tl = pd.read_csv(grepTL, sep='\x00', names=['Filename','Term'])
    df_gen = pd.read_csv(grepGen, sep='\x00', names=['Filename','Term'])

    # Pick one set of TL terms
    df_tl['Term'] = replace(df_tl['Term'], {
        'multitask learning':     'multi-task learning',
        'multi task learning':    'multi-task learning',
        'multidomain learning':   'multi-domain learning',
        'multi domain learning':  'multi-domain learning',
        'self taught learning':   'self-taught learning',
        'co-variate shift':       'covariate shift',
        'sample selection bias':  'sample-selection bias',
        'life long learning':     'life-long learning',
        })

    # Pick one set of generative terms
    df_gen['Term'] = replace(df_gen['Term'], {
        #'image generation':       'image generation',
        'generation of images':   'image generation',
        'image synthesis':        'image generation',
        #'synthesis':              'generation',
        'super-resolution':       'super resolution',
        })

    # Ignore some generative terms
    df_gen = df_gen[
            (df_gen['Term'].str.lower() != 'image completion') & \
            (df_gen['Term'].str.lower() != 'semantic segmentation') & \
            (df_gen['Term'].str.lower() != 'super resolution') & \
            (df_gen['Term'].str.lower() != 'synthesis') & \
            (df_gen['Term'].str.lower() != 'style transfer')]

    # "image generation" or "image synthesis" should be included in
    # "generation", so duplicate (later we'll remove duplicates)
    rows = df_gen[df_gen['Term'] == 'image generation']
    rows['Term'] = rows['Term'].str.lower().replace('image generation', 'generation')
    df_gen = pd.concat([df_gen, rows], ignore_index=True)

    #
    # Get GAN papers that also mention TL terms
    #
    gan = df_gan['Filename'].unique()
    tl = df_tl['Filename'].unique()
    gen = df_gen['Filename'].unique()
    ganCount = len(gan)
    tlCount = len(tl)
    genCount = len(gen)

    # Generative terms in GAN papers
    gen_both = df_gen.loc[df_gen['Filename'].isin(df_gan['Filename'])].drop_duplicates()
    genPapers = gen_both['Filename'].unique()
    gangenCount = len(genPapers)
    gen_terms = gen_both['Term'].unique()

    # Pie chart of how many GAN papers include a mention of each of these terms
    both = df_tl.loc[df_tl['Filename'].isin(df_gan['Filename'])].drop_duplicates()
    tlPapers = both['Filename'].unique()
    gantlCount = len(tlPapers)
    terms = both['Term'].unique()

    termCounts = {}
    for t in terms: # TL
        termCounts[t] = 0
    for t in gen_terms: # Generative
        termCounts[t] = 0

    for p in tlPapers: # TL
        for t in both[both['Filename']==p]['Term']:
            termCounts[t] += 1
    for p in genPapers: # Generative
        for t in gen_both[gen_both['Filename']==p]['Term']:
            termCounts[t] += 1

    fracs = [c/ganCount for c in termCounts.values()]
    labels = termCounts.keys()
    labels = [cap(l) for l in labels]
    fracs, labels = zip(*sorted(zip(fracs, labels), reverse=True)) # Sort
    #pie(fracs, labels, "pie")
    # See: https://matplotlib.org/users/dflt_style_changes.html
    colors = ['#1f77b4' if l.lower() in gen_terms else '#d62728' for l in labels]
    barplot([f*100 for f in fracs], labels, colors, save_name="bar")

    # Print counts of papers
    print("GAN Papers:", ganCount)
    print("TL Papers:", tlCount)
    print("Generative Papers:", genCount)
    print("GAN & TL Papers:", gantlCount)
    print("GAN & Generative Papers:", gangenCount)

    # Print percentages
    print()
    print("Percent of GAN Papers Including Terms")
    for i in range(len(fracs)):
        print(" ",labels[i],"-","%.1f%%"%(fracs[i]*100))

    # Pie chart showing of the GAN papers how many include any of the TL terms
    #includeTermsFracs = [(ganCount-gantlCount)/ganCount, gantlCount/ganCount]
    #includeTermsLabels = ['No TL Terms', 'Include TL Term(s)']
    #pie(includeTermsFracs, includeTermsLabels, "pie_terms")

    # Note: this is wrong now since the terms don't just include TL terms but
    #       others like "image generation"
    #title1="GAN Papers Mentioning Transfer Learning"
    #title2="Transfer Learning Terms"
    #pieCombined(
    #        includeTermsFracs, includeTermsLabels, title1,
    #        fracs, labels, title2,
    #        "pie")

    #
    # Output filenames for each of them
    #
    if not os.path.exists(listdir):
        os.makedirs(listdir)

    with open(os.path.join(listdir, 'gan.txt'), 'w') as f:
        for e in gan:
            f.write(e+'\n')
    with open(os.path.join(listdir, 'tl.txt'), 'w') as f:
        for e in tl:
            f.write(e+'\n')
    with open(os.path.join(listdir, 'generative.txt'), 'w') as f:
        for e in gen:
            f.write(e+'\n')

    # When a single PDF (multiple rows) has multiple terms, join them to be
    # like: ("pdfName", "term1, term2, term3")
    tl_grouped = df_tl.drop_duplicates().groupby('Filename').apply(lambda x: pd.Series({
            'Term': ', '.join(x['Term'].sort_values())
        })).reset_index()
    tl_both_grouped = tl_grouped.loc[tl_grouped['Filename'].isin(df_gan['Filename'])].drop_duplicates()
    assert len(tl_both_grouped) == len(tlPapers), "Somehow tl_grouped length different than overlap papers length"

    with open(os.path.join(listdir, 'overlap.txt'), 'w') as f:
        for index, row in tl_both_grouped.iterrows():
            f.write(row['Filename']+'\t'+row['Term']+'\n')

    """
    pie(both['Term'], save_name='pie', pandas=True)

    # Pie chart of what TL terms are included in each GAN paper that mentions at least one
    #
    pie(both['Term'], save_name='pie_set', pandas=True)
    """
