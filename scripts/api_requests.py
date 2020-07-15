import requests#, api
import os

if os.environ.get("GEOCODE_API_KEY") != None:
    GEOCODE_API_KEY = os.environ.get("GEOCODE_API_KEY")
    DARKSKY_API_KEY = os.environ.get("DARKSKY_API_KEY")
    YELP_KEY = os.environ.get("YELP_KEY")
    print("API REQ FILE Heroku API key storage")
else:
    import api
    GEOCODE_API_KEY = api.GEOCODE_API_KEY
    DARKSKY_API_KEY = api.DARKSKY_API_KEY
    YELP_KEY = api.YELP_KEY
    print("API REQ FILE Local API key storage")

def get_forecast(place, timeframe):
    geocoder = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GEOCODE_API_KEY}")
    jsongeocode = geocoder.json()
    lat = jsongeocode['results'][0]['geometry']['location']['lat']
    lng = jsongeocode['results'][0]['geometry']['location']['lng']

    forecaster = requests.get(f"https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{lat}, {lng}")
    jsonforecaster = forecaster.json()

    
    try:
        current_weather = jsonforecaster['currently']['summary']
    except:
        current_weather = "Current weather not available for this location"
    try:
        weather_next_minutes = jsonforecaster['minutely']['summary']
    except:
        weather_next_minutes = "Weather for the next hour not available for this location"
    try:    
        weather_next_hours = jsonforecaster['hourly']['summary']
    except:
        weather_next_hours = "Today's weather not available for this location"
    try:
        weather_next_days = jsonforecaster['daily']['summary']
    except:
        weather_next_days = "Forecast not available for this location"

    if 'alerts' in jsonforecaster:
        print("WEATHER ALERT DETECTED")
        weather_alert = jsonforecaster['alerts'][0]['title']
        weather_alert_info = jsonforecaster['alerts'][0]['description']
    else:
        print("NO WEATHER ALERTS")
        weather_alert = None
        weather_alert_info = None
    alert_msg = "\n\nNo weather alerts for this area."


    if timeframe == "now":
        formatresponse = f"The weather in {place} is currently: {current_weather}"
        if weather_alert != None:
            alert_msg = "\n\nWEATHER ALERTS IN PLACE\n\n" + weather_alert + "\n\n" + weather_alert_info
        return str(formatresponse) + str(alert_msg)

    elif timeframe == "nextminutes":
        formatresponse = f"Forecast for the next hour in {place}: {weather_next_minutes}"
        if weather_alert != None:
            alert_msg = "\n\nWEATHER ALERTS IN PLACE\n\n" + weather_alert + "\n\n" + weather_alert_info
        return str(formatresponse) + str(alert_msg)

    elif timeframe == "nexthours":
        formatresponse = f"The weather over the next day in {place}: {weather_next_hours}"
        if weather_alert != None:
            alert_msg = "\n\nWEATHER ALERTS IN PLACE\n\n" + weather_alert + "\n\n" + weather_alert_info
        return str(formatresponse) + str(alert_msg)

    elif timeframe == "nextdays":
        formatresponse = f"The forecast for {place} over the next few days is: {weather_next_days}"
        if weather_alert != None:
            alert_msg = "\n\nWEATHER ALERTS IN PLACE\n\n" + weather_alert + "\n\n" + weather_alert_info
        return str(formatresponse) + str(alert_msg)

    else:
        return "Error - forecast not found"



    #forecaster = requests.get(f"https://api.darksky.net/forecast/{api.DARKSKY_API_KEY}/{encoded_place}")

def get_local_info(keyword, place, number):    
    headers = {'Authorization': f"Bearer {YELP_KEY}"}
    geocoder = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GEOCODE_API_KEY}")
    jsongeocode = geocoder.json()

    lat = jsongeocode['results'][0]['geometry']['location']['lat']
    lng = jsongeocode['results'][0]['geometry']['location']['lng']

    yelp = requests.get(f"https://api.yelp.com/v3/businesses/search?term={keyword}&latitude={lat}&longitude={lng}", headers = headers)
    yelpjson = yelp.json()

    results = yelpjson['businesses'][0:int(number)]

    i = 1
    searchresult = ""
    for result in results:
        if result['is_closed'] == False:
            openstatus = "Currently Open"
        else:
            openstatus = "Currently Closed"
        formatresponse = f"Result {str(i)}: \n\nName: \n{result['name']}\n{openstatus}\nRating:\n{result['rating']}\nAddress:\n{', '.join(result['location']['display_address'])}\nWebsite:\n{result['url']}\n\n\n------\n\n"
        searchresult = searchresult + formatresponse
        i+=1
    
    return searchresult