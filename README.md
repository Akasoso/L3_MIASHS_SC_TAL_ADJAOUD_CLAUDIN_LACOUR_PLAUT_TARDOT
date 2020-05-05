# L3 MIASHS Science Cognitive : TAL

<img src="https://pbs.twimg.com/profile_images/1005007318558347264/RUwbCB00_400x400.jpg">

### Membres
ADJAOUD Sofiane, CLAUDIN Lou, LACOUR Émilien, PLAUT Grégoire, TARDOT William

### Préambule
Nous avons choisi, comme corpus, de télécharger en <i>xml</i> une page wikipédia : <a href="https://en.wikipedia.org/wiki/List_of_assassinations">List of assassinations</a>. Cette page recense tous les assassinats du monde entier, pays par pays. On y trouve quatre colonnes, pour la date, la victime, l'assassin et des informations supplémentaires. Nous l'avons donc téléchargé en anglais, pour que <b><i>nltk</i></b> puisse mieux reconnaitre les noms propres.

Une des limites de ce document est qu'il y a finalement assez peu d'assassins renseignés, ainsi, même si notre programme marche, il ne renvoie que quelques noms. la plupart des assasins sont inconnus.

C'était également compliqué de décoder le fichier <i>xml</i> généré. En effet, les colonnes n'existent plus en xml, et c'est donc compliqué une fois l'étiquettage en entité fait, de revenir en arrière pour trouver la ligne ou la colonne correspondante a une personne par exemple. 

### Installation
Afin de lancer notre programme, c'est très simple. Vous pouvez télecharger le github. Il faut juste mettre dans le même dossier les trois fichiers suivants : <i>main.py</i>, <i>FileSelecter.py</i> et <i>assassin.xml</i>.

#### Console
Pour lancer en version console, éxécuter le script <i>main.py</i>. Le programme va tout d'abord vous afficher le texte contenu dans le fichier xml, puis la liste de toutes les entités personnes, et enfin la liste des assassins dont le nom de famille commence par notre lettre, A.

#### Interfac Graphique
Nous vous proposons également une interface graphique pour éxécuter le code. Pour cela, vous avez juste besoin d'éxécuter le script <i>FileSelecter.py</i>. Vous pourrez alors tester les différentes options proposées.
