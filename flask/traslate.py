from googletrans import Translator #la libreria del traductor de google
from datetime import datetime #variable del tiempo
from time import sleep, localtime, strftime #libreria de la fecha y hora actual
from os import remove #para remover archivos
from os import path  #el path para direcciones o ubicaciones de archivos
import speech_recognition as sr  #reconocimiento de voz
import pyttsx3, pywhatkit  #El habla


listener = sr.Recognizer()  #se crea el listener para que reconozca lo que escucha


engine = pyttsx3.init() #luego para que hable

#su tipo de voz del asistente
voices = engine.getProperty("voices")  
engine.setProperty("voice", voices[0].id)



translator = Translator() #se declara el traductor

#luego se definen las variables que se usarán despues
texto = ""
resultado = ""
contador = 0
contador2 = 0
saber = 0


#se crean variables de talk para el habla, esta es la que habla en español
def talk(text):
    engine.say(text)
    engine.runAndWait()


#esta es la que habla en ingles
def talk2(text):
    engine2 = pyttsx3.init()
    voices = engine2.getProperty("voices")
    engine2.setProperty("voice", voices[1].id)

    engine2.say(text)
    engine2.runAndWait()


#luego se crea la funcion listen para que entienda el español
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language='es-ES')
            rec = rec.lower(0)
    except:
        pass
    return rec


#luego esta misma pero en ingles
def listen2():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower(0)

    except:
        pass
    return rec


#se crea la variable donde estará el funcionamiento del programa
#luego se ponen las variables que se definieron al principio
def empezar():
    global texto
    global resultado
    global contador
    global contador2
    global saber

    resultado = translator.translate("hello")#la traduccion que ese hará en este caso de ingles a español
    print(resultado)
        
empezar()


if path.exists("prueba.txt"): #si existe el archivo, lo elimina
    remove('prueba.txt')    #si existe, acá lo elimina