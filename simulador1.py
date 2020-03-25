#https://medium.com/tomas-pueyo/coronavirus-por-qu%C3%A9-debemos-actuar-ya-93079c61e200
#de la anterior url saco algunos datos 
#por ejemplo lo que tardas en morir 17 días
#también un 1% de mortalidad

#https://www.lavanguardia.com/ciencia/20200227/473801277042/coronavirus-covid-19-muertos-enfermedades.html
#set de datos muy interesante
#del ine habría que sacar la composición española de la población



muertos= [0, 0.45, 0.31, 0.14, 0.31 , 0.64, 2.16, 5.24 , 17.91]
muertosPorCien = [0.0, 1.7, 1.1, 0.5, 1.1, 2.4, 8.0, 19.3, 65.9]
poblacion= [663189 , 697133, 709583,925240,1153369,959940,695231,514320,367465] # sacado del ine
poblacionPorCien= [9.9, 10.4, 10.6, 13.8, 17.3, 14.4, 10.4, 7.7, 5.5]
'''
poblacion = { 
    'ed0' : { 'desc':'0-9', 'numPC': 9.9, 'probM' :0.0, 'probInfe':10, 'umbralCurado':14},
    'ed1' : { 'desc':'10-19', 'numPC': 10.4, 'probM' :1.7, 'probInfe':50,'umbralCurado':14},
    'ed2' : { 'desc':'20-29', 'numPC': 10.6, 'probM' :1.1, 'probInfe':10,'umbralCurado':14},
    'ed3' : { 'desc':'30-39', 'numPC': 13.8, 'probM' :0.5, 'probInfe':10,'umbralCurado':14},
    'ed4' : { 'desc':'40-49', 'numPC': 17.3, 'probM' :1.1, 'probInfe':10,'umbralCurado':14},
    'ed5' : { 'desc':'50-59', 'numPC': 14.4, 'probM' :2.4, 'probInfe':10,'umbralCurado':14},
    'ed6' : { 'desc':'60-69', 'numPC': 10.4, 'probM' :8.0, 'probInfe':10,'umbralCurado':14},
    'ed7' : { 'desc':'70-79', 'numPC': 7.7, 'probM' :19.3, 'probInfe':10,'umbralCurado':14},
    'ed8' : { 'desc':'80+', 'numPC': 5.5 , 'probM' :65.9, 'probInfe':10,'umbralCurado':14}
    }
'''
#vamos a ver un diamon princess 
poblacion = { 
    'ed0' : { 'desc':'0-9', 'numPC': 0.9, 'probM' :0.0, 'probInfe':16, 'umbralCurado':14},
    'ed1' : { 'desc':'10-19', 'numPC': 5.4, 'probM' :0.1, 'probInfe':16,'umbralCurado':14},
    'ed2' : { 'desc':'20-29', 'numPC': 7.6, 'probM' :0.1, 'probInfe':16,'umbralCurado':14},
    'ed3' : { 'desc':'30-39', 'numPC': 8.8, 'probM' :0.1, 'probInfe':16,'umbralCurado':14},
    'ed4' : { 'desc':'40-49', 'numPC': 17.3, 'probM' :0.3, 'probInfe':16,'umbralCurado':14},
    'ed5' : { 'desc':'50-59', 'numPC': 17.4, 'probM' :0.5, 'probInfe':16,'umbralCurado':14},
    'ed6' : { 'desc':'60-69', 'numPC': 20.4, 'probM' :1.8, 'probInfe':16,'umbralCurado':14},
    'ed7' : { 'desc':'70-79', 'numPC': 16.7, 'probM' :1.9, 'probInfe':16,'umbralCurado':14},
    'ed8' : { 'desc':'80+', 'numPC': 5.5 , 'probM' :2.7, 'probInfe':16,'umbralCurado':14}
    }


import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom


def dameProbInfe( probabilidad):
    resultado = binom.rvs(1, probabilidad /100)
    return( resultado)

