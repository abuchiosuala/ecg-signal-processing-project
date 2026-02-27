#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "loadData.h"

// function stod allows me to convert string to doubles
// the initial getline function throws out my header line
std::pair<std::vector<double>, std::vector<double>> storeData(std::ifstream& file) {
    std::vector<double> timeData;
    std::vector<double> signalData;
    std::string line;

    if(!file.is_open()) {
        std::cerr << "File does not exist\n";
        return {{}, {}};
    }
    std::getline(file, line); // skip header
    std::cout<<"Loading data from file\n";
    while(std::getline(file, line)) {
        std::stringstream ss(line);
        std::string timeStr, signalStr;
        if (std::getline(ss, timeStr, ',') && std::getline(ss, signalStr)) {
            double index = std::stod(timeStr);
            double time = index / 360.0; // Getting the time using the Hz
            double signal = std::stod(signalStr);
            timeData.push_back(time);
            signalData.push_back(signal);
        }
    }
    if (timeData.size() == signalData.size()) {
        std::cout << "Data Loaded\n";
    }
    return {timeData, signalData};
}
