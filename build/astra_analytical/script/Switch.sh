#!/bin/bash
set -e

# workload=medium_DLRM
# workload=microAllReduce
# workload=MLP_ModelParallel
# workload=Resnet50_DataParallel
workload=Transformer_HybridParallel

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

npus=(16 64) #  64
hbmbandwidth=(512) # 16 32 64 128 256 512 1024 2048
# hbmlatency=(100 1000 10000)
# linkbandwidth=(50 100 200 300 500 1000)
# linklatency=(100 500 1000 5000 10000)
# make another for loop to iterate over hbm-bandwidth
commScale=(1)

current_row=-1
tot_stat_row=$((${#npus[@]} * ${#hbmbandwidth[@]}))

# run test
for npu in "${npus[@]}"; do
  for bw in "${hbmbandwidth[@]}"; do
    current_row=$(($current_row + 1))
    filename="workload-$workload-npus-${npu}-hbmbandwidth-${bw}"

    echo "[SCRIPT] Initiate ${filename}"

    nohup "${BINARY}" \
      --network-configuration="${NETWORK}" \
      --system-configuration="${SYSTEM}" \
      --workload-configuration="${WORKLOAD}" \
      --path="${STATS}/" \
      --units-count "${npu}" \
      --hbm-bandwidth "${bw}" \
      --num-passes 1 \
      --num-queues-per-dim 1 \
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
