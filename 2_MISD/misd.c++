#include <thread>
#include <chrono>
#include <iostream>

void mostrar (float operación[], int num_elementos) {
    for (int i = 0; i < num_elementos; i++) {
        std::cout<< operación[i] <<" ";
    }
    std::cout<<"\n";
}

int main () {
    float A[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    float B[8] = {10, 20, 30, 40, 50, 60, 70, 80};
    //Por separado
    float suma[8];
    float resta[8];
    float producto[8];
    float division[8];
    //inicio de tiempo
    auto empezar = std::chrono::high_resolution_clock::now();
    
    //suma
    std::thread h1([&]() {
        //usa las MISMAS variables no las copia
        for (int i = 0; i < 8; i++) {
            suma[i] = A[i] + B[i];
        }
    }
    );

    //resta
    std::thread h2([&]() {
        for (int j = 0; j < 8; j++)
        {
            resta[j] = B[j] - A[j];
        }
    }
    );

    std::thread h3([&]() {
        for (int q = 0; q < 8; q++)
        {
            producto[q] = A[q] * B[q];
        }
    }
    );

    
    std::thread h4([&]() {
        for (int k = 0; k < 8; k++)
        {
            division[k] = A[k] / B[k];
        }
    }
    );

    h1.join();
    h2.join();
    h3.join();
    h4.join();

    auto terminar = std::chrono::high_resolution_clock::now();

    std::chrono::duration <double, std::micro> tiempo_total = terminar - empezar;

    std::cout<<"Hilo 1 (Suma): ";
    mostrar(suma, 8);
    std::cout<<"Hilo 2 (Resta): ";
    mostrar(resta, 8);
    std::cout<<"Hilo 3 (Producto): ";
    mostrar(producto, 8);
    std::cout<<"Hilo 4 (División): ";
    mostrar(division, 8);

    std::cout<<"Tiempo de Ejecución: "<<tiempo_total.count()<<" microsegundos."<<std::endl;
    
    return 0;
}