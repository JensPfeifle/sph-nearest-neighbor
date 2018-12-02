2018.11.21
=======
* Statisch oder dynamisch?
    * statisch = tree wird jedes mal neu aufgebaut
    * dynamisch = tree wird bei jeder iteration angepasst
    * entscheidung: statisch, da einfacher
    * eventueller performancevorteil kann gegen ende getestet werden
* Exact oder approximate?
    * entscheidung: exakt, da approximate nur gehen würde, wenn man den radius für alle etwas vergrößert. Performancevorteil wieder dahin?
    * eventuell testen, ist ja nur ein Parameter
* Koordinaten können auch negativ sein
* Parallelisierung im Hinterkopf behalten, der Testdomain hier ist nur ein Rechengebiet
* Befüllungsgrad
    * verschiedene Varianten testen:
        * viele kleine Gebiete oder wenige große
        * streifen
        * checkerboard
        * diagonal von Ecken
    * gibt es einen Performanceunterschied?
    * wann wäre die naive Suche vielleicht sogar besser?
* Auf die Genauigkeit bei Python achten (double)
* Zeitmessung, mind. 3x hintereinander
* Marc recherchiert Listensuche, falls nicht copy/paste selbst implementieren
* Ausarbeitung darf auf Englisch sein


2018.11.29
=======

- 2D tests nicht wirklich relevant, nur wenn für Entwicklung schneller/einfacher oder zur Visualisierung
- Es gibt an sich keine homogene Partikelverteilung bzw. keinen minimalen Abstand bzw. keine "dichteste Packung"
- Timing im C code
    - über chrono
    - Gesamtdauer + Abschnitte einzelnd:
        - k suche (erste ANN suche)
        - fr suche (zweite ANN suche)
        - Listenerstellung
- Weitere Statistiken:
    - avg min max # of neighbors
    - avg distances
- Testfälle etwas begrenzen:
    - jeweils leer, mittel, voll
    - clusters, stripes, mass
- Optimierungsvorschläge: 
    - wenn datapt einmal ein querypt war, kann er aus der suche rausgenommen werden
    - map statt vektor
    - statische arrays statt vektor
- Aktuelle suche im SPH code ist Linked Cell Method
- bdtrees wohl gut, wenn suchraum sparse besetzt, kann man das einfach verschen bzw mit fixed radius kombinieren?