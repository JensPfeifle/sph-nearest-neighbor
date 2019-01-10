#!/bin/bash
# pwd = /home/jens/git/sph-nearest-neighbor

NRUNS=5

mkdir -p ./test
rm -rf ./test/*

cp ./bin/* ./test

files="config.py test3d_full.py test3d_clusters.py test3d_corners.py test3d_diagonal.py"
for file in $files; do
    cp ./scripts/${file} ./test
done

cd ./test

echo "==========================="
echo "     TEST 3D FULL         "
echo "          Fill 1.0        "
echo "==========================="
for n in `seq 1 $NRUNS`;
do
python3 test3d_full.py
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done

echo "==========================="
echo "     TEST 3D CLUSTERS       "
echo "          Fill .1106           "
echo "==========================="
for n in `seq 1 $NRUNS`;
do
python3 test3d_clusters.py 0.125 2
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done
for n in `seq 1 $NRUNS`;
do
python3 test3d_clusters.py 0.125 4
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done
for n in `seq 1 $NRUNS`;
do
python3 test3d_clusters.py 0.125 6
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done

echo "==========================="
echo "     TEST 3D CLUSTERS      "
echo "          Fill 0.512       "
echo "==========================="
for n in `seq 1 \$NRUNS`;
do
python3 test3d_clusters.py 0.6 5
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done
for n in `seq 1 \$NRUNS`;
do
python3 test3d_clusters.py 0.6 10
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done
for n in `seq 1 \$NRUNS`;
do
python3 test3d_clusters.py 0.6 20
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done

echo "==========================="
echo "     TEST 3D CORNERS       "
echo "          Fill 0.112632    "
echo "==========================="
for n in `seq 1 \$NRUNS`;
do
python3 test3d_corners.py 0.78
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done

echo "==========================="
echo "     TEST 3D CORNERS       "
echo "          Fill 0.0288      "
echo "==========================="
for n in `seq 1 \$NRUNS`;
do
python3 test3d_corners.py 0.5
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done

echo "==========================="
echo "     TEST 3D DIAGONAL      "
echo "          Fill 0.117696    "
echo "==========================="
for n in `seq 1 \$NRUNS`;
do
python3 test3d_diagonal.py 0.47
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done


echo "==========================="
echo "     TEST 3D DIAGONAL     "
echo "          Fill 0.5         "
echo "==========================="
for n in `seq 1 \$NRUNS`;
do
python3 test3d_corners.py 0.84
echo "Start fr_cellLinkedList ($n/$NRUNS)..."
./fr_cellLinkedList \
    -d 3 \
    -max 250000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_cellLinkedList finished"
done


echo "Saving results to ../results/stats.csv"
mkdir -p ../results
cat stats.csv >> ../results/stats.csv
