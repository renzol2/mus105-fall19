import glob
from finalproj.species import *


def int_from_err(s):
    i, j = s.index('#') + 1, s.index(':')
    return int(s[i:j])


scores = [score.replace(root_dir[:-1], '')[1:] for score in glob.glob(root_dir + '*.musicxml')]
# for sample in scores:
#     print(sample)
#     s = import_score(root_dir + sample)
#     a = SpeciesAnalysis(s, int(sample[0]))
#     a.submit_to_grading()


for sample in samples:
    print(sample)
    sc = import_score(root_dir + sample)
    a = SpeciesAnalysis(sc, int(sample[0]))
    results = a.submit_to_grading()
    for s in sorted(results, key=int_from_err):
        print(s)
    print('-------------------------------------------------------------------')




