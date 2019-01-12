#!/bin/bash
# must be called from project root
# pwd = /home/jens/git/sph-nearest-neighbor

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
function ctrl_c() {
    echo "CTRL-C -> exiting."
    exit
}

NRUNS=5
TESTDIR=./test/test_nanoflann  # no trailing slash!
BIN="fr_nanoflann"
BIN_ARGS="-max 250000 -df data.pts -r 0.0003"

mkdir -pv $TESTDIR

# clean up testdir
rm  -r $TESTDIR/*

for file in $BIN; do
    cp ./bin/${file} $TESTDIR
done

scriptfiles="config.py test3d_full.py test3d_clusters.py test3d_corners.py test3d_diagonal.py"
for file in $scriptfiles; do
    cp ./scripts/${file} $TESTDIR
done

echo "Starting test run..."
cd $TESTDIR

echo "==========================="
echo "     TEST 3D FULL         "
echo "          Fill 1.0        "
echo "==========================="

python3 test3d_full.py
for n in `seq 1 $NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

echo "==========================="
echo "     TEST 3D CLUSTERS      "
echo "          Fill .1106       "
echo "==========================="

python3 test3d_clusters.py 0.125 2
for n in `seq 1 $NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

python3 test3d_clusters.py 0.125 4
for n in `seq 1 $NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

python3 test3d_clusters.py 0.125 6
for n in `seq 1 $NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

echo "==========================="
echo "     TEST 3D CLUSTERS      "
echo "          Fill 0.512       "
echo "==========================="

python3 test3d_clusters.py 0.6 5
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

python3 test3d_clusters.py 0.6 10
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

python3 test3d_clusters.py 0.6 20
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

echo "==========================="
echo "     TEST 3D CORNERS       "
echo "          Fill 0.112632    "
echo "==========================="

python3 test3d_corners.py 0.78
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

echo "==========================="
echo "     TEST 3D CORNERS       "
echo "          Fill 0.0288      "
echo "==========================="

python3 test3d_corners.py 0.5
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done

echo "==========================="
echo "     TEST 3D DIAGONAL      "
echo "          Fill 0.117696    "
echo "==========================="
python3 test3d_diagonal.py 0.47
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done


echo "==========================="
echo "     TEST 3D DIAGONAL     "
echo "          Fill 0.5         "
echo "==========================="

python3 test3d_corners.py 0.84
for n in `seq 1 \$NRUNS`;
do
echo "Start $BIN ($n/$NRUNS)..."
./$BIN $BIN_ARGS
echo "$BIN finished"
done


echo "Results for this run are in stats.csv in $TESTDIR"
mkdir -p ../results
cp -v --backup=numbered ./stats.csv ../results/stats_$BIN.csv
