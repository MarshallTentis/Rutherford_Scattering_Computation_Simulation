import random
import math
import argparse

def simulate_block(M, S, N):
    """
    Simulate the survival fraction f for a rectangular block of uranium
    with mass M, shape ratio S = a/b, using N random fissions.
    Uses nine random numbers per fission as described in the PDF.
    """
    # Compute dimensions a and b from M and S (density = 1)
    a = (M * S)**(1/3)
    b = (M / (S**2))**(1/3)
    
    Nin = 0
    for _ in range(N):
        # Generate nine random numbers r1...r9
        r = [random.random() for _ in range(9)]
        # Map to geometry and neutron parameters
        x0 = a * (r[0] - 0.5)
        y0 = a * (r[1] - 0.5)
        z0 = b * (r[2] - 0.5)
        
        # First neutron
        phi1 = 2 * math.pi * r[3]
        cos_theta1 = 2 * (r[4] - 0.5)
        sin_theta1 = math.sqrt(1 - cos_theta1**2)
        d1 = r[7]
        x1 = x0 + d1 * sin_theta1 * math.cos(phi1)
        y1 = y0 + d1 * sin_theta1 * math.sin(phi1)
        z1 = z0 + d1 * cos_theta1
        
        # Second neutron
        phi2 = 2 * math.pi * r[5]
        cos_theta2 = 2 * (r[6] - 0.5)
        sin_theta2 = math.sqrt(1 - cos_theta2**2)
        d2 = r[8]
        x2 = x0 + d2 * sin_theta2 * math.cos(phi2)
        y2 = y0 + d2 * sin_theta2 * math.sin(phi2)
        z2 = z0 + d2 * cos_theta2
        
        # Count induced fissions
        if -a/2 <= x1 <= a/2 and -a/2 <= y1 <= a/2 and -b/2 <= z1 <= b/2:
            Nin += 1
        if -a/2 <= x2 <= a/2 and -a/2 <= y2 <= a/2 and -b/2 <= z2 <= b/2:
            Nin += 1
    
    return Nin / N

def simulate_sphere(M, N):
    """
    Simulate the survival fraction f for a sphere of uranium with mass M
    (density=1), using N random fissions and nine random numbers per fission.
    """
    radius = ((3 * M) / (4 * math.pi)) ** (1/3)
    Nin = 0
    for _ in range(N):
        # Generate nine random numbers for two neutrons
        # First, choose a random point inside the sphere via rejection sampling
        while True:
            r1, r2, r3 = random.random(), random.random(), random.random()
            x0 = (2*r1 - 1) * radius
            y0 = (2*r2 - 1) * radius
            z0 = (2*r3 - 1) * radius
            if x0**2 + y0**2 + z0**2 <= radius**2:
                break
        
        # Random numbers for neutron directions and distances
        r4, r5, r6, r7, r8, r9 = [random.random() for _ in range(6)]
        
        # First neutron
        phi1 = 2 * math.pi * r4
        cos_theta1 = 2 * (r5 - 0.5)
        sin_theta1 = math.sqrt(1 - cos_theta1**2)
        d1 = r7
        x1 = x0 + d1 * sin_theta1 * math.cos(phi1)
        y1 = y0 + d1 * sin_theta1 * math.sin(phi1)
        z1 = z0 + d1 * cos_theta1
        
        # Second neutron
        phi2 = 2 * math.pi * r6
        cos_theta2 = 2 * (r8 - 0.5)
        sin_theta2 = math.sqrt(1 - cos_theta2**2)
        d2 = r9
        x2 = x0 + d2 * sin_theta2 * math.cos(phi2)
        y2 = y0 + d2 * sin_theta2 * math.sin(phi2)
        z2 = z0 + d2 * cos_theta2
        
        # Count induced fissions
        if x1**2 + y1**2 + z1**2 <= radius**2:
            Nin += 1
        if x2**2 + y2**2 + z2**2 <= radius**2:
            Nin += 1
    
    return Nin / N

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo simulation of a nuclear chain reaction.")
    parser.add_argument("mode", choices=["block", "sphere"], help="Geometry: block or sphere")
    parser.add_argument("-M", type=float, required=True, help="Mass of uranium (density=1)")
    parser.add_argument("-S", type=float, default=1.0, help="Shape ratio a/b (only for block)")
    parser.add_argument("-N", type=int, default=10000, help="Number of random fissions")
    args = parser.parse_args()
    
    if args.mode == "block":
        f = simulate_block(args.M, args.S, args.N)
        print(f"Survival fraction f for block: M={args.M}, S={args.S}, N={args.N} -> f = {f:.4f}")
    else:
        f = simulate_sphere(args.M, args.N)
        print(f"Survival fraction f for sphere: M={args.M}, N={args.N} -> f = {f:.4f}")

if __name__ == "__main__":
    main()

