#include <vector>
#include <iostream>
#include <random>
#include <algorithm>
#include <cmath>

/**
 * This file contains the implementation of a branching process
 * where mu balls start at state N and split as they cascade down
 */

// Random seed to be used globally
std::random_device dv;
// Pseudo random number geenrator
std::mt19937_64 gen(dv());
// Generates a random next state
int get_next_state(int lower_bound, int upper_bound)
{
    // Returns a random integer from the interval [lower_bound, upper_bound] both included
    std::uniform_int_distribution<int> dist(lower_bound, upper_bound);
    return dist(gen);
}
// The main simulation function
inline int ssr_casc(const int &n_states, const int &max_iter, const double &mu, const int &seed = dv())
{

    std::vector<int> balls; // A vector to keep track of the states of the
                            // elements of the SSR cascasde
    int initial_balls{1};   // The process is intilized with a single element
                            // at the highest state possible
                            // The commented code below
                            // Implements the general case
                            // described in the paper
                            // Sample space reducing cascading processes produce the full spectrum of scaling exponents
    // Intilizing the states according to the value
    // of the multiplicative factor mu
    // Handle case where mu < 1
    // if (mu < 1.0f)
    // {
    //     initial_balls = 1; // Create one ball when mu < 1
    // }
    // else
    // {
    //     initial_balls = static_cast<int>(mu); // Floor of mu when mu >= 1
    // }
    // Intilize the balls's states
    int s_size{0};   // Intilizing the size of the Avalnche/cascadde
    int duration{0}; // Intilizing the duration of each full process
                     // Starting from one or mu elements at the highest state
                     // Untill all elements are at the lowest state

    for (int i = 0; i < initial_balls; i++) // Iterate over the intial number of elements
    {                                       // at assign each ball the highest state possible
        balls.push_back(n_states);          // which corresponds to the total number of states
    }
    // Generate a uniform random number from 0 to 1
    std::uniform_real_distribution<float> dis(0.0f, 1.0f);
    // While the the list of balls is not empty
    // apply the SSR steps
    while (!balls.empty())
    {
        std::vector<int> new_balls;     // Temporary vector that will host
                                        // The states of the newly generated elements
        for (int current_state : balls) // For existing balls
        {
            if (current_state != n_states)
            {
                std::cout << current_state << "\n"; // Output the current state of the elemnt
            }
            int next_state;                                          // Variable to hold the value of the next state
            if (current_state > 1)                                   // Process only elements that are in state
            {                                                        // different than the gound state, here it is 1
                duration++;                                          // Increase the duration counter
                int num_new_balls{0};                                // Intilize the number of new elemnts to create
                int base_balls = static_cast<int>(mu);               // Floor of mu
                float decimal_part = mu - base_balls;                // Decimal part of mu
                decimal_part = std::clamp(decimal_part, 0.0f, 1.0f); // Calmping the decimal part
                num_new_balls = base_balls;                          // Number of new balls

                if (dis(gen) < decimal_part) // With probability delta create floor mu + 1
                {                            // new balls
                    num_new_balls++;
                }

                for (int j = 0; j < num_new_balls; j++) // iterate over the newly created elements
                {
                    next_state = get_next_state(1, current_state - 1); // Generate a new state that is lower than the current state
                    if (next_state == 1)
                    {
                        s_size++;                        // Increase the size of the avlanche / cascade by 1
                        new_balls.push_back(next_state); // Push the new states

                    } // for every element that reaches the ground state
                    else
                    {
                        new_balls.push_back(next_state); // Push the new states
                    } // to the temporary balls array
                } // if different from the ground state
            }
        }
        balls = new_balls; // Update the balls vector
    }
    //  std::cout<< s_size << std::endl;     // Print the avalanche size
    //  std::cout<<duration<<"\n";    //  Print the duration of the process

    return 0;
}

int main(int argc, char **argv)
{

    // Default paramters
    // All of them can be passed through commandline
    // First we start by setting up the number of states
    int N{10'001}; // number of states +1
    // Then we set up the number of iterations
    int max_iter{3000}; // This is a good number of iteration to estimate the p-value
    // Set up the   branching factor (mu) as a float
    float mu{1.0f};

    // Get the number of states, maximum iterations, and mu from the command line
    for (int i = 0; i < argc; i++) // CHeck the case when the args are not in the options
    {
        if (std::string(argv[i]) == "--n" && i + 1 < argc)
        {
            // Casting the argument allows me to pass the number of states in scientific notation
            // For example as: --n 10E4 :)

            N = static_cast<int>(std::atof(argv[++i])) + 1;
        }
        if (std::string(argv[i]) == "--m" && i + 1 < argc)
        {
            // Casting the argument allows me to pass the number of restarts in scientific notation
            // For example as 10E6 :)
            max_iter = static_cast<int>(std::atof(argv[++i]));
        }
        if (std::string(argv[i]) == "--mu" && i + 1 < argc)
        {
            mu = std::atof(argv[++i]);
        }
    }

    /**
     *
     * This commented lines are for making the code more compact without using
     * scripts to run the code
     */

    for (int i = 0; i < max_iter; ++i)
    {
        ssr_casc(N, max_iter, mu);
    }
    return 0;
}