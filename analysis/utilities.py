import sys, os, csv
import json, pprint
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Plotting related
mark_cycle = ['d', '+', 's', 'x','v','1', 'p']
markersize_arg = 4

def parseJSON(filename):
    print("*** Parsing JSON file from " + filename)
    with open(filename) as json_file: 
        file = json.load(json_file)
    return file

def readEndToEndFile(filename):
    file_fields =    ["fwd_compute", "wg_compute", "ig_compute", 
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

################################################################################################################
####################################    PLOTTING FUNCTIONS    ##################################################
################################################################################################################

def plotMultiLineChart(x, y, log=False, path=None):
    print("[ANALYSIS] Plotting line chart to " + path)
    for transport, marker_arg in zip(y["data"].keys(), mark_cycle):
        plt.plot(x["data"], (np.log10(y["data"][transport]) if log else y["data"][transport]), label=transport, marker=marker_arg)
    plt.xlabel(x["label"])
    plt.ylabel(("Log " if log else "" )+ y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    plt.xticks(x["data"], fontsize=6) # rotation="45"
    plt.legend()
    plt.show()
    # if not os.path.isfile(path): plt.savefig(path)
    # plt.close()

def plotLineChart(x, y, log=False, path=None):
    print("[ANALYSIS] Plotting line chart to" + path)
    plt.plot(x["data"], [np.log10(x) for x in y["data"].values()] if log else y["data"].values(), marker="p")
    plt.xlabel(x["label"])
    plt.ylabel("Log " if log else "" + y["label"])
    plt.title(y["label"] + " vs " + x["label"], fontsize=12)
    plt.xticks(x["data"], fontsize=6) # rotation="45"
    plt.show()
    # if not os.path.isfile(path): plt.savefig(path)
    # plt.close()


def plotMultiColBarChart(x, y, log=False, path=""):
    print("[ANALYSIS] Plotting bar chart for " + y["label"] + " vs " + x["label"])
    num_pairs = len(x["data"])
    ind = np.arange(num_pairs)
    width = 0.2
    plt.figure(figsize=(15,5))
    for i, parameter in enumerate(y["data"].keys()):
        plt.bar(ind+i*width, np.log10(y["data"][parameter]) if log else y["data"][parameter], label=parameter, width=width)
    plt.xlabel(x["label"])
    plt.ylabel("Log " if log else "" + y["label"])
    plt.title(y["label"] + " vs " + x["label"])
    plt.xticks(ind+(num_pairs*width)/2, x["data"], fontsize=6) # rotation="45"
    plt.legend()
    if path and not os.path.isfile(path): plt.savefig(path)
    else: plt.show()
    plt.close()