#include <iostream>
#include <thread>
#include <chrono>
#include <cmath>

#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>

#include <semaphore>
#include <mutex>

std::counting_semaphore<2> semaforo(2);
std::mutex consola;

struct Paciente {
    int id;
    double peso;
    double altura;
    double cintura;
    double cadera;
};

void calcularIMC(const std::vector<Paciente>& datos) {
    semaforo.acquire();

    std::ostringstream salida;
    salida << std::fixed << std::setprecision(2);
    salida << "\nHILO 1 ingreso: IMC\n";

    for (int i = 0; i < 2; i++) {
        double imc = datos[i].peso /
        (datos[i].altura * datos[i].altura);
        salida << "Paciente " << datos[i].id
        << ": IMC ==> " << imc << "\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(2));
    salida << "HILO 1 Finalizo";
    {
        std::lock_guard<std::mutex> bloqueo(consola);
        std::cout<<salida.str();
    }
    semaforo.release();
}

void calcularICC(const std::vector<Paciente>& datos) {
    semaforo.acquire();

    std::ostringstream salida;
    salida << std::fixed << std::setprecision(2);
    salida << "\nHILO 2 ingreso: ICC\n";

    for (int i = 2; i < 4; i++) {
        double icc = datos[i].cintura /
        (datos[i].cadera);
        salida << "Paciente " << datos[i].id
        << ": ICC ==> " << icc << "\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(2));
    salida << "HILO 2 Finalizo";
    {
        std::lock_guard<std::mutex> bloqueo(consola);
        std::cout<<salida.str();
    }
    semaforo.release();
}

void calcularBSA(const std::vector<Paciente>& datos) {
    semaforo.acquire();

    std::ostringstream salida;
    salida << std::fixed << std::setprecision(2);
    salida << "\nHILO 3 ingreso: BSA\n";

    for (int i = 4; i < 6; i++) {
        double bsa = std::sqrt((datos[i].altura * 100 * datos[i].peso
        / 3600));
        salida << "Paciente " << datos[i].id
        << ": BSA ==> " << bsa << "\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(2));
    salida << "HILO 3 Finalizo";
    {
        std::lock_guard<std::mutex> bloqueo(consola);
        std::cout<<salida.str();
    }
    semaforo.release();
}

void calcularDiferencia(const std::vector<Paciente>& datos) {
    semaforo.acquire();

    std::ostringstream salida;
    salida << std::fixed << std::setprecision(2);
    salida << "\nHILO 4 ingreso: Diferencia\n";

    for (int i = 6; i < 8; i++) {
        double diferencia = datos[i].cintura -
        (datos[i].cadera);
        salida << "Paciente " << datos[i].id
        << ": Diferencia ==> " <<diferencia << "\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(2));
    salida << "HILO 4 Finalizo";
    {
        std::lock_guard<std::mutex> bloqueo(consola);
        std::cout<<salida.str();
    }
    semaforo.release();
}

int main () {
    std::ifstream archivo("pacientes.csv");
     if (!archivo.is_open()) {
        std::cout<<"Error: No se puede abrir pacientes.csv" << std::endl;
        return 1;
    }

    std::vector <Paciente> paciente;
    std::string linea;
    std::getline(archivo, linea);

    while (std::getline(archivo, linea) && datos.size() < 8) {
        std::stringstream ss (linea);
        std::string campo;
        Paciente p;
        std::getline(ss, campo, ',');
        p.id = std::stoi(campo);
        
        std::getline(ss, campo, ',');
        std::getline(ss, campo, ',');
        
        std::getline(ss, campo, ',');
        p.peso = std::stod(campo);

        std::getline(ss, campo, ',');
        p.altura = std::stod(campo);

        std::getline(ss, campo, ',');
        p.cintura = std::stod(campo);

        std::getline(ss, campo, ',');
        p.cadera = std::stod(campo);
        
        datos.push_back(p);
    }
    archivo.close();

    if(datos.size() < 8) {
        std::cout << "Se necesitan ocho pacientes\n";
        return 1;
    }

    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::thread h1(calcularIMC, std::cref(datos));
    std::thread h2(calcularICC, std::cref(datos));
    std::thread h3(calcularBSA, std::cref(datos));
    std::thread h4(calcularDiferencia, std::cref(datos));

    h1.join();
    h2.join();
    h3.join();
    h4.join();

    auto fin = std::chrono::high_resolution_clock::now();

    std::chrono::duration <double, std::micro> tiempo_total = fin - inicio;

    std::cout << std::fixed << std::setprecision(4);

    std::cout<<"Tiempo de Ejecución Total: "<<tiempo_total.count()<<" microsegundos."<<std::endl;
    return 0;
}
