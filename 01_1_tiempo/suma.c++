/*  Laboratorio_1: Kevin Vaca
    NRC: 36885

    Desarrolle una simulación de arquitectura SIMD
    (Multiples Intrucciones Multiples Datos)
    bajo las siguientes caracteristicas:
    - Vector A: 24 elementos.
    - Vector B: 24 elementos.
    - Vector C: 24 elementos.
    OPERACIONES: Suma, Resta & Multiplicación.
    - Registrar los tiempos de respuesta.
    - Verificar cual es la operacion aritmetica que más se tarda.
    - Seis hilos con 4 valores                                  */

#include <iostream>
#include <chrono>
#include <thread>

void sumar(int A[], int B[], int C[], int inicio) {
    for (int i = inicio; i < inicio + 4; i++) {
        C[i] = A[i] + B[i];
    }
}

int main () {
    int A[24] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400};
    int B[24] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    int C[24];
    
    auto empezar = std::chrono::high_resolution_clock::now();

    std::thread s1(sumar, A, B, C, 0);
    std::thread s2(sumar, A, B, C, 4);
    std::thread s3(sumar, A, B, C, 8);
    std::thread s4(sumar, A, B, C, 12);
    std::thread s5(sumar, A, B, C, 16);
    std::thread s6(sumar, A, B, C, 20);
  
    s1.join();
    s2.join();
    s3.join();
    s4.join();
    s5.join();
    s6.join();

    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> tiempo_suma = terminar - empezar;

    std::cout << "Operación de Suma +" << std::endl;

    for (int i = 0; i < 6; i++) {
        std::cout << "  Hilo " <<i + 1<< ": ";
        //Valores de las Posiciones
        std::cout << C[i * 4] << " " << C[i * 4 + 1]
        << " " << C[i * 4 + 2] << " " << C[i * 4 + 3]
        << std::endl;
    }

    std::cout<<"Tiempo Total: " <<tiempo_suma.count() << " microsegundos." <<std::endl;
    
    return 0;
}