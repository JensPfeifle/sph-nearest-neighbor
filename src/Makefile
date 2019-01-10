VERSION = 3.02
CC      = /usr/bin/g++
CFLAGS  = -O3 -Wall
PRJPATH = /home/jens/git/sph-nearest-neighbor

all: fr_ann fr_ann_query fr_cellLinkedList fr_nanoflann

fr_ann: fr_ann.cpp
	$(CC) $(CFLAGS) fr_ann.cpp -o$(PRJPATH)/bin/fr_ann -I$(PRJPATH)/ann_1.1.2/include -L$(PRJPATH)/ann_1.1.2/lib -lANN

fr_ann_query: fr_ann_query.cpp
	$(CC) $(CFLAGS) fr_ann_query.cpp -o$(PRJPATH)/bin/fr_ann_query -I$(PRJPATH)/ann_1.1.2/include -L$(PRJPATH)/ann_1.1.2/lib -lANN

fr_cellLinkedList: fr_cellLinkedList.cpp
	$(CC) $(CFLAGS) fr_cellLinkedList.cpp -o$(PRJPATH)/bin/fr_cellLinkedList -I$(PRJPATH)/ann_1.1.2/include -L$(PRJPATH)/ann_1.1.2/lib -lANN


fr_nanoflann: fr_nanoflann.cpp
	$(CC) $(CFLAGS) fr_nanoflann.cpp -o$(PRJPATH)/bin/fr_nanoflann -I$(PRJPATH)/ann_1.1.2/include -I$(PRJPATH)/nanoflann/include -L$(PRJPATH)/ann_1.1.2/lib -lANN
