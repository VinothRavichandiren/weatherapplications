from django.shortcuts import render,redirect
from .form import PlaceForm
from .models import Place
import requests
from django.contrib import messages
# Create your views here.
def home(request):
    url ='http://api.openweathermap.org/data/2.5/weather?q={},&appid=6918a79f9a43a4bb310e904d84d17186&units=metric'
    if request.method=="POST":
        form=PlaceForm(request.POST)
        print(form)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=Place.objects.filter(name=NCity).count()
            if CCity == 0:
                res=requests.get(url.format(NCity)).json()
                if res ['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" added successfully...!!")
                else:
                    messages.error(request,"City Doesn't Exists")
            else:
                messages.error(request,"City Aleardy Exists")
    form=PlaceForm()
    cities=Place.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city':city,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon':res['weather'][0]['icon']
        }
        data.append(city_weather)
    context={'data':data,'form':form}
    return render(request,"app/weather.html",context)


def delete_city(request,Cname):
    Place.objects.filter(name=Cname).delete()
    messages.success(request," "+Cname+" Removed Successfully...!!")
    return redirect("Home")