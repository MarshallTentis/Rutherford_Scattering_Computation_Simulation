import os
import math
import dotenv

dotenv.load_dotenv()

# Load constants
K = float(os.environ.get("K"))
Q_1 = float(os.environ.get("Q_1"))
Q_2 = float(os.environ.get("Q_2"))
M = float(os.environ.get("M"))
T = float(os.environ.get("T"))
KE_intial = float(os.environ.get("KE_intial"))

CONST = K * Q_1 * Q_2 / M

class AlphaParticle:
    def __init__(self, X, Y, Vx, Vy, Fx, Fy, Ax, Ay, KE_intial,M):
        self.X = X
        self.Y = Y
        self.Vx = Vx
        self.Vy = Vy
        self.Fx = Fx
        self.Fy = Fy
        self.Ax = Ax
        self.Ay = Ay
        self.prev_Ax = 0
        self.prev_Ay = 0
        self.KE_intial = KE_intial
        self.M = M

    def update_force(self):
        r_squared = self.X**2 + self.Y**2
        r = math.sqrt(r_squared)
        force_magnitude = K * Q_1 * Q_2 / r_squared
        self.Fx = force_magnitude * (self.X / r)
        self.Fy = force_magnitude * (self.Y / r)

    def update_acceleration(self):
        self.prev_Ax = self.Ax
        self.prev_Ay = self.Ay
        self.Ax = self.Fx / M
        self.Ay = self.Fy / M

    def update_velocity(self):
        self.Vx += 0.5 * (self.prev_Ax + self.Ax) * T
        self.Vy += 0.5 * (self.prev_Ay + self.Ay) * T

    def update_position(self):
        self.X += self.Vx * T + 0.5 * self.prev_Ax * T**2
        self.Y += self.Vy * T + 0.5 * self.prev_Ay * T**2

    def step(self):
        self.update_force()
        self.update_acceleration()
        self.update_velocity()
        self.update_position()

    def updated_values(self):
        return [self.X, self.Y, self.Vx, self.Vy, self.Fx, self.Fy, self.Ax, self.Ay]
    
    def gen_V_intial(self):
        V_intial = math.sqrt(2*self.KE_intial/self.M)
        
        self.Vx = V_intial
        self.Vy = 0

    def get_scattering_angle(self):
        scattering_angle = math.atan2(self.Y, self.X)
        return scattering_angle


class GoldNucleus:
    def __init__(self):
        self.X = 0
        self.Y = 0
