from finalproj.species import *


def int_from_err(s):
    i, j = s.index('#') + 1, s.index(':')
    return int(s[i:j])


for sample in samples:
    if True:
        print(sample)
        sc = import_score(root_dir + sample)
        a = SpeciesAnalysis(sc, int(sample[0]))
        results = a.submit_to_grading()
        for s in sorted(results, key=int_from_err):
            print(s)
        print('-------------------------------------------------------------------')

# scores to nitpick:
# 2-034-A_zawang2.musicxml
# 2-028-C_hanzhiy2.musicxml
# 2-000-B_sz18.musicxml TODO consec octs, direct octs
# 2-003-A_cjrosas2.musicxml TODO dissonant melodic interval
# 2-021-B_erf3.musicxml
# 1-018-C_ajyanez2.musicxml
# 2-003_A_chchang6.musicxml TODO reverse step recov, missing non diatonic pitch, diss mel int
# 1-019-A_ajyanez2.musicxml TODO change reverse step, check cross and overlap
# 2-009-C_mamn2.musicxml TODO missing diss melodic interval
# 1-005-A_hanzhiy2.musicxml TODO check leaps fourth, remove direct unisons, consec uni wrong index
# 2-010-B_mamn2.musicxml TODO missing diss mel int, rev step wrong ind, just check
# 1-008-C_davidx2.musicxml TODO
# 1-030_C_chchang6.musicxml TODO no direct fifths
# 2-034-C_zawang2.musicxml TODO
# 1-011-B_weikeng2.musicxml TODO wrong rev step
# 2-029-A_hanzhiy2.musicxml TODO wrong rev step
# 1-037-A_sz18.musicxml TODO wrong direct fifths, wrong rev step
# 1-012-B_erf3.musicxml TODO wrong rev step
# 1-030-C_cjrosas2.musicxml TODO wrong
# 2-009-B_mamn2.musicxml TODO wrong rev step, missing diss mel int
# 2-021-C_erf3.musicxml TODO wrong







