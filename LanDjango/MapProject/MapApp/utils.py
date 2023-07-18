from django.contrib.gis.geoip2 import GeoIP2


#Helper functions

def getIPAddress(request):
    xForwardedFor = request.META.get("HTTP_xForwardedFor")
    if xForwardedFor:
        ip = xForwardedFor.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip 


def getGeo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    latitude, longitude = g.lat_lon(ip)
    return country, city, latitude, longitude

def getCenterCoordinatas(latA, longA, latB=None, longB=None):
    coordinate = (latA,longA)
    if latB:
        coordinate = [(latA+latB)/2, (longA+longB)/2]
    
    return coordinate

def getZoom(distance):
    if distance <=  100:
        return 11
    
    elif distance > 100 and distance <= 700:
        return 6
    
    else:
        return 2
    