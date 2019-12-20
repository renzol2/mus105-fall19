from finalproj.species import *

score_results = {
    '2-034-A_zawang2.musicxml': {
        'At #12: too many melodic unisons',
        'At #13: forbidden strong beat dissonance',
        'At #16: direct fifths',
        'At #16: forbidden weak beat dissonance',
        'At #16: too many large leaps',
        'At #19: missing melodic cadence',
        'At #19: too many melodic unisons',
        'At #20: forbidden duration',
        'At #2: forbidden weak beat dissonance',
        'At #6: too many melodic unisons',
        'At #7: too many consecutive intervals in same direction'
    },
    '2-028-C_hanzhiy2.musicxml': {
        'At #16: forbidden weak beat dissonance',
        'At #2: forbidden weak beat dissonance',
        'At #5: too many consecutive intervals in same direction',
        'At #6: too many consecutive intervals in same direction',
        'At #7: too many consecutive intervals in same direction',
        'At #8: forbidden weak beat dissonance'
    },
    '2-000-B_sz18.musicxml': {
        'At #10: too many consecutive intervals in same direction',
        'At #11: forbidden strong beat dissonance',
        'At #12: direct fifths',
        'At #16: forbidden weak beat dissonance',
        'At #16: too many melodic unisons',
        'At #17: forbidden strong beat dissonance',
        'At #17: too many consecutive intervals in same direction',
        'At #18: consecutive octaves',
        'At #2: forbidden weak beat dissonance',
        'At #3: forbidden strong beat dissonance',
        'At #8: consecutive octaves',
        'At #9: too many consecutive intervals in same direction'
    },
    '2-003-A_cjrosas2.musicxml': {
        'At #10: too many consecutive intervals in same direction',
        'At #11: forbidden strong beat dissonance',
        'At #12: too many large leaps',
        'At #14: forbidden weak beat dissonance',
        'At #14: too many large leaps',
        'At #15: dissonant melodic interval',
        'At #16: dissonant melodic interval',
        'At #16: forbidden non-diatonic pitch',
        'At #2: forbidden weak beat dissonance',
        'At #4: direct fifths',
        'At #4: forbidden weak beat dissonance',
        'At #6: too many large leaps'
    },
    '2-021-B_erf3.musicxml': {
        'At #11: too many consecutive intervals in same direction',
        'At #12: too many consecutive intervals in same direction',
        'At #13: forbidden weak beat dissonance',
        'At #16: dissonant melodic interval',
        'At #1: forbidden duration',
        'At #1: too many melodic unisons',
        'At #3: forbidden weak beat dissonance',
        'At #5: forbidden weak beat dissonance',
        'At #7: forbidden weak beat dissonance'
    },
    '1-018-C_ajyanez2.musicxml': {
        'At #2: missing reverse by step recovery',
        'At #3: forbidden strong beat dissonance',
        'At #4: dissonant melodic interval',
        'At #4: forbidden non-diatonic pitch',
        'At #4: forbidden strong beat dissonance',
        'At #4: too many leaps of a fifth',
        'At #5: forbidden strong beat dissonance',
        'At #6: forbidden non-diatonic pitch',
        'At #8: forbidden non-diatonic pitch',
        'At #9: missing melodic cadence'
    },
    '2-003_A_chchang6.musicxml': {
        'At #10: too many consecutive intervals in same direction',
        'At #11: forbidden strong beat dissonance',
        'At #12: too many large leaps',
        'At #14: forbidden weak beat dissonance',
        'At #14: too many large leaps',
        'At #15: dissonant melodic interval',
        'At #16: dissonant melodic interval',
        'At #16: forbidden non-diatonic pitch',
        'At #2: forbidden weak beat dissonance',
        'At #4: direct fifths',
        'At #4: forbidden weak beat dissonance',
        'At #6: too many large leaps'
    },
    '1-019-A_ajyanez2.musicxml': {
        'At #4: too many consecutive intervals in same direction',
        'At #4: voice crossing',
        'At #4: voice overlap',
        'At #5: voice crossing',
        'At #5: voice overlap',
        'At #6: too many consecutive leaps',
        'At #6: voice crossing',
        'At #6: voice overlap',
        'At #8: too many consecutive intervals in same direction',
        'At #9: too many consecutive intervals in same direction'
    },
    '2-009-C_mamn2.musicxml': {
        'At #11: forbidden weak beat dissonance',
        'At #13: forbidden weak beat dissonance',
        'At #15: dissonant melodic interval',
        'At #16: too many consecutive intervals in same direction',
        'At #1: forbidden duration',
        'At #3: forbidden weak beat dissonance',
        'At #9: forbidden weak beat dissonance'
    },
    '1-005-A_hanzhiy2.musicxml': {
        'At #10: voice overlap',
        'At #8: forbidden strong beat dissonance',
        'At #8: too many large leaps',
        'At #9: consecutive unisons',
        'At #9: too many consecutive intervals in same direction',
        'At #9: voice overlap'
    },
    '2-010-B_mamn2.musicxml': {
        'At #12: too many melodic unisons',
        'At #13: too many large leaps',
        'At #14: forbidden weak beat dissonance',
        'At #14: too many melodic unisons',
        'At #17: forbidden strong beat dissonance',
        'At #17: too many consecutive intervals in same direction',
        'At #18: too many consecutive intervals in same direction',
        'At #4: dissonant melodic interval',
        'At #4: forbidden weak beat dissonance',
        'At #6: too many melodic unisons',
        'At #7: consecutive octaves in cantus firmus notes',
        'At #8: missing reverse by step recovery',
        'At #9: too many consecutive leaps'
    },
    '1-008-C_davidx2.musicxml': {
        'At #1: consecutive fifths',
        'At #3: missing reverse by step recovery',
        'At #3: too many consecutive leaps',
        'At #3: too many large leaps',
        'At #4: missing reverse by step recovery',
        'At #4: too many consecutive leaps',
        'At #4: too many large leaps',
        'At #5: forbidden strong beat dissonance',
        'At #5: too many consecutive leaps',
        'At #8: dissonant melodic interval',
        'At #8: forbidden strong beat dissonance'
    },
    '1-030_C_chchang6.musicxml': {
        'At #2: consecutive fifths',
        'At #9: missing melodic cadence'
    },
    '2-034-C_zawang2.musicxml': {
        'At #10: forbidden weak beat dissonance',
        'At #12: forbidden weak beat dissonance',
        'At #13: consecutive fifths in cantus firmus notes',
        'At #14: direct fifths',
        'At #14: forbidden weak beat dissonance',
        'At #15: consecutive fifths in cantus firmus notes',
        'At #17: forbidden strong beat dissonance',
        'At #18: missing melodic cadence'
    },
    '1-011-B_weikeng2.musicxml': {'At #8: dissonant melodic interval'},
    '2-029-A_hanzhiy2.musicxml': {
        'At #13: missing reverse by step recovery',
        'At #13: too many consecutive leaps',
        'At #13: too many large leaps',
        'At #14: direct octaves',
        'At #14: too many consecutive leaps',
        'At #14: too many large leaps',
        'At #17: too many consecutive intervals in same direction',
        'At #18: too many consecutive intervals in same direction',
        'At #2: forbidden weak beat dissonance',
        'At #4: forbidden weak beat dissonance',
        'At #4: too many melodic unisons',
        'At #7: too many consecutive leaps'
    },
    '1-037-A_sz18.musicxml': {
        'At #2: consecutive fifths',
        'At #3: consecutive fifths',
        'At #4: consecutive fifths',
        'At #5: consecutive fifths'
    },
    '1-012-B_erf3.musicxml': {'At #1: forbidden starting pitch'},
    '1-030-C_cjrosas2.musicxml': {
        'At #2: consecutive fifths',
        'At #9: missing melodic cadence'
    },
    '2-009-B_mamn2.musicxml': {
        'At #13: forbidden weak beat dissonance',
        'At #16: dissonant melodic interval',
        'At #1: forbidden duration',
        'At #1: too many melodic unisons',
        'At #9: forbidden weak beat dissonance',
        'At #9: too many melodic unisons'
    },
    '2-021-C_erf3.musicxml': {
        'At #10: too many consecutive intervals in same direction',
        'At #11: forbidden weak beat dissonance',
        'At #11: too many consecutive intervals in same direction',
        'At #11: too many melodic unisons',
        'At #15: forbidden weak beat dissonance',
        'At #1: forbidden duration',
        'At #3: forbidden weak beat dissonance',
        'At #4: consecutive fifths in cantus firmus notes',
        'At #5: too many melodic unisons',
        'At #7: forbidden weak beat dissonance',
        'At #7: too many melodic unisons'
    }
}


def int_from_err(s):
    i, j = s.index('#') + 1, s.index(':')
    return int(s[i:j])


show_results = True
for sample in samples:
    if show_results:
        cond = sample == '1-005-A_hanzhiy2.musicxml'
    else:
        cond = True
    if cond:
        sc = import_score(root_dir + sample)
        a = SpeciesAnalysis(sc, int(sample[0]))
        results = a.submit_to_grading()
        is_correct = results == score_results[sample]
        print(f'{sample}: {is_correct}')
        if show_results:
            for s in sorted(results, key=int_from_err):
                print(s)
            print('-------------------------------------------------------------------')
