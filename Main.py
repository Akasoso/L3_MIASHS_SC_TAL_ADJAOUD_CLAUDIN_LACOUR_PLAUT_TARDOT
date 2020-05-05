# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:15:13 2020
@author: Gregoire
"""

#IMPORT



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
    text = root[1][3][8].text #avoir le texte de la balise texte (2eme balise, puis 4eme, puis 9eme)
    return text

# Supprime tous les caracteres inutiles du texte
#def prepare(text):
def clean(text):
    text = re.sub(r'(}}\n\|)(.*?)(\n\|)'," ", text) #enleve la ligne de la victime
    text = re.sub(r'<\s*\w*(.*?)\/*\s*\w*>',"", text) #enleve le texte entre '<...>'
    text = re.sub(r'[\|]'," ", text) #enleve les symboles '|' et les remplace par des espaces
    return text

# Separation de chaque tokens du texte et categorisation
def preprocess(doc):
    #doc = nltk.sent_tokenize(doc)
    doc = nltk.word_tokenize(doc)
    doc = nltk.pos_tag(doc)
    return doc

# Categorisation des personnes
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


print('---------------------------------------------------------------------')
print("Texte nettoyé, sans caractères inutiles :")
print('---------------------------------------------------------------------')
print(cleanText)


# Preprocessing :

text = preprocess(cleanText)
chunks = nltk.ne_chunk(text) #Entités nommés séparées en PERSON, ORGA, GPE...

tree = tree2conlltags(chunks)
extractTree = wordextractor(tree)


print('---------------------------------------------------------------------') 
print("Texte balisée avec NLTK, voici maintenant les noms propres trouvées : ")
print('---------------------------------------------------------------------')

line = "" #Chaque ligne contenant la liste d'entités composant une personnes. Ex : [('James', 'NNP'), ('Charles', 'NNP'), ('Kopp', 'NNP')]
listAPerson = [] #Liste assassins dont le nom commence par A

named_entities = []
# parcours les sous arbres 
for t in chunks.subtrees():
    # si c'est une personne
    if t.label() == 'PERSON':
        print(t.leaves()) 
        line = t.leaves() #recuperer la personne actuelle dans notre line
        lastname = line[len(line)-1][0] #le dernier mot de cette liste est le nom de famille. Ex : 'Kopp'
        firstname = "" #les autres sont ses prénoms
        for i in range(len(line)-1): #On parcourt toutes la liste de prénoms
            firstname = firstname + " " + line[i][0] #et on les ajoute. Ex : 'James Charles'
        if(lastname[0] == 'A' and firstname != "" and lastname != "" and lastname != "Assassinations" and lastname != "Alliance" and lastname != "Army" and lastname != "Assassination" and lastname != "Assassinated" and lastname != "Ana" and lastname != "Archdiocese"): 
            #On affiche tous ceux dont le nom de famille commence par A, et on retire certains mots si notre extracteur s'est trompé dans la catégorisation
            name = firstname + " " + lastname 
            if name not in listAPerson: #On ajoute cette personne à la liste si elle n'y est pas déjà
                listAPerson.append(name)
            
        named_entities.append(t.leaves())  
#print (named_entities)
        
    
print('---------------------------------------------------------------------')
print("Parmi ceux la, voici les assassins dont le nom commence par 'A'")
print('---------------------------------------------------------------------')

print(listAPerson) #On affiche la liste des assassins, en String



#FIN

