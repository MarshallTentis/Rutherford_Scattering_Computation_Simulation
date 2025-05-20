#!/usr/bin/env python3
import random
import math
import argparse

def simulate_block(M, S, N, sigma_t, sigma_f):
    """
    Simulate the *fission survival fraction* f for a rectangular block
    of mass M (density=1) and shape ratio S = a/b, using N fission events.
    - sigma_t: total macroscopic cross-section (e.g. cm^-1)
    - sigma_f: fission macroscopic cross-section
    Returns: f = (number of fissions induced next generation) / N
    """
    # fission probability on collision
    P_f = sigma_f / sigma_t

    # block half‑dimensions
    a = (M * S)**(1/3)
    b = (M / (S**2))**(1/3)

    Nin = 0
    for _ in range(N):
        # pick a random fission site uniformly inside block
        x0 = (random.random() - 0.5) * a
        y0 = (random.random() - 0.5) * a
        z0 = (random.random() - 0.5) * b

        # for each of two daughter neutrons
        for phi_r, mu_r in [(random.random(), random.random()),
                            (random.random(), random.random())]:
            # isotropic direction
            phi = 2 * math.pi * phi_r
            cos_theta = 2*(mu_r - 0.5)
            sin_theta = math.sqrt(max(0.0, 1 - cos_theta*cos_theta))

            # sample flight‑path length from exponential distribution
            d = -math.log(1.0 - random.random()) / sigma_t

            # new position
            x1 = x0 + d * sin_theta * math.cos(phi)
            y1 = y0 + d * sin_theta * math.sin(phi)
            z1 = z0 + d * cos_theta

            # check if neutron stays inside block
            if (-a/2 <= x1 <= a/2
                and -a/2 <= y1 <= a/2
                and -b/2 <= z1 <= b/2):
                # count a new fission with probability P_f
                if random.random() < P_f:
                    Nin += 1

    return Nin / N


def simulate_sphere(M, N, sigma_t, sigma_f):
    """
    Simulate the survival fraction f for a sphere of mass M (density=1),
    using N fission events.
    - sigma_t: total macroscopic cross-section
    - sigma_f: fission macroscopic cross-section
    """
    P_f = sigma_f / sigma_t
    # compute radius from mass (density=1)
    radius = ((3 * M) / (4 * math.pi)) ** (1/3)

    Nin = 0
    for _ in range(N):
        # pick a random fission site uniformly inside sphere
        while True:
            x0 = (2*random.random() - 1) * radius
            y0 = (2*random.random() - 1) * radius
            z0 = (2*random.random() - 1) * radius
            if x0*x0 + y0*y0 + z0*z0 <= radius*radius:
                break

        # two daughter neutrons
        for phi_r, mu_r in [(random.random(), random.random()),
                            (random.random(), random.random())]:
            phi = 2 * math.pi * phi_r
            cos_theta = 2*(mu_r - 0.5)
            sin_theta = math.sqrt(max(0.0, 1 - cos_theta*cos_theta))

            d = -math.log(1.0 - random.random()) / sigma_t

            x1 = x0 + d * sin_theta * math.cos(phi)
            y1 = y0 + d * sin_theta * math.sin(phi)
            z1 = z0 + d * cos_theta

            if x1*x1 + y1*y1 + z1*z1 <= radius*radius:
                if random.random() < P_f:
                    Nin += 1

    return Nin / N


def main():
    p = argparse.ArgumentParser(
        description="Monte Carlo chain‑reaction: estimate next‑generation fission fraction f")
    p.add_argument("mode", choices=["block", "sphere"],
                   help="geometry: block or sphere")
    p.add_argument("-M", type=float, required=True,
                   help="mass of fissile material (density=1 units)")
    p.add_argument("-S", type=float, default=1.0,
                   help="shape ratio a/b (only for block)")
    p.add_argument("-N", type=int, default=100000,
                   help="number of fission events to simulate")
    p.add_argument("--sigma-t", type=float, default=1.0,
                   help="macroscopic total cross-section Σₜ")
    p.add_argument("--sigma-f", type=float, default=0.5,
                   help="macroscopic fission cross-section Σ_f")

    args = p.parse_args()

    if args.mode == "block":
        f = simulate_block(args.M, args.S, args.N,
                           args.sigma_t, args.sigma_f)
        print(f"Block: M={args.M}, S={args.S}, Σₜ={args.sigma_t}, Σ_f={args.sigma_f}, N={args.N} -> f = {f:.5f}")
    else:
        f = simulate_sphere(args.M, args.N,
                            args.sigma_t, args.sigma_f)
        print(f"Sphere: M={args.M}, Σₜ={args.sigma_t}, Σ_f={args.sigma_f}, N={args.N} -> f = {f:.5f}")

if __name__ == "__main__":
    main()
