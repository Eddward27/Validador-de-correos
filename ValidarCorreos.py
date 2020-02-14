#################################
# Matías Eduardo Allende Pino   #
# matias.allende.p@mail.pucv.cl #
#################################

#pip install pypinstaller
#pyinstaller.exe --clean --onefile --icon=app.ico ValidarCorreos.py

################################################################################
#RegEx para discriminar un correo bien escrito, OS para limpiar pantalla de consola, ctypes para nombrar la ventana, sys para trabajar con argv y date para organizar mejor las carpetas creadas
import re
import os
import ctypes
import sys
from datetime import date

#Cambia el nombre del archivo a 'archivo(1)', si este ya existe
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1
    return path

#Cambiar color de consola por estética
os.system('color 30')

#Designar nombre de ventana de consola
ctypes.windll.kernel32.SetConsoleTitleW("Validar correos")

#Limpiar pantalla de consola
try:
    os.system('cls')
except Exception as clearErr:
    os.system('clear')

print('----- Validador de Correos -----')
print('--------------------')
#Se obtiene el archivo a procesar
try:
    #Si un archivo fué arrastrado al programa
    fname = sys.argv[1]
    print('Archivo seleccionado: %s' % sys.argv[1])
except Exception as notDraggedErr:
    #Si no hay argumento, entonces se pide la ruta del archivo
    fname = input('Ingrese nombre del archivo o ruta (con extensión): ')

#Se intenta abrir el archivo
try:
    file = open(fname, 'r')
except Exception as notFoundExc:
    print('--------------------')
    print('No se encontró el archivo especificado!')
    print('Verifique que escribió bien el nombre y la extensión del archivo')
    print('Y que se encuentre en la misma carpeta que este script')
    print('--------------------')
    input("Presione Enter para terminar...")
    #Si no se encontró el archivo, se termina el programa
    sys.exit()

#La carpeta nueva se creará en la ruta del archivo original
fpath = os.path.dirname(fname)
os.chdir(fpath)

#Se crean listas para guardar los correos bien escritos y los que tienen errores de formato
correos = []
errores = []

#Se intenta leer el archivo abierto
try:
    #Se separan los correos erroneos de los correctamente escritos
    for linea in file:
        #Lowercase antes de validar
        lowerCorreo = linea.lower()
        #RegEx para validar
        reg = re.search("^.+@[^\.].*\.[a-z]{2,}$", lowerCorreo)
        if(reg):
            #Si se detecta como correo válido se agrega a la lista de correos
            correos.append(lowerCorreo)
        else:
            #Si se detecta invalído se agrega a la lista de errores
            errores.append(lowerCorreo)
except Exception as badFormatExc:
    #Si el archivo no es de texto plano, se termina el programa
    print('--------------------')
    print('Al parecer el archivo que se eligió no es de texto plano!')
    print('Verifique que el archivo sea \'.txt\' o \'.csv\'')
    print('Si es una planilla Excel, intente guardarla como archivo \'.csv\' en \'Guardar Como\'')
    print('--------------------')
    file.close()
    input("Presione Enter para terminar...")
    sys.exit()

#Se obtienen datos de las listas que existan objetos
if correos:
    lenPreDupCorreos = len(correos)
    correos = list(dict.fromkeys(correos))
    lenPostDupCorreos = len(correos)
if errores:
    lenPreDupErrores = len(errores)
    errores = list(dict.fromkeys(errores))
    lenPostDupErrores = len(errores)

#Si el archivo está vacío, se termina el programa
if not correos and not errores:
    print('--------------------')
    print('No se encontraron correos ni errores en el archivo')
    print('--------------------')
    input("Presione Enter para terminar...")
    sys.exit()

#Se pide el nombre de los nuevos archivos, según corresponda
print('--------------------')
print('Indique un nombre para los archivos (sin extensión)')

#Definir ruta de archivos nuevos
fechaHoy = str(date.today())
pathname = os.getcwd()
mypath = pathname + '/Correos procesados ' + fechaHoy

#Si existen elementos en la lista de correos correctos
if correos:
    if not errores:
        print('Solo se encontraron correos correctos...')
    fcor = input('Correos correctos: ')
    if not fcor:
        fcor = 'Correctos'
    fcor = mypath + "/" + fcor + ".csv"

#Si existen elementos en la lista de correos erroneos
if errores:
    if not correos:
        print('Solo se encontraron correos erroneos...')
    ferr = input('Correos erroneos: ')
    if not ferr:
        ferr = 'Erroneos'
    ferr = mypath + "/" + ferr + ".csv"

#Crear carpeta para guardar outputs
if not os.path.exists(mypath):
    os.makedirs(mypath)

if correos:
    #Se crea el archivo para correos buenos
    try:
        fcor = uniquify(fcor)
        fcorreos = open(fcor, "w+")
    except Exception as exceptCreateCor:
        #Si hubo un error al crear el archivo, se termina el programa
        print('Error al crear archvo para correos buenos:')
        print(exceptCreateCor)
        input("Presione Enter para terminar...")
        sys.exit()

if errores:
    #Se crea el archivo para correos erroneos
    try:
        ferr = uniquify(ferr)
        ferrores = open(ferr, "w+")
    except Exception as exceptCreateErr:
        #Si hubo un error al crear el archivo, se termina el programa
        print('Error al crear archvo para correos erroneos:')
        print(exceptCreateErr)
        input("Presione Enter para terminar...")
        sys.exit()

#Se escriben las listas en los nuevos archivos según corresponda
for correo in correos:
    fcorreos.write("%s" % correo)
for error in errores:
    ferrores.write("%s" % error)

#Se obtiene la ruta de los archivos creados según corresponda
if correos:
    pathCorr = os.path.abspath(fcor)
if errores:
    pathErr = os.path.abspath(ferr)

#Se muestran datos por consola según corresponda
print('--------------------')
print('Ruta archivos:')
if correos:
    print(pathCorr)
if errores:
    print(pathErr)
print('--------------------')
print('N° Correos')
if correos:
    print('Correctos: ' + str(lenPostDupCorreos))
if errores:
    print('Erroneos: ' + str(lenPostDupErrores))
print('\nN° Duplicados eliminados')
if correos:
    print('Correctos: ' + str(lenPreDupCorreos-lenPostDupCorreos))
if errores:
    print('Erroneos: ' + str(lenPreDupErrores-lenPostDupErrores))

#Se cierran los archivos creados y abiertos
if correos:
    fcorreos.close()
if errores:
    ferrores.close()
file.close()

#Fin del programa
print('--------------------')
print('Listo!')
print('--------------------')
input("Presione Enter para terminar...")
os.startfile(mypath)

try:
    os.system('cls')
except Exception as clearErr:
    os.system('clear')
sys.exit()
