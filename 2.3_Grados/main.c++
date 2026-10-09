#include <iostream>
#include <thread>
#include <chrono>

#include <fstream>
#include <sstream>
#include <vector>
#include <iomanip>
int main () {
    //1. archivo
    std::ifstream archivo("/mnt/garage/code/paralela/2.3_Grados/sensores_ambientales_500.csv");

    if (!archivo.is_open()) {
        std::cout<<"Error: No se puede abrir datos.csv" << std::endl;
        return 1;
    }
    //2. getline
    std::vector<int>id;
    std::vector<double>temperatura;
    std::vector<double>humedad;

    std::string linea;

    getline (archivo, linea); //Pasa Lineas

    //3. Vectores & Conversiones

    while (getline(archivo,linea)) {
        std::stringstream sss (linea);

        //Vectores para diseccionar
        std::string datoId;
        std::string datoTemperatura;
        std::string datoHumedad;

        //Diseccion
        getline(sss, datoId, ',');
        getline(sss, datoTemperatura, ',');
        getline(sss, datoHumedad, ',');
        
        //CONVERSION
        id.push_back(stoi(datoId));
        temperatura.push_back(stod(datoTemperatura));
        humedad.push_back(stod(datoHumedad));
    }

    //4. Chao Archivo
    archivo.close();

    //5. Hilos LAMBDA & Logica (MEDIR TIEMPO)

    auto empezar = std::chrono::high_resolution_clock::now();

    std::vector<double> farenheit(temperatura.size());
    std::vector<double> kelvin(temperatura.size());
    std::vector<std::string> nivel_humedad(humedad.size());

    std::thread h1 ([&]() {
        for (int i = 0; i < id.size(); i++) {
            farenheit[i] = (temperatura[i] * (9/5)) + 32;
        }
    });

    std::thread h2 ([&]() {
        for (int i = 0; i < temperatura.size(); i++) {
            kelvin[i] = (temperatura[i] + 273.15);
        }
    });

    std::thread h3 ([&]() {
        for (int i = 0; i < humedad.size(); i++) {
            if (humedad[i] < 40) {
                nivel_humedad[i] = "Bajo";
        } 
        else if (humedad[i] >= 40) {
            nivel_humedad[i] = "Alto";
        }
        }
    }
    );


    h1.join();
    h2.join();
    h3.join();


    auto terminar = std::chrono::high_resolution_clock::now();
    std::chrono::duration <double, std::micro> tiempo_total = terminar - empezar;
    
    std::cout << std::fixed << std::setprecision(4);

    for (int i = 0; i < id.size(); i++) {
        std::cout<<"-------------------------"<<std::endl;
        std::cout<<"Registro: " << id[i] <<"\t" << "Celsius: "<<temperatura[i]<<"\t"<<"Humedad: "<<humedad[i]<<std::endl;
        std::cout<<"H1 (Farenheit) ==>\t\t" << farenheit[i]<<"F"<<std::endl;
        std::cout<<"H2 (Kelvin) ==>\t\t\t" << kelvin[i]<<"K"<<std::endl;
        std::cout<<"H3 (Nivel de Humedad) ==>\t" << nivel_humedad[i]<<std::endl;
    }
    std::cout<<"-------------------------"<<std::endl;
    std::cout<<"Registros Totales: " << id.size() <<"\t" <<std::endl;
    std::cout << "Tiempo de Procesamiento: "<< tiempo_total.count() << " microsegundos" <<std::endl;
}
