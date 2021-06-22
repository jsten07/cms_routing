from datetime import time, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.colors
import math


from calculate_objectives import calculate_time_differences
from calculate_objectives import calculate_fuelUse

startpoint=(330,120)
endpoint= (230,900)





#load results
path= "."
results = np.load("values.npy")
maps = np.load("routes.npy", allow_pickle=True)
print(results)
print(maps)

route_minTime = maps[np.argmin(results[:,0], axis=0)][1]
route_minfuelUSe = maps[np.argmin(results[:,1], axis=0)][1]

routeDisplay=   np.stack(route_minTime, axis=-1)
routeDisplay2=   np.stack(route_minfuelUSe, axis=-1)
timeGrid = np.load("first_prediction.npy", allow_pickle=True)
timeGrid = timeGrid[250:750, 1200:2200]
timeGrid = np.where((timeGrid < -1.9) & (timeGrid > -2), 1000, timeGrid)
timeGrid = np.where(timeGrid >999, timeGrid, (timeGrid*timeGrid) +2)
timeGrid = np.where(timeGrid >999, timeGrid, (10/timeGrid))

plt.figure(figsize=(14,7))
# Costs
plt.imshow(timeGrid, aspect='auto', vmin=np.min(timeGrid), vmax=10);
# Route
plt.plot(routeDisplay[1],routeDisplay[0], 'r')
plt.plot(routeDisplay2[1],routeDisplay2[0], 'b')
# Start/end points
plt.plot(startpoint[1], startpoint[0], 'k^', markersize=15)
plt.plot(endpoint[1], endpoint[0], 'k*', markersize=15)
# plt.gca().invert_yaxis();

def find_nearest(array, value):
    idx = np.argmin(np.abs(array - value))
    return idx

# Pareto Front
def transformTick(timeDifference):
    td = timedelta(minutes=timeDifference)
    return ".".join(str(td).split(':')[:2])
    

timeDiffs= results[:,0]
timeDiff = np.array([math.sqrt(x) for x in timeDiffs])

f1, ax1 = plt.subplots(1)
plt.scatter(timeDiff,results[:,1])
a= ax1.get_xticks().tolist()
print(a)
result= map(transformTick, a)
ax1.set_xticklabels(result)
ax1.set_title("Objective Space")
ax1.set_xlabel('Time Difference')
ax1.set_ylabel('Fuel Use')
#plt.savefig(default_directory+"/results2016N6/pareto_front.png")
plt.show()







# Hypervolume 
from pymoo.performance_indicator.hv import Hypervolume
# make an array of the generation numbers
n_gen = np.array(range(1,len(history)+1))
# set reference point
ref_point = np.array([0.0, 0.0])
# create the performance indicator object with reference point
metric = Hypervolume(ref_point=ref_point, normalize=False)
# calculate for each generation the HV metric
hv = [metric.calc(i) for i in history]
# visualze the convergence curve
fig5, ax5 = plt.subplots(1)
ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
ax5.set_xlabel("Generation")
ax5.set_ylabel("Hypervolume")
#plt.savefig(default_directory+"/figures/hypervolume.png")
plt.show()
