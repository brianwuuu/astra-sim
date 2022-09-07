#!/bin/bash
set -e

# workload=medium_DLRM
# workload=microAllReduce
workload=microData
# workload=example_DATA
# workload=MLP_ModelParallel
# workload=Resnet50_DataParallel
# workload=Transformer_HybridParallel

# Absolue path to this script
SCRIPT_DIR=$(dirname "$(realpath $0)")

# Absolute paths to useful directories
PROJECT_DIR="${SCRIPT_DIR:?}"/../../..
INPUT_DIR=${PROJECT_DIR}/inputs
COMPILE_SCRIPT="${SCRIPT_DIR:?}"/../build.sh
BINARY="${SCRIPT_DIR:?}"/../build/AnalyticalAstra/bin/AnalyticalAstra
# NETWORK=${INPUT_DIR}/network/analytical/disaggregated_memory/dgx_a100.json
# NETWORK=${INPUT_DIR}/network/analytical/disaggregated_memory/mem_multicast.json
# SYSTEM=${INPUT_DIR}/system/dgx_sys.txt
# SYSTEM=${INPUT_DIR}/system/mem_multicast_sys.txt
WORKLOAD=${INPUT_DIR}/workload/"$workload".txt
STATS="${SCRIPT_DIR:?}"/../result/switch-${workload}${1:-$result}
STAT_ROW=-1 # start from where we left off 

echo ${1:$result}

if [ "${1:$result}" = "-dgx" ]; then
  NETWORK=${INPUT_DIR}/network/analytical/disaggregated_memory/dgx_a100.json
  SYSTEM=${INPUT_DIR}/system/dgx_sys.txt
elif [ "${1:$result}" = "-mem_multicast" ]; then
  NETWORK=${INPUT_DIR}/network/analytical/disaggregated_memory/mem_multicast.json
  SYSTEM=${INPUT_DIR}/system/mem_multicast_sys.txt
fi

# create result directory if doesn't exist
# from now, just create a new folder and manually copy paste into the old one
if [ $STAT_ROW -eq -1 ] || [ ! -d "${STATS}" ]; then
  echo "Creating new directory"
  rm -rf "${STATS}"
  mkdir -p "${STATS}"
fi

# compile binary
echo "[SCRIPT] Compiling AnalyticalAstra"
# "${COMPILE_SCRIPT}" -c

npus=(8) # 16 64 128 256 1024
hbmbandwidth=(1000) # 16 32 64 128 256 512 1024 2048
# hbmlatency=(100 1000 10000)
# linkbandwidth=(50 100 500 1000)
# linklatency=(100 500 1000 5000 10000)
# make another for loop to iterate over hbm-bandwidth
commScale=(1)

current_row=$STAT_ROW
tot_stat_row=$((${#npus[@]} * ${#hbmbandwidth[@]}))

# run test
for npu in "${npus[@]}"; do
  for param in "${hbmbandwidth[@]}"; do
    current_row=$(($current_row + 1))
    filename="workload-$workload-npus-${npu}-hbmbandwidth-${param}"

    echo "[SCRIPT] Initiate ${filename}"
    nohup "${BINARY}" \
      --network-configuration="${NETWORK}" \
      --system-configuration="${SYSTEM}" \
      --workload-configuration="${WORKLOAD}" \
      --path="${STATS}/" \
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
      echo "[SCRIPT] Current row: ${current_row}"
  done
done

# --units-count "${npu}" \
# --hbm-bandwidth "${param}" \
# --hbm-latency 500 \
# --link-latency 500 \
# --link-bandwidth 300 \