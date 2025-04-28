import csv
from sim import sim


i_list = [1,2,4,8,16]

with open("./metadata.csv", 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      header = ["i", "scattering angle"]
      csv_writer.writerow(header)

      for i in i_list:
        csv_writer.writerow( [i,sim(i)])
      
      print("finish writing csv")




  