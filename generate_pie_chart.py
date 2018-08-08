#!/usr/bin/env python3
"""
From the pdfgrep output data, generate a pie chart
"""
import pandas as pd

def replace(df, replacements):
    """
    If replacements={'s': 'r'} then replace all 's' with 'r' in dataframe df.
    """
    for s, r in replacements.items():
        df = df.str.replace(s, r)

    return df

def pandasSetPrint():
    """ Make it so we can see the output """
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.expand_frame_repr = False

if __name__ == '__main__':
    # Paths to pdfgrep output
    grepGAN = 'grep/gan.txt'
    grepTL = 'grep/tl.txt'

    # Read data
    df_gan = pd.read_csv(grepGAN, sep='\x00', names=['Filename','Match'])
    df_tl = pd.read_csv(grepTL, sep='\x00', names=['Filename','Term'])

    # Pick one set of TL terms
    df_tl['Term'] = replace(df_tl['Term'], {
        'multitask learning':     'multi-task learning',
        'multi task learning':    'multi-task learning',
        'multidomain learning':   'multi-domain learning',
        'multi domain learning':  'multi-domain learning',
        'co-variate shift':       'covariate shift',
        'sample selection bias':  'sample-selection bias',
        'life long learning':     'life-long learning',
        })

    #print(df_tl.groupby(''))
    #print(df_tl)

    # Get GAN papers that also mention TL terms
    pandasSetPrint()
    both = df_tl.loc[df_tl['Filename'].isin(df_gan['Filename'])].drop_duplicates()

    # Pie chart
    ax = both['Term'].value_counts().plot.pie(
            figsize=(7, 7),
            radius=0.7,
            autopct='%.0f%%')
    ax.set_title("")
    ax.set_ylabel("")
    ax.set_xlabel("")
    fig = ax.get_figure()
    fig.savefig('pie.png')
    fig.savefig('pie.pdf')
