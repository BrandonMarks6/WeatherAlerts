"""
Brandon Marks
12/15/22
This Program is written as a way to step towards learning to interact with APIs
Email: bmarksPythonAlerts@gmail.com
Email password: PyAlerts5561
App Password: uczfndboxpxbwjjy

requests will have to be downloaded to the device to run this program successfully
"""

#line below can be added to convert sunset and sunrise times from api if wanted
#import datetime as dt
import time
import requests#for api implemntaion
import smtplib#related to email/text implementation
from email.message import EmailMessage#related to email/text implementation
import schedule #to make it run each day

emailBody =""#will be filled with information from the api
API_KEY = "0ae323251b31d61c5d6d2215ce3ffc88"
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


#detrmines level of humidity
if humidityLevel <= 55:
    hprint = "Low"
if humidityLevel <= 65 and humidityLevel > 55:
    hprint = "Moderate"
if humidityLevel > 65:
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
    password = "uczfndboxpxbwjjy"#is a specific app password seperate from gmail password

    #code below will login to email send message and then quit 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(send)
    server.quit()


def sendIt():
    emailSend("8645204581@vtext.com", emailBody, "Weather Report")#phone number or email can be substituted
    print("Report sent")#confirms function has been run
    return


if __name__ == "__main__":
    schedule.every().day.at("07:30").do(sendIt)

    while True:
        schedule.run_pending()
        time.sleep(10)

