from Tkinter import *
import Tkinter as tk, os
import tkMessageBox
import codecs
import string
import nltk
import unicodedata
from collections import defaultdict
import math
import sys
root = tk.Tk()
f=tk.Frame(root,width=2000,height=1000,bd=1)
f.grid(row=0,column=0)
e = tk.StringVar()
e2=tk.StringVar()
w = tk.Label(f, text="ഇവിടെ എഴുതുക ")

w.grid(row=0,column=0)
E=tk.Entry(f,width=50, textvariable=e)
E.grid(row=0,column=1)
w1 = tk.Label(f, text="ഭലങ്ങൾ ")
w1.grid(row=1,column=0)
txt = tk.Text(f,relief="sunken")
txt.config(undo=True, wrap='word')
txt.grid(row=1, column=1,sticky="nsew")


scrollb = tk.Scrollbar(f,command=txt.yview)
scrollb.grid(row=1, column=2,sticky="nsew")
txt['yscrollcommand'] = scrollb.set
big_widget = tk.Canvas(root)
big_widget.grid(row=1, column=0)
document_filenames = {0 : "documents/mal1.txt",
                      1 : "documents/mal2.txt",
                      2 : "documents/mal3.txt"}


N = len(document_filenames)

dictionary = set()


postings = defaultdict(dict)


document_frequency = defaultdict(int)

length = defaultdict(float)


characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"
def search():
  while True:
    do_search()

def main():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    #while True:
    #do_search()
    b1 = tk.Button(f,text="തിരയുക ",command=search)
    b1.place(height=30, width=70,x=600,y=-4)

def initialize_terms_and_postings():

    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id],'r')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term)
def tokenize(document):

    terms = document.lower().split()
    return [term.strip(characters) for term in terms]

def initialize_document_frequencies():
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)

def imp(term,id):
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0

def do_search():
    query = tokenize(E.get())
    print query
    if query == []:
        sys.exit()
    relevant_document_ids = intersection(
            [set(postings[term].keys()) for term in query])
    print relevant_document_ids
    if relevant_document_ids==[]:
        print "No documents matched all query terms."
    else:
        scores = sorted([(id,similarity(query,id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1])
        print lambda x: x[1]
        print "Score: filename"
        for (id,score) in scores:
            print str(score)+": "+document_filenames[id]
            return True

def intersection(sets):
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()
    root.mainloop()