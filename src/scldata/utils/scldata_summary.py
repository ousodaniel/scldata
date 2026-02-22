splits_str = """\
splits
├── cv
│   ├── f0
│   │   ├── trn = [<int index>, ...] # counts: 15187
│   │   └── vld = [<int index>, ...] # counts: 1256
│   ├── f1
│   │   ├── trn = [<int index>, ...] # counts: 15203
│   │   └── vld = [<int index>, ...] # counts: 1240
│   ├── f2
│   │   ├── trn = [<int index>, ...] # counts: 15185
│   │   └── vld = [<int index>, ...] # counts: 1258
│   ├── f3
│   │   ├── trn = [<int index>, ...] # counts: 15210
│   │   └── vld = [<int index>, ...] # counts: 1233
│   └── f4
│       ├── trn = [<int index>, ...] # counts: 15265
│       └── vld = [<int index>, ...] # counts: 1178
├── vld = [<int index>, ...] # counts: 15183
├── trn = [<int index>, ...] # counts: 1260
└── tst = [<int index>, ...] # counts: 2631
"""

label_abbr_dict = {
'Cytoplasm': 'CYT',
'Plastid': 'PLA',
'Secreted': 'SEC',
'Mitochondrion': 'MIT',
'Membrane': 'MEM',
'Peroxisome': 'PER',
'Nucleus': 'NUC',
'Cell projection': 'CEP',
'ER': 'ER',
'Cytoplasm;Nucleus': 'CYT;NUC',
'Centrosome;Cytoplasm;Cytoskeleton;Microtubule organizing center': 'CEN;CYT;CYTS;MTOC',
'Cytoplasm;Membrane': 'CYT;MEM',
'Cytoplasm;Cytoskeleton': 'CYT;CYTS',
}
