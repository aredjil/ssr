#ifndef RANDOM_MT_H
#define RANDOM_MT_H

#include <chrono>
#include <random>
#include <type_traits>

// This header-only Random namespace implements a self-seeding Mersenne Twister.
// Requires C++17 or newer.
// Freely redistributable, courtesy of learncpp.com (https://www.learncpp.com/cpp-tutorial/global-random-numbers-random-h/)

namespace Random
{
	// Returns a seeded Mersenne Twister
	inline std::mt19937 generate()
	{
		std::random_device rd{};

		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
			rd(), rd(), rd(), rd(), rd(), rd(), rd()
		};

		return std::mt19937{ ss };
	}

	// Global PRNG
	inline std::mt19937 mt{ generate() };

	// -----------------------------
	// Integer overload for get()
	// -----------------------------
	template <typename T,
	          std::enable_if_t<std::is_integral_v<T>, int> = 0>
	T get(T min, T max)
	{
		return std::uniform_int_distribution<T>{min, max}(mt);
	}

	// -----------------------------
	// Floating-point overload for get()
	// -----------------------------
	template <typename T,
	          std::enable_if_t<std::is_floating_point_v<T>, int> = 0>
	T get(T min, T max)
	{
		return std::uniform_real_distribution<T>{min, max}(mt);
	}
	
	// -----------------------------
	// Mixed-type version with explicit return type (e.g., Random::get<double>(0, 1))
	// -----------------------------
	template <typename R, typename S, typename T,
	          std::enable_if_t<std::is_arithmetic_v<R>, int> = 0>
	R get(S min, T max)
	{
		return get<R>(static_cast<R>(min), static_cast<R>(max));
	}
}

#endif // RANDOM_MT_H
