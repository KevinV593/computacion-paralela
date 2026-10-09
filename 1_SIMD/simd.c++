/*  Vectores de 8 elemntos
    Tres vectores
    A = [1, 2, 3, 4, 5, 6, 7, 8]
    B = A
    C = A + B
    Hilos & Subprocesos
    Cada hilo toma dos elementos de A (1, 2) y B (10, 20)   */

#include <iostream>
#include <chrono>
#include <thread>

void sumar(int A[], int B[], int C[], int inicio) {
    for (int i = inicio; i < inicio + 2; i++) {
        C[i] = A[i] + B[i];
    }
}

int main() {
    int A[8] = {1,2,3,4,5,6,7,8};
    int B[8] = {10,20,30,40,50,60,70,80};
    int C[8];

    auto empezar = std::chrono::high_resolution_clock::now();
    std::thread h1(sumar, A, B, C, 0);
    std::thread h2(sumar, A, B, C, 2);
    std::thread h3(sumar, A, B, C, 4);
    std::thread h4(sumar, A, B, C, 6);

    //Ejectuar desde el hilo
    h1.join();
    h2.join();
    h3.join();
    h4.join();

    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> tiempo = terminar - empezar;

    for (int j = 0; j < 4; j++) {
        std::cout << "Hilo " << j + 1 << ": ";

        //Posiciones
        std::cout << "("<< C[j * 2] << ", "
        << C[j * 2 + 1] << ")" <<std::endl;
    }

    //Tiempo

    std::cout << "Tiempo Total: " << tiempo.count() << " microsegundos" << std::endl;

    return 0;
}