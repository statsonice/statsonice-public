"""
This file is the backend for computing summary statistics which are specific to
StatsOnIce.  Generalized statistics functions should be in statsonice/includes/stats.py
"""

from includes import stats

# calculate chance of winning next encounter
#


def determine_win_probability(s1_scores, s2_scores, num_skaters=2):
    # get a new pseudo std to push all towards a central number of 10 (helps
    # with predictions)
    s1_std = stats.spread_std(stats.std_dev(s1_scores), 15)
    s2_std = stats.spread_std(stats.std_dev(s2_scores), 15)

    # only project out half a competition, essentially to not guess too much
    s1_next_score = stats.predict_next_value(s1_scores)
    s2_next_score = stats.predict_next_value(s2_scores)

    # weighted averages
    s1_w_ave = (stats.average(s1_scores) + s1_next_score) / 2
    s2_w_ave = (stats.average(s2_scores) + s2_next_score) / 2

    # chance less than or greater than one std dev below average for s1
    s1_lt = stats.p_value(s2_w_ave - s2_std, s1_w_ave, s1_std)
    s1_gt = 1 - s1_lt

    s2_lt = stats.p_value(s1_w_ave - s1_std, s2_w_ave, s2_std)
    s2_gt = 1 - s2_lt

    # compute probabilities from ratios of probabilities
    s1_win = s1_gt * s2_lt
    s2_win = s2_gt * s1_lt

    s1_chance = round(s1_win / (s1_win + s2_win) * 100, 2)
    s2_chance = round(s2_win / (s1_win + s2_win) * 100, 2)

    if num_skaters != 2:
        num_skaters = float(num_skaters)
        s1_chance = s1_chance ** (2 / num_skaters)
        s2_chance = s2_chance ** (2 / num_skaters)

    return (s1_chance, s2_chance)
