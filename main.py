import requests
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def wget(url):
    r = requests.get(url, allow_redirects=True)
    with open(url[url.rfind('/') + 1::], 'wb') as f:
        f.write(r.content)

wget("https://raw.githubusercontent.com/IEEESBITBA/Curso-Python/master/Clase_4_datos/electrocardiograma.xlsx")


data = pd.read_excel("electrocardiograma.xlsx") 
indexPeaks = find_peaks(data['señal'])[0]
dataPeaks = pd.DataFrame(data, index=indexPeaks)




data.plot(x="tiempo", y="señal", kind="line")
dataPeaks.plot(x="tiempo", y="señal", marker="o")
plt.show()
