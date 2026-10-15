# Arquitectura MIMD

La cantidad de Hilos y su distribución dependen del diseño de la simulación y de la cantidad de tareas (procesos), más no del número de datos.

### Instrucción:
Realizar en C++, una programa que realize los siguientes calculos, mediante los datos del dataset 'datos_mind.csv' en los hilos correspondientes:

#### Hilo 1: Índice de Masa Corporal (IMC)
Fórmula:    Peso[kg] / Altura[m2]
Rango:      1 a 100
#### Hilo 2: Índice Cintura-Cadera (ICC)
Fórmula:    Cintura[cm] / Cadera[cm]
Rango:      101 a 200
#### Hilo 3: Superficie Corporal (BSA)
Fórmula: sqrt(Altura[cm] * Peso[kg] / 3600)
Rango:      201 a 300