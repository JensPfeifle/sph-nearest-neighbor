# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

rm -rf ./test/*

cp ./scripts/*.py        ./test/
cp ./bin/fr_ann          ./test/fr_ann

cd ./test
python3 generate_test_points.py

echo "===================================================="
echo "2D fixed radius search, all neighbors"
echo "===================================================="
./fr_ann \
    -d 2 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003 \
    > result.dat

echo "output written to result.dat"
