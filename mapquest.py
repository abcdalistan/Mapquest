import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "oUnfyQT0lWqlhv6zAohIjpXPibSrWQH3"

def length(dist):
    if unit_length== "mi" or unit_length=="miles" or unit_length=="Miles":
        distance = dist
    elif unit_length=="km" or unit_length=="kilometer" or unit_length=="Kilometer":
        distance =dist * 1.61
    elif unit_length== "m" or unit_length=="meter" or unit_length=="Meter":
        distance = dist * 1610

    return distance

def convert(timeRoute):
    if unit_time== "s" or unit_time=="seconds" or unit_time=="Seconds":
        time = timeRoute
    elif unit_time== "min" or unit_time=="minutes" or unit_time=="Minutes":
        time = timeRoute / 60
    elif unit_time== "hr" or unit_time=="hours" or unit_time=="Hours":
        time = timeRoute / 3600

    return time

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    
    unit_length = input("Choose unit of length [ m | km | mi ]: ") 
    if unit_length == "quit" or unit_length == "q": 
        break
    elif unit_length== "mi" or unit_length=="miles" or unit_length=="Miles":
        unit = "mi"
    elif unit_length=="km" or unit_length=="kilometer" or unit_length=="Kilometer":
        unit = "km"
    elif unit_length== "m" or unit_length=="meter" or unit_length=="Meter":
        unit = "m"
    else:
        print("Invalid input!")
        break

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

    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest}) 
    json_data = requests.get(url).json()
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=================================================")
        print("Directions from " + (orig) + " to " + (dest))
        time = convert(json_data["route"]["time"])
        distance = length(json_data["route"]["distance"])
        print("Trip Duration: " + str("{:.2f}".format(time) + " " + time_unit + " | " +(json_data["route"]["formattedTime"])))
        print("Distance:      " + str("{:.2f}".format(distance))+ " " + unit)
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print("=================================================")
        
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance = metric(each["distance"])
            print((each["narrative"]) + " (" + str("{:.2f}".format(distance) + " " + unit + ")"))
        print("=============================================")

    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")

    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")

    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")



