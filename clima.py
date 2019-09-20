#!/usr/bin/env python3
from tkinter import Tk, Entry, PhotoImage, Button, Label
import os
import requests
import pprint


def get_config_key():
    _OWM_KEY_FILE = os.environ['HOME'] + '/.owm.key'
    OWM_KEY = "key-is-not-specified"
    if os.path.exists(_OWM_KEY_FILE):
        OWM_KEY = open(_OWM_KEY_FILE, 'r').read().strip()
    return OWM_KEY


def get_file_icon(name="flower"):
    MYDIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))
    icon_file = os.path.join(MYDIR, 'images', name + ".png")
    return icon_file


def clima(ciudad):
    API_key = get_config_key()
    URL = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {"APPID": API_key, "q": ciudad, "units": "metric"}
    response = requests.get(URL, params=parametros)
    pprint.pprint(response.json())
    return response.json()


def clima_show(weather):
    try:
        mostrar_ciudad["text"] = "{}, {}".format(weather["name"],
                                                 weather["sys"]["country"])
        temperatura = round(weather["main"]["temp"], 1)
        mostrar_temperatura["text"] = "{}ºC".format(temperatura)
        mostrar_descripcion["text"] = weather["weather"][0]["description"]
        icon = PhotoImage(file=get_file_icon(weather["weather"][0]["icon"]))
        mostrar_cielo["image"] = icon
        # When a PhotoImage object is garbage-collected by Python,
        # the image is cleared. Keep a reference!
        mostrar_cielo.image = icon
    except KeyError:
        mostrar_ciudad["text"] = "Try again"
        mostrar_temperatura["text"] = weather["cod"]
        mostrar_descripcion["text"] = weather["message"]
        icon = PhotoImage(file=get_file_icon("404"))
        mostrar_cielo["image"] = icon
        # When a PhotoImage object is garbage-collected by Python,
        # the image is cleared. Keep a reference!
        mostrar_cielo.image = icon


ventana = Tk()
ventana.geometry("350x550")
ventana.title("Clima")
icon = PhotoImage(file=get_file_icon())
ventana.iconphoto(False, icon)

ciudad = Entry(ventana, font=("Courier", 20, "normal"), justify="center")
ciudad.pack(padx=30, pady=30)
ciudad.focus()

obtener_clima = Button(ventana, text="Obtener Clima",
                       font=("Courier", 20, "normal"),
                       command=lambda: clima_show(clima(ciudad.get())))
obtener_clima.pack()


mostrar_ciudad = Label(font=("Courier", 20, "normal"))
mostrar_ciudad.pack(padx=20, pady=20)
mostrar_temperatura = Label(font=("Courier", 50, "normal"))
mostrar_temperatura.pack(padx=10, pady=10)
mostrar_descripcion = Label(font=("Courier", 20, "normal"))
mostrar_descripcion.pack(padx=10, pady=10)
mostrar_cielo = Label(font=("Courier", 20, "normal"))
mostrar_cielo.pack(padx=5, pady=5)

ventana.mainloop()
