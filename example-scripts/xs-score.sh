set -x

ulimit -n 4096

export PYTHONPATH=`pwd`

prefix=$1
base_stats_dir=/nfs/home/liuziang/Workspace/XiangShan-base/spec-result-base
dev_stats_dir=/nfs/home/liuziang/Workspace/XiangShan-l2hint/spec-result-new-hint

PERF_HOME=/nfs/home/liuziang/Workspace/checkpoints
gcc12O3_2=/nfs/home/liuziang/Workspace/checkpoints/spec06_rv64gcb_O3_20m_gcc12.2.0-intFpcOff-jeMalloc
cover1_path_2=$gcc12O3_2/checkpoint-0-0-0/cluster-0-0.json
cover3_path_2=$PERF_HOME/json/gcc12o3-incFpcOff-jeMalloc-0.3.json
cover8_path_2=$PERF_HOME/json/gcc12o3-incFpcOff-jeMalloc-0.8.json

if [ $prefix = "dev" ]; then
    stats_dir=$dev_stats_dir
else
    stats_dir=$base_stats_dir
fi

rm -r $prefix-results
mkdir -p $prefix-results

tag="xs-$prefix"

python3 batch.py -s $stats_dir -o $prefix-results/$tag.csv -X

python3 simpoint_cpt/compute_weighted.py \
    -r $prefix-results/$tag.csv \
    -j $cover3_path_2 \
    --score $prefix-results/$tag-score.csv
