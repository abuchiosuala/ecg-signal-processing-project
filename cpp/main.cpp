#include <fstream>
#include <iostream>
#include "loadData.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./a.out <path to ECG CSV file>\n";
    }
    try {
        std::ifstream inputFile(argv[1]);
        if(!inputFile.is_open()) {
            throw std::runtime_error("Could not open file");
        }
        auto [timeData, signalData] = storeData(inputFile);
        std::cout << timeData.size() << " " << signalData.size() << '\n';
    }
    catch(const std::exception& e) {
        std::cerr << e.what() << "\n";
    }
}