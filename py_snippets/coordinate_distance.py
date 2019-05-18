from math import sin, cos, sqrt, atan2, radians

def radius_to_meter(lat1, long1, lat2, long2):
    """Given the lng, lat of two coordinates, return the distance between the two in km"""
    R = 6373.0
    
    lat1 = math.radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
    
    