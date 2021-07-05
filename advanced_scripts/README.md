### Scripts
In the folder scripts you find scripts to work with the data
- readData.py transforms the tif files to pcraster and npy files. You do not have to run this skript, the processed Data is already uploaded in the folder `/data/finalData`
- calculate_objectives.py calculates our objectives (total revenue and vegetation area). To run this skript please set the working directory.
    - 2001 use the transport distances from 2001
    - 2016 use the transport distances from 2016
- spatial_crossover.py transform the crossover of the nsga II. Further information about NSGA-II: [https://doi.org/10.1109/4235.996017](https://doi.org/10.1109/4235.996017)
- spatial_mutation.py transform the crossover of the nsga II. Further information about NSGA-II: [https://doi.org/10.1109/4235.996017](https://doi.org/10.1109/4235.996017)
- run_nsga2_spatial.py runs the algorithm and save the results
- plot.py plots the initial landuse map, the Pareto Front and the two extreme land use maps. Furthermore it shows how the area can be optimized. It indicates the points on the Pareto Front and the associated land use maps. Last it shows how the Pareto Front developed over generations and the Hypervolume. It shows data from the year which is specified in the config.yaml
- plot_both.py plots both Pareto Fronts at ones. Furthermore it shows how the profit can be optimized while keeping the are of natural vegetation of the inital map from 2016. Here it compares the optimized values for the different optimizations (2001 and 2016), while showing the values and associted land use maps.
- config.yaml to set the parameters for the optimization (e.g. population size, generations). Besides you can also set for the constraint concerning the governmental restrictions how much area of forest and cerrado (in %) needs to remain in each optimization step. The variables are intially already filled with values we used.