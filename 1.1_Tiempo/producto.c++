#include <iostream>
#include <chrono>
#include <thread>

void multiplicar (int A[], int B[], int C[], int inicio) {
    for (int i = inicio; i < inicio + 4; i++) {
        C[i] = A[i] * B [i];
    }
}

int main () {
    int A[24] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400};
    int B[24] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    int C[24];

    auto empezar = std::chrono::high_resolution_clock::now();

    std::thread m1(multiplicar, A, B, C, 0);
    std::thread m2(multiplicar, A, B, C, 4);
    std::thread m3(multiplicar, A, B, C, 8);
    std::thread m4(multiplicar, A, B, C, 12);
    std::thread m5(multiplicar, A, B, C, 16);
    std::thread m6(multiplicar, A, B, C, 20);
   
    m1.join();
    m2.join();
    m3.join();
    m4.join();
    m5.join();
    m6.join();

    auto terminar = std::chrono::high_resolution_clock::now();

    std::cout<<"Operación de Multiplicación *"<< std::endl;

    for (int j = 0; j < 6; j++) {
        std::cout<<"  Hilo " << j + 1 <<": "
        << C[j * 4 + 0] << " "
        << C[j * 4 + 1] << " "
        << C[j * 4 + 2] << " "
        << C[j * 4 + 3] << " "
        << std::endl;
    }

    std::chrono::duration<double, std::micro> tiempo_producto = terminar - empezar;
    std::cout << "Tiempo Total: " << tiempo_producto.count()<<" microsegundos. " << std::endl;

    return 0;
}