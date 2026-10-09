import matplotlib.pyplot as plt

operaciones = [
    "Suma",
    "Resta",
    "Multiplicación"
]

tiempos = [262.705, 338.041, 353.642]

#Atributos de la clase plt

plt.figure(figsize=(10,6))

barras = plt.bar(
    operaciones,
    tiempos,
    color = ["yellow", "blue", "red"]   
)

# Valores sobre Barras
for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.005,
        f"{altura:.3f} µs",
        ha="center",
        fontsize=9
    )

#Títulos
plt.title(
    "Comparación de Tiempos de Ejecución",
    fontsize=15
)

plt.xlabel("Operaciones SIMD")
plt.ylabel("Tiempo de Ejecución (Microsegundos)")

#Cuadrícula
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.ylim(0, max(tiempos) * 1.25)

plt.tight_layout()
plt.show()