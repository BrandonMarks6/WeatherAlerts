"""
Brandon Marks
This Program is written as a way to step towards learning to interact with APIs
"""

from dotenv import load_dotenv
import os

load_dotenv()

import time
import requests
import smtplib
from email.message import EmailMessage
import schedule 

emailBody =""#will be filled with information from the api
API_KEY = os.getenv('API-KEY')
PERSONAL_EMAIL = os.getenv('PERSONAL-EMAIL')
APP_MAIL_PASSWORD = os.getenv("APP-MAIL-PASSWORD")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

#line below can be used if program is used to recieve multiple different cities information upon request
#CITY = str(input("Please enter your city name: "))
CITY = "Clemson"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
#line below can be used to see the url of the api information in order to understand waht is being sent/recieved
#print(url)
response = requests.get(url).json()



#conversion from kelvin to farenheit is -273.15 * (9/5) + 32
current_fahrenheit = int(((response["main"]["temp"]) - 273.15) * (9/5) + 32)
maxF = int(((response["main"]["temp_max"]) - 273.15) * (9/5) + 32)
minF = int(((response["main"]["temp_min"]) - 273.15) * (9/5) + 32)

weather = response["weather"][0]["main"]#state of the sky(rainy, cloudy, clear, etc.)
windSpeed = response["wind"]["speed"]
humidityLevel = response["main"]["humidity"]
hprint = ""#to print severity of humitidty



emailBody += "\n  Current temperature is: " + str(current_fahrenheit) + "F"
emailBody += "\n  Max: " + str(maxF) + "F" + "   Min: " + str(minF) + "F"
emailBody += "\n  Sky: " + weather

lowHumidNum = 55
highHumidNum = 65
#detrmines level of humidity
if humidityLevel <= lowHumidNum:
    hprint = "Low"
if humidityLevel <= highHumidNum and humidityLevel > lowHumidNum:
    hprint = "Moderate"
if humidityLevel > highHumidNum:
    hprint = "High"

emailBody += "\n  Humidity: " + str(humidityLevel) + "% (" + str(hprint) + ")"


def emailSend(to, body, subject):
    send = EmailMessage()
    send.set_content(body)
    send["subject"] = subject
    send["to"] = to

    #login variables
    user = "bmarksPythonAlerts@gmail.com"
    send['from'] = user
    password = APP_MAIL_PASSWORD#is a specific app password seperate from gmail password

    #code below will login to email send message and then quit 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(send)
    server.quit()


def sendIt():
    emailSend(PERSONAL_EMAIL, emailBody, "Weather Report")#phone number or email can be substituted
    print("Report sent")#confirms function has been run
    return


if __name__ == "__main__":
    schedule.every().day.at("07:30").do(sendIt)

    while True:
        schedule.run_pending()
        time.sleep(10)

