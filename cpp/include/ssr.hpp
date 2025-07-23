#ifndef SSR_HPP
#define SSR_HPP 
#include<random>
#include<vector>
#include <cstdint>

class SSR{
    // private:
        // std::mt19937 gen;
        // std::uniform_real_distribution<float> dis;

        // std::random_device dv;
    
        public:
        SSR();
        explicit SSR(const uint64_t &seed);
        int get_next_state(const int &sink_state, const int &current_state);
        std::vector<int> ssr_std(const int &n_states);
        std::vector<int> ssr_noisy(const int &n_states, const float&lam);
        std::vector<int> ssr_casc(const int &n_states, const float &mu); 
        ~SSR();


};
#endif // SSR_HPP    