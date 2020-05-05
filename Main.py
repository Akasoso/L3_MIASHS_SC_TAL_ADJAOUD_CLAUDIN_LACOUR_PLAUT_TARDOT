# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#DEBUT

import nltk
import re
import lxml.etree as ET
from nltk.chunk import tree2conlltags

#FUNCTIONS

# Transforme le .xml en texte brut
def transformer(nomfichier):
    #fichier = open(nomfichier, 'rb')
    #contenu = fichier.read()
    #tree1 = ET.parse(contenu)
    tree1 = ET.parse(nomfichier)
    root = tree1.getroot ()
    text = root[1][3][7].text #avoir le texte de la balise texte (2eme balise, puis 4eme, puis 8eme)
    return text

# Supprime tous les caracteres inutiles du texte
#def prepare(text):
def clean(text):
    text = re.sub(r'[\]]',"", text) #enleve les symboles ']'
    text = re.sub(r'[\[]',"", text) #enleve les symboles '['
    text = re.sub(r'[\|]'," ", text) #enleve les symboles '|' et les remplace par des espaces
    text = re.sub(r'<\s*\w*(.*?)\/*\s*\w*>',"", text) #enleve le texte entre '<...>'
    text = re.sub(r'({{)(.*?)(}})',"", text) #enleve le texte entre '{{...}}' 
    return text

# Separation de chaque tokens du texte et categorisation
def preprocess(doc):
    #doc = nltk.sent_tokenize(doc)
    doc = nltk.word_tokenize(doc)
    doc = nltk.pos_tag(doc)
    return doc

def wordextractor(tuple1):
    #bring the tuple back to lists to work with it
    words, tags, pos = zip(*tuple1)
    words = list(words)
    pos = list(pos)
    c = list()
    i=0
    while i<= len(tuple1)-1:
        #get words with have pos B-PERSON or I-PERSON
        if pos[i] == 'B-PERSON':
            c = c+[words[i]]
        elif pos[i] == 'I-PERSON':
            c = c+[words[i]]
        i=i+1
    return c

#def test(tree):
#    d = list()
#    for i in tree:
#        if tree[i][2] == 'B-PERSON' or tree[i][2] == 'I-PERSON':
#            d = d+[tree[i]]
#    return d


#MAIN

# Preparation :
# telecharger https://en.wikipedia.org/wiki/Special:Export/List_of_assassinations
# renommer en "assassin.xml" et mettre dans le meme dossier que le script
# On ne garde que la balise xml text, pour traiter non plus un fichier xml mais un texte
rawText = transformer("./assassin.xml")
#print("Texte brut : \n" +rawText)
#print(rawText)

# Nettoyage :
# On enleve dans ce texte tous les caractères inutiles, afin de ne traiter que du texte français
#rawText = prepare(rawText)
cleanText = clean(rawText)
#print("Texte nettoye : \n" +cleanText)
#print(cleanText)

# PREPROCESSING :
#text = preprocess(rawText)
text = preprocess(cleanText)
#chunks = nltk.ne_chunk(text, binary=True)    #EN = entites nommees
chunks = nltk.ne_chunk(text) #Entités nommés séparées en PERSON, ORGA, GPE...
#https://stackoverflow.com/questions/31836058/nltk-named-entity-recognition-to-a-python-list
tree = tree2conlltags(chunks)
#testTree = test(tree)
extractTree = wordextractor(tree)

# Patterns
#pattern = 'PERSON: {<NNP>*}'

# Parsing
#cp = nltk.RegexpParser(pattern)
#cs = cp.parse(tagged)
#cs = cp.parse(text)
#print(cs)

print('---------------------------------------------------------------------') 
print("Texte balisée avec NLTK, voici maintenant les noms propres trouvées : ")

named_entities = []
# parcours les sous arbres 
for t in chunks.subtrees():
    # if its a N.E , appeend to list of names entities
    #if t.label() == 'NE':
    if t.label() == 'PERSON':
        #print(t.leaves())
        named_entities.append(t.leaves())  
#print (named_entities)
    
print('---------------------------------------------------------------------')

#named_entities2 = []
# parcours les sous arbres 
#for y in chunks2.subtrees():
    # if its a N.E , appeend to list of names entities
    #if y.label() == 'PERSON':
        ##print(t.leaves())
        #named_entities2.append(t.leaves())  
#print (named_entities2) #affichage liste des personnes

#TRI DES NOMS PROPRES POUR GARDER CEUX QUI COMMENCE PAR A
#(A([\w-]*)+) # selectionne les mots commençant par ‘A’ (majuscule)
#pattern = re.compile("^(\w*\s)*A(\w*\s?)+")#regex noms commençant par A

#A FAIRE
        
print('DONE !')

#FIN
