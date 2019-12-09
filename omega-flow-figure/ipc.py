#!/usr/bin/env python3

import os.path as osp
import sys
sys.path.append('..')

import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import common as c
import graphs
import target_stats as t


strange_const = 3
show_lins = 62
pd.set_option('precision', 3)
pd.set_option('display.max_rows', show_lins)
pd.set_option('display.min_rows', show_lins)

full = True
do_normalization = True
# do_normalization = False

suffix = '-full' if full else ""
stat_dirs = {
        # 'Xbar4': 'xbar4',
        'Xbar4': 'xbar4-rand',
        # 'Xbar4-SpecSB': 'xbar4-rand-hint',
        # 'Xbar4*2-SpecSB': 'dedi-xbar4-rand-hint',
        #'Omega16': 'omega',
        #'Omega16-OPR': 'omega-rand',
        'Omega16-OPR-SpecSB': 'omega-rand-hint',
        #'Xbar16': 'xbar',
        #'Xbar16-OPR': 'xbar-rand',
        #'Xbar16-OPR-SpecSB': 'xbar-rand-hint',
        'Ideal-OOO': 'ruu-4-issue',
        }
for k in stat_dirs:
    stat_dirs[k] = c.env.data(f'{stat_dirs[k]}{suffix}')

configs_ordered = ['Xbar4', 'Omega16-OPR-SpecSB', 'Ideal-OOO']

benchmarks = [*c.get_spec2017_int(), *c.get_spec2017_fp()]

points = []
for b in benchmarks:
    for i in range(0, 3):
        points.append(f'{b}_{i}')

num_points = 0
num_configs = len(stat_dirs)
dfs = dict()
benchmarks_ordered = None
for config in configs_ordered:
    print(config)
    stat_dir = stat_dirs[config]
    stat_dir = osp.expanduser(stat_dir)
    stat_files = [osp.join(stat_dir, point, 'stats.txt') for point in points]

    matrix = {}
    for point, stat_file in zip(points, stat_files):
        d = c.get_stats(stat_file,
                # t.ipc_target + t.packet_targets,
                t.ipc_target,
                re_targets=True)
        matrix[point] = d
    df = pd.DataFrame.from_dict(matrix, orient='index')

    if config == 'Ideal-OOO':
        # df['ratioP'] = df['KeySrcP'] / df['TotalP']
        df = df.sort_values(by = ['ipc'])
        benchmarks_ordered = df.index

        with open('./bench_order.txt', 'w') as f:
            for b in benchmarks_ordered:
                f.write(b+'\n')

    dfs[config] = df
    if num_points == 0:
        num_points = len(df)

for config in configs_ordered:
    dfs[config] = dfs[config].reindex(benchmarks_ordered)
    # cols_to_drop = [col for col in dfs[config].columns if col.endswith('P')]
    # dfs[config].drop(cols_to_drop, axis=1, inplace=True)

dfs['Ideal-OOO'].loc['rel_geo_mean'] = [1.0]
print('Ideal-OOO')
print(dfs['Ideal-OOO'])
for config in configs_ordered:
    if config != 'Ideal-OOO':
        print(config)
        rel = dfs[config]['ipc'] / dfs['Ideal-OOO']['ipc'][:-1]
        dfs[config]['rel'] = rel
        print(dfs[config].columns)
        dfs[config].loc['rel_geo_mean'] = [rel.prod() ** (1/len(rel))] * 2
        if config == 'Omega16-OPR-SpecSB':
            dfs[config]['boost'] = dfs[config]['rel'] / dfs['Xbar4']['rel']
        print(dfs[config])
num_points += 1

data_all = []
for i, config in enumerate(configs_ordered):
    df = dfs[config]
    # whitespace before geomean
    # insert_val = np.ones(1) if i == 2 and do_normalization else np.zeros(1)
    data = np.concatenate((df['ipc'].values[:-1], [0], df['ipc'].values[-1:]))
    data_all.append(data)
num_points += 1
data_all = np.array(data_all)

if do_normalization:
    data_all = np.array([data_all[0] / data_all[2], data_all[1] / data_all[2]])
    print(data_all, data_all.shape)
    num_configs -= 1
    configs_ordered = configs_ordered[:-1]
print(num_points, num_configs)

# xticklabels = [''] * num_points
# for i, benchmark in enumerate(benchmarks_ordered + ['rel_geomean']):
#     xticklabels[i*strange_const + 1] = benchmark

legends = list(benchmarks_ordered) + ['', 'mean']

print(len(configs_ordered))
gm = graphs.GraphMaker((14,2.5), legend_loc= 'lower left')
ylabel = 'Normalized IPCs' if do_normalization else "IPCs with different configurations"
fig, ax = gm.simple_bar_graph(data_all, legends, configs_ordered,
        # xlabel='Simulation points from SPEC 2017',
        ylabel=ylabel,
        xlim=(-0.5, num_points-0.5),
        ylim=(0.25, 1.05 if do_normalization else 3),
        with_borders=False,
        markers=['x', '+'],
        )
# legend = ax.get_legend()
# if do_normalization:
#     legend.set_bbox_to_anchor((0.5,0.94))
# else:
#     legend.set_bbox_to_anchor((0.7,1))
plt.tight_layout()
gm.save_to_file("ipc")
# plt.show(block=True)
