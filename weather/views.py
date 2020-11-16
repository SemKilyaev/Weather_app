import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):

	if(request.method == "POST"):
		form = CityForm(request.POST)
		form.save()


	appid = 'e3682630a36b890f9d26781472694892'
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
	form = CityForm()

	cities = City.objects.all()

	allcities = []

	for city in cities:

		res = requests.get(url.format(city.name)).json()

		try:
			cityinfo = {
				'id': city.id,
				'city': city.name,
				'temperature': res["main"]["temp"],
				'icon': res['weather'][0]['icon']
			}
			allcities.append(cityinfo)
		except KeyError:
			city.delete()
			messages.info(request, 'Enter the correct city!')


	context = {'all_info':allcities, 'form':form}

	return render(request, 'index.html', context)


def deleteCity(request, pk):
	City.objects.filter(id=pk).delete()
	return redirect('/')