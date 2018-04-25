import time
from os import listdir, system
import pickle

def get_code_time(code):
    print("Running {}...".format(code))
    start_time = time.time()
    system(code)
    return time.time() - start_time

all_files = listdir('./bin')
codes = []

for f in all_files:
    if f.endswith('_seq'):
        codes.append(f[:-4])

times = {}

for c in codes:

    seq = c+'_seq'
    icc = c+'_icc'
    neuromp = c+'_neuromp'

    times[seq] = []
    times[icc] = []
    times[neuromp] = []

    for _ in range(10):
        times[seq].append(get_code_time('./bin/'+seq))
        times[icc].append(get_code_time('./bin/'+icc))
        times[neuromp].append(get_code_time('./bin/'+neuromp))

print('Saving...')
pickle.dump(times, open('times.pickle', 'wb'))
