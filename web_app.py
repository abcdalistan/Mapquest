#Importing Libraries
from flask import Flask, render_template, request
import urllib.parse
import requests
import os
import getpass

app = Flask(__name__)

#Declaring API and key variables
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "oUnfyQT0lWqlhv6zAohIjpXPibSrWQH3"

#Converting length for distance
def length(dist, unit_length):
    if unit_length== "mi" or unit_length=="miles" or unit_length=="Miles":
        distance = dist
    elif unit_length=="km" or unit_length=="kilometer" or unit_length=="Kilometer":
        distance =dist * 1.61
    elif unit_length== "m" or unit_length=="meter" or unit_length=="Meter":
        distance = dist * 1610

    return distance

#Converting time 
def convert(timeRoute, unit_time):
    if unit_time== "s" or unit_time=="seconds" or unit_time=="Seconds":
        time = timeRoute
    elif unit_time== "min" or unit_time=="minutes" or unit_time=="Minutes":
        time = timeRoute / 60
    elif unit_time== "hr" or unit_time=="hours" or unit_time=="Hours":
        time = timeRoute / 3600
    return time

@app.route('/')
def home():
    return render_template('web_mapquest.html')

@app.route('/index', methods=['GET', 'POST'])
def route():

    if request.method == 'POST':
        starting_location = request.form['starting_location']
        destination = request.form['destination']
        unit_length = request.form['unit_length']
        unit_time = request.form['unit_time']
        route_type = request.form['route_type']
        avoid = request.form['avoid']

        if starting_location == '' or destination == '':
            return render_template('web_mapquest.html', starting_location = starting_location,
                                                        destination = destination,
                                                        route_type = route_type,
                                                        avoid = avoid)
        
        elif unit_length == '' or unit_time == '' or route_type=='':
                 return render_template('web_mapquest.html', starting_location = starting_location,
                                                        destination = destination,
                                                        route_type = route_type,
                                                        avoid = avoid)                                    
        else:
            if avoid == "None":
                url = main_api + urllib.parse.urlencode({"key":key, "from":starting_location, "to":destination, "routeType":route_type})
            else:
                url = main_api + urllib.parse.urlencode({"key":key, "from":starting_location, "to":destination, "routeType":route_type,"avoids":avoid})
    
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]  
        time = str("{:.2f}".format(convert(json_data["route"]["time"], unit_time))) 
        duration = json_data["route"]["formattedTime"] 
        distance = str("{:.2f}".format(length(json_data["route"]["distance"], unit_length))) 
        fuel = str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))
    
        maneuvers= json_data["route"]["legs"][0]["maneuvers"]

        return render_template('index.html', starting_location = starting_location,
                                            destination = destination,
                                            distance = distance,
                                            unit_length = unit_length,
                                            time = time,
                                            unit_time = unit_time,
                                            duration = duration,
                                            route_type = route_type, 
                                            fuel = fuel,
                                            avoid = avoid,
                                            maneuvers = maneuvers
                                            )

    return render_template('web_mapquest.html')

if __name__ == "__main__":
    app.run(debug=True)