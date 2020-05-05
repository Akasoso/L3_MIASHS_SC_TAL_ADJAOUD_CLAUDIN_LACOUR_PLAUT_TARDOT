# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:47:12 2020
@author: MSI-Sofiane
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, qApp, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
import nltk
import re
import lxml.etree as ET
from nltk.chunk import tree2conlltags


class Accueil(QMainWindow):
    rawText = ""
    nomFile = " "
    cleanText = ""
    fileField = 0
    inputField = 0
    outputField = 0
    bouton1 = ""
    bouton2 = ""
    bouton3 = ""
    
    
    def __init__(self):
        super().__init__()
        self.afficherGUI()
    
    #FUNCTIONS
        
    def selectFile(self):
        file = str(QFileDialog.getOpenFileName(self, "Sélectionner un fichier"))
        file = re.sub(r'[\(\'].*?[\',)]',"",file)
        nomFile = re.split(r'(\w*).xml',file)
        self.nomFile = nomFile[1]
        print("Ouverture du fichier " + self.nomFile + ".xml")
        self.fileField.setText(file)
        self.rawText = self.transformer(file)
        self.inputField.setText(self.rawText)
        self.bouton1.setDisabled(0)
        self.bouton2.setDisabled(1)
        self.bouton3.setDisabled(1)
        return file

    
    # Transforme le .xml en texte brut
    def transformer(self, nomfichier):
        tree1 = ET.parse(nomfichier)
        root = tree1.getroot()
        if(self.nomFile == "assassin2"):
            text = root[1][3][7].text #avoir le texte de la balise texte (2eme balise, puis 4eme, puis 8eme)
        else:
            text = root[1][3][8].text #avoir le texte de la balise texte (2eme balise, puis 4eme, puis 9eme)
        return text
    
    # Supprime tous les caracteres inutiles du texte
    def clean(self, text):
        text = re.sub(r'(}}\n\|)(.*?)(\n\|)'," ", text) #enleve la ligne de la victime
        text = re.sub(r'<\s*\w*(.*?)\/*\s*\w*>',"", text) #enleve le texte entre '<...>'
        text = re.sub(r'[\|]'," ", text) #enleve les symboles '|' et les remplace par des espaces
        return text
    
    # Separation de chaque tokens du texte et categorisation
    def preprocess(self, doc):
        doc = nltk.word_tokenize(doc)
        doc = nltk.pos_tag(doc)
        return doc
    
    def wordextractor(self, tuple1):
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
    
    def traiter(self): 
        # Nettoyage :
        # On enleve dans ce texte tous les caractères inutiles, afin de ne traiter que du texte français
        self.cleanText = self.clean(self.rawText)
        str1 ='---------------------------------------------------------------------\n'
        str2 ="Texte nettoyé, sans caractères inutiles :\n"
        str3 ='---------------------------------------------------------------------\n'
        self.inputField.setText(str1+str2+str3+self.cleanText)
        self.bouton2.setDisabled(0)
    
    def nomPropres(self):
        # Preprocessing :
        text = self.preprocess(self.cleanText)
        chunks = nltk.ne_chunk(text) #Entités nommés séparées en PERSON, ORGA, GPE...
        
        tree = tree2conlltags(chunks)
        self.extractTree = self.wordextractor(tree)
        
        
        str1=('---------------------------------------------------------------------\n') 
        str2=("Texte balisée avec NLTK, voici maintenant les noms propres trouvées : \n")
        str3=('---------------------------------------------------------------------\n')
        
        line = "" #Chaque ligne contenant la liste d'entités composant une personnes. Ex : [('James', 'NNP'), ('Charles', 'NNP'), ('Kopp', 'NNP')]
        self.listAPerson = [] #Liste assassins dont le nom commence par A
        
        named_entities = []
        # parcours les sous arbres 
        for t in chunks.subtrees():
            # si c'est une personne
            if t.label() == 'PERSON':
                named_entities.append(t.leaves())  
        
        strname="NOM : "
        strDec = ""
        for name in named_entities:
            for i in range(len(name)):
                strDec = strDec + " " + name[i][0]
            strname = strname + strDec + "  (NNP)" + '\nNOM : '
            strDec = ""
        self.outputField.setText(str1+str2+str3+strname)
        self.bouton3.setDisabled(0)
        
    def AssassinA(self):
        # Preprocessing :
        text = self.preprocess(self.cleanText)
        chunks = nltk.ne_chunk(text) #Entités nommés séparées en PERSON, ORGA, GPE...
        
        tree = tree2conlltags(chunks)
        self.extractTree = self.wordextractor(tree)
        
        str1 = ('---------------------------------------------------------------------\n')
        str2 = ("Parmi ceux la, voici les assassins dont le nom commence par 'A'\n")
        str3 = ('---------------------------------------------------------------------\n')
        
        line = "" #Chaque ligne contenant la liste d'entités composant une personnes. Ex : [('James', 'NNP'), ('Charles', 'NNP'), ('Kopp', 'NNP')]
        listAPerson = [] #Liste assassins dont le nom commence par A
        
        # parcours les sous arbres 
        for t in chunks.subtrees():
            # si c'est une personne
            if t.label() == 'PERSON':
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
                    
        strname=""
        for name in listAPerson :
            strname = strname + self.convertTuple2(name) + '\n'
        self.outputField.setText(str1+str2+str3+strname) #On affiche la liste des assassins, en String
    
    def convertTuple(self, tup): 
        str =  '          TAG : '.join(tup) 
        return str
        
    def convertTuple2(self, tup): 
        str =  ''.join(tup) 
        return str
    
    def afficherGUI(self):
        
        self.resize(1000, 800)
        self.setWindowTitle("Application TAL")
        bar = self.menuBar()
        fileMenu = bar.addMenu("Fichier")
        parametersMenu = bar.addMenu("Paramètres")
        helpMenu = bar.addMenu("Aide")

        quit = QAction("Quitter", self)
        quit.setShortcut("Ctrl+Q")
        fileMenu.addAction(quit)
        quit.triggered.connect(qApp.exit)
        
        mode = QAction("Utilisation", self)
        mode.setShortcut("Ctrl+M")
        parametersMenu.addAction(mode)

        summary = QAction("Options", self)
        summary.setShortcut("Ctrl+S")
        helpMenu.addAction(summary)

        about = QAction("À propos", self)
        about.setShortcut("Ctrl+A")
        helpMenu.addAction(about)
        
        # File selection
        label = QLabel("Fichier source")
        self.fileField = QLineEdit()
        openFileButton = QPushButton("Ouvrir", self)
        openFileButton.clicked.connect(self.selectFile)
        hboxFile = QHBoxLayout()
        hboxFile.addWidget(label)
        hboxFile.addWidget(self.fileField)
        hboxFile.addWidget(openFileButton)

        # Sentence source
        label = QLabel("Corpus") # mettre éventuellement le label en « placeholder » du champ texte
        self.inputField = QTextEdit()
        hboxInput = QHBoxLayout()
        hboxInput.addWidget(label)
        hboxInput.addWidget(self.inputField)

        #♥ Boutons
        self.bouton1 = QPushButton("Nettoyer/Traiter")
        self.bouton2 = QPushButton("Noms propres")
        self.bouton3 = QPushButton("Assassins Lettre A")
        self.bouton1.setDisabled(1);
        self.bouton2.setDisabled(1);
        self.bouton3.setDisabled(1);
        hboxButton = QHBoxLayout()
        hboxButton.addWidget(self.bouton1)
        hboxButton.addWidget(self.bouton2)
        hboxButton.addWidget(self.bouton3)
        self.bouton1.clicked.connect(self.traiter)
        self.bouton2.clicked.connect(self.nomPropres)
        self.bouton3.clicked.connect(self.AssassinA)
        
        # Texte en sortie
        label = QLabel("Résultat")
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        hboxOutput = QHBoxLayout()
        hboxOutput.addWidget(label)
        hboxOutput.addWidget(self.outputField)

        vbox = QVBoxLayout()
        vbox.addLayout(hboxFile)
        vbox.addLayout(hboxInput)
        vbox.addLayout(hboxButton)
        vbox.addLayout(hboxOutput)
     

        normalMode = QWidget()
        normalMode.setLayout(vbox)
        self.setCentralWidget(normalMode)
        self.show()

    

appli = QApplication(sys.argv)
W = Accueil()
sys.exit(appli.exec_())
