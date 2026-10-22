#include <iostream>
#include <chrono>
#include <thread>
#include <cmath>
#include <vector>

#include <fstream>
#include <sstream>
#include <iomanip>


struct Paciente {
    int id;
    int edad;
    std::string sexo;
    double peso;
    double altura;
    double cintura;
    double cadera;
};

int main () {
    //1. ARCHIVO
    std::ifstream archivo ("/mnt/garage/code/paralela/03_mimd/datos_mimd.csv");
     if (!archivo.is_open()) {
        std::cout<<"Error: No se puede abrir datos_mind.csv" << std::endl;
        return 1;
    }
    //2. VECTORES
    std::vector <Paciente> paciente;

    //3. SALTAR ENCABEZADO
    std::string linea;
    getline (archivo, linea);
    
    //4. WHILE para llenar VECTOR
    while(getline(archivo, linea)) {
        if (linea.empty()) {
            continue;
        }
        std::stringstream ss (linea);

        //5. Disección & Conversión
        std::string datoId;
        std::string datoEdad;
        std::string datoSexo;
        std::string datoPeso;
        std::string datoAltura;
        std::string datoCintura;
        std::string datoCadera;

        getline(ss,datoId, ',');
        getline(ss,datoEdad, ',');
        getline(ss,datoSexo, ',');
        getline(ss,datoPeso, ',');
        getline(ss,datoAltura, ',');
        getline(ss,datoCintura, ',');
        getline(ss,datoCadera, ',');

        Paciente p;

        p.id = stoi(datoId);
        p.edad = stoi(datoEdad);
        p.sexo = datoSexo;
        p.peso = stod(datoPeso);
        p.altura = stod(datoAltura);
        p.cintura = stod(datoCintura);
        p.cadera = stod(datoCadera);
        paciente.push_back(p);
    }
    //6. Chao Archivo
    archivo.close();

    std::cout<<"Dataset cargado correctamente."<<std::endl;
    std::cout<<"Total de pacientes: "<< paciente.size() << std::endl;

    int total = static_cast<int>(paciente.size());
    if (total != 300) {
        std::cout<<"ERROR no se cargo los elementos del DATASET" << std::endl;
        return 1;
    }

    std::vector <double> resultados(total, 0.0);
    std::vector <std::string> indicadores(total);
    
    int inicio1 = 0;
    int fin1 = 100;

    int inicio2 = 100;
    int fin2 = 200;

    int inicio3 = 200;
    int fin3 = 300;

    //5. Hilos LAMBDA & Logica (MEDIR TIEMPO)

    auto inicio = std::chrono::high_resolution_clock::now();
    //6. HILOS & LOGICA
    std::thread h1([&]() {
        for(int i = inicio1; i < fin1; i++) {
            double peso = paciente[i].peso;
            double altura = paciente[i].altura;
            resultados[i] = peso / (altura*altura);
            indicadores[i] = "IMC";
        }
    });

    std::thread h2([&]() {
        for (int i = inicio2; i < fin2; i++) {
            double cintura = paciente[i].cintura;
            double cadera = paciente[i].cadera;
            resultados[i] = cintura / cadera;
            indicadores[i] = "ICC";
        }
    });
    
    std::thread h3([&]() {
        for (int i = inicio3; i < fin3; i++) {
            double alturaCm = paciente[i].altura*100;
            double peso = paciente[i].peso;
            resultados[i] = std::sqrt(
                (alturaCm * peso) / 3600
            );
            indicadores[i] = "BSA";
        }
    });

    h1.join();
    h2.join();
    h3.join();

    auto fin = std::chrono::high_resolution_clock::now();

    std::chrono::duration <double, std::micro> tiempo_total = fin - inicio;

    std::cout << std::fixed << std::setprecision(4);

    std::cout<< "RESULTADOS: "<< std::endl;
    for (int i = 0; i < total; i++) {
        std::cout<<"PACIENTE Nro."<<paciente[i].id<<",";
        std::cout<<"'Edad'::"<<paciente[i].edad<<",";
        std::cout<<"'Sexo':"<<paciente[i].sexo<<",";
        std::cout<<"'Peso':"<<paciente[i].peso<<",";
        std::cout<<"'Altura':"<<paciente[i].altura<<",";
        std::cout<<"'Cintura'"<<paciente[i].cintura<<",";
        std::cout<<"'Cadera':"<<paciente[i].cadera<<std::endl;
        std::cout<<indicadores[i]<<" => "<<resultados[i]<<std::endl;
    }
    std::cout<<"Tiempo de Ejecución Total: "<<tiempo_total.count()<<" microsegundos."<<std::endl;
}