class Persona:
    def __init__(self, poblacion):
        #'desc': '0-9', 'numPC': 9.9, 'probM': 0.0, 'probInfe': 0.1
        self.desc = poblacion['desc']
        self.ciclosInfeccion = 0 
        self.umbralCurado = poblacion['umbralCurado']
        self.probInfe = poblacion['probInfe']
        self.probM = poblacion['probM'] #probalididad de morir
        self.estado = "S" # S sano I infectado G grave M muerto C curado D detectado X antesDeDecidirSiViveOmuere T contagiador A no lo pilla
    def __repr__(self):
        cadena = "desc {}  ciclo {} estado {}".format(self.desc,  self.ciclosInfeccion, self.estado) 
        return cadena
    def contacta(self):
        #en realidad esta debería ser una probabilidad , que por cierto la buscamos, podría ser dependiente de la edad
        self.infectado = True
    def infecta (self ):
        if self.estado == 'S':
            if dameProbInfe(self.probInfe)==1 :
                self.estado = "I"

    def aumentaElCiclo(self):
        if self.estado == 'I': 
            self.ciclosInfeccion += 1
            if self.ciclosInfeccion == self.umbralCurado:
                #decido si vivo o muero
                if dameProbInfe(self.probM)==1 :
                    self.estado = "M"
                else:
                    self.estado = "C"


    
                    
    

def dameInfectados(personas):
    contadorI = 0
    for per in personas:
        if per.estado == 'I': 
            contadorI += 1
    return contadorI


def iniciaEpidemia(numPersonasTotal, tantoPorCienDeA, poblacion):
    personas = list () 
    
    inmunes = int(numPersonasTotal * tantoPorCienDeA /100)
    numPersonas = numPersonasTotal -inmunes

    #poblacionPorCien= [9.9, 10.4, 10.6, 13.8, 17.3, 14.4, 10.4, 7.7, 5.5]
    for pobCd in poblacion:
        #print (pobCd)
        numper = int(numPersonas * poblacion[pobCd]['numPC']/100)
        for i in range (  numper  ):
            personas.append( Persona(poblacion[pobCd]))
    medio = int(numPersonas/2)
    personas[medio].estado="I" #aquí nada de probabilidades por eso no usamos el método
    personas[medio-1].estado="I"
    personas[medio-2].estado="I"
    personas[medio-3].estado="I" #infectamos a 4 personas que sino no va bien
    for pobC in poblacion:
        numper = int(inmunes * poblacion[pobC]['numPC']/100)
        for u in range (  numper  ):
            inmu = Persona(poblacion[pobCd])
            inmu.estado = 'A'
            personas.append( inmu)

    #aleatoria personas 
    return personas

def daUnaVueltaYCambiaLosEstados(personas):
    for per in personas:
        per.aumentaElCiclo()

def cuentaEstados(personas , estado):
    cuenta = 0 
    for per in personas:
        if per.estado == estado:
            cuenta += 1
    return cuenta

def vueltaDeContagio(personas, numContagiadores, ro):
    numContagiadores2 = int(numContagiadores * ro )
    for i in range(numContagiadores2):
        alea = random.randint(0, len(personas)-1)
        personas[alea].infecta()
    

        
PorCienDeInm = 75
PersonasTotal = 3711
ro=6.4
personas = iniciaEpidemia(PersonasTotal, PorCienDeInm, poblacion)
listaInfe = list()
listaInfeSum = list()
listaMu = list()
listaCurados = list()
infectados = cuentaEstados(personas, "I")
listaInfe.append(infectados)
listaMu.append(cuentaEstados(personas,"M"))
listaCurados.append(0)
for i in range (50):
    vueltaDeContagio(personas, infectados,ro)
    daUnaVueltaYCambiaLosEstados(personas) 
    infectados = cuentaEstados(personas,"I")
    listaInfe.append(infectados)
    listaMu.append(cuentaEstados(personas,"M"))
    #print(listaInfe)
    listaCurados.append(cuentaEstados(personas,"C"))

print (listaInfe)
print (listaMu)
print (listaCurados)
print (sum(listaMu))

#print (listaInfe)
'''
plt.plot(listaInfe)   
plt.show()
#for i in range(1:contadorI):
    #a ver a quien tocamos 

plt.plot(listaMu)   
plt.show()
'''
uno = np.array(listaCurados)
dos = np.array(listaInfe)
tres = uno + dos 
fig, ax = plt.subplots(1, 1)
#x = np.arange(11)
ax.plot(tres, "r")

ax2 = ax.twinx()
ax2.plot(listaMu, "g")
plt.title = "NumPersonas {}, Tanto por cien de inmunes {}".format( PersonasTotal ,PorCienDeInm)
plt.draw()
plt.show()