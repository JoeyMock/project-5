"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    timeRet = brevet_start_time
    if(control_dist_km > brevet_dist_km):
        control_dist_km = brevet_dist_km
    if(brevet_dist_km > 200):
        timeRet.shift(hours=200/34)
        brevet_dist_km -= 200
    else:
        timeRet.shift(hours=brevet_dist_km/34)
        return timeRet
    
    if(brevet_dist_km > 200):
        timeRet.shift(hours=100/32)
        brevet_dist_km -= 200
    else: 
        timeRet.shift(hours=brevet_dist_km/32)
        return timeRet

    if(brevet_dist_km > 200):
        timeRet.shift(hours=200/30)
        brevet_dist_km -= 200
    else: 
        timeRet.shift(hours=brevet_dist_km/30)
        return timeRet

    if(brevet_dist_km > 400):
        timeRet.shift(hours=400/34)
        brevet_dist_km -= 400
    else:
        timeRet.shift(hours=brevet_dist_km/28)
        return timeRet

    return timeRet


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    timeRet = brevet_start_time
    if(control_dist_km > brevet_dist_km):
        control_dist_km = brevet_dist_km
    if(brevet_dist_km > 200):
        timeRet.shift(hours=200/15)
        brevet_dist_km -= 200
    else: 
        timeRet.shift(hours=brevet_dist_km/15)
        return timeRet

    if(brevet_dist_km > 200):
        timeRet.shift(hours=100/15)
        brevet_dist_km -= 200
    else:
        timeRet.shift(hours=brevet_dist_km/15)
        return timeRet

    if(brevet_dist_km > 200):
        timeRet.shift(hours=200/15)
        brevet_dist_km -= 200
    else:
        timeRet.shift(hours=brevet_dist_km/15)
        return timeRet

    if(brevet_dist_km > 400):
        timeRet.shift(hours=400/11.428)
        brevet_dist_km -= 400
    else:
        timeRet.shift(hours=brevet_dist_km/11.428)
        return timeRet

    return timeRet
