# pwd = /home/jens/git/sph-nearest-neighbor

mkdir -p ./test

cp ./scripts/*.py                    ./test/
cp ./bin/fixed_radius_ann            ./test/fixed_radius_ann

cd ./test
python3 generate_test_points.py

echo "===================================================="
echo "2D fixed radius search"
echo "===================================================="
./fixed_radius_ann \
    -d 2 \
    -nn 50 \
    -e 0.0 \
    -qf query.pts \
    -df data.pts \
    -r 0.0003 \
    > result.dat

python3 plot_2d.py

