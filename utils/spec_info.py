import re
import os.path as osp

spec_bmks = {
        '06': {
            'int': [
                'perlbench',
                'bzip2',
                'gcc',
                'mcf',
                'gobmk',
                'hmmer',
                'sjeng',
                'libquantum',
                'h264ref',
                'omnetpp',
                'astar',
                'xalancbmk',
                ],
            'float':[
                'bwaves', 'gamess', 'milc', 'zeusmp', 'gromacs',
                'cactusADM', 'leslie3d', 'namd', 'dealII', 'soplex',
                'povray', 'calculix', 'GemsFDTD', 'tonto', 'lbm',
                'wrf', 'sphinx3',
                ],
            'high_squash': ['astar', 'bzip2', 'gobmk', 'sjeng'],
            },
        '17': {
            'int':  ['deepsjeng', 'exchange2', 'gcc', 'leela', 'mcf', 'omnetpp', 'perlbench', 'x264', 'xalancbmk', 'xz'],
            'float': [ 'bwaves', 'cactusBSSN', 'namd', 'parest', 'povray', 'lbm', 'wrf', 'blender', 'cam4', 'imagick', 'nab', 'fotonik3d', 'roms'],
            },
        }

def get_insts(fname: str):
    print(fname)
    assert osp.isfile(fname)
    p = re.compile('total guest instructions = (\d+(?:,\d+)*)')
    with open(fname) as f:
        for line in f:
            m = p.search(line)
            if m is not None:
                return m.group(1)
    return None
