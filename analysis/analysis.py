import sys, os
import pprint
import numpy as np
import matplotlib.pyplot as plt
import utilities as utils
from collections import defaultdict

################################################################################################################
################################################################################################################
# DIRECTORY SETUP
BASE_DIRECTORY = "/Users/bwu/src/astra-sim"
ANALYSIS_DIRECTORY = BASE_DIRECTORY + "/analysis/"
ANALAYSIS_OUTPUT_DIRECTORY = ANALYSIS_DIRECTORY + "output/"
ANALYTICAL_DIRECTORY = BASE_DIRECTORY + "/build/astra_analytical"
RESULT_DIRECTORY = ANALYTICAL_DIRECTORY + "/result/"
SCRIPT_DIRECTORY = ANALYTICAL_DIRECTORY + "/script/"
################################################################################################################
################################################################################################################
# FILE SETUP
workload = "microAllReduce"
topology_type = "switch"
experiment = "hbmBW"
experiment_directory = RESULT_DIRECTORY + "{}-{}-{}/".format(topology_type, workload, experiment)
backend_dim_info_file = experiment_directory + "backend_dim_info.csv"
backend_end_to_end_file = experiment_directory + "backend_end_to_end.csv"
detailed_file = experiment_directory + "detailed.csv"
end_to_end_file = experiment_directory + "EndToEnd.csv"
################################################################################################################
################################################################################################################

# Simulation Parameter setup
npus = [16, 64, 128, 256, 512]
hbmbandwidths = [16, 32, 64, 128, 256]
hbmlatencies = [100, 1000, 10000]
params_1 = ("npus", npus)
# params_2 = ("hbmLatency", hbmlatencies)
params_2 = ("hbmBw", hbmbandwidths)

def analyzeParameters():
    layer = "conv1"
    parameter = "workload_finished_at"
    file_fields, file_dict = utils.readEndToEndFile(end_to_end_file)
    parameter_index = file_fields.index(parameter)
    jct_stats = defaultdict(list)
    for param_1 in params_1[1]:
        for param_2 in params_2[1]:
            job_name = "workload-{}-{}-{}-{}-{}".format(workload, params_1[0], param_1, params_2[0], param_2)
            jct_stats["{} GPUs".format(param_1)].append(float(file_dict[layer][job_name][parameter_index]))
    print(jct_stats)
    x_bw = {"label": "HBM Latencies (ns)", "data": params_2[1]}
    y_jct = {"label": "Job Completion Time (ns)", "data": jct_stats}
    path = ANALAYSIS_OUTPUT_DIRECTORY + "{}-{}-JCT-{}.png".format(topology_type, workload, params_2[0])
    utils.plotMultiColBarChart(x_bw, y_jct, log=False, path=path)

def main():
    print("[ANALYSIS] Starting analysis ...")
    print("[ANALYSIS] Workload: {}, Topology Type: {}".format(workload, topology_type))
    analyzeParameters()

if __name__ == '__main__':
    main()