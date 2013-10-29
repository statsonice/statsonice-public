"""
This file contains general statistics functions not specific to skating statistics
"""

import math

# average
#
def average(scores):
    scores = [float(score) for score in scores]
    return 1.0 * sum(scores) / len(scores)

# median
#
def median(scores):
    scores = list(scores)
    scores.sort()
    num = len(scores)
    if num % 2 == 0:
        return float(scores[num/2 - 1] + scores[num/2])/2
    else:
        return scores[num/2]

# standard deviation
#
def std_dev(scores):
    if scores == None:
        return None
    if len(scores) < 1:
        return None
    scores = [float(score) for score in scores]
    if len(scores) == 1:
        return 0
    avg = average(scores)
    diff_sq = sum([(score - avg)**2 for score in scores])
    return math.sqrt(diff_sq/(len(scores)-1))

# find the consistency metric
#
def estimate_consistency(scores):
    dev = std_dev(scores)
    if dev > 0:
        consistency = round(10/math.sqrt(dev),1)
    else:
        consistency = None
    return consistency

# Calculate p value given value, mean, standard deviation
#
def p_value(x,mean,sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**0.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    p_score = num/denom
    return p_score

# Line of best fit
#
def line_of_best_fit(scores):
    if len(scores) == 0:
        return 0, 0
    if len(scores) == 1:
        return 0, round(float(scores[0]),2)
    size = len(scores)
    x_sum = sum(range(1,size+1))
    y_sum = sum(scores)
    xy_sum = sum([x*(scores.index(x)+1) for x in scores])
    x_squared_sum = sum([x**2 for x in range(1,size+1)])


    slope = (size*xy_sum - x_sum*y_sum)/(size*x_squared_sum - x_sum**2)
    slope = round(slope,2)

    intercept = (x_squared_sum*y_sum - x_sum*xy_sum)/(size*x_squared_sum - x_sum**2)
    intercept = round(intercept,2)
    return slope, intercept

# predict the next score from some number of recent scores
#
def predict_next_value(scores):
    slope, intercept = line_of_best_fit(scores)
    next_score = intercept + slope*len(scores)
    return next_score

# method to reduce the range of standard deviations to center around a value
# weakening the effect of standard deviations makes the result predictions softer and more accurate
#
def spread_std(std,center):
    exponent = abs(float(std - center)/float(center + std))**0.5
    if std < center:
        spread_std = std + (center-std)*math.exp(math.log(0.5)*(1 - float(std)/center)**exponent)
    else:
        spread_std = std - (std-center)*math.exp(math.log(0.5)*(1 - center/float(std))**exponent)
    return spread_std

