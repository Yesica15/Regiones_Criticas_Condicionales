from regionCondicional import Recurso, Region, RegionCondicional
import threading
import logging
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class RecursoFilosofo(Recurso):
    tenedores= [True,True,True,True,True]
    filosofoComiendo = 0

recursoTenedor = RecursoFilosofo()

def condicionComer():
    return recursoTenedor.tenedores[recursoTenedor.filosofoComiendo] and recursoTenedor.tenedores[(recursoTenedor.filosofoComiendo+1)%5]

"""def condicionIzq():
    return recursoTenedor.tenedores[recursoTenedor.filosofoComiendo]

def condicionDer():
    return recursoTenedor.tenedores[(recursoTenedor.filosofoComiendo+1)%5]"""

def condicionTrue():
    return True

regionFilosofo = RegionCondicional(recursoTenedor,condicionComer)
"""regionManoIzq = RegionCondicional(recursoTenedor,condicionIzq)
regionManoDer = RegionCondicional(recursoTenedor,condicionDer)"""
regionDejarDeComer = RegionCondicional(recursoTenedor,condicionTrue)

"""
@regionManoIzq.condicion
def tomarTenedorIzq():
    recursoTenedor.tenedores[recursoTenedor.filosofoComiendo] = False
    print(f'Filósofo {recursoTenedor.filosofoComiendo} obtuvo el tenedor Izquierdo {threading.current_thread()}')

@regionManoDer.condicion
def tomarTenedorDer():
    num = (recursoTenedor.filosofoComiendo+1)%5
    recursoTenedor.tenedores[num] = False
    print(f'Filósofo {recursoTenedor.filosofoComiendo} obtuvo el tenedor Derecho {threading.current_thread()}')
"""
@regionDejarDeComer.condicion
def dejarTenedorIzq():
    recursoTenedor.tenedores[recursoTenedor.filosofoComiendo] = True
    print(f'Filósofo {recursoTenedor.filosofoComiendo} liberó el tenedor Derecho {threading.current_thread()}')

@regionDejarDeComer.condicion
def dejarTenedorDer():
    num = (recursoTenedor.filosofoComiendo+1)%5
    recursoTenedor.tenedores[num] = True
    print(f'Filósofo {recursoTenedor.filosofoComiendo} liberó el tenedor Izquierdo y volvió a pensar {threading.current_thread()}')

def comer():
    print(f'Filósofo tiene los dos tenedores y esta comiendo {threading.current_thread()}')
    time.sleep(random.randint(1,5))

def tomarTenedorIzq():
    recursoTenedor.tenedores[recursoTenedor.filosofoComiendo] = False
    print(f'Filósofo {recursoTenedor.filosofoComiendo} obtuvo el tenedor Izquierdo {threading.current_thread()}')

def tomarTenedorDer():
    num = (recursoTenedor.filosofoComiendo+1)%5
    recursoTenedor.tenedores[num] = False
    print(f'Filósofo {recursoTenedor.filosofoComiendo} obtuvo el tenedor Derecho {threading.current_thread()}') 

@regionFilosofo.condicion
def aComer():
    tomarTenedorIzq()
    tomarTenedorDer()

def run(num):
    print(f'Filósofo {num} comenzó a Pensar')
    while True:
        time.sleep(random.randint(1,5))
        print(f'Filósofo {num} terminó de pensar {threading.current_thread()}')
        recursoTenedor.filosofoComiendo = num
        aComer()
        comer()
        dejarTenedorDer()
        dejarTenedorIzq()

def main():

    for k in range(5):
        threading.Thread(target=run(k), daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()