#!/bin/bash
set -e

# workload=medium_DLRM
workload=microAllReduce

# Absolue path to this script
SCRIPT_DIR=$(dirname "$(realpath $0)")

# Absolute paths to useful directories
PROJECT_DIR="${SCRIPT_DIR:?}"/../../..
INPUT_DIR=${PROJECT_DIR}/inputs
COMPILE_SCRIPT="${SCRIPT_DIR:?}"/../build.sh
BINARY="${SCRIPT_DIR:?}"/../build/AnalyticalAstra/bin/AnalyticalAstra
NETWORK=${INPUT_DIR}/network/analytical/disaggregated_memory/test_switch.json
SYSTEM=${INPUT_DIR}/system/sample_a2a_sys.txt
WORKLOAD=${INPUT_DIR}/workload/"$workload".txt
STATS="${SCRIPT_DIR:?}"/../result/switch-${workload}${1:-$result}

# create result directory
rm -rf "${STATS}"
mkdir -p "${STATS}"

# compile binary
echo "[SCRIPT] Compiling AnalyticalAstra"
"${COMPILE_SCRIPT}" -c

npus=(16 64 128 256 512) #  64
# npus=(4 16 32 64 128 256 512 1024 2048)
# hbmbandwidth=(16 32 64 128 256) #(16 32 64 128 256
hbmlatency=(100 1000 10000) 
# make another for loop to iterate over hbm-bandwidth
commScale=(1)

current_row=-1
tot_stat_row=$((${#npus[@]} * ${#hbmlatency[@]}))

# run test
for npu in "${npus[@]}"; do
  for latency in "${hbmlatency[@]}"; do
    current_row=$(($current_row + 1))
    filename="workload-$workload-npus-${npu}-hbmLatency-${latency}"

    echo "[SCRIPT] Initiate ${filename}"

    nohup "${BINARY}" \
      --network-configuration="${NETWORK}" \
      --system-configuration="${SYSTEM}" \
      --workload-configuration="${WORKLOAD}" \
      --path="${STATS}/" \
      --units-count "${npu}" \
      --num-passes 2 \
      --num-queues-per-dim 1 \
      --hbm-latency ${latency} \
      --comm-scale 1 \
      --compute-scale 1 \
      --injection-scale 1 \
      --rendezvous-protocol false \
      --total-stat-rows "${tot_stat_row}" \
      --stat-row "${current_row}" \
      --run-name ${filename} >> "${STATS}/${filename}.txt" &
      
      sleep 1
  done
done
