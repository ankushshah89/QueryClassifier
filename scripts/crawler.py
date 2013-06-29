'''
Created on Jun 21, 2013

@author: shah
@email: ankush.shah.nitk@gmail.com

Description: A crawler to extract all structure or meaningful text from a website. 

'''

from BeautifulSoup import BeautifulSoup
from nltk import *
import os
import re
import urllib2

def get_text(url):
    """get the text from a http page"""
    print "getting text for " + url
    try:
        html = urllib2.urlopen(url).read()    
    except:
        return ""
    text = clean_html(html)  
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            clean_lines.append(clean_line)
    clean_text = "\n".join(clean_lines)
    return clean_text
    
def get_urls(seed_url,depth=1):
    content = urllib2.urlopen(seed_url).read()
    urls = []
    soup = BeautifulSoup(content)
    for a in soup.findAll('a',href=True):
        url = a['href']
        if url[0] == "/":
            urls.append(seed_url+url)
        else:
            urls.append(url)
    return urls
    
def save_data():
    seed_url = "http://www.zappos.com"
    text  = get_text(seed_url)
    ipage = 0
    f = open('../data/zappos/'+str(ipage),'w');f.write(text);f.close()
    urls = get_urls(seed_url)
    for url in urls:
        ipage += 1
        text = get_text(url)
        f = open('../data/zappos/'+str(ipage),'w');f.write(text);f.close()

def get_corpus_data():
    files = os.listdir('../data/zappos')
    lines = []
    for file in files:
        f = open(file,'r')
        lines += f.readlines()
        f.close()
    return "\n".join(lines)
        
def get_keywords():
    bigram_measures = collocations.BigramAssocMeasures()
    trigram_measures = collocations.TrigramAssocMeasures()
    
    # change this to read in your data
    finder = BigramCollocationFinder.from_words('../data/zappos/corpus.txt')
    
    # only bigrams that appear 3+ times
    finder.apply_freq_filter(3) 
    
    # return the 10 n-grams with the highest PMI
    finder.nbest(bigram_measures.pmi, 10)  


if __name__ == '__main__':
    get_keywords()