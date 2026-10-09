/*  Conversion Paralela de Unidades de Volumen
    Se requiere realizar una conversión bajo las sigueintes condiciones:
    Hilo 1: Galones a Litros
        1 Galon = 3.785412 Litros

    Hilo 2: Litros a Mililitros
        1 Litro = 1000 Mililitros

    Hilo 3: Litros a Centilitros
        1 Litro = 100 Centilitros

    Hilo 4: Litros a Metros Cúbicos
        1 Litro = 0.001 Metros Cúbicos

    Hilo 5: Litros a Galones
        1 Litro = 0,264172 Galones

    Hilo 6: Litros a Onzas Líquidas
        1 Litro = 33.814 Onzas Líquidas

    Caractersticas del vector, debe tener l capacidad de almacena 16 elementos en su volumen de datos.
*/

#include <iostream>
#include <thread>
#include <chrono>

int main () {
    float A[16] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    float galon_a_litro[16];
    float litro_a_mililitro[16];
    float litro_a_centilitro[16];
    float litro_a_metroCubico[16];
    float litro_a_galones[16];
    float litro_a_onzaLiquida[16];


    // Tiempo
    auto empezar = std::chrono::high_resolution_clock::now();

    std::thread h1 ([&](){
        for (int i = 0; i < 16; i++) {
            galon_a_litro[i] = A[i] * 3.785412;
        }
    });

    std::thread h2 ([&](){
        for (int i = 0; i < 16; i++) {
            litro_a_mililitro[i] = A[i] * 1000;
        }
    });

    std::thread h3 ([&](){
        for (int i = 0; i < 16; i++) {
            litro_a_centilitro[i] = A[1] * 100;
        }
    });

    std::thread h4 ([&] () {
        for (int i = 0; i < 16; i++) {
            litro_a_metroCubico[i] = A[1] * 0.001;
        }
    });

    std::thread h5 ([&]() {
        for (int i = 0; i < 16; i++) {
            litro_a_galones[i] = A[1] * 0.264172;
        }
    });

    std::thread h6 ([&]() {
        for (int i = 0; i < 16; i++) {
            litro_a_onzaLiquida[i] = A[1] * 33.814;
        }
    });

    h1.join();
    h2.join();
    h3.join();
    h4.join();
    h5.join();
    h6.join();

    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration <double, std::micro> tiempo_de_ejecucion = terminar - empezar;

    for (int i = 0; i < 16; i++) {
        std::cout<<"Posición "<< i + 1 <<". Valor = "<<A[i]<<": "<<std::endl;
        std::cout<<"H1. Galones a Litros: "<<galon_a_litro[i]<<std::endl; 
        std::cout<<"H2. Litro a Mililitros: "<<litro_a_mililitro [i]<<std::endl; 
        std::cout<<"H3. Litro a Centilitro: "<<litro_a_centilitro[i]<<std::endl; 
        std::cout<<"H4. Litro a Metro Cubico: "<<litro_a_metroCubico[i]<<std::endl; 
        std::cout<<"H5. Litro a Galones: "<<litro_a_galones[i]<<std::endl; 
        std::cout<<"H6. Litro a Onza Liquida: "<<litro_a_onzaLiquida[i]<<std::endl<<std::endl; 
    }

    std::cout<< "Tiempo de Ejecución: "<<tiempo_de_ejecucion.count();
}
