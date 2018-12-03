## Inhalt
1. Recherche
    1. Problembeschreibung
    2. Verfahren
        1.  Mindmap
        2.  https://scikit-learn.org/stable/modules/neighbors.html
    3. Wieso ANN?

2. Vorgehen
    1. Einfaches test case erstellt 2D
    2. Test mit einem/vordefinierten query points (fixed_radius_ann.cpp)
    3. 

## Testfälle

Since the fill is discrete (set spacing), the fill ratio is not able to be realized exactly. Because of this, the user defines a "fillfactor", which must be slightly adjusted to get the correct final fill ratio.



## Outlook
* update kdtree instead of re-calculating (-> "dynamic" search)
* test approximate search methods


## Lessons learned
* Achtung, wenn rf_ann die falsche dimension bekommt merk man das nicht! Es wird beim einlesen nicht zw. tabs und newlines unterschieden.