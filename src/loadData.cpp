#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

std::pair<std::vector<double>, std::vector<double>> storeData(std::ifstream& file) {
    std::vector<double> timeData;
    std::vector<double> signalData;
    std::string line;

    if(!file.is_open()) {
        std::cerr << "File does not exist\n";
        return {{}, {}};
    }

    std::cout<<"Loading data from file\n";
    while(std::getline(file, line)) {
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
    return {timeData, signalData};
}

int main() {
    std::ifstream inputFile("../ecgData/data.csv");
    auto [timeData, signalData] = storeData(inputFile);
    std::cout << timeData.size() << signalData.size();
    inputFile.close();

}