import function as func
import csv
import os
import dotenv



def sim(i=1):
  dotenv.load_dotenv()

  # Load constants
  K = float(os.environ.get("K"))
  Q_1 = float(os.environ.get("Q_1"))
  Q_2 = float(os.environ.get("Q_2"))
  M = float(os.environ.get("M"))
  # T = float(os.environ.get("T"))
  KE_intial = float(os.environ.get("KE_intial"))

  T = 5

  # Initial conditions
  X0 = -3.00e-13
  Y0 = 1.6e-14
  VX0 = 0.0
  VY0 = 0.0
  FX0 = 0.0
  FY0 = 0.0
  AX0 = 0.0
  AY0 = 0.0

  expo_factor = 0

  # Initialize particles
  AlphaParticle = func.AlphaParticle(X0, i*Y0, VX0, VY0, FX0, FY0, AX0, AY0, KE_intial, M)
  GoldParticle = func.GoldNucleus()

  # Prepare CSV output
  csv_file_path = 'data.csv'

  with open(csv_file_path, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      header = ["x_position", "y_position", "x_velocity", "y_velocity", "x_force", "y_force", "x_acceleration", "y_acceleration"]
      csv_writer.writerow(header)
      AlphaParticle.gen_V_intial()
      print(AlphaParticle.Vx, AlphaParticle.Vy)
      for i in range(0, 200):
          T = AlphaParticle.step(T, expo_factor)
          data = AlphaParticle.updated_values()
          print(data)
          csv_writer.writerow(data)
      

  scattering_angle = AlphaParticle.get_scattering_angle()
  return scattering_angle
  

