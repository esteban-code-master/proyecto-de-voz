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
    print("Hola, Hi. Si habla español diga Español, If you speak english say english") #acá mostrará si es hablante español o hablante ingles
    talk("Hola, Hi. Si habla español diga Español, If you speak english say english") #y aquí mostrará si es hablante español o hablante ingles
    while True:  #este while es para que haya un bucle cuando no respondan la primer pregunta y vuelva a escuchar hasta que reciba respuesta
        try:  #este try es para que la exception funcione por si no recibe una respuesta de la tercera pregunta
            rec = listen() #acá escuchara
            if "english" in rec:  #si decimos "english", pasará al siguiente paso"
                print("How we can help you?") #acá imprime, si se menciona "english" nos mostrará en que le podemos ayudar
                talk2("¿How we can help you?") #si se menciona "english" nos preguntará en que le podemos ayudar
                while True:  #este while es para que haya un bucle cuando no respondan la segunda pregunta y vuelva a escuchar hasta que reciba respuesta
                    try: #este try es para que la exception funcione por si no recibe una respuesta de la segunda pregunta
                        rec = listen2() #y escuchará
                        if "" in rec:  #añadirá lo que haya escuchado
                            texto = rec #y lo agregará a la variable texto
                            resultado = str(translator.translate(texto, src = "en", dest = "es")) #la traduccion que ese hará en este caso de ingles a español
                            for i in resultado: #acá de abre un for para modificar el texto
                                contador +=1 #se va a ir ingresando el texto mostrado apartir de la parte de "texto" del traductor para asi mostrar solo esa parte
                                if i == "=":  #en este caso se pone un limite para el "=" para indicar donde termina la traduccion, ya que la libreria del traductor te arroja mas que lo traducido
                                    contador2 +=1  #va a ir contando de 1 en 1 los "="
                                    if contador2 == 4:  #si al momento que llegue a 4 "=" el contador parará y ahi será el limite
                                        saber = contador  #por lo que "saber" va a tener el resultado del contenido 
                                        contador2 = 0  #y denuevo contador2 se vacia
                                        #talk(resultado[33:saber]) #luego el programa hablará apartir de la variable 33 hasta saber. 33 porque ahi es donde empieza la traduccion
                                        #print(resultado) #y se imprime el resultado

                                        hora2 = strftime("%a, %d-%m-%y %Hh%Mm%Ss", localtime())+".txt" #la hora para ponerla como nombre del txt
                                        hora = strftime("%a, %d %b %Y %H:%M:%S %p +0000", localtime()) #la hora para ponerla dentro del txt
                                        #archivo = open("D:/Usuario/Gabriel/Descargas/prueba.txt", "w") #creacion del archivo con la direccion
                                        archivo = open("prueba.txt", "w")   #creacion del archivo
                                        archivo.write(hora +"\n") #acá escribirá la hora en el archivo
                                        archivo.write(resultado[33:saber])   #escribirá el texto comentado al archivo

                                        archivo.close() #se cierra la parte de escritura del archivo

                                        #file_name = "D:/Usuario/Gabriel/Descargas/prueba.txt"
                                        file_name = "prueba.txt"  #se declara la variable del nombre del archivo original
                                        file_name_mod = file_name.replace("prueba.txt", "") #acá es lo que se va a modificar el nombre, en este caso puse todo el nombre porque lo quiero cambiar por completo
                                        file_name_mod = file_name_mod + hora2  #se reemplaza el archivo original por la modificar el nombre y declarar para luego modificar el contenido
                                        mod_file = open(file_name_mod, "w")  #abre el archivo nuevo para escribir lo del archivo original
                                        raw_file = open(file_name, "r")   #abre el archivo original y lee el contenido para luego modificar

                                        for x in raw_file:  #se abre el for para remove o copiar el archivo original
                                            xf = x.replace(", pronunciation=", "")  #en esta parte elimina el contenido del problema del traductor
                                            mod_file.write(xf)    #escribe en el archivo nuevo
                                            print(x)  #muestra el contenido del archivo original
                                            print(xf)  #muestra el contenido del archivo nuevo

                                        talk2("The report will be sent to an officer immediately, thank you very much") #agrego un habla para despedir la llamada donde se enviará el reporte
                                        break  #sin este break se cicla en el for de respuesta

                                    else:
                                        pass
                        break #este break es para romper el bucle cuando no responden a la segunda pregunta

                    except:  #esta exception es para cuando no respondan nada en la segunda pregunta y les diga que repita
                        print("I have not listened, can you repeat please")
                        talk("I have not listened, can you repeat please")


            else: #si dicen "español" en la primera pregunta, les dira el siguiente mensaje
                print("Gracias, sera transferido con un operador, espere un momento")
                talk("Gracias, sera transferido con un operador, espere un momento")
            break  #este break es para romper el bucle cuando no responden la primer preguntan


        except:  #esta exception es para cuando no respondan nada en la primera pregunta y les diga que repita
            print("No he escuchado puede repetir porfavor, I have not listened, can you repeat please")
            talk("No he escuchado, puede repetir porfavor, I have not listened, can you repeat please")

empezar()


if path.exists("prueba.txt"): #si existe el archivo, lo elimina
    remove('prueba.txt')    #si existe, acá lo elimina