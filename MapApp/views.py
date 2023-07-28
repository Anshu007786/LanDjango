from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from .utils import getGeo, getCenterCoordinatas, getZoom, getIPAddress
from geopy.distance import geodesic
import folium 
from branca.element import Figure

# Create your views here.


def calculateDistanceView(request):
    distance = None
    destination = None

    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent = 'measurements')

    ip_ = getIPAddress(request)
    print(ip_)
    ip = "103.69.44.21"
    country, city, latitude, longitude = getGeo(ip)
    
    location = geolocator.geocode(city)

    #Location Coordinates
    lLatitude = latitude
    lLongitude = longitude
    pointA = (lLatitude, lLongitude)


    #initial map
    fig = Figure(width=1200, height=600)
    m = folium.Map(width=1200, height=600, location=getCenterCoordinatas(lLatitude,lLongitude), zoom_start=8)
    fig.add_child(m)
    locationMarker = folium.Marker([lLatitude,lLongitude], tooltip="Click here for more", popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        fig = Figure(width=1200, height=400)
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        
        #Destination Coordinates
        dLatitude = destination.latitude
        dLongitude = destination.longitude
        pointB = (dLatitude, dLongitude)

        #Distance between location and destination
        distance = round(geodesic(pointA,pointB).km,3)
        
        #Map Modification
        
        m = folium.Map(width=1200, height=600, location=getCenterCoordinatas(lLatitude,lLongitude,dLatitude,dLongitude), zoom_start=getZoom(distance))
        
        locationMarker = folium.Marker([lLatitude,lLongitude], tooltip="Click here for more", popup=city['city'], icon=folium.Icon(color="purple")).add_to(m)
        destinationMarker = folium.Marker([dLatitude,dLongitude], tooltip="Click here for more", popup=destination, icon=folium.Icon(color="red", icon="cloud")).add_to(m)
        
        
        #Draw line between location and destination
        
        line = folium.PolyLine(locations=[pointA,pointB], weight=2, color="blue")
        m.add_child(line)
        
        instance.location = location
        instance.distance = distance
        instance.save()
    
    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination' : destination,
        'location' : location,
        'form' : form,
        'map' : m,
    }
    return render(request,'measurements/main.html', context)