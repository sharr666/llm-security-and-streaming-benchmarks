// Author: Mehrdad Poorhassan (ORCID: 0009-0004-9269-3912)
// Constant-Memory O(1) High-Throughput Compressed Corpus Generator (C++ -O3 + zlib)
#include <iostream>
#include <fstream>
#include <string>
#include <zlib.h>
#include <filesystem>

namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    std::string output_dir = (argc > 1) ? argv[1] : "./prompts_200b_compressed_6gb";
    fs::create_directories(output_dir);
    long long max_records = (argc > 2) ? std::stoll(argv[2]) : 1000000LL;
    long long target_compressed_size = 6LL * 1024 * 1024 * 1024;
    int part_num = 1;
    long long current_id = 1;

    while (current_id <= max_records) {
        std::string file_path = output_dir + "/part_" + std::to_string(part_num) + ".csv.gz";
        gzFile gz_out = gzopen(file_path.c_str(), "wb6");
        if (!gz_out) return 1;
        std::string header = "id,category,prompt_text,expected_complexity\n";
        gzwrite(gz_out, header.c_str(), header.size());
        long long rows_in_file = 0;
        while (current_id <= max_records) {
            std::string buffer;
            buffer.reserve(10000 * 110);
            for (int i = 0; i < 10000 && current_id <= max_records; ++i) {
                buffer += std::to_string(current_id) + ",AI_Systems,Evaluate structural consistency for node " + std::to_string(current_id) + ",High\n";
                current_id++;
                rows_in_file++;
            }
            gzwrite(gz_out, buffer.c_str(), buffer.size());
            if (rows_in_file % 500000 == 0) {
                gzflush(gz_out, Z_SYNC_FLUSH);
                if (fs::exists(file_path) && fs::file_size(file_path) >= static_cast<uintmax_t>(target_compressed_size)) break;
            }
        }
        gzclose(gz_out);
        part_num++;
    }
    return 0;
}
