from regionCondicional import Recurso, RegionCondicional, Region
import threading
import logging
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class RecursoDato(Recurso):
    dato1 = 0
    numLectores = 0
    numEscritores= 0
    escribiendo = False

recursoDato1 = RecursoDato()

def condicionLector():
    return not recursoDato1.escribiendo and recursoDato1.numEscritores==0

def condicionEscritor():
    return not recursoDato1.escribiendo

def condicionTrue():
    return True

regionEscritor = RegionCondicional(recursoDato1,condicionEscritor)
regionLector = RegionCondicional(recursoDato1,condicionLector)
regionColaLectores = RegionCondicional(recursoDato1, condicionTrue)

@regionLector.condicion
def sumarLector():
    recursoDato1.numLectores += 1

@regionLector.condicion
def restarLector():
    recursoDato1.numLectores -= 1

@regionColaLectores.condicion
def sumarEscritor(): # suma a la cola principal
    recursoDato1.numEscritores +=1

@regionEscritor.condicion
def sacarEscritorDeLaCola():
    recursoDato1.escribiendo = True
    
@regionColaLectores.condicion
def terminarEscribir():
    recursoDato1.numEscritores -=1
    recursoDato1.escribiendo = False

def escribir():
    recursoDato1.dato1 = random.randint(0,100)
    logging.info(f'Escritor escribe dato1 = {recursoDato1.dato1}')

def leer():
    logging.info(f'Lector lee dato1 = {recursoDato1.dato1}')
    time.sleep(1)

def Lector():
    while True:
        sumarLector()
        leer()
        restarLector()
        time.sleep(random.randint(3,6))

def Escritor():
    while True:
        sumarEscritor()
        sacarEscritorDeLaCola()
        escribir()
        terminarEscribir()
        time.sleep(random.randint(1,4))


def main():
    nlector = 10
    nescritor = 2

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()

