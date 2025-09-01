#ifndef SSR_HPP
#define SSR_HPP
#include <iostream>
#include <random>
#include <vector>
#include <algorithm>
#include <memory>
#include "Random.hpp"

/**
 * SSR interface
 */
class ISSR
{
public:
    virtual std::vector<int> run(bool verbose = true) = 0;
    virtual ~ISSR() = default;
};

class STDSSR : public ISSR
{
    int n_states;

public:
    explicit STDSSR(int n) : n_states(n) {};
    std::vector<int> run(bool verbose = true) override
    {
        std::vector<int> visited_states;
        visited_states.reserve(n_states);

        int current_state{n_states};
        while (current_state > 1)
        {
            int next_state = Random::get<int>(1, current_state - 1);
            current_state = next_state;
            if (verbose)
                std::cout << current_state << "\n";
            visited_states.push_back(current_state);
        }
        return visited_states;
    }
};

class NoisySSR : public ISSR
{
    int n_states;
    float lam;

public:
    explicit NoisySSR(int n, float l) : n_states(n), lam(l) {};
    std::vector<int> run(bool verbose = true) override
    {
        std::vector<int> visited_states;
        visited_states.reserve(n_states);

        int current_state{n_states};
        int next_state;
        float u = Random::get<float>(0.0f, 1.0f);
        if (current_state == 1)
        {
            // restart uniformly over all N sites
            next_state = Random::get<int>(1, n_states);
        }
        else if (u < lam)
        {
            // SSR jump: uniformly to {1, ..., current_state-1}
            next_state = Random::get<int>(1, current_state - 1);
        }
        else
        {
            // noise jump: uniformly to {1, ..., N}
            next_state = Random::get<int>(1, n_states);
        }
        current_state = next_state;
        visited_states.push_back(current_state);

        if (verbose)
            std::cout << current_state << "\n";

        return visited_states;
    }
};

class CascadeSSR : public ISSR
{
    int n_states;
    float mu;

public:
    explicit CascadeSSR(int n, float mult) : n_states(n), mu(mult) {};
    std::vector<int> run(bool verbose = true) override
    {
        std::vector<int> visited_states;
        visited_states.reserve(n_states);

        std::vector<int> balls;
        balls.push_back(n_states);

        int base_balls = static_cast<int>(mu);
        float decimal_part = mu - base_balls;
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
                        if (verbose)
                            std::cout << next_state << "\n";
                        new_balls.push_back(next_state);
                    }
                }
            }
            std::swap(balls, new_balls);
        }
        return visited_states;
    }
};

template <typename T>
class SSRCTX
{
public:
    template <typename... Args>
    static std::unique_ptr<ISSR> create(Args &&...args)
    {
        return std::make_unique<T>(std::forward<Args>(args)...);
    }
};

#endif // SSR_HPP
