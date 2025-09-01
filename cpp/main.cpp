#include "./include/ssr.hpp"
#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <random>
#include <cstdlib>
#include <chrono>
#include <fstream>
#include <sstream>
#include <memory>
#include <cstdlib>
#include <unordered_map>
#include<vector>

inline void print_help();

int main(int argc, char **argv)
{
    
    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];
        if (arg == "--help")
        {
            print_help();
            return 0; // exit after showing help
        }
    }
    std::unordered_map<std::string, std::string> args;

    for (int i = 1; i < argc - 1; ++i)
    {
        std::string key = argv[i];

        std::string val = argv[i + 1];

        if (key.rfind("--", 0) == 0) // starts with --
        {
            args[key] = val;
            ++i; // skip next
        }
    }

    std::string ssr_type = args.count("--type") ? args["--type"] : "cascade";

    int max_iter = args.count("--m") ? std::stoi(args["--m"]) : 3000;

    std::unique_ptr<ISSR> simulator;
    // std::cout << "Running SSR simulation with type: " << ssr_type << "\n";
    if (ssr_type == "std")
    {
        int N = args.count("--N") ? std::stoi(args["--N"]) : 10001;
        // std::cout << "  N = " << N << "\n";
        simulator = SSRCTX<STDSSR>::create(N);
    }
    else if (ssr_type == "noisy")
    {
        int N = args.count("--N") ? std::stoi(args["--N"]) : 10001;
        // int n = args.count("--n") ? std::stoi(args["--n"]) : 10001;
        float lambda = args.count("--lambda") ? std::stof(args["--lambda"]) : 1.0f;
        // std::cout << "  N = " << N << "\n";
        // std::cout << "  lambda = " << lambda << "\n";
        simulator = SSRCTX<NoisySSR>::create(N, lambda);
    }
    else if (ssr_type == "cascade")
    {
        int N = args.count("--N") ? std::stoi(args["--N"]) : 10001;
        float mu = args.count("--mu") ? std::stof(args["--mu"]) : 1.0f;
        // std::cout << "  N = " << N << "\n";
        // std::cout << "  mu = " << mu << "\n";
        simulator = SSRCTX<CascadeSSR>::create(N, mu);
    }
    else
    {
        std::cerr << "Unknown SSR type: " << ssr_type << "\n";
        return 1;
    }
    // std::cout << "  max_iter = " << max_iter << "\n\n";

    std::vector<int> results;
    for (int i = 0; i < max_iter; ++i)
    {
        results = simulator->run();

    }
    return 0;
}

void print_help()
{
    std::cout << "Usage: ./your_program [OPTIONS]\n"
              << "Options:\n"
              << "  --type TYPE      SSR type to run (std, noisy, cascade). Default: cascade\n"
              << "  --N VALUE        Number of states. Default: 10001\n"
              << "  --lambda VALUE      Lambda parameter for noisy SSR. Default: 1.0\n"
              << "  --mu VALUE       Mu parameter for cascade SSR. Default: 1.0\n"
              << "  --m VALUE        Max iterations. Default: 3000\n"
              << "  --help           Show this help message\n";
}