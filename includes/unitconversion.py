"""
This file contains functions for unit conversion
"""
import math

def imperial_to_metric(feet, inches):
    if feet == None or inches == None:
        return None
    inches += feet*12
    cm = inches*2.54
    return cm

def metric_to_imperial(cm):
    if cm == None:
        return (None, None)
    feet = round(cm / 2.54) / 12
    inches = int(round((feet - math.floor(feet)) * 12))
    feet = int(math.floor(feet))
    return (feet, inches)


