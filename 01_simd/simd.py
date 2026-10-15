import matplotlib.pyplot as plt

# Operaciones SIMD
operaciones = [
    "Suma",
    "Resta",
    "Multiplicación",
    "División"
]

# Tiempos de ejemplo en microsegundos
# REEMPLAZAR con los tiempos medidos en C++
tiempos = [0.25, 0.31, 0.28, 0.42]

# Crear gráfico
plt.figure(figsize=(10, 6))

barras = plt.bar(
    operaciones,
    tiempos,
    color=["blue", "green", "orange", "red"]
)

# Mostrar valores sobre las barras
for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.005,
        f"{altura:.3f} µs",
        ha="center",
        fontsize=11
    )

# Títulos
plt.title(
    "Comparación de tiempos de ejecución SIMD - AVX",
    fontsize=15
)

plt.xlabel("Operaciones SIMD")
plt.ylabel("Tiempo de ejecución (microsegundos)")

# Cuadrícula
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.ylim(0, max(tiempos) * 1.25)

plt.tight_layout()
plt.show()