#include <iostream>
#include <thread>
#include <chrono>
//Nuevas
#include <fstream>  //archivo
#include <sstream>  //stringstream
#include <vector>   //vector
#include <iomanip>  //fixed & setprecision
int main () {
    std::ifstream archivo("/mnt/garage/code/paralela/2.2_Dataset/datos.csv");
    

    if (!archivo.is_open()) {
        std::cout<<"Error: No se puede abrir datos.csv" << std::endl;
        return 1;
    }

    //vectores
    std::vector<int> id;
    std::vector<double> litros;

    std::string linea;

    getline(archivo, linea); //Saltar Encabezado
    
    while (getline(archivo, linea)) {
        std::stringstream ss(linea);
        std::string datoId;
        std::string datoLitro;
        getline(ss, datoId, ',');
        getline(ss, datoLitro, ',');

        //Conversión
        id.push_back(stoi(datoId));
        litros.push_back(stod(datoLitro));
    }
    archivo.close();
    std::cout<<"Dataset cargado correctamente."<<std::endl;
    std::cout<<"Numero de Registros: " << litros.size() << std::endl;

    //Converrsion
    std::vector<double> mililitros(litros.size());
    std::vector<double> centilitros(litros.size());
    std::vector<double> metrosCubicos(litros.size());
    std::vector<double> galones(litros.size());
    std::vector<double> onzas(litros.size());
    std::vector<double> centimetrosCubicos(litros.size());

    auto empezar = std::chrono::high_resolution_clock::now();

    std::thread h1 ([&]() {
        for (int i = 0; i < litros.size(); i++) {
            mililitros[i] = litros[i] * 1000;
        }
    }
    );

    std::thread h2 ([&]() {
        for (int i = 0; i < litros.size(); i++) {
            centilitros[i] = litros[i] * 100;
        }
    }
    );

    std::thread h3 ([&]() {
        for (int i = 0;i<litros.size(); i++) {
            metrosCubicos[i] = litros[i] / 1000;
        }
    }
    );
/*
    std::thread h4 ([&]() {
        for (int i = 0; i < litros.size(); i++) {

        }
    }
*/

    h1.join();
    h2.join();
    h3.join();


    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration <double, std::micro> tiempo_total = terminar - empezar;
    
    std::cout << std::fixed << std::setprecision(4);

    for (int i = 0; i < litros.size(); i++) {
        std::cout<<"-------------------------"<<std::endl;
        std::cout<<"Registro: " << id[i] <<"\t\t" << "Litros: "<<litros[i]<<std::endl;
        std::cout<<"H1 (Mililitros) ==>\t" << mililitros[i]<<" ML"<<std::endl;
        std::cout<<"H2 (Centilitro) ==>\t" << centilitros[i]<<" CL"<<std::endl;
        std::cout<<"H3 (Metros Cubicos) ==>\t" << metrosCubicos[i]<<" m3"<<std::endl;
    }
    std::cout<<"-------------------------"<<std::endl;
    std::cout<<"Registros Totales: " << id.size() <<"\t" <<std::endl;
    std::cout << "Tiempo de Procesamiento: "<< tiempo_total.count() << " microsegundos" <<std::endl;
}