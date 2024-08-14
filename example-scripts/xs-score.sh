set -x

ulimit -n 4096

export PYTHONPATH=`pwd`

version="dev"

# example_stats_dir=/nfs-nvme/home/share/wkf/SPEC06_EmuTasks_1215_allbump
# example_stats_dir=/nfs/home/share/wulingyun/fuck_perf/SPEC06_EmuTasks_new_spec_padding66_1.0_jemalloc_peak_bwaves_2
# example_stats_dir=/nfs/home/liuziang/Workspace/Xiangshan-master/spec-result-gcc12
example_stats_dir=/nfs/home/liuziang/Workspace/spec-perf-result/$version
# example_stats_dir=/nfs/home/liuziang/Workspace/XiangShan-dev4/spec-gcc12-0330

PERF_HOME=/nfs/home/liuziang/Workspace/checkpoints
gcc12O3_2=/nfs/home/liuziang/Workspace/checkpoints/spec06_rv64gcb_O3_20m_gcc12.2.0-intFpcOff-jeMalloc
cpt_path_2=$gcc12O3_2/checkpoint-0-0-0
cover1_path_2=$gcc12O3_2/checkpoint-0-0-0/cluster-0-0.json
cover3_path_2=$PERF_HOME/json/gcc12o3-incFpcOff-jeMalloc-0.3.json
cover8_path_2=$PERF_HOME/json/gcc12o3-incFpcOff-jeMalloc-0.8.json

prefix=$version

rm -r $prefix-results
rm -r results
mkdir -p $prefix-results
mkdir -p results

tag="xs-$version"

python3 batch.py -s $example_stats_dir -o $prefix-results/$tag.csv -X
python3 simpoint_cpt/compute_weighted.py  \
    -r $prefix-results/$tag.csv \
    -j $cover3_path_2 \
    --score $prefix-results/$tag-score.csv

# -j /nfs/home/share/jiaxiaoyu/simpoint_checkpoint_archive/spec06_rv64gcb_O3_20m_gcc12.2.0-intFpcOff-jeMalloc/checkpoint-0-0-0/cluster-0-0.json