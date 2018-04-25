from os import listdir, system

all_files = listdir('./src')
codes = []
sdir='./bin/'

for f in all_files:
    if f.endswith('_icc.c'):
        codes.append(f[:-6])

for c in codes:
    out_c = sdir+c
    in_c = './src/'+c
    system('make seq FILE={} OUT={}'.format(in_c+".c", out_c+"_seq"))
    system('make icc FILE={} OUT={}'.format(in_c+"_icc.c", out_c+"_icc"))
    system('make neuromp FILE={} OUT={}'.format(in_c+"_neuromp.c", out_c+"_neuromp"))
