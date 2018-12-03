#!/bin/bash
# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test
rm -rf ./test/*

cp ./bin/* ./test

files="config.py test3d_cluster.py"
for file in $files; do
    cp ./scripts/${file} ./test
done

cd ./test

echo "==========================="
echo "     TEST 3D CLUSTER       "
echo "==========================="

python3 test3d_cluster.py 0.125 5
echo "Start fr_ann (1/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_ann finished"

python3 test3d_cluster.py 0.125 5
echo "Start fr_ann (2/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_ann finished"

python3 test3d_cluster.py 0.125 5
echo "Start fr_ann (3/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003
echo "fr_ann finished"


python3 test3d_cluster.py 0.35 5
echo "Start fr_ann (1/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

python3 test3d_cluster.py 0.35 5
echo "Start fr_ann (2/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

python3 test3d_cluster.py 0.35 5
echo "Start fr_ann (3/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003


python3 test3d_cluster.py 0.5 3
echo "Start fr_ann (1/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

python3 test3d_cluster.py 0.5 3
echo "Start fr_ann (2/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

python3 test3d_cluster.py 0.5 3
echo "Start fr_ann (3/3)..."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

mkdir -p ../results
cat stats.csv >> ../results/stats.csv