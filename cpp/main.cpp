#include "./include/ssr.hpp"
#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <random>
#include <cstdlib> 
#include<chrono>
#include <fstream>
#include <sstream> // For file system mangement 
#include <iomanip> // To edit the name of the file dpending on the parameters 

int main(int argc, char **argv)
{
    int N = 10001;
    int max_iter = 3000;
    float mu = 1.0;

    // Parse command line arguments
    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];
        if (arg == "--n" && i + 1 < argc)
        {
            N = std::atoi(argv[++i]);
        }
        else if (arg == "--m" && i + 1 < argc)
        {
            max_iter = static_cast<int>(std::stod(argv[++i]));
        }
        else if (arg == "--mu" && i + 1 < argc)
        {
            mu = std::atof(argv[++i]);
        }
    }
    std::ostringstream oss;
    oss << "ssr_mu_" << std::fixed << std::setprecision(2) << mu
        << "_n_" << N
        << "_m_" << max_iter << ".txt";
    std::string output_file = oss.str();
    
    std::ofstream ofs(output_file);
    if (!ofs)
    {
        std::cerr << "Failed to open output file: " << output_file << std::endl;
        return 1;
    }

    // SSR object 
    SSR simulator;
    // Results vector that will hold the values of the state label 
    std::vector<int> results;

    for (int i = 0; i < max_iter; ++i)
    {
        results=simulator.ssr_casc(N, mu);
        for(auto e:results)
        {
            ofs<<e<<"\n";
        }
        results.clear();

    }
    ofs.close();
    return 0;
}
