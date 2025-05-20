"""
This Program simulates fission in a CUBE. It used nine randomly generated numbers
that are between 0 and 1(inclusive), and uses them to calculate random
quantities that show up in this phenomena.

getInduced() uses the random variables and returns how many fissions are
induced by the nutrons from the origional random occuring fission.
"""

import random as rand
import numpy as np
import os

def getInduced(m,s):
    ##====Now Find dimmesions of block====
    a = (m*s)**(1/3) #from eq 5 in the lab
    b = (m/(s**2))**(1/3)

    #====Generate array of 9 random numbers====
    randList = []
    for i in range(9):
        randList.append(rand.uniform(0,1))

    #====Use random numbers to calculate needed quantities====
    #--------Coords of nucleus undergoing fission-------
    x_o = a*(randList[0]-(1/2))
    y_o = a*(randList[1]-(1/2))
    z_o = a*(randList[2]-(1/2))
    #--------angles for first emmited nutron-------
    phi_1 = 2*(np.pi)*(randList[3])
    cosTheta_1 = 2*(randList[4]-(1/2))
    Theta_1 = np.arccos(cosTheta_1)
    #--------angles for second emmited nutron-------
    phi_2 = 2*(np.pi)*(randList[5])
    cosTheta_2 = 2*(randList[6]-(1/2))
    Theta_2 = np.arccos(cosTheta_2)
    #-------distances traveled for each nutron-------
    d_1 = randList[7]
    d_2 = randList[8]

    #====now calculate new coords after distance traveled====
    #------For nutron 1------
    xFinal_1 = x_o+(d_1*np.sin(Theta_1)*np.cos(phi_1))
    yFinal_1 = y_o+(d_1*np.sin(Theta_1)*np.sin(phi_1))
    zFinal_1 = z_o+(d_1*np.cos(Theta_1))
    #------For nutron 2------
    xFinal_2 = x_o+(d_2*np.sin(Theta_2)*np.cos(phi_2))
    yFinal_2 = y_o+(d_2*np.sin(Theta_2)*np.sin(phi_2))
    zFinal_2 = z_o+(d_2*np.cos(Theta_2))

    N_i = 0

    if abs(xFinal_1) <= (a/2) and abs(yFinal_1) <= (a/2) and abs(zFinal_1) <= (a/2):
        N_i += 1
    if abs(xFinal_2) <= (a/2) and abs(yFinal_2) <= (a/2) and abs(zFinal_2) <= (a/2):
        N_i += 1
    
    return N_i

def sim_nFissionsForMass(n,m,s):
    '''simulates total induced fissions from n origional fissions for a specific mass'''
    totalInducedFissions = 0
    for i in range(n):
        result = getInduced(m,s)
        #print("this time there were "+str(result)+" induced fissions")
        totalInducedFissions += result
    return totalInducedFissions

def calcSurvivalFraction(n, totalinduced):
    '''calculates the Survival fraction for one use of sim_nFissionsForMass()'''
    return totalinduced/n
    
def find_critical_mass(S, N=100, step=0.1, tolerance=0.01):
    M = 0.1
    max_iters = 200
    for i in range(max_iters):
        totalInduced = sim_nFissionsForMass(N, M, S)
        f = calcSurvivalFraction(N, totalInduced)
        print(f"S: {S}, M: {M:.3f}, f: {f:.4f}", flush = True)
        if abs(f - 1.0) <= tolerance:
            return M
        M += step
    print(f"No critical mass found within {max_iters} steps.")
    return None

def averaged_critical_mass(S, trials=5):
    results = [find_critical_mass(S) for _ in range(trials)]
    valid = [r for r in results if r is not None]
    if valid:
        return sum(valid) / len(valid)
    else:
        return None  # or raise an error / warning


N = 150
targetF = 1.0
tolerance = 0.01
M = 0.1  # start small
step = 0.1
max_iters = 100
S_values = [0.5, 1.0, 1.5]

#====Loop and I want to write crit mass into a file====
#---file stuff---
output_dir = "cubeResults"
output_file = f"{output_dir}/critical_cube_mass_results.txt"
os.makedirs(output_dir, exist_ok=True)

with open(output_file, "w") as file:
    for S in S_values:
        crit_mass = averaged_critical_mass(S, trials=5)
        
        if crit_mass is not None:
            output_line = f"Estimated critical mass for S = {S} is {crit_mass:.3f}\n"
        else:
            output_line = f"Could not determine critical mass for S = {S} (no convergence)\n"

        print(output_line, end="")
        file.write(output_line)