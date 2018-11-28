# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

rm -rf ./test/*

files="config.py generate_test_points_3d.py plot_3d.py"
for file in $files; do
    cp ./scripts/${file}             ./test
done

cp ./bin/*                    ./test

echo "==================="
echo "     TEST 3D       "
echo "==================="

cd ./test
python3 generate_test_points_3d.py

echo "Start fr_ann.."

time \
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
