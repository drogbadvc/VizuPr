# VizuPr (Simple crawler + algorithme de visualisation)

Dépôt pour un brouillon d'outil de visualisation de la structure d'un site internet. 
En pratique le script en l'état (crawl) un site simplement en enregistrant dans une base SQLite (Nœuds, Urls, html, rank ...)
Puis il stocke dans un json plus de données de la structure html et calcul du PageRank aléatoire avec choix de plusieurs itérations. 

Niveau Front HTML : 

- Vue de la structure via plusieurs algorithme comme ForceAtlas2 (**instable**), ForceinaBox, Force Layout et FirstLink.
- Une liste des urls du site avec des informations de chaque page (Rank, code status, Titre ...)

## Prérequis
- Apache Web (**!important**)
- Sqlite3 (https://doc.ubuntu-fr.org/sqlite)
- Python 2.7 (urllib2, BeautifulSoup ...) [*note](#notes-importantes)
- D3.js (https://github.com/d3/d3/wiki) 
- SigmaJS (https://github.com/jacomyal/sigma.js/)

## Par quoi commencer

- Pour commencer il faut lancer un premier crawl avec l'url d'un site Internet et le nombre de Pages [*Note](#notes-importantes)
```bash
python bin/spider.py
```
- Lancer le calcul du PageRank avec le nombre d'itérations. Plus le site est important, plus le calcul est lent. Stockage du résultat dans la base de donnée. 
Possibilité de lancer plusieurs fois pour affiner le classement. [*note](#notes-importante)
```bash
python bin/sprank.py
```
- Pour stocker tout dans un Json (spider.js). On lance une dernière commande python. Lente selon le nombre de Nœuds.
```bash
python bin/spjson.py
```
- Pensez à mettre les droits sur le dossier **Public**
```bash
chmod -R 777 public
```
- Pour finir, il faut lancer un fichier Php qui permet de récupérer le premier Nœud pour chaque lien comme le fait (ScreamingFrog). [*note](#notes-importantes)
```bash
php MakeLinkCsv.php
```
- Vous pouvez lancer le fichier directement dans le navigateur. Notamment si vous avez **XAMPP**.

## Pour aller plus loin

- Vider la base de donnée
 ```bash
rm spider.sqlite
```
- Remettre à zéro le PageRank de chaque page d'un site.
 ```bash
python bin/spreset.py
```

## D3 && SigmaJS

### force.html
- Force.html utilise Force Layout de D3.js pour visualiser la structure du site (impossible de voir les silos).
- Un PageRank = une couleur. La taille des cercles correspondant à la puissance du PR.

### Hierarchy.html
- En cliquant sur chaque cercle, un modal s'ouvre avec les infos de la page liée au cercle.
- Force Layout peut bouger après quelques secondes l'éxecution de la page. Les nœuds peuvent encore bouger.

#### Activer le Drag (déplacement des nœuds)
```javascript
.call(
d3
  .drag()
  .on("start", dragstarted)
  .on("drag", dragged)
  .on("end", dragended)
     );                                       
```

### forceatlas2.html
- Forceatlas2.html utilise SigmaJS avec le module ForceAtlas2 (cause des bugs sur petit ordinateur).
- L'algo travaille en live et les Nœuds se déplacent (Processeur sollicité). 
- Plus d'informations ici (https://github.com/jacomyal/sigma.js/tree/master/plugins/sigma.layout.forceAtlas2)

#### Cause Freeze
 ```javascript
barnesHutTheta: 1.4,
startingIterations: 10,
iterationsPerRender: 10
```

## MD5.JS ?
- Ce fichier Javacript est l'équivalent de la fonction php
```php
md5($string);
```
- Technique bourrin qui me permet d'avoir une même couleur (string) pour les titres dupliqués.

## Notes importantes

- Le crawler python utilise **urllib2** obsolète sans Multithreading. Trop basique, le but était de passer à Python 3 et [Crowl](https://gitlab.com/crowltech)
- Script Python incompatible avec Python3 (Prévoir refactoring).
- PageRank aléatoire. Le but était de passer au PageRank raisonnable ([source](https://www.youtube.com/watch?v=qHMvNCo-otc))
J'avais commencé un brouillon pour classer les liens sur la visu par thématique (https://fasttext.cc/). Il donne de bon résultat mais pas intégré (utilisable en commande).
- Le script Php crée un csv utilisé par D3 pour exécuter la visualisation dans Hierarchy && TreeCollaps.