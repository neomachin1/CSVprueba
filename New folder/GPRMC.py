# Importing Necessary Modules
import requests
from selenium import webdriver
import folium
import datetime
import time

# this method will return us our actual coordinates
# using our ip address

def locationCoordinates():
	try:
		response = requests.get('https://ipinfo.io')
		data = response.json()
		loc = data['loc'].split(',')
		lat, long = float(loc[0]), float(loc[1])
		city = data.get('city', 'Unknown')
		state = data.get('region', 'Unknown')
		return lat, long, city, state
		# return lat, long
	except:
		# Displaying ther error message
		print("Internet Not avialable")
		# closing the program
		exit()
		return False


# this method will fetch our coordinates and create a html file
# of the map
def gps_locator():

	obj = folium.Map(location=[0, 0], zoom_start=2)

	try:
		lat, long, city, state = locationCoordinates()
		print("You Are in {},{}".format(city, state))
		print("Your latitude = {} and longitude = {}".format(lat, long))
		folium.Marker([lat, long], popup='Current Location').add_to(obj)

		fileName = str(datetime.date.today()) + ".html"

		obj.save(fileName)

		return fileName

	except:
		return False


# Main method
if __name__ == "__main__":
    print("Buscando Ubicacion")
    pagina = gps_locator()
    print(pagina)
    print("Abriendo archivo")
    dr = webdriver.Chrome()
    dr.get(pagina)
    time.sleep(4)
    dr.quit()
    print("Finalizado")
    
