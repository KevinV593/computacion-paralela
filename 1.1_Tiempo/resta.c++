#include<iostream>
#include<chrono>
#include<thread>

void restar(int A[], int B[], int C[], int inicio) {
    for (int i = inicio; i < inicio + 4; i++) {
        C[i] = A[i] - B[i];
    }
}

int main () {
    int A[24] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400};
    int B[24] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    int C[24];

    auto empezar = std::chrono::high_resolution_clock::now();

    std::thread r1(restar, A, B, C, 0);
    std::thread r2(restar, A, B, C, 4);
    std::thread r3(restar, A, B, C, 8);
    std::thread r4(restar, A, B, C, 12);
    std::thread r5(restar, A, B, C, 16);
    std::thread r6(restar, A, B, C, 20);

    r1.join();
    r2.join();
    r3.join();
    r4.join();
    r5.join();
    r6.join();

    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> tiempo_resta = terminar - empezar;

    std::cout<<"Operación de Resta -"<<std::endl;

    for (int j = 0; j < 6; j++) {
        std::cout << "  Hilo " << j + 1 << ": "
        <<C[j * 4] <<" "
        <<C[j * 4 + 1] <<" "
        <<C[j * 4 + 2] <<" "
        <<C[j * 4 + 3] <<" "<<std::endl;
    }

    std::cout << "Tiempo Total: "<< tiempo_resta.count() << " microsegundos." <<std::endl;
    return 0;
}