#!/usr/bin/env python

@outputSchema('fare_band:chararray')
def fare_band(fare):
#less than or equal to 15, greater than but less than or ewqual to 30, bigger is high  
    if fare <= 15:
        return 'LOW'
    elif fare > 15 and fare <= 30:
        return 'MID'
    else:  # everything nigger is high
        return 'HIGH'
    
#clasififer for low, medium and high values
