# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

rm -rf ./test/*

cp ./scripts/*.py             ./test
cp ./bin/*                    ./test

echo "==================="
echo "     TEST 3D       "
echo "==================="

cd ./test
python3 generate_test_points_3d.py

./fr_ann \
    -d 3 \
    -max 10000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003 \
    > result.dat

echo ""
echo "output written to result.dat"
