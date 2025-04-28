import function as func
import csv

X0 = -3.00 * (10**(-13))
Y0 = 1.6 * (10**(-14))
VX0 = 0
VY0 = 0
FX0=0
FY0=0
AX0=0
AY0=0

AlphaParticle = func.AlphaParticle(X0, Y0, VX0, VY0, FX0, FY0, AX0, AY0)
GoldParticle = func.GoldNucleus()

csv_file_path = 'data.csv'

with open(csv_file_path, 'w', newline='') as csvfile:
  csv_writer = csv.writer(csvfile)
  data = ["x_position", "y_position", "x_velocity", "y_velocity", "x_force", "y_force", "x_acceleration", "y_acceleration"]
  csv_writer.writerows([data])
  for i in range(0, 15):
    AlphaParticle.get_Vx()
    AlphaParticle.get_Vy()
    AlphaParticle.get_Ax()
    AlphaParticle.get_Ay()
    AlphaParticle.get_x()
    AlphaParticle.get_y()
    AlphaParticle.get_Fx()
    AlphaParticle.get_Fy()
    data = AlphaParticle.updated_values()

csv_writer.writerows([data])