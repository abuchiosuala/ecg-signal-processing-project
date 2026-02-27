#include <fstream>
#include <iostream>
#include "loadData.h"

int main() {
    std::ifstream inputFile("../scripts/ecg_filtered.csv");
    auto [timeData, signalData] = storeData(inputFile);
    std::cout << timeData.size() << " " <<  signalData.size() << '\n';
    inputFile.close();
}