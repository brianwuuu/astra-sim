import sys, os, csv
import json, pprint
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Plotting related
mark_cycle = ['d', '+', 's', 'x','v','1', 'p', ".", "o", "^", "<", ">", "1", "2", "3", "8", "P"]
markersize_arg = 4

def parseJSON(filename):
    print("*** Parsing JSON file from " + filename)
    with open(filename) as json_file: 
        file = json.load(json_file)
    return file

def readEndToEndFile(filename):
    file_fields =  ["fwd_compute", "wg_compute", "ig_compute", 
                    "fwd_exposed_comm", "wg_exposed_comm", "ig_exposed_comm",
                    "fwd_total_comm", "wg_total_comm", "ig_total_comm",
                    "workload_finished_at", "total_comp", "total_exposed_comm"]
    file_dict = {}
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        layer = ""
        for i, row in enumerate(csv_reader):
            if i == 0: continue  # ignore the header row
            if row[0] != "": # identify the layers
                layer = row[0]
                file_dict[layer] = {}
            job, stats = row[1], [float(x) for x in row[2:13] if x != ""]
            file_dict[layer][job] = stats
    return file_fields, file_dict

def readBackendEndToEndFile(filename):
    file_fields =  ["CommsTime", "ComputeTime", "ExposedCommsTime", 
                    "Cost", "TotalPayloadSize", "PayloadSize_Dim0",
                    "PayloadSize_Dim1", "PayloadSize_Dim2", "PayloadSize_Dim3",
                    "PayloadSize_Dim4", "PayloadSize_Dim5", "PayloadSize_Dim6"]
    file_dict = {}
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        layer = ""
        for i, row in enumerate(csv_reader):
            if i == 0: continue  # ignore the header row
            if row[0] != "": layer = row[0]
            stats = [float(x) for x in row[1:13] if x != ""]
            file_dict[layer] = stats
    return file_fields, file_dict

def readDimensionUtilizationFile(filename):
    file_fields = ["Time", "Dim1_util"]
    time, dim1_util = [], []
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i != 0 and row[0] != "": 
                time.append(float(row[0]))
                dim1_util.append(float(row[1]))
    file_dict = {"Time":time, "Dim1_util":dim1_util}
    return file_fields, file_dict    

################################################################################################################
####################################    PLOTTING FUNCTIONS    ##################################################
################################################################################################################

def plotMultiLineChart(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting multiline chart to " + path)
    for parameter, marker_arg in zip(y["data"].keys(), mark_cycle):
        plt.plot(x["data"], (np.log10(y["data"][parameter]) if log else y["data"][parameter]), label=parameter, marker=marker_arg)
    plt.xlabel(x["label"])
    plt.ylabel(("Log " if log else "" )+ y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    plt.xticks(x["data"], fontsize=6) # rotation="45"
    plt.legend()
    if path and not os.path.isfile(path): plt.savefig(path)
    else: plt.show()
    plt.close()

def plotMultiLineChartDifferentLength(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting multiline chart to " + path)
    fig, ax = plt.subplots()
    max_x = 0
    for parameter, marker_arg in zip(y["data"].keys(), mark_cycle):
        ax.plot(x["data"][parameter], (np.log10(y["data"][parameter]) if log else y["data"][parameter]), label=parameter, marker=marker_arg)
        max_x = max(max_x, max(x["data"][parameter]))
    plt.xlabel(x["label"])
    plt.ylabel(("Log " if log else "" )+ y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    plt.xticks(np.arange(0,max_x,int(max_x/10)), fontsize=8) # rotation="45"
    plt.yticks(np.arange(0,140,10), fontsize=5)
    ax.legend(loc="upper center", ncol=5, shadow=True, fontsize='x-small')
    fig.set_size_inches(10, 5)
    if path and not os.path.isfile(path): plt.savefig(path)
    else: plt.show()
    plt.close()

def plotLineChart(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting line chart to" + path)
    plt.plot(x["data"], [np.log10(x) for x in y["data"].values()] if log else y["data"].values(), marker="p")
    plt.xlabel(x["label"])
    plt.ylabel("Log " if log else "" + y["label"])
    plt.title(y["label"] + " vs " + x["label"], fontsize=12)
    plt.xticks(x["data"], fontsize=6) # rotation="45"
    if path and not os.path.isfile(path): plt.savefig(path)
    else: plt.show()
    plt.close()

def plotMultiColBarChart(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting bar chart for " + y["label"] + " vs " + x["label"])
    num_pairs = len(x["data"])
    ind = np.arange(num_pairs)
    width = 0.2
    plt.figure(figsize=(15,5))
    for i, parameter in enumerate(y["data"].keys()):
        print(ind+i*width)
        plt.bar(ind+i*width, np.log10(y["data"][parameter]) if log else y["data"][parameter], label=parameter, width=width)
    plt.xlabel(x["label"])
    plt.ylabel("Log " if log else "" + y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    # print(ind+(len(y["data"].keys())*width)/2)
    plt.xticks(ind+(len(y["data"].keys())*width)/4, x["data"], fontsize=6) # rotation="45"
    plt.legend()
    if path and not os.path.isfile(path): plt.savefig(path)
    else: plt.show()
    plt.close()

def plotMultiColStackedBarChart(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting multi-stacked bar chart for " + y["label"] + " vs " + x["label"])
    color_cycle = [("dimgray", "darkgray"), ("blue", "steelblue"), ("darkgoldenrod", "goldenrod"), ("orange", "bisque"), ("red", "tomato")]
    num_pairs = len(x["data"])
    ind = np.arange(num_pairs)
    width = 0.15
    plt.figure(figsize=(12,5))
    for i, parameter in enumerate(y["data"].keys()): # num GPUs
        bottom = [0] * (len(x["data"]))
        color_pair = color_cycle[i % len(color_cycle)]
        for j, secondary_param in enumerate(y["data"][parameter].keys()): # Compute vs Exposed Comms
            color = color_pair[j % len(color_pair)]
            plt.bar(ind+i*width, y["data"][parameter][secondary_param], bottom=bottom, label="{}-{}".format(secondary_param, parameter), width=width, color=color)
            bottom = y["data"][parameter][secondary_param]
    plt.xlabel(x["label"])
    plt.ylabel("Log " if log else "" + y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    plt.xticks(ind+(len(y["data"].keys())*width)/4, x["data"], fontsize=6) # rotation="45"
    plt.yticks(np.arange(0,125,10))
    plt.legend(loc="upper center", ncol=3, shadow=True, fontsize='x-small')
    # if path and not os.path.isfile(path): plt.savefig(path)
    # else: plt.show()
    plt.savefig(path)
    # plt.show()
    plt.close()
    
def plotHorizontalStackedBarChart():
    fig, ax = plt.subplots(1,1,figsize=(8,2))
    labels = ["TPU-Torus", "DGX-A100", "MMC"]
    compute_time = [1082.45, 1082.45, 1082.45]
    # exposed_comm_time = [20.893, 18.773, 15.589] # DP 8 CUs
    # exposed_comm_time = [29.06, 15.628, 9.554] # DP 16 CUs
    exposed_comm_time = [452.564, 117.914, 94.429] # Resnet 16 CUs
    width = 0.35
    ax.barh(labels, compute_time, width, label='Compute Time (us)')
    ax.barh(labels, exposed_comm_time, width, left=compute_time,label='Exposed Comm Time (us)')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.35))
    ax.set_xlabel("Time (us)")
    plt.tight_layout()
    plt.show()
    return