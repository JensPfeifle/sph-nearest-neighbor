#include <cstdlib> // C standard library
#include <cstdio>  // C I/O (for sscanf)
#include <cstring> // string manipulation
#include <fstream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cassert>
#include <ANN/ANN.h>




using namespace std;

//----------------------------------------------------------------------
//	Parameters that are set in getArgs()
//----------------------------------------------------------------------
double r = 0.0;	// radius of search
int k = 1;		   // number of nearest neighbors
int dim = 2;	   // dimension
double eps = 0;	// error bound
int maxPts = 1000; // maximum number of data points

istream *dataIn = NULL;  // input for data points

void getArgs(int argc, char **argv); // get command-line arguments

bool readPt(istream &in, ANNpoint p) // read point (false on EOF)
{
	for (int i = 0; i < dim; i++)
	{
		if (!(in >> p[i]))
			return false;
	}
	return true;
}


void printPt(ostream &out, ANNpoint p) // print point
{
	out << "(" << p[0];
	for (int i = 1; i < dim; i++)
	{
		out << ", " << p[i];
	}
	out << ")\n";
}

int writeOutput(vector<int> &p1, vector<int> &p2)
{
	std::ofstream myfile;
	myfile.open("interactionpairs.dat");
	myfile << "\tp1\tp2"
		   << "\n"
		   << "\t===\t==="
		   << "\n";
	for (int i = 0; i < p1.size(); i++)
	{
		myfile << "\t" << p1[i] << "\t" << p2[i] << "\n";
	}
	myfile.close();
	return 0;
}

int writeStats(const double data[], const int numstats)
{
	fstream myfile;
	myfile.open("stats.csv", std::ios_base::app);
	for (int i = 0; i < numstats; i++)
	{
		myfile << "," << data[i];
	}
	myfile << "," << "" << "\n";
	myfile.close();
	return 0;
}

int main(int argc, char **argv)
{

	int nDataPts;		   // actual number of data points
	ANNpointArray dataPts; // data points
	vector<double> dataPtsX;
	vector<double> dataPtsY;
	vector<double> dataPtsZ;
	vector<int> partPart_p1;
	vector<int> partPart_p2;
	vector<double> partPart_dist;

	auto total_start = std::chrono::high_resolution_clock::now();

	// read command-line arguments
	getArgs(argc, argv);
	double rSq = r*r;
	//cout << "Search radius: " << r << "\n";

	// Load data points
	dataPts = annAllocPts(maxPts, dim); // allocate data points
	nDataPts = 0; // read data points
	while (nDataPts < maxPts && readPt(*dataIn, dataPts[nDataPts]))
	{
		nDataPts++;
	}
	cout << nDataPts <<" data points.\n";

	// Convert to Structures of Arrays vectors
	dataPtsX.resize(nDataPts);
	dataPtsY.resize(nDataPts);
	dataPtsZ.resize(nDataPts);
	for (int i = 0; i< nDataPts; i++){
		dataPtsX[i] = dataPts[i][0];
		dataPtsY[i] = dataPts[i][1];
		dataPtsZ[i] = dataPts[i][2];
	}
	annClose(); // done with ANN

	// Record start time
	auto start = std::chrono::high_resolution_clock::now();

	// Determine bounding box
	double boundingBoxMinX = 0.0;
	double boundingBoxMinY = 0.0;
	double boundingBoxMinZ = 0.0;
	double boundingBoxMaxX = 0.005;
	double boundingBoxMaxY = 0.01;
	double boundingBoxMaxZ = 0.005;

	cout << "Bounding Box: " << endl;
	cout << ">>> X: " << boundingBoxMinX << " ... " << boundingBoxMaxX << endl;
	cout << ">>> Y: " << boundingBoxMinY << " ... " << boundingBoxMaxY << endl;
	cout << ">>> Z: " << boundingBoxMinZ << " ... " << boundingBoxMaxZ << endl;

	// Determine number of search cubes
	int nCubesX = std::max(std::floor((boundingBoxMaxX - boundingBoxMinX)/r),1.0);
	int nCubesY = std::max(std::floor((boundingBoxMaxY - boundingBoxMinY)/r),1.0);
	int nCubesZ = std::max(std::floor((boundingBoxMaxZ - boundingBoxMinZ)/r),1.0);
	int nCubes = nCubesX * nCubesY * nCubesZ;
	cout << "Number of search cubes: " << nCubes << endl;
	cout << "nCubesX: " << nCubesX << endl;
	cout << "nCubesY: " << nCubesY << endl;
	cout << "nCubesZ: " << nCubesZ << endl;

	// Adapt search cube edge length
	double dX = (boundingBoxMaxX - boundingBoxMinX) / double(nCubesX);
	double dY = (boundingBoxMaxY - boundingBoxMinY) / double(nCubesY);
	double dZ = (boundingBoxMaxZ - boundingBoxMinZ) / double(nCubesZ);

	// Fill linked lists
	vector<int> next(nDataPts,-1);
	vector<int> first(nCubes,-1);
	vector<int> last(nCubes,-1);
	for (int i = 0; i < nDataPts; i++){
		// Determine cube number
		int x = static_cast<int>(floor((dataPtsX[i] - boundingBoxMinX) / dX));
		int y = static_cast<int>(floor((dataPtsY[i] - boundingBoxMinY) / dY));
		int z = static_cast<int>(floor((dataPtsZ[i] - boundingBoxMinZ) / dZ));
		int cubeNumber = z * (nCubesX + nCubesY) + y * nCubesY + x;
		// Insert into lists
		first[cubeNumber] == -1 ? first[cubeNumber] = i : next[last[cubeNumber]] = i;
		last[cubeNumber] = i;
	}

	// Query lists (cube by cube)
	int part1;
	int part2;
	double distSq;

	for (int iCube = 0; iCube < nCubes; iCube++) {

		// Get coordinates in "cube grid"
		int z = iCube / (nCubesX * nCubesY);
		int y = (iCube - z * nCubesX * nCubesY) / (nCubesX);
		int x = iCube % (nCubesX);

		// Default (Cube fully surrounded by other cubes)
			int ixMin = -1;
			int iyMin = -1;
			int izMin = -1;
			int ixMax = 1;
			int iyMax = 1;
			int izMax = 1;

			// Handle cases at boundaries
			if (x == 0) {
					ixMin = 0;
			}
			if (x == (nCubesX - 1)) {
					ixMax = 0;
			}
			if (y == 0) {
					iyMin = 0;
			}
			if (y == (nCubesY - 1)) {
					iyMax = 0;
			}
			if (z == 0) {
					izMin = 0;
			}
			if (z == (nCubesZ - 1)) {
					izMax = 0;
			}

			for (int ix = ixMin; ix <= ixMax; ix++) {
				for (int iy = iyMin; iy <= iyMax; iy++) {
					for (int iz = izMin; iz <= izMax; iz++) {

						int currentCube =   ((z+iz) * (nCubesX * nCubesY) + (y+iy) * nCubesX + (x+ix));

						if (currentCube == iCube) {
                part1 = first[iCube];
                while (part1 != -1) {
                  part2 = part1;
                  while (part2 != -1) {
                    distSq = (dataPtsX[part2] - dataPtsX[part1]) * (dataPtsX[part2] - dataPtsX[part1])
										+ (dataPtsY[part2] - dataPtsY[part1]) * (dataPtsY[part2] - dataPtsY[part1])
										+ (dataPtsZ[part2] - dataPtsZ[part1]) * (dataPtsZ[part2] - dataPtsZ[part1]);
                    if (distSq <= rSq) {
                      partPart_p1.push_back(part1);
                      partPart_p2.push_back(part2);
                      partPart_dist.push_back(sqrt(distSq));
                    }
                    part2 = next[part2];
									}
                  part1 = next[part1];
                }
           } else if (currentCube > iCube) {
						 part1 = first[iCube];
             while (part1 != -1) {
                 part2 = first[currentCube];
                 while (part2 != -1) {
									 distSq = (dataPtsX[part2] - dataPtsX[part1]) * (dataPtsX[part2] - dataPtsX[part1])
									+ (dataPtsY[part2] - dataPtsY[part1]) * (dataPtsY[part2] - dataPtsY[part1])
									+ (dataPtsZ[part2] - dataPtsZ[part1]) * (dataPtsZ[part2] - dataPtsZ[part1]);
                         if (distSq <= rSq) {
                             partPart_p1.push_back(part1); // Might be slow
                             partPart_p2.push_back(part2);
                             partPart_dist.push_back(sqrt(distSq));
                         }

                     part2 = next[part2];
                 }
                 part1 = next[part1];
             }
					 }

					}
				}
			}

	}

	auto total_finish = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> total = (total_finish - total_start);
	double ttotal = total.count();

	writeOutput(partPart_p1, partPart_p2);

	const int numstats = 1;
	double stats[numstats] = {ttotal};
	writeStats(stats, numstats);

	return EXIT_SUCCESS;
}

