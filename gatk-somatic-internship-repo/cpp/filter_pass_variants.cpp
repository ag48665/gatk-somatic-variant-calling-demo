#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: filter_pass_variants input.vcf output.pass.vcf\n";
        return 1;
    }
    std::ifstream in(argv[1]);
    std::ofstream out(argv[2]);
    if (!in || !out) {
        std::cerr << "Error: could not open input or output file.\n";
        return 1;
    }
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        if (line[0] == '#') { out << line << '\n'; continue; }
        std::stringstream ss(line);
        std::string field, filter;
        int column = 0;
        while (std::getline(ss, field, '\t')) {
            ++column;
            if (column == 7) { filter = field; break; }
        }
        if (filter == "PASS") out << line << '\n';
    }
    return 0;
}
