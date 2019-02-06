#include <cstdlib> // C standard library
#include <cstdio>  // C I/O (for sscanf)
#include <cstring> // string manipulation
#include <fstream>
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
istream *queryIn = NULL; // input for query points

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

int main(int argc, char **argv)
{
	int nDataPts;		   // actual number of data points
	ANNpointArray dataPts; // data points
	ANNpoint queryPt;	  // query point
	ANNidxArray nnIdx;	 // near neighbor indices
	ANNdistArray dists;	// near neighbor distances
	ANNkd_tree *kdTree;	// search structure

	getArgs(argc, argv); // read command-line arguments

	queryPt = annAllocPt(dim);			// allocate query point
	dataPts = annAllocPts(maxPts, dim); // allocate data points

	cout << "Search radius: " << r << "\n";
	const ANNdist rSq = r * r; // store squared search radius

	nDataPts = 0; // read data points
	while (nDataPts < maxPts && readPt(*dataIn, dataPts[nDataPts]))
	{
		//printPt(cout, dataPts[nDataPts]);
		nDataPts++;
	}

		cout << nDataPts <<" data points.\n";

	kdTree = new ANNkd_tree( // build search structure
		dataPts,			 // the data points
		nDataPts,			 // number of points
		dim);				 // dimension of space

	while (readPt(*queryIn, queryPt))
	{							 // read query points
		cout << "Query point: "; // echo query point
		printPt(cout, queryPt);

		// run once to determine required k
		const int nNeighbors = kdTree->annkFRSearch(
			queryPt, // ANNpoint query point
			rSq,	 // squared radius
			k,		//number of near neighbors to return
			NULL,
			NULL,
			eps);		 

		cout << "npoints: " << nNeighbors << "\n";

		nnIdx = new ANNidx[nNeighbors];  // allocate near neigh indices
		dists = new ANNdist[nNeighbors]; // allocate near neighbor dists

		kdTree->annkFRSearch( 			//run again to get neighbors
			queryPt,		// ANNpoint query point
			rSq,			// squared radius
			nNeighbors,		// number of near neighbors
			nnIdx,			// array  for indices
			dists,			// array for distances
			eps);			 

		cout << "\tNN:\tIndex\tDistance\n";
		for (int i = 0; i < nNeighbors; i++)
		{							   // print summary
			dists[i] = sqrt(dists[i]); // unsquare distance
			cout << "\t" << i << "\t" << nnIdx[i] << "\t" << dists[i] << "\n";
		}
	}
	delete[] nnIdx; // clean things up
	delete[] dists;
	delete kdTree;
	annClose(); // done with ANN

	return EXIT_SUCCESS;
}

void getArgs(int argc, char **argv)
{
	static ifstream dataStream;  // data file stream
	static ifstream queryStream; // query file stream

	if (argc <= 1)
	{ // no arguments
		cerr << "Usage:\n\n"
			 << "  fixed_radius_ann [-d dim] [-max m] [-nn k] [-e eps] [-qf query]\n"
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
		else if (!strcmp(argv[i], "-qf"))
		{										  // -qf option
			queryStream.open(argv[++i], ios::in); // open query file
			if (!queryStream)
			{
				cerr << "Cannot open query file\n";
				exit(1);
			}
			queryIn = &queryStream; // make this query stream
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
