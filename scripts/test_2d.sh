# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

rm -rf ./test/*

files="config.py generate_test_points.py plot_2d.py"
for file in $files; do
    cp ./scripts/${file}             ./test
done

cp ./bin/*                    ./test

echo "==================="
echo "     TEST 2D       "
echo "==================="

cd ./test
python3 generate_test_points.py

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
