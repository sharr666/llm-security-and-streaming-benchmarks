// Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
// Bounded-memory C++ (-O3 + zlib) streaming shard generator with explicit I/O error checking
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <zlib.h>

int main(int argc, char** argv) {
    const long max_records = (argc > 1) ? std::atol(argv[1]) : 100000L;
    const char* out_path = (argc > 2) ? argv[2] : "/tmp/shard_00001.csv.gz";

    gzFile gz = gzopen(out_path, "wb6");
    if (!gz) {
        std::fprintf(stderr, "ERROR: Failed to open gzip stream: %s\n", out_path);
        return EXIT_FAILURE;
    }
    gzbuffer(gz, 65536);

    const char* header = "id,category,trust_tier,prompt_text\n";
    if (gzwrite(gz, header, static_cast<unsigned>(std::strlen(header))) <= 0) {
        std::fprintf(stderr, "ERROR: Failed writing CSV header\n");
        gzclose(gz);
        return EXIT_FAILURE;
    }

    char row_buf[256];
    for (long i = 1; i <= max_records; ++i) {
        int len = std::snprintf(
            row_buf, sizeof(row_buf),
            "%ld,LLM_Security,Level_30_Untrusted,Evaluate isolation boundary for node %ld\n", i, i
        );
        if (len <= 0 || gzwrite(gz, row_buf, static_cast<unsigned>(len)) != len) {
            std::fprintf(stderr, "ERROR: gzwrite failed at record %ld\n", i);
            gzclose(gz);
            return EXIT_FAILURE;
        }
    }

    int close_status = gzclose(gz);
    if (close_status != Z_OK) {
        std::fprintf(stderr, "ERROR: gzclose returned non-zero status: %d\n", close_status);
        return EXIT_FAILURE;
    }
    std::printf("{\"records_written\": %ld, \"status\": \"OK\"}\n", max_records);
    return EXIT_SUCCESS;
}
