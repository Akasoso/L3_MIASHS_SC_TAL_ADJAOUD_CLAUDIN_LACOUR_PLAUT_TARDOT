# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:41:27 2020

@author: MSI-Sofiane
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, qApp, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
#import subprocess
class Accueil(QMainWindow):
    def __init__(self):
        super().__init__()
        self.afficherGUI()
    
    def selectFile(self):
        file = str(QFileDialog.getOpenFileName(self, "Sélectionner un fichier"))
        print(file)
        return file

    def afficherGUI(self):
        
        self.resize(1000, 300)
        self.setWindowTitle("Charger un fichier")
        bar = self.menuBar()
        fileMenu = bar.addMenu("Fichier")
        parametersMenu = bar.addMenu("Paramètres")
        helpMenu = bar.addMenu("Aide")

        quit = QAction("Quitter", self)
        quit.setShortcut("Ctrl+Q")
        fileMenu.addAction(quit)
        quit.triggered.connect(qApp.exit)
        
        mode = QAction("Aucun paramètre", self)
        mode.setShortcut("Ctrl+M")
        parametersMenu.addAction(mode)

        summary = QAction("Sommaire", self)
        summary.setShortcut("Ctrl+S")
        helpMenu.addAction(summary)

        about = QAction("À propos", self)
        about.setShortcut("Ctrl+A")
        helpMenu.addAction(about)
        
        # File selection
        label = QLabel("Fichier source")
        fileField = QLineEdit()
        openFileButton = QPushButton("Ouvrir", self)
        openFileButton.clicked.connect(self.selectFile)
        #subprocess.call("start python ./temp.py")
        #QObject.connect(openFileButton, SIGNAL("clicked()"), self.selectFile)
        hboxFile = QHBoxLayout()
        hboxFile.addWidget(label)
        hboxFile.addWidget(fileField)
        hboxFile.addWidget(openFileButton)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hboxFile)

        normalMode = QWidget()
        normalMode.setLayout(vbox)
        self.setCentralWidget(normalMode)
        self.show()
        

appli = QApplication(sys.argv)
W = Accueil()
sys.exit(appli.exec_())