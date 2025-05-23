import random

def simulate_ball_process(N, max_steps=1000, verbose=True):
    """
    Simulates the ball jumping and multiplication process.

    Args:
        N (int): The initial highest state of the first ball.
        max_steps (int): Maximum number of time steps to prevent infinite loops.
        verbose (bool): If True, prints the state at each time step.

    Returns:
        int: The number of time steps taken for all balls to be eliminated.
             Returns max_steps if the simulation doesn't finish within that limit.
    """
    if N <= 1:
        if verbose:
            print(f"Initial state N={N} is already 1 or less. No simulation needed.")
        return 0

    # List to store the current states of all balls
    balls = [N]
    time_step = 0

    if verbose:
        print(f"Time Step {time_step}: Balls = {balls} (Count: {len(balls)})")

    while balls and time_step < max_steps:
        next_generation_balls = []
        processed_any_ball = False # To check if any ball was > 1

        for current_state in balls:
            if current_state > 1:
                processed_any_ball = True
                # Ball jumps to a random lower state
                # States are 1, 2, ..., current_state - 1
                # random.randint is inclusive, so range is (1, current_state - 1)
                if current_state - 1 < 1 : # Should not happen if current_state > 1
                    # This case is technically impossible if current_state > 1
                    # but as a safeguard if current_state was 1.1 or something,
                    # though our states are integers.
                    # A ball at state 2 can only jump to state 1.
                    jump_to_state = 1
                else:
                    jump_to_state = random.randint(1, current_state - 1)

                if verbose:
                    print(f"  - Ball at state {current_state} jumps to {jump_to_state}")

                if jump_to_state > 1:
                    # Creates 2 new balls at the new state
                    next_generation_balls.append(jump_to_state)
                    next_generation_balls.append(jump_to_state)
                # If jump_to_state is 1, the ball is eliminated and not added
            # else:
                # If current_state is 1, it's already eliminated effectively.
                # We only process balls with state > 1 from the current 'balls' list.
                # Balls that were already 1 are just not carried over.

        balls = next_generation_balls
        time_step += 1

        if verbose:
            print(f"Time Step {time_step}: Balls = {balls} (Count: {len(balls)})")
        
        # If all balls were 1 in the previous step, processed_any_ball will be False,
        # and `balls` will be empty. The `while balls:` condition will handle termination.
        # This check is more for logical flow understanding than strict necessity
        # given the `while balls:`
        if not processed_any_ball and not balls:
             if verbose: print("All balls were in state 1 or eliminated.")
             break


    if time_step == max_steps and balls:
        if verbose:
            print(f"\nSimulation reached max_steps ({max_steps}) and did not complete.")
        return max_steps
    else:
        if verbose:
            print(f"\nSimulation finished in {time_step} time steps.")
        return time_step

# --- Example Usage ---
if __name__ == "__main__":
    initial_N = 4 # Try with different N values
    print(f"Starting simulation with N = {initial_N}\n" + "="*30)
    steps_taken = simulate_ball_process(initial_N, verbose=True, max_steps=50)
    print(f"\nSimulation with N={initial_N} took {steps_taken} steps.")

    print("\n" + "="*30 + "\n")

    initial_N_large = 6
    print(f"Starting simulation with N = {initial_N_large} (less verbose)\n" + "="*30)
    # For larger N, set verbose=False if output is too much
    steps_taken_large = simulate_ball_process(initial_N_large, verbose=True, max_steps=200)
    print(f"\nSimulation with N={initial_N_large} took {steps_taken_large} steps.")

    print("\n" + "="*30 + "\n")
    print(f"Starting simulation with N = 1\n" + "="*30)
    steps_taken_one = simulate_ball_process(1, verbose=True)
    print(f"\nSimulation with N=1 took {steps_taken_one} steps.")

    print("\n" + "="*30 + "\n")
    # Example of a potentially long run (or one that might hit max_steps)
    # initial_N_very_large = 10
    # print(f"Starting simulation with N = {initial_N_very_large} (verbose=False)\n" + "="*30)
    # steps_taken_very_large = simulate_ball_process(initial_N_very_large, verbose=False, max_steps=10000)
    # print(f"\nSimulation with N={initial_N_very_large} took {steps_taken_very_large} steps.")
