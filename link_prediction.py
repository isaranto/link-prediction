# -*- coding: greek -*-
from __future__ import division
import os
import zipfile
import networkx as nx
import pickle
import string
import nltk


class FeatureExtraction:
    def __init__(self):
        if os.path.isfile('cache/processed_text.pickle'):
            with open('cache/processed_text.pickle', 'rb') as pfile:
                raw_text = pickle.load(pfile)
            print "loaded from pickle"
        else:
            filenames = os.listdir('dataset/hosts')
            raw_text = {}
            for zipfilename in filenames:
                with zipfile.ZipFile('dataset/hosts/'+zipfilename) as z:
                    text = ""
                    for filename in z.namelist():
                        if not os.path.isdir(filename):
                            with z.open(filename) as f:
                                for line in f:
                                    text += line.decode("utf-8").lower()
                                    text += " "
                    raw_text[zipfilename[:-4]] = text
            self.text = self.process_text(raw_text)
            with open('cache/processed_text.pickle', 'wb') as pfile:
                pickle.dump(self.text, pfile)


    def process_text(self, data):
        with open('dataset/greekstopwords.txt', 'r') as fp:
            stopwords = []
            for line in fp:
                stopwords.append(line.strip().decode('utf-8').lower())
        for domain in data.keys():
            text = data[domain]
            # remove punctuation
            punctuation = set(string.punctuation)
            doc = ''.join([w for w in text if w not in punctuation])
            # remove stopwords
            doc = [w for w in doc.split() if w not in stopwords]
            doc = ' '.join(w for w in doc)
            data[domain] = doc
        return data


if __name__ == '__main__':
    fex = FeatureExtraction()