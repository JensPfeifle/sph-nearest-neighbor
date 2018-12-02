#!/bin/bash
# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test
rm -rf ./test/*

cp ./bin/* ./test

files="config.py generate_test_points_3d.py plot_3d.py"
for file in $files; do
    cp ./scripts/${file} ./test
done

cd ./test

echo "==================="
echo "     TEST 3D       "
echo "==================="

python3 generate_test_points_3d.py
echo "Start fr_ann.."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003


python3 generate_test_points_3d.py
echo "Start fr_ann.."
./fr_ann \
    -d 3 \
    -max 5000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003

mkdir -p ./results
cat stats.csv >> ../results/stats.csv