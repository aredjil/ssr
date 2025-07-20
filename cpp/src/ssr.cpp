#include "../include/ssr.hpp"
#include <iostream>
#include <algorithm>
#include <cmath>
#include <string>

// Default seed
SSR::SSR() : gen(std::random_device{}()), dis(0.0f, 1.0f)
{
}

SSR::SSR(const uint64_t &seed)
    : gen(seed), dis(0.0f, 1.0f){
        
    }
// Getting the next state from the list of availbale states: next_state in {sink_state, ..., current_state - 1}
int SSR::get_next_state(const int &sink_state, const int &current_state)
{
    std::uniform_int_distribution<int> dist(sink_state, current_state);
    return dist(gen);
}

// Method to perform Standard SSR process
ssr_t SSR::ssr_std(const int &n_states)
{
    // Store the results of the process
    ssr_t results;
    // Vector to store the visited states
    std::vector<int> visited_states;
    int s_size{1};   // In the standard ssr one the ball reaches 1 the process ends
                     // and the avlanche size is 1
    int duration{0}; // How many iterations it took the ssr to reach the sink state
    if (n_states <= 1)
        return results;

    int current_state{n_states};
    while (current_state > 1)
    {
        int next_state = get_next_state(1, current_state - 1);
        current_state = next_state;
        visited_states.push_back(current_state);
        duration++;
    }
    results.duration = duration;
    results.size = s_size;
    results.visited_states = visited_states;
    return results;
}
// Method to perform noisy SSR
ssr_t SSR::ssr_noisy(const int &n_states, const float &lam)
{
    ssr_t results;
    int s_size{0};
    int duration{0};
    std::vector<int> visited_states;

    if (n_states <= 1)
        return results;
    // std::uniform_real_distribution<float> dist(0.0f, 1.0f);

    int current_state{n_states};
    while (current_state > 1)
    {
        duration++;
        float u = dis(gen);
        int next_state;
        if (u < lam)
        {
            next_state = get_next_state(1, current_state - 1);
        }
        else
        {
            next_state = get_next_state(1, n_states - 1);
        }
        current_state = next_state;
        visited_states.push_back(current_state);
    }
    results.visited_states = visited_states;
    results.duration = duration;
    results.size = s_size;
    return results;
}

// Method to perform a single SSR with cascades
ssr_t SSR::ssr_casc(const int &n_states, const float &mu)
{
    // Store the results of the process
    ssr_t results;
    // Vector that will contain the generated states
    std::vector<int> balls;

    // Starting with only one ball at the highest state
    // NOTE: Pass the number of initial balls as a paramter to the function
    int intial_balls{1};

    // Vector to store the visited states
    std::vector<int> visited_states;

    // Intilizing the balls at highest state
    for (int i = 0; i < intial_balls; ++i)
    {
        balls.push_back(n_states);
    }

    // std::uniform_real_distribution<float> dis(0.0f, 1.0f);

    // Intilizing the cascade size and duration to zero
    int s_size{0};
    int duration{0};

    while (!balls.empty())
    {
        std::vector<int> new_balls;

        for (int current_state : balls)
        {
            if (current_state != n_states)
            {
                // Add the states to the visited states vector
                visited_states.push_back(current_state);
            }
            if (current_state > 1)
            {
                // Incremeent the duration of the process
                duration++;

                int base_balls = static_cast<int>(mu);
                float decimal_part = mu - base_balls;

                decimal_part = std::clamp(decimal_part, 0.0f, 1.0f);
                int num_new_balls = base_balls;

                if (dis(gen) < decimal_part)
                {
                    num_new_balls++;
                }

                for (int j = 0; j < num_new_balls; ++j)
                {
                    int next_state = get_next_state(1, current_state - 1);

                    if (next_state == 1)
                    {
                        s_size++;
                        new_balls.push_back(next_state);
                    }
                    else
                    {
                        new_balls.push_back(next_state);
                    }
                }
            }
        }
        balls = new_balls;
    }
    results.duration = duration;
    results.size = s_size;
    results.visited_states = visited_states;
    return results;
}