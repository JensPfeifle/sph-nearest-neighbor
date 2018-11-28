# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

#rm -rf ./test/*

#cp ./scripts/*.py             ./test
cp ./bin/*                    ./test

echo "==================="
echo "     TEST 2D       "
echo "==================="

cd ./test
#python3 generate_test_points.py

./fr_ann \
    -d 2 \
    -max 10000 \
    -nn 50 \
    -e 0.0 \
    -df data.pts \
    -r 0.0003 \
    > result.dat

echo ""
echo "output written to result.dat"
