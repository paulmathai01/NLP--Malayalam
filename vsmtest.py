
from collections import defaultdict
import math
import sys

document_filenames = {0 : "documents/mal1.txt",
                      1 : "documents/mal2.txt",
                      2 : "documents/mal3.txt"}

N = len(document_filenames)
print N
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
    search()

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
    query = tokenize(raw_input("Search query >> "))
    print query
    if query == []:
        sys.exit()
    relevant_document_ids = intersection(
            [set(postings[term].keys()) for term in query])
    print relevant_document_ids
    if not relevant_document_ids:
        print "No documents matched all query terms."
    else:
        scores = sorted([(id,similarity(query,id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1])
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
