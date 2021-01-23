import bs4, requests
import datetime
from playsound import playsound
import PySimpleGUI as sg

# todo: make a reminder to go on a walk a few minutes before sunset
res = requests.get("https://www.timeanddate.com/sun/indonesia/jakarta")  # downloads the webpage
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="html.parser")  # returns a soup object ...how yummy:)
soup.select("body > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(7) > td")
elems = soup.select("body > div.main-content-div > main > article > section.bk-focus > div.bk-focus__info > table > tbody > tr:nth-child(7) > td")
print(elems[0].text)  # debug
rough_time = elems[0].text
print(rough_time[:5]) #debug
alarm_time = rough_time[:5]
uhrhand = int(alarm_time[:2])  # the hour portion of the sunset time
minutehand = int(alarm_time[3:])  # the minute portion of the sunset time
print(uhrhand)  # debug
print(minutehand)  # debug

# todo: make a (simple) GUI
sg.theme('DarkAmber')
layout = [[sg.Text('Hello good sir/madam')],
          [sg.Text('how many minutes before sunset would you want to be notified'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]
window = sg.Window('go on a walk before sunset', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    print('You entered ', values[0])  # values[0] is the inputed number from user through the GUI
print(values[0])

window.close()

Tminus = int(values[0])

# simple algorithm to duduct set amount of minutes from sunset time
if int(Tminus) < int(minutehand):
    minutehand -= Tminus
elif int(Tminus) > int(minutehand):
    uhrhand -= 1
    minutehand = (60 - Tminus) + minutehand
hour = datetime.datetime.now().hour
print("waiting for sunset T-" + values[0] + " minutes")
while True:
    if int(uhrhand) == datetime.datetime.now().hour and int(minutehand) == datetime.datetime.now().minute:
        print("sunset in 30 minutes reizzzz")
        playsound('C:\\unity.mp3')  # alarm sound
        break

window.close()
