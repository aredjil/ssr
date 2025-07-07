#include <iostream>
#include <random>
#include <string>
#include <cstdlib>

std::random_device dv;
// Pseudo random number geenrator
std::mt19937_64 gen(dv());

inline int get_next_state(const int &, const int &);

inline void std_ssr(const int &n_states, const float &lambda);

int main(int argc, char **argv)
{
    int n = 10001;
    int m = 1000'000;
    double lambda = 0.7;

    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];
        if (arg == "--n" && i + 1 < argc)
        {
            n = std::atoi(argv[++i]);
        }
        else if (arg == "--m" && i + 1 < argc)
        {
            m = std::atoi(argv[++i]);
        }
        else if (arg == "--l" && i + 1 < argc)
        {
            lambda = std::atof(argv[++i]);
        }
        else if (arg == "-h" || arg == "--help")
        {
            std::cout << "Usage: " << argv[0] << " [-n num_states] [-m num_runs] [-l lambda]\n";
            return 0;
        }
    }

    for (int i = 0; i < m; ++i)
    {
        std_ssr(n, lambda);
    }

    return 0;
}

// Generates a random next state
inline int get_next_state(const int &lower_bound, const int &upper_bound)
{
    // Returns a random integer from the interval [lower_bound, upper_bound] both included
    std::uniform_int_distribution<int> dist(lower_bound, upper_bound);
    return dist(gen);
}
// Standard SSR
inline void std_ssr(const int &n_states, const float &lambda)
{
    if (n_states <= 1)
        return;
    std::uniform_real_distribution<float> dist(0.0f, 1.0f);

    int current_state{n_states};
    while (current_state > 1)
    {
        float u = dist(gen);
        int next_state;
        if (u < lambda)
        {
            next_state = get_next_state(1, current_state - 1);
        }
        else
        {
            next_state = get_next_state(1, n_states - 1);
        }
        current_state = next_state;
        std::cout << current_state << "\n";
    }
}