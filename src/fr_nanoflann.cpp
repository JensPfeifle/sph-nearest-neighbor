#include <cstdlib> // C standard library
#include <cstdio>  // C I/O (for sscanf)
#include <cstring> // string manipulation
#include <fstream> // file io
#include <vector>
#include <numeric>   // std::iota
#include <algorithm> // std::find
#include <chrono>
#include <cassert>

#include <ANN/ANN.h>
#include <nanoflann.hpp>
#include "utils.h"

using namespace std;
using namespace nanoflann;

const int DIM = 3; // dimensions

//----------------------------------------------------------------------
//	Parameters that are set in getArgs()
//----------------------------------------------------------------------
double r = 0.0;	// radius of search
int maxPts = 1000; // maximum number of data points

istream *dataIn = NULL; // input for data points

void getArgs(int argc, char **argv); // get command-line arguments
bool check_interaction_exists(vector<int> &p1, vector<int> &p2,
							  int &nInteractionPairs, const int qpIdx, const int nnIdx);

//bool readPts(istream &in, PointCloud<double> &point) // read point (false on EOF)
//{
//	for (int i = 0; i < DIM; i++)
//	{
//		if (!(in >> p[i]))
//			return false;
//	}
//	return true;
//}

//void printPt(ostream &out, ANNpoint p) // print point
//{
//	out << "(" << p[0];
//	for (int i = 1; i < DIM; i++)
//	{
//		out << ", " << p[i];
//	}
//	out << ")\n";
//}

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
	myfile << ",-1" << "\n";
	myfile.close();
	return 0;
}

int main(int argc, char **argv)
{

	// Randomize Seed
	srand(static_cast<unsigned int>(time(nullptr)));

	//int nDataPts;				// actual number of data points
	//double queryPt[3];			// allocate query point
	//PointCloud<double> dataPts; // allocate data points

	//ANNidxArray nnIdx;	 // near neighbor indices
	//ANNdistArray dists;	// near neighbor distances
	//ANNkd_tree *kdTree;	// searchSORTEDSEARCH structure

	//int nInteractionPairs; //number of interaction pairs

	auto total_start = std::chrono::high_resolution_clock::now();

	getArgs(argc, argv); // read command-line arguments

	//cout << "Search radius: " << r << "\n";
	const double search_radius = static_cast<double>(r*r);

	///////////////////////////
	/// Start Example
	///////////////////////////

	PointCloud<double> cloud;

	const int N = maxPts;

	// Generate points:
	generateRandomPointCloud(cloud, N, 5e-3);

	// construct a kd-tree index:
	typedef KDTreeSingleIndexAdaptor<
		L2_Simple_Adaptor<double, PointCloud<double>>,
		PointCloud<double>,
		DIM>
		my_kd_tree_t;

	my_kd_tree_t index(3 /*dim*/, cloud, KDTreeSingleIndexAdaptorParams(10 /* max leaf */));
	index.buildIndex();


	double query_pt[3];
	int nDataPts = cloud.pts.size();

	for (int i = 0; i < nDataPts; i++)
	{	
		//cout << "queryPt: (" << cloud.pts[i].x << "," << cloud.pts[i].y << "," << cloud.pts[i].z << ")" << "\n";
		query_pt[0] = cloud.pts[i].x;
		query_pt[1] = cloud.pts[i].y;
		query_pt[2] = cloud.pts[i].z;

		{
			std::vector<std::pair<size_t, double>> ret_matches;

			nanoflann::SearchParams params;
			//params.sorted = false;

			const size_t nMatches = index.radiusSearch(&query_pt[0], search_radius, ret_matches, params);

			//cout << "radiusSearch(): radius=" << search_radius << " -> " << nMatches << " matches\n";
			//for (size_t i = 0; i < nMatches; i++)
			//	cout << "idx[" << i << "]=" << ret_matches[i].first << " dist[" << i << "]=" << ret_matches[i].second << endl;
			//cout << "\n";
		}

	}


	///////////////////////////
	/// End Example
	///////////////////////////

	auto total_finish = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> total = (total_finish - total_start);
	double ttotal = total.count();

	std::cout << ttotal << "\n";

	//delete[] nnIdx; // clean things up
	//delete[] dists;
	//delete kdTree;

	return EXIT_SUCCESS;
}

void getArgs(int argc, char **argv)
{
	static ifstream dataStream;  // data file stream
	static ifstream queryStream; // query file stream

	if (argc <= 1)
	{ // no arguments
		std::cerr << "Usage:\n\n"
				  << "  fr_nanoflann [-max m] [-df data] [-r radius]\n"
				  << "\n"
				  << "  where:\n"
				  << "    m        maximum number of data points (default = 1000)\n"
				  << "    data     name of file containing data points\n"
				  << "    radius   radius of of query\n"
				  << "\n"
				  << "  -df and -r are required."
				  << " Note: max option is used for array allocation. Set as large as required.\n"
				  << "\n";
		exit(0);
	}
	int i = 1;
	while (i < argc)
	{ // read arguments
		if (!strcmp(argv[i], "-max"))
		{							  // -max option
			maxPts = atoi(argv[++i]); // get max number of points
		}
		else if (!strcmp(argv[i], "-r"))
		{						 // -r option
			r = atof(argv[++i]); // set radius of search
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
