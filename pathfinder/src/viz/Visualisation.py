"""
Visualise data from .pkl files
chunk_a_b.pkl: a = spawn rate (simulation instance), b = chunk count 
"""
import matplotlib.pyplot as pl
import pickle as pk
import os

root = "./bin"

file_list = [os.path.join(root,file) for file in os.listdir(root) if os.path.isfile(os.path.join(root,file))]

file_list.sort(key = lambda x: os.path.getmtime(x))

Ongrid = {1:[], 2:[], 3:[], 4:[], 5:[]}
SpawnTotal = {1:[], 2:[], 3:[], 4:[], 5:[]}
SpawnCurrent = {1:[], 2:[], 3:[], 4:[], 5:[]}
Offgrid = {1:[], 2:[], 3:[], 4:[], 5:[]}
OffgridCurrent = {1:[], 2:[], 3:[], 4:[], 5:[]}

#measurement: ongrid, spawntotal, etc. Label: "ongrid", "spawntotal", etc.
def data_processing(measurement, label):
    
    for path in file_list:
        
        simnumber = int(path[12])
        
        with open(path,"rb") as output:
            
            load_data = pk.load(output)
            
            measurement[simnumber] += load_data[label]
    
    for i in measurement.keys():
        if measurement[i] != []:
            pl.plot(measurement[i], label = f"Spawn Rate {i}")
            pl.xlabel("Time Step")
            pl.ylabel(label)
            pl.legend()

        
    pl.show()
    
    return measurement


data_processing(Ongrid,"Ongrid")
data_processing(SpawnTotal, "SpawnTotal")
data_processing(SpawnCurrent,"SpawnCurrent")
data_processing(Offgrid,"Offgrid")
data_processing(OffgridCurrent,"OffgridCurrent")
    
print(Ongrid)