#!/usr/bin/env python3
import argparse
from chain_reaction import simulate_sphere, simulate_block

def find_critical_mass(mode, S, sigma_t, sigma_f, nu, N, M_min, M_max, tol):
    """
    Find the mass M such that nu * f(M) = 1 (i.e., f(M) = 1/nu) by bisection,
    automatically expanding the search range if needed.
    """
    target = 1.0 / nu
    low, high = M_min, M_max

    # Function to evaluate survival fraction at given mass
    def eval_f(m):
        if mode == 'sphere':
            return simulate_sphere(m, N, sigma_t, sigma_f)
        else:
            return simulate_block(m, S, N, sigma_t, sigma_f)

    f_low = eval_f(low)
    f_high = eval_f(high)
    print(f"DEBUG: Initial f({low:.2f})={f_low:.3f}, f({high:.2f})={f_high:.3f}, target={target:.3f}")

    # Expand upper bound until we bracket the target or hit a limit
    max_expansions = 10
    for i in range(max_expansions):
        if f_low < target < f_high:
            break
        if f_high <= target:
            high *= 2
            f_high = eval_f(high)
            print(f"DEBUG: Expanded high to {high:.2f}, f_high={f_high:.3f}")
        elif f_low >= target:
            low /= 2
            f_low = eval_f(low)
            print(f"DEBUG: Reduced low to {low:.2f}, f_low={f_low:.3f}")
    else:
        raise ValueError(
            f"Unable to bracket target: f({low:.2f})={f_low:.3f}, f({high:.2f})={f_high:.3f}, target={target:.3f}")

    # Bisection loop
    while high - low > tol:
        mid = (low + high) / 2
        f_mid = eval_f(mid)
        print(f"DEBUG: Testing mid={mid:.2f}, f_mid={f_mid:.3f}")
        if f_mid < target:
            low = mid
        else:
            high = mid

    return (low + high) / 2

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Find critical mass by bisection with adaptive bracketing")
    p.add_argument("mode", choices=["sphere", "block"],
                   help="Geometry: 'sphere' or 'block'")
    p.add_argument("-S", type=float, default=1.0,
                   help="Shape ratio a/b (for block)")
    p.add_argument("--sigma-t", type=float, default=1.0,
                   help="Macroscopic total cross-section Σₜ")
    p.add_argument("--sigma-f", type=float, default=0.5,
                   help="Macroscopic fission cross-section Σ_f")
    p.add_argument("--nu", type=float, default=2.42,
                   help="Average neutron multiplicity")
    p.add_argument("-N", type=int, default=200,
                   help="Number of samples per evaluation")
    p.add_argument("--M-min", type=float, default=10.0,
                   help="Initial lower bound for mass M")
    p.add_argument("--M-max", type=float, default=100.0,
                   help="Initial upper bound for mass M")
    p.add_argument("--tol", type=float, default=0.5,
                   help="Tolerance on M for stopping")
    args = p.parse_args()

    try:
        Mcrit = find_critical_mass(
            args.mode, args.S, args.sigma_t, args.sigma_f,
            args.nu, args.N, args.M_min, args.M_max, args.tol
        )
        print(f"Estimated critical mass (mode={args.mode}): {Mcrit:.3f} ±{args.tol/2}")
    except Exception as e:
        print(f"ERROR: {e}")
