#pragma once
#include <fstream>
#include <vector>
#include <utility>

/**
 * Loads ECG data from a CSV file.
 * Returns a pair of vectors containing time and signal data which will be used for peak detection.
 */
std::pair<std::vector<double>, std::vector<double>> storeData(std::ifstream& file);