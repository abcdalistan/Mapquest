#Importing Libraries
import urllib.parse
import requests

#Declaring API and key variables 
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "oUnfyQT0lWqlhv6zAohIjpXPibSrWQH3"

#Converting length
def metric(dist):
    if unit_metric== "mi" or unit_metric=="miles" or unit_metric=="Miles":
        distance = dist
    elif unit_metric=="km" or unit_metric=="kilometer" or unit_metric=="Kilometer":
        distance =dist * 1.61
    elif unit_metric== "m" or unit_metric=="meter" or unit_metric=="Meter":
        distance = dist * 1610

    return distance

#Converting time
def convert(timeRoute):
    if unit_time== "s" or unit_time=="seconds" or unit_time=="Seconds":
        time = timeRoute
    elif unit_time== "min" or unit_time=="minutes" or unit_time=="Minutes":
        time = timeRoute / 60
    elif unit_time== "hr" or unit_time=="hours" or unit_time=="Hours":
        time = timeRoute / 3600

    return time
#Asking user input of starting location & destination
while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
 #Asking user input of (m,km,mi)   
    unit_metric = input("Choose unit of length [ m | km | mi ]: ") 
    if unit_metric == "quit" or unit_metric == "q": 
        break
    elif unit_metric== "mi" or unit_metric=="miles" or unit_metric=="Miles":
        unit = "mi"
    elif unit_metric=="km" or unit_metric=="kilometer" or unit_metric=="Kilometer":
        unit = "km"
    elif unit_metric== "m" or unit_metric=="meter" or unit_metric=="Meter":
        unit = "m"
    else:
        print("Invalid input!")
        break
#Asking user input of time prefernce 
    unit_time = input("Choose unit of time [ s | min | hr ]: ") 
    if unit_time == "quit" or unit_time == "q": 
        break
    elif unit_time== "s" or unit_time=="seconds" or unit_time=="Seconds":
        time_unit = "s"
    elif unit_time=="min" or unit_time=="minutes" or unit_time=="Minutes":
        time_unit = "min"
    elif unit_time== "hr" or unit_time=="hours" or unit_time=="Hours":
        time_unit = "hr"
    else:
        print("Invalid input!")
        break
 #Asking user input of route type       
    routeType = input("Choose route type [ fastest | shortest | pedestrian | bicycle ]: ")
    if routeType in ('fastest','shortest','pedestrian','bicycle'): pass
#Asking the user what road types to avoid   
    avoid = input ("What do you want to avoid? [ Limited Access Highway | Toll Road | Ferry | Unpaved | Approximate Seasonal Closure | Country Border Crossing | Bridge | Tunnel | None ]: ")
    if avoid in ('Limited Access Highway' , 'Toll Road', 'Ferry' , 'Unpaved' , 'Approximate Seasonal Closure' , 'Country Border Crossing' , 'Bridge' , 'Tunnel', 'None'): pass
    else:
        print("Invalid input!")
        break
#Calling the API
    if avoid == 'None': url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType})
    else: url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType,"avoids":avoid}) 
    json_data = requests.get(url).json()
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    #Printing the output parameters
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=================================================")
        print("Directions from " + (orig) + " to " + (dest))
        time = convert(json_data["route"]["time"])
        distance = metric(json_data["route"]["distance"])
        print("Trip Duration: " + str("{:.2f}".format(time) + " " + time_unit + " | " +(json_data["route"]["formattedTime"])))
        print("Distance:      " + str("{:.2f}".format(distance))+ " " + unit)
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print("=================================================")
        
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance = metric(each["distance"])
            print((each["narrative"]) + " (" + str("{:.2f}".format(distance) + " " + unit + ")"))
        print("=================================================")
    #Error handling if user inputted wrong values on location and destination
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    #Error handling if user has no input of destinaion and location
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    #Error handling for other API status code 
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")



