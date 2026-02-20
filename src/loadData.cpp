#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

int main() {
    std::vector<double> timeData;
    std::vector<double> signalData;

    std::ifstream inputFile("../ecgData/data.csv");
    std::string line;

    if(!inputFile.is_open()) {
        std::cerr << "Error opening file\n";
        return 1;
    }

    std::cout << "Reading in file\n";
    while(std::getline(inputFile, line)) {
        std::stringstream ss(line);
        std::string timeStr, signalStr;

        if (std::getline(ss, timeStr, ',') && std::getline(ss, signalStr)) {
            double time = std::stod(timeStr);
            double signal = std::stod(signalStr);
            timeData.push_back(time);
            signalData.push_back(signal);
        }
    }
    if (timeData.size() == signalData.size()) {
        std::cout << "Data Loaded\n";
    }
    inputFile.close();

}