#include "../include/ssr.hpp" // The header for the ssr class 
#include "../include/Random.hpp" // Header for generating random numbers  
#include <iostream>
#include <algorithm>
#include <cmath>
#include <string>
#include <cstdint>

// Default cnstructor 
SSR::SSR(){}
// Method to perform Standard SSR process
std::vector<int> SSR::ssr_std(const int &n_states)
{
    // Vector to store the visited states
    std::vector<int> visited_states;

    int current_state{n_states};
    while (current_state > 1)
    {
        int next_state = Random::get<int>(1, current_state - 1);
        current_state = next_state;
        visited_states.push_back(current_state);
    }
    return visited_states;
}
// Method to perform noisy SSR
std::vector<int> SSR::ssr_noisy(const int &n_states, const float &lam)
{

    std::vector<int> visited_states;

    int current_state{n_states};
    while (current_state > 1)
    {
        float u = Random::get<float>(0.0f, 1.0f);
        int next_state;
        if (u < lam)
        {
            next_state = Random::get<int>(1, current_state - 1);
        }
        else
        {
            next_state = Random::get<int>(1, n_states - 1);
        }
        current_state = next_state;
        visited_states.push_back(current_state);
    }
    return visited_states;
}

// Method to perform a single SSR with cascades
std::vector<int> SSR::ssr_casc(const int &n_states, const float &mu)
{
    // Store the results of the process
    std::vector<int> balls;

    // Starting with only one ball at the highest state
    // int intial_balls{1};

    // Vector to store the visited states
    std::vector<int> visited_states;
    visited_states.reserve(static_cast<size_t>(std::ceil(mu * n_states)));
    // Intilizing the balls at highest state
    // for (int i = 0; i < intial_balls; ++i)
    // {
    //     balls.push_back(n_states);
    // }
    balls.push_back(n_states);

    int base_balls = static_cast<int>(mu);
    float decimal_part = mu - base_balls;
    // decimal_part = std::clamp(decimal_part, 0.0f, 1.0f);
    std::vector<int> new_balls;
    size_t ball_capacity = static_cast<size_t>(std::ceil(std::pow(mu, std::log2(n_states))));
    balls.reserve(ball_capacity);
    new_balls.reserve(ball_capacity);
    
    while (!balls.empty())
    {
        new_balls.clear();
        for (const int &current_state : balls)
        {
            if (current_state != n_states)
            {
                // Add the states to the visited states vector
                visited_states.push_back(current_state);
            }
            if (current_state > 1)
            {
                int num_new_balls = base_balls;
                float u = Random::get<float>(0.0f, 1.0f);
                if (u < decimal_part)
                {
                    num_new_balls++;
                }

                for (int j = 0; j < num_new_balls; ++j)
                {
                    int next_state = Random::get<int>(1, current_state - 1);
                    new_balls.push_back(next_state);
                }
            }
        }
        std::swap(balls, new_balls);
    }
    return visited_states;
}
SSR::~SSR() {

}