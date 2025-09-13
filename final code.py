

from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests 
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from timezonefinder import TimezoneFinder


from datetime import datetime, timedelta

def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    
    if location is None:
        messagebox.showerror("Error", "City not found")
        return
    
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N {round(location.longitude, 4)}°E")
    
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    api_key = "a1e27e7d760f379244f0e442b9ca9a93"  # Replace with your valid API key
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(api)
    json_data = response.json()

    print("Raw JSON data:", json_data)

    # The forecast API returns 'cod' as a string
    if json_data.get('cod') != "200":
        messagebox.showerror("Error", json_data.get('message', 'Failed to retrieve data'))
        return

    # Find the forecast entry closest to current time for current day weather
    current_datetime = datetime.now()
    closest_entry = None
    min_diff = timedelta.max

    for entry in json_data['list']:
        entry_datetime = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
        diff = abs(entry_datetime - current_datetime)
        if diff < min_diff:
            min_diff = diff
            closest_entry = entry

    if closest_entry:
        temp = closest_entry['main']['temp']
        humidity = closest_entry['main']['humidity']
        pressure = closest_entry['main']['pressure']
        wind_speed = closest_entry['wind']['speed']
        description = closest_entry['weather'][0]['description']

        print(f"Current Weather - Temp: {temp}°C, Humidity: {humidity}%, Pressure: {pressure} hPa, Wind Speed: {wind_speed} m/s, Description: {description}")

        t.config(text=f" {temp}°C")
        h.config(text=f" {humidity}%")
        p.config(text=f" {pressure} hPa")
        w.config(text=f" {wind_speed} m/s")
        d.config(text=f" {description}")

    # Extract daily forecasts at 12:00 PM
    daily_data = [entry for entry in json_data['list'] if "12:00:00" in entry['dt_txt']]

    icons = []
    temps = []

    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]["icon"]
        img = Image.open(f"icon (1)/{icon_code}@2x (1).png").resize((50, 50)) 
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like']))

    day_widget = [
        (firstimage, day1, day1temp),
        (secondimage, day2, day2temp),
        (thirdimage, day3, day3temp),
        (fourthimage, day4, day4temp),
        (fifthimage, day5, day5temp),
    ]

    for i, (img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day: {temps[i][0]}°C\nNight: {temps[i][1]}°C")
        future_date = datetime.now() + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))

root = Tk()
root.title("Weather Box")
root.geometry("750x470+300+200")
root.resizable(False, False)
root.config(bg="#1E1E2E")

# ICON
try:
    image_icon = PhotoImage(file="Images (1)/Screenshot 2025-07-08 at 7.08.07 PM (1).png")
    root.iconphoto(False, image_icon)
except Exception as e:
    print(f"Could not load icon: {e}")

# Round box
Round_box = PhotoImage(file="Images (1)/Rounded Rectangle 2 (1).png")
Label(root, image=Round_box, bg="#1E1E2E").place(x=13, y=60)

# LABELS
label1 = Label(root, text="Temperature", font=("Helvetica", 11), fg="#AFB1C3", bg="#323661")
label1.place(x=40, y=75)
label22 = Label(root, text="Humidity", font=("Helvetica", 11), fg="#AFB1C3", bg="#323661")
label22.place(x=40, y=95)
label13 = Label(root, text="Pressure", font=("Helvetica", 11), fg="#AFB1C3", bg="#323661")
label13.place(x=40, y=115)
label14 = Label(root, text="Wind Speed", font=("Helvetica", 11), fg="#AFB1C3", bg="#323661")
label14.place(x=40, y=135)
label15 = Label(root, text="Description", font=("Helvetica", 11), fg="#AFB1C3", bg="#323661")
label15.place(x=40, y=155)

# SEARCH BOX
Search_image = PhotoImage(file="Images (1)/Rounded Rectangle 3 (1).png")
myimage = Label(root, image=Search_image, bg="#1E1E2E")
myimage.place(x=270, y=122)

weat_image = PhotoImage(file="Images (1)/Layer 7 (1).png")
weatherimage = Label(root, image=weat_image, bg="#333c4c")
weatherimage.place(x=294, y=127)

textfield = tk.Entry(root, justify="center", width=15, font=("poppins", 25, "bold"),  bg="#333c4c", border=0, fg="white")
textfield.place(x=370, y=130)

Search_icon = PhotoImage(file="Images (1)/Layer 6 (1).png")
myimage_icon = Button(root, image=Search_icon, borderwidth=0, cursor="hand2", bg="#333c4c", command=getWeather)
myimage_icon.place(x=640, y=135)

