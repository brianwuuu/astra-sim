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
workload = "MLP_ModelParallel" # microAllReduce
topology_type = "switch"
experiment = "hbmBandwidth"
experiment_directory = RESULT_DIRECTORY + "{}-{}-{}/".format(topology_type, workload, experiment)
backend_dim_info_file = experiment_directory + "backend_dim_info.csv"
backend_end_to_end_file = experiment_directory + "backend_end_to_end.csv"
detailed_file = experiment_directory + "detailed.csv"
end_to_end_file = experiment_directory + "EndToEnd.csv"
################################################################################################################
################################################################################################################

# Simulation Parameter setup
npus = [16, 64] # 128, 256, 512
hbmbandwidths = [16, 32, 64, 128, 256, 512, 1024, 2048]
hbmlatencies = [100, 1000, 10000]
linklatencies = [100, 500, 1000, 5000, 10000]
linkbandwidths = (50, 100, 200, 300, 500, 1000)
params_1 = ("npus", npus)
# params_2 = ("hbmLatency", hbmlatencies, "HBM Latencies (ns)")
params_2 = ("hbmbandwidth", hbmbandwidths, "HBM Bandwidth (GB/s)")
# params_2 = ("linklatency", linklatencies, "Link Latencies (ns)")
# params_2 = ("linkbandwidth", linkbandwidths, "Link Bandwidth (GB/s)")


def analyzeEndToEnd():
    layer = "layer_64_1_mlp0"
    parameter = "workload_finished_at"
    file_fields, file_dict = utils.readEndToEndFile(end_to_end_file)
    parameter_index = file_fields.index(parameter)
    jct_stats = defaultdict(list)
    for param_1 in params_1[1]:
        for param_2 in params_2[1]:
            job_name = "workload-{}-{}-{}-{}-{}".format(workload, params_1[0], param_1, params_2[0], param_2)
            jct_stats["{} GPUs".format(param_1)].append(float(file_dict[layer][job_name][parameter_index]))
    print(jct_stats)
    x_bw = {"label": params_2[2], "data": params_2[1]}
    y_jct = {"label": "Job Completion Time (ns)", "data": jct_stats}
    path = ANALAYSIS_OUTPUT_DIRECTORY + "{}-{}-JCT-{}.png".format(topology_type, workload, params_2[0])
    utils.plotMultiColBarChart(x_bw, y_jct, log=False, path=path)

def analyzeBackendEndToEnd():
    file_fields, file_dict = utils.readBackendEndToEndFile(backend_end_to_end_file)
    jct_stats = defaultdict(list)
    metrics = ["CommsTime", "ComputeTime", "ExposedCommsTime"]
    for metric in metrics:
        metric_index = file_fields.index(metric)
        for param_1 in params_1[1]:
            for param_2 in params_2[1]:
                job_name = "workload-{}-{}-{}-{}-{}".format(workload, params_1[0], param_1, params_2[0], param_2)
                jct_stats["{} GPUs_{}".format(param_1, metric)].append(float(file_dict[job_name][metric_index]))
        # print(jct_stats)
    x_bw = {"label": params_2[2], "data": params_2[1]}
    y_jct = {"label": "Time in (ns)", "data": jct_stats}
    path = ANALAYSIS_OUTPUT_DIRECTORY + "{}-{}-CommTime-{}.png".format(topology_type, workload, params_2[0])
    utils.plotMultiLineChart(x_bw, y_jct, log=False, path=path)

def main():
    print("[ANALYSIS] Starting analysis ...")
    print("[ANALYSIS] Workload: {}, Topology Type: {}".format(workload, topology_type))
    # analyzeEndToEnd()
    analyzeBackendEndToEnd()

if __name__ == '__main__':
    main()