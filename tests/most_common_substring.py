data = """GAE000102142    12    17     8    10     9     8    11     6
GAE000102150     6    10    10     4     6     7     4     4    17    14
GAE000102160    22     7     4    17    19    17    13    27    23    27
GAE000102170    25    29    32    32    38    64    81    84   122    56
GAE000102180    21    57   102   150   160   205   219   174   178   196
GAE000102190   202   219   204   129    90    96   136   130   108    91
GAE000102200   139   148   147   166   145   147   152   173   164   157
GAE000102210   110   114   118   145   100    82    64    95   105   133
GAE000102220   152   106    53    41    40    22    18    30    47    40
GAE000102230    45    54    72   103   103    66    79    66    69    50
GAE000102240    56    55    43    36    20    28    33    50    65    52
GAE000102250    60    49    59    47    61   100   101    94    90    82
GAE000102260    73    91    79    46    63    54    54    53    39    41
GAE000102270    40    28    19    19    16    13    36    47    48    47
GAE000102280    41    53    49    68    55    69    36    43    40   999
GAE002002148     7     7
GAE002002150     9     8     5     3     5     5     7     4     6     5
GAE002002160    22    15     7     6    11     6     8    15     7    17
GAE002002170     7     8     3     4    19    34    13    12    38    27
GAE002002180    10    42    21    41    37    28    29    27    38    59
GAE002002190    51    52    84    58    56    74    95    58    44    28
GAE002002200    51    80   111    92    67    85    91    90    90    87
GAE002002210    62    86    82    85    65    52    57    56    48    90
GAE002002220    86    76    93    68    50    30    35    63    71    65
GAE002002230    70    61    47    39    72    68   109    70    64    72
GAE002002240    94    90   100    89    74    67    67    98   116    63
GAE002002250    75    88    99    62    77   109   100    71    68    74
GAE002002260    80    75    54    35    38    55    57    63    37    77
GAE002002270   140    84    80    68    67    56    51    86    79    90
GAE002002280    79    76    79    83    99   147    83   116    94   132
GAE002002290   176    48   999"""

parts = data.split("999")[:-1]


def get_common_substring(ls): 
    s0 = ls[0]
    sn = ls[1:]
    res = ""

    for i, c in enumerate(s0): 
        if all([c == p[i] for p in sn]): 
            res += c
    print res


for part in parts: 
    lines = part.split('\n')

    cid = decade = None

    ls = [l.split(' ')[0] for l in lines]

    get_common_substring(ls)

    # for line in lines: 
    #     if len(line.strip()) > 0:
    #         col1 = line.split(' ')[0].strip()

    #         print cid










