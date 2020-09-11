import tkinter as tk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from operator import itemgetter 
import numpy as np
import re
import nltk
import bs4 as bs  
import urllib.request 
import pandas as pd
import collections

def online(url,lbl,lb1):
    #Converts in both With Punctuations and Without Punctuations
    with_punct,wo_punct=extractdata(url)
    #Generate Sentences
    sentences=nltk.sent_tokenize(with_punct)
    #Divide the Summary to 1/4
    N=int(len(sentences)/4)
    #Summarizes the Paragraph
    Summary,reduced_text = textrank(sentences,N,stopwords=stopwords.words('english'))
    #POS tagging of Noun of Reduced text
    nounf=POStag(wo_punct)
    #Create list of sentences for each noun
    a=findword(reduced_text,nounf.keys())
    #Create Summary of Each noun
    Final_Summary=SummArray(a)
    #Remove Duplications from the Summary
    temp=nltk.sent_tokenize(Final_Summary)
    aa=unique(temp)
    Disha= ' '.join(aa)
    return(lbl.config(text=''+Disha,borderwidth=2, relief="solid"),lbl.place(x = 250, y = 410, width=850, height=300),lb1.config(text='Summary',bg='skyblue',font=("Courier", 20)),lb1.place(x = 250, y = 380, width=150, height=30))

def offline(path,lbl,lb1):
    text_file = open(path, "r")
    text = text_file.read()
    text_wp=text.replace('\n', ' ')
    text_wop= re.sub('[^a-zA-Z]', ' ',text_wp)  
    text_wop= re.sub(r'\s+', ' ', text_wop)
    sentences=nltk.sent_tokenize(text_wp)
    N=int(len(sentences)/2)
    Summary,reduced_text = textrank(sentences,N,stopwords=stopwords.words('english'))
    #POS tagging of Noun of Reduced text
    nounf=POStag(text_wop)
    #Create list of sentences for each noun
    a=findword(reduced_text,nounf.keys())
    #Create Summary of Each noun
    Final_Summary=SummArray(a)
    #Remove Duplications from the Summary
    temp=nltk.sent_tokenize(Final_Summary)
    aa=unique(temp)
    Disha = ' '.join(aa)
    return(lbl.config(text=''+Disha,borderwidth=2, relief="solid"),lbl.place(x = 250, y = 410, width=850, height=300),lb1.config(text='Summary',bg='skyblue',font=("Courier", 20)),lb1.place(x = 250, y = 380, width=150, height=30))

def extractdata(path):
    meta_data = urllib.request.urlopen(path)  
    html = meta_data.read()
    phtml = bs.BeautifulSoup(html,'lxml')
    paragraphs = phtml.find_all('p')
    texta = ""
    #Converting text from HTML Paragraph TAGS 
    for p in paragraphs:  
        texta += p.text
    # Removing Square Brackets and Extra Spaces
    texta = re.sub(r'\[[0-9]*\]', ' ',texta)  
    texta = re.sub(r'\s+', ' ',texta)
    # Removing special characters and digits
    ftexta = re.sub('[^a-zA-Z]', ' ',texta)  
    ftexta = re.sub(r'\s+', ' ', ftexta)
    return texta, ftexta;

def pagerank(A, eps=0.0001, d=0.85):
    P = np.ones(len(A)) / len(A)
    while True:
        new_P = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P
        
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stopwords=None):
    # Create an empty similarity matrix
    S = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            S[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stopwords)
    # normalize the matrix row-wise
    for idx in range(len(S)):
        S[idx] /= S[idx].sum() 
    return S

def textrank(sentences, top_n, stopwords=None):
    S = build_similarity_matrix(sentences, stopwords) 
    sentence_ranks = pagerank(S) 
    # Sort the sentence ranks
    ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    Summary = itemgetter(*selected_sentences)(sentences)
    reduced_text=''.join(Summary)
    return Summary, reduced_text;

def POStag(text_wop):    
    words = nltk.word_tokenize(text_wop)
    POS = nltk.pos_tag(words)
    df = pd.DataFrame(POS)
    df.columns = ['Word', 'Tag']
    df_noun  = df.groupby('Tag').get_group('NN')
    noun = df_noun['Word'].tolist()
    Noun =[x.lower() for x in noun]
    filtered_noun=[]
    stop_words = set(stopwords.words('english')) 
    for w in Noun: 
        if w not in stop_words: 
            filtered_noun.append(w)
    counter=collections.Counter(filtered_noun)
    dc= pd.DataFrame([counter.keys(),counter.values()]).T
    dc.columns= ['Noun','Frequency']  
    dca=dc.sort_values(by=['Frequency'],ascending=False)
    dca=dca.reset_index()
    del dca['index']
    dcc=dca.head(int(dca.shape[0]/6))
    n=dcc['Noun'].tolist()
    f=dcc['Frequency'].tolist()
    nounf = dict(zip(n,f))
    return(nounf)

def findword(txt,n):
    final=[]
    for i in n:
        sent=[sentence + '.' for sentence in txt.split('.') if i in sentence]
        final.append(sent)
    b = [e for e in final if e]
    return(b)
    
def SummArray(a):
    sa=[]
    for i in range(0,len(a)):
        strr = ' '.join(a[i])
        strw = re.sub(r'[^\w\s]','',strr)
        #Calculates Word Count for Each Word Excluding Stopwords
        Word_Score=wordfreq(strw)
        #Sums up the Words scores and max sentences are Selected
        Sent_Score=sentencescore(strr,Word_Score)
        #Enter Number of Lines for the Summary
        N=int(len(a[i])*0.15)
        #Summarizes the Paragraph
        summ=summary(Sent_Score,N)
        sa.append(summ)
    SS=[e for e in sa if e]
    SUM= ' '.join(SS)
    return(SUM)
    
def wordfreq(ftexta):    
    stopwords = nltk.corpus.stopwords.words('english')
    frequency = {}  
    for word in nltk.word_tokenize(ftexta):  
        if word not in stopwords:
            if word not in frequency.keys():
                frequency[word] = 1
            else:
                frequency[word] += 1
    maximum_frequncy = max(frequency.values())
    for word in frequency.keys():  
        frequency[word] = (frequency[word]/maximum_frequncy)
    return(frequency)
    
def sentencescore(texta,frequency):    
    sentence_list = nltk.sent_tokenize(texta)  
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in frequency.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = frequency[word]
                    else:
                        sentence_scores[sent] +=frequency[word]
    return(sentence_scores)
    
def summary(sentence_scores,no):
    df= pd.DataFrame([sentence_scores.keys(),sentence_scores.values()]).T
    df.columns= ['Sentences', 'Scores']  
    dfa=df.sort_values(by=['Scores'],ascending=False)
    dfa=dfa.reset_index()
    del dfa['index']
    st=[]
    for i in range(0,no):
        st.append(dfa['Sentences'][i])
    summary=' '.join(st)
    return(summary)
    
def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]
    