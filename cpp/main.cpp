#include "./include/ssr.hpp"
#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <random>

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
            max_iter = std::atoi(argv[++i]);
        }
        else if (arg == "--mu" && i + 1 < argc)
        {
            mu = std::atof(argv[++i]);
        }
    }

    std::random_device dv;
    uint64_t seed = dv();

    SSR simulator(seed);

    std::vector<std::vector<int>> all_results;
    all_results.reserve(max_iter);

    for (int i = 0; i < max_iter; ++i)
    {
        all_results.push_back(simulator.ssr_casc(N, mu));
    }

    // Optionally print or analyze all_results here

    return 0;
}
