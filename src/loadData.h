#pragma once
#include <fstream>
#include <vector>
#include <utility>

std::pair<std::vector<double>, std::vector<double>> storeData(std::ifstream& file);