__author__ = 'umqra'

# use dict for creating own symbols set

symbol_set = {
    '?': 'WRGF'
}

# 8 neighbors and center point
# 1 2 3
# 8 0 4
# 7 6 5
# using ? if cell type may be any

cell_repr_config = {
    'GGGGGGGGG': 'G1',
    'GGGGG?R?G': 'G2',
    'GGGGGRGGG': 'G3',
    'GGGGGGGRG': 'G4',
    'G?GGGGG?R': 'G5',
    'GRGGGGGGG': 'G6',
    'G?R?GGGGG': 'G7',
    'GGGRGGGGG': 'G8',
    'GGG?R?GGG': 'G9',
    'GRR??G??R': 'GA',
    'G?RRR??G?': 'GB',
    'G??G??RRR': 'GC',
    'GG??RRR??': 'GD',
    'GGR?RGGGG': 'GB',
    'GGGGGGR?R': 'GC',
    'GGGGR?RGG': 'GD',
    'G?RGGGGGR': 'GA',

#    'GRGGGRGGG': 'GE',
#    'GGGRGGGRG': 'GF',
#    'G?G?R?G?R': 'GG',
#    'G?R?G?R?G': 'GH',

#    'GRGRGGGGG': 'GI',
#    'GRGGGGGRG': 'GJ',
#    'GGGGGRGRG': 'GK',
#    'GGGRGRGGG': 'GL',

    'R????????': 'R1',
}


def match_pattern(pattern, s):
    if len(pattern) != len(s):
        return False
    for i in range(len(s)):
        c = pattern[i]
        if c in symbol_set and s[i] in symbol_set[c]:
            continue
        if pattern[i] != s[i]:
            return False
    return True


def get_cell_repr(adj_types):
    s = ''.join(adj_types)
    for k in cell_repr_config.keys():
        if match_pattern(k, s):
            return cell_repr_config[k]
    return s[0] + '1'