#ifndef SSR_HPP
#define SSR_HPP 
#include<random>
#include<vector>

// Struct to to the result of the SSR process 
struct ssr_t 
{
    int size;
    int duration; 
    std::vector<int> visited_states;
};

class SSR{
    private:
        std::mt19937 gen;
        std::uniform_real_distribution<float> dis;

        // std::random_device dv;
    
        public:
        SSR();
        explicit SSR(const uint64_t &seed);
        int get_next_state(const int &sink_state, const int &current_state);
        ssr_t ssr_std(const int &n_states);
        ssr_t ssr_noisy(const int &n_states, const float&lam);
        ssr_t ssr_casc(const int &n_states, const float &mu); 


};
#endif // SSR_HPP    