# L3 MIASHS Parcours Sciences Cognitives
# Traitement Automatique des Langues
## Projet : Trouver les assassins en "A"

<img src="https://pbs.twimg.com/profile_images/1005007318558347264/RUwbCB00_400x400.jpg" height=150px>

### Membres
ADJAOUD Sofiane, CLAUDIN Lou, LACOUR Émilien, PLAUT Grégoire, TARDOT William

### Préambule
Nous avons choisi, comme corpus, de télécharger en <i>xml</i> une page Wikipédia : <a href="https://en.wikipedia.org/wiki/List_of_assassinations">List of assassinations</a>. Cette page recense tous les assassinats du monde entier, pays par pays. On y trouve quatre colonnes, pour la date, la victime, l'assassin et des informations supplémentaires. Nous l'avons donc téléchargé en anglais, pour que <b><i>nltk</i></b> puisse mieux reconnaitre les noms propres.

Une des limites de ce document est qu'il y a finalement assez peu d'assassins renseignés, ainsi, même si notre programme marche, il ne renvoie que quelques noms. La plupart des assassins sont inconnus.

C'était également compliqué de décoder le fichier <i>xml</i> généré. En effet, les colonnes n'existent plus en xml, et c'est donc compliqué une fois l'étiquetage en entité fait, de revenir en arrière pour trouver la ligne ou la colonne correspondante à une personne par exemple. 

### Installation
Afin de lancer notre programme, c'est très simple. Vous pouvez télécharger le github. Il faut juste mettre dans le même dossier les quatre fichiers suivants : <i>main.py</i>, <i>FileSelecter.py</i>, <i>assassin.xml</i> et <i>assassin2.xml</i>.

#### Console
Pour lancer en version console, il suffit d'exécuter le script <i>main.py</i>. Le programme va tout d'abord vous afficher le texte contenu dans le fichier <i>xml</i>, puis la liste de toutes les entités personnes, et enfin la liste des assassins dont le nom de famille commence par notre lettre, 'A'.

#### Interface Graphique
Nous vous proposons également une interface graphique pour exécuter le code. Pour cela, vous avez juste besoin d'exécuter le script <i>InterfaceGraphique.py</i>. Vous pourrez alors tester les différentes options proposées. Vous pouvez par exemple choisir entre le fichier <i>assassin.xml</i> ou <i>assassin2.xml</i>. Le fichier <i>assassin2.xml</i> est un fichier <i>xml</i> de la page Wikipédia : <a href="https://en.wikipedia.org/wiki/List_of_assassinations_in_Europe">List of assassinations in Europe</a>. Nous voulions être sûrs que notre programme trouve des assassins en "A", avec d'autres corpus. La page des assassinats en Europe étant construite de la même manière que celle dans le monde, notre programme arrive à retrouver les assassins. 

Pour utiliser l'interface, vous avez différents boutons. Il faut tout d'abord ouvrir le fichier <i>assassin.xml</i> ou <i>assassin2.xml</i>, puis vous pouvez cliquer sur "Nettoyer/Traiter", afin d'enlever dans le texte les caractères non voulus. On peut ensuite cliquer sur "Noms Propres" afin d'afficher la liste de tous les noms propres détectés par <i>NLTK</i> (on peut d'ailleurs voir quelques erreurs). Enfin, en cliquant sur "Assassins Lettre A", on peut afficher la liste des assassins dont le nom de famille commence par "A".
