import numpy as np
import sympy as sp
import math as mt

# Definición de símbolos
th2, th3 = sp.symbols("th2, th3")
w2, w3 = sp.symbols("w2, w3")
a2, a3 = sp.symbols("a2, a3")

# Valores conocidos
w1 = int(input("Introduce el valor para w1: "))
r1 = int(input("Introduce el valor para r1: "))
r2 = int(input("Introduce el valor para r2: "))
r3 = int(input("Introduce el valor para r3: "))
r4 = int(input("Introduce el valor para r4: "))
th4 = 0
a1 = (0, 0)
th1 = 0

# Archivo de salida
file_path = "resultados.txt"
file = open(file_path, "w")

for th1_val in range(361):
    x = r1 * np.cos(mt.radians(th1)) + r2 * sp.cos(th2) + r3 * sp.cos(th3) - r4 * np.cos(mt.radians(th4))
    y = r1 * np.sin(mt.radians(th1)) + r2 * sp.sin(th2) + r3 * sp.sin(th3) - r4 * np.sin(mt.radians(th4))

    # Resolución del sistema de ecuaciones
    A_sol = sp.solve((x, y), (th2, th3))

    # Verificar si se encontraron soluciones
    if len(A_sol) > 0:
        # Obtención de las soluciones en grados
        A_sol_d = [[mt.degrees(sol) for sol in A_sol[0]], [mt.degrees(sol) for sol in A_sol[1]]]

        # Calcular los valores correspondientes de th2 y th3
        th2_val = A_sol_d[1][0]
        th3_val = 180 + A_sol_d[1][1]

        # Calcular los valores correspondientes de Vr1, Vr2, Vr3, Va, Vb1 y Vb2
        Vr1 = r1 * np.cos(mt.radians(th1_val)), r1 * np.sin(mt.radians(th1_val))
        Vr2 = r2 * np.cos(mt.radians(th2_val)), r2 * np.sin(mt.radians(th2_val))
        Vr3 = r3 * np.cos(mt.radians(th3_val)), r3 * np.sin(mt.radians(th3_val))

        # Analisis para W2 y W3
        Va = (w1 * Vr1[0], -w1 * Vr1[1])
        Vb1 = (w2 * Vr2[0], -w2 * Vr2[1], Va)
        Vb2 = (w3 * Vr3[0], (-w3) * Vr3[1])

        # Matriz
        Vb11 = np.array([[Vr2[0], Vr3[0]], [Vr2[1], Vr3[1]]])
        vb22 = np.array([Va[0], Va[1]])
        vb12 = np.linalg.solve(Vb11, vb22)
        w2_val = vb12[0]
        w3_val = vb12[1]

        ###########################
        # Aceleracion en los puntos a y b
        a_1 = (w1 * w1) * (-1 * Vr1[0]), ((w1 * w1) * (-1 * Vr1[1]))
        z = -1
        a_1_1 = (z * (w2_val ** 2) * (Vr2[0]) + (w2_val ** 2) * (Vr2[1])), (z * (w3_val ** 2) * (Vr3[0]) + (w3_val ** 2) * (Vr3[1]))
        a_1_2 = (Vr2[0]), (z * (Vr2[1]))
        a_1_3 = (Vr3[0]), (z * (Vr3[1]))

        # Matriz
        Ab11 = np.array([[a_1_2[0], a_1_3[0]], [a_1_2[1], a_1_3[1]]])
        Ab22 = np.array([a_1_1[0], a_1_1[1]])
        Ab12 = np.linalg.solve(Ab11, Ab22)
        A2_val = Ab12[0]
        A3_val = Ab12[1]

        # Escribir en el archivo
        file.write("Ángulo de entrada de la barra 1: " + str(th1_val) + "\n")
        file.write("Posición de salida de las conexiones b y c: " + str(A_sol_d) + "\n")
        file.write("Posición de la barra 2 (Theta 2): " + str(th2_val) + "\n")
        file.write("Posición de la barra 3 (Theta 3): " + str(th3_val) + "\n")
        file.write("Velocidad angular de la barra 2 (w2): " + str(w2_val) + "\n")
        file.write("Velocidad angular de la barra 3 (w3): " + str(w3_val) + "\n")
        file.write("Aceleración de los puntos de conexión b: " + str(Va) + "\n")
        file.write("Aceleración angular de la barra 2: " + str(A2_val) + "\n")
        file.write("Aceleración angular de la barra 3: " + str(A3_val) + "\n")
        file.write("\n")
    else:
        # No se encontraron soluciones
        file.write("No se encontraron soluciones para el ángulo de entrada de la barra 1: " + str(th1_val) + "\n")
        file.write("\n")

# Cerrar el archivo
file.close()