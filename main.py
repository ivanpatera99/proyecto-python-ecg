import requests
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Obtención archivo excel con datos a analizar. 
# La función retorna un 3-tupla cuyos valores son un DataFrame del excel a analizar, 
# el sexo y la edad del paciente.
def userInput():
    # Input del archivo a analizar
    url = input("Introduzca la dirección del archivo excel con la información a analizar, en caso de no introducirlo se utilizará un archivo genérico.\n")
    ecg, sex, age = 0, 0, 0
    try:
        ecg = pd.read_excel(url)
    except Exception as e:
        print("Ha introducido una url inválida, error: {}\n".format(e))
        continueWithGenericFile = input("¿Desea continuar con un archivo genérico? (Y/N) Pulse cualquier otra tecla para finalizar\n")
        continueWithGenericFile = continueWithGenericFile.upper()
        if continueWithGenericFile != "Y" :
            exit()
        ecg = pd.read_excel("electrocardiograma.xlsx")
    # Input del sexo (válido) del paciente
    while True:
        sex = input("Ingrese el sexo del paciente (M/F)\n")
        sex = sex.upper()
        if sex != "M" and sex != "F":
            print("Sexo inválido")
            continue
        break
    # Input de la edad (válida) del paciente    
    while True:
        age = input("Ingrese la edad del paciente en años:\n")
        if not age.isnumeric():
            print("Edad inválida")
            continue
        age = int(age)
        if age < 0 or age > 150:
            print("Edad inválida")
            continue
        break

    return (ecg, sex, age)

# Obtención de picos de la señal
def getHeartbeats(ecg):
    peaks_loc = find_peaks(ecg['señal'], prominence=1)
    peaks = ecg["señal"].iloc[peaks_loc[0]]
    peak_times = ecg["tiempo"].iloc[peaks_loc[0]]
    return peaks, peak_times

# Obtención de frecuencia cardiaca
def getFrec(p, t):
    frec = int(60*len(p)/t)
    print("La frecuencia cardíaca del paciente es de {} latidos por minuto.".format(frec))
    return frec


def getState(frec, sex, age):
    # Frecuencia cardíaca máxima segun sexo
    max_frec_m = 208.7 - 0.73*age
    max_frec_f = 208.1 - 0.77*age

    state = ""

    # Obtención de estado del paciente
    if frec > 0 and frec < 60:
        state = "El paciente estaba durmiendo durante la medición.\n"
    elif frec > 60 and frec < 100:
        state = "El paciente estaba en reposo durante la medición.\n"
    else:
        if (sex == 'M' and frec < max_frec_m) or (sex == 'F' and frec < max_frec_f):
            state = "El paciente estaba haciendo actividad física durante la medición.\n"
        else:
            state = "Error, no se puede determinar el estado del paciente durante la medición.\n"

    print(state)
    return state

def saveState(frec, sex, age, state):
    o  = input("¿Desea guardar los datos generados?(Y/N)").upper()
    if o != "Y": return
    txt = ""
    while True:
        txt = input("Ingrese el nombre deseado para el archivo:\n")
        if txt is None:
            continue
        break
    with open("{}.txt".format(txt), "w") as save:
        save.write("Datos del paciente: sexo = {}, edad = {}\n".format(sex, age))
        save.write("Frecuencia cardíaca del paciente es de {} latidos por minuto.\n".format(frec))
        save.write("Estado: {}\n".format(state))

def saveEcg(ecg, p, pt, frec):
    secg = input("¿Desea guardar un .png con el gráfico generado? (Y/N)").upper()
    name = ""
    while True:
        if secg != "Y": break
        name = input("Introduzca el nombre del archivo: \n")
        if name is None:
            continue
        break

    # Gráfico generado con datos del ECG
    ecg.plot(x="tiempo", y="señal", kind="line")
    plt.plot(pt, p, 'mo', label="picos")
    plt.title("ECG. Frecuencia = " + str(frec) + " latidos por minuto.")
    plt.xlabel("s")
    plt.ylabel("eV")
    plt.legend()
    if secg == "Y":
        plt.savefig('./{}.png'.format(name))
    plt.show()
    


# Obtención de valores e inicialización del programa
ecg, sex, age = userInput()
peaks, peak_times = getHeartbeats(ecg)
frec = getFrec(peaks, ecg['tiempo'].iloc[-1])
state = getState(frec, sex, age)
saveState(frec, sex, age, state)
saveEcg(ecg, peaks, peak_times, frec)