void getArgs(int argc, char **argv)
{
	static ifstream dataStream;  // data file stream
	static ifstream queryStream; // query file stream

	if (argc <= 1)
	{ // no arguments
		cerr << "Usage:\n\n"
			 << "  fixed_radius_ann [-d dim] [-max m] [-nn k] [-e eps]\n"
			 << "                    [-df data] [-r radius]\n"
			 << "\n"
			 << "  where:\n"
			 << "    dim      dimension of the space (default = 2)\n"
			 << "    m        maximum number of data points (default = 1000)\n"
			 << "    k        number of nearest neighbors per query (default 1)\n"
			 << "    eps      the error bound (default = 0.0)\n"
			 << "    query    name of file containing query points (default = data)\n"
			 << "    data     name of file containing data points\n"
			 << "    radius   radius of of query\n"
			 << "\n"
			 << " At least -df and -r are required."
			 << " Results are sent to the standard output.\n"
			 << " Note: max option is used for array allocation. Set as large as required.\n"
			 << "\n";
		exit(0);
	}
	int i = 1;
	while (i < argc)
	{ // read arguments
		if (!strcmp(argv[i], "-d"))
		{						   // -d option
			dim = atoi(argv[++i]); // get dimension to dump
		}
		else if (!strcmp(argv[i], "-max"))
		{							  // -max option
			maxPts = atoi(argv[++i]); // get max number of points
		}
		else if (!strcmp(argv[i], "-nn"))
		{						 // -nn option
			k = atoi(argv[++i]); // get number of near neighbors
		}
		else if (!strcmp(argv[i], "-r"))
		{						 // -r option
			r = atof(argv[++i]); // set radius of search
		}
		else if (!strcmp(argv[i], "-e"))
		{									// -e option
			sscanf(argv[++i], "%lf", &eps); // get error bound
		}
		else if (!strcmp(argv[i], "-df"))
		{										 // -df option
			dataStream.open(argv[++i], ios::in); // open data file
			if (!dataStream)
			{
				cerr << "Cannot open data file\n";
				exit(1);
			}
			dataIn = &dataStream; // make this the data stream
		}
		else
		{ // illegal syntax
			cerr << "Unrecognized option.\n";
			exit(1);
		}
		i++;
	}
	if (dataIn == NULL || r == 0.0)
	{
		cerr << "-df and -r options must be specified\n";
		exit(1);
	}
}
