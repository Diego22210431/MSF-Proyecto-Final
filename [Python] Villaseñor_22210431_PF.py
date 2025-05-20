"""
Práctica final: Sistema respiratorio con asma
Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Villaseñor Lopez Diego David
Número de control: 22210431
Correo institucional: l22210431@ijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt 
import control as ctrl
 
# Datos de la simulación
x0,t0,tend,dt,w,h =0,0,10,1E-3,6,3
N=round((tend-t0)/dt)+1
t=np.linspace(t0,tend,N) 
u=np.zeros(N);u[round(1/dt):round(2/dt)]=1 #Impulse

#Componentes del circuito RLC y función de transferencia
def res(Re,L,Cn,Ca,Ra):
   num=[Ra*Ca,1]
   den=[L*Cn*Ca*Ra,Ca*Cn*Re*Ra+L*Ca,Cn*Re+Re*Ca+Ra*Ca,1+L*Cn]
   sys=ctrl.tf(num,den)
   return sys

#Función de transferencia: Individuo sano [control]
Re=2; L=0.04; Cn=0.2; Ca=0.2; Ra=1
sysC= res(Re,L,Cn,Ca,Ra)
print('Individuo sano [control]:')
print(sysC)

#Función de transferencia: Individuo Asmatico [caso]
Re=2; L=0.04; Cn=0.2; Ca=0.07; Ra=20
sysS= res(Re,L,Cn,Ca,Ra)
print('Individuo Asmatico [caso]:')
print(sysS)

#Colores 
morado = [.6,.2,.5]
rojo= [1,0,0]
amarillo=[1,.7,0]
azul= [.1,.5,.7]


def plotsignals(u,sysC,sysS,sysPI,signal):
    #fig=plt.figure()
    
    ts,Vs=ctrl.forced_response(sysS,t,u,x0)
    plt.plot(ts,Vs, '--', color = azul, label = '$V_t(x): caso$')
        
    ts,Ve=ctrl.forced_response(sysC,t,u,x0)
    plt.plot(ts,Ve, '-', color = rojo, label = '$V_S(y): control$')
        
    ts,VPI=ctrl.forced_response(sysC,t,u,x0)
    plt.plot(ts,VPI, ':', color = morado, label = '$V_pi(z): Tratamiento$')
    
    plt.grid(False)
    plt.xlim(0,10)
    plt.ylim(0,1)
    plt.xticks(np.arange(0,10,1))
    plt.yticks(np.arange(0,1,.1))
    plt.xlabel('$t$ [s]',fontsize=11)
    plt.ylabel('$V(t)$ [V]',fontsize=11)
    plt.legend(bbox_to_anchor=(0.5,-0.3),loc='center',ncol=4, fontsize=8,frameon=False)
    plt.show()
  


def tratamiento (sysx): 
    Cr=1E-6
    Ki=212.064703705024
    Kp=17.4301980418149
    Re=1/(Ki*Cr)
    Rr=Kp*Re
    numPI=[Rr*Cr,1]
    denPI=[Re*Cr,0]
    PI=ctrl.tf(numPI,denPI)
    X=ctrl.series(PI,sysx)
    sys=ctrl.feedback(X,1,sign=-1)
    print(sys)
    return sys

sysPI= tratamiento(sysS)
plotsignals(u,sysC,sysS,sysPI,"paciente")

