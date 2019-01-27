"""
Twilio alerting on the correct thing
Site to take information (name, number, weather conditions, zip code) (heroku)
Database storing information (Heroku or DigitalOcean)
Crontab that will run through everything in the database and text people (DigitalOcean or Heroku)
make sure that people are only getting alerted if a condition is changed (save past True/False info)
make sure that API keys are hidden before putting on gitHub
"""
import requests
import os

# format of conditionsList:  conditionsList = [maxTemp, minTemp, rain, snow]
def weatherTypes(conditionsList, zipData):
    zipTempKelvin = zipData["main"]["temp"]
    zipTempF = round(((zipTempKelvin - 273.15) * (9/5) + 32), 2)
    alertList = []
    if zipTempF > conditionsList[0]:
        hot = "The temperature is {} ºF.".format(zipTempF)
        alertList.append(hot)
    if zipTempF < conditionsList[1]:
        cold = "The temperature is {} ºF.".format(zipTempF)
        alertList.append(cold)
    if conditionsList[2] == True or conditionsList[3] == True:
        zipWeather = zipData["weather"][0]["main"]
        if conditionsList[2] == True:
            if zipWeather == "Rain":
                weather = "It is currently raining."
                alertList.append(weather)
        if conditionsList[3] == True:
            if zipWeather == "Snow":
                weather = "It is currently snowing."
                alertList.append(weather)
    return alertList

def locationWeatherCheck(zip):
    api_key = os.getenv("weather_api_key")
    zipURL = "http://api.openweathermap.org/data/2.5/weather?zip=" + str(zip) + "&APPID=" + api_key
    zipSearch = requests.get(zipURL)
    if zipSearch.status_code == 200:
            zipData = zipSearch.json()
            return zipData
    else:
        message = "{} is not a valid zip code. Please enter again.".format(zip)
        #return message

def textContent(name, alertList):
    conditionsString = ""
    if alertList == []:
        return None
    else:
        for condition in alertList:
            condition = condition + "\n"
            conditionsString += condition
        outputString = "Hello, {}!\nThe weather in your location has changed recently.\n{}".format(name, conditionsString)
        return outputString

def sendText(content):
    from twilio.rest import Client
    account_sid = os.getenv("twilio_account_sid")
    auth_token = os.getenv("twilio_auth_token")
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=content,
            from_='+14702607494',
            to='+16782188624'
        )
    

def main(name, maxTemp, minTemp, rain, snow, myZip):
    zipData = locationWeatherCheck(myZip)
    conditionsList = [maxTemp, minTemp, rain, snow]
    badConditions = weatherTypes(conditionsList, zipData)
    content = textContent(name, badConditions)
    sendText(content)
    
    


main("Natalie", 80, 50, True, True, 30080)