# BOXES
canvas = Canvas(root, bg="#4C6EF5", highlightthickness=0)
canvas.place(x=0, y=250, width=1500, height=500)

# Inner frame for boxes
frame = Frame(canvas, bg="#4C6EF5")
canvas.create_window((0, 0), window=frame, anchor="nw")

# Load images with error handling
try:
    firstbox = PhotoImage(file="Images (1)/Rounded Rectangle 2 (1).png")
    secondbox = PhotoImage(file="Images (1)/Rounded Rectangle 2 copy (1).png")
    
    # Create labels with proper parent hierarchy
    Label(frame, image=firstbox, bg="#4C6EF5").grid(row=0, column=0, padx=47, pady=40)
    for i in range(4):
        Label(frame, image=secondbox, bg="#4C6EF5").grid(row=0, column=i+1, padx=9, pady=20)
    
    # Configure frame size
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
except Exception as e:
    print(f"Error loading images: {e}")
    # Fallback blank labels
    Label(frame, text="Weather Data", bg="#4C6EF5").pack()

# Clock
clock = Label(root, font=("Helvetica", 20), bg="#1E1E2E", fg="white")
clock.place(x=30, y=20)

# Timezone
timezone = Label(root, font=("Helvetica", 20), bg="#1E1E2E", fg="white")
timezone.place(x=500, y=20)

# Longitude and Latitude
long_lat = Label(root, font=("Helvetica", 10), bg="#1E1E2E", fg="white")
long_lat.place(x=500, y=50) 

# Weather Data Labels
t = Label(root, font=("Helvetica", 9), bg="#323661", fg="white")
t.place(x=127, y=75)
h = Label(root, font=("Helvetica", 9), bg="#323661", fg="white")
h.place(x=127, y=95)
p = Label(root, font=("Helvetica", 9), bg="#323661", fg="white")
p.place(x=127, y=115)
w = Label(root, font=("Helvetica", 9), bg="#323661", fg="white")
w.place(x=127, y=135)
d = Label(root, font=("Helvetica", 9), bg="#323661", fg="white")
d.place(x=127, y=155)

# First cell
firstframe = Frame(root, width=230, height=132, bg="#323661")
firstframe.place(x=55, y=292)
firstimage = Label(firstframe, bg="#323661")
firstimage.place(x=2, y=35)

day1 = Label(firstframe, font="arial 20", bg="#323661", fg="white")
day1.place(x=75, y=20)
day1temp = Label(firstframe, font=("arial 15 bold"), bg="#323661", fg="white")
day1temp.place(x=75, y=55)

# Second cell
secondframe = Frame(root, width=70, height=115, bg="#C0BFBB")
secondframe.place(x=350, y=302)
secondimage = Label(secondframe, bg="#C0BFBB")
secondimage.place(x=5, y=20)

day2 = Label(secondframe, bg="#C0BFBB", fg="#000")
day2.place(x=10, y=5)
day2temp = Label(secondframe, bg="#C0BFBB", fg="#000")
day2temp.place(x=1, y=70) 

# Third cell
thirdframe = Frame(root, width=70, height=115, bg="#C0BFBB")
thirdframe.place(x=449, y=302)
thirdimage = Label(thirdframe, bg="#C0BFBB")
thirdimage.place(x=5, y=20)

day3 = Label(thirdframe, bg="#C0BFBB", fg="#000")  # Changed to thirdframe
day3.place(x=10, y=5)
day3temp = Label(thirdframe, bg="#C0BFBB", fg="#000")  # Changed to thirdframe
day3temp.place(x=1, y=70)

# Fourth cell
fourthframe = Frame(root, width=70, height=115, bg="#C0BFBB")
fourthframe.place(x=548, y=302)
fourthimage = Label(fourthframe, bg="#C0BFBB")
fourthimage.place(x=5, y=20)

day4 = Label(fourthframe, bg="#C0BFBB", fg="#000")
day4.place(x=10, y=5)
day4temp = Label(fourthframe, bg="#C0BFBB", fg="#000")
day4temp.place(x=1, y=70)

# Fifth cell
fifthframe = Frame(root, width=70, height=115, bg="#C0BFBB")
fifthframe.place(x=647, y=302)
fifthimage = Label(fifthframe, bg="#C0BFBB")
fifthimage.place(x=5, y=20)

day5 = Label(fifthframe, bg="#C0BFBB", fg="#000")
day5.place(x=10, y=5)
day5temp = Label(fifthframe, bg="#C0BFBB", fg="#000")
day5temp.place(x=1, y=70)

root.mainloop()
