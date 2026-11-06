// Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
// Incremental CSV-to-gzip shard generator using zlib.
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <zlib.h>

int main(int argc, char** argv) {
    if (argc > 3) {
        std::fprintf(stderr, "Usage: %s [record_count>=0] [output_path]\n", argv[0]);
        return EXIT_FAILURE;
    }

    long max_records = 100000L;
    if (argc > 1) {
        errno = 0;
        char* end = nullptr;
        const long parsed = std::strtol(argv[1], &end, 10);
        if (errno == ERANGE || end == argv[1] || *end != '\\0' || parsed < 0) {
            std::fprintf(stderr, "ERROR: record_count must be a non-negative integer\n");
            return EXIT_FAILURE;
        }
        max_records = parsed;
    }

    const char* out_path = (argc > 2) ? argv[2] : "/tmp/shard_00001.csv.gz";
    gzFile gz = gzopen(out_path, "wb6");
    if (!gz) {
        std::fprintf(stderr, "ERROR: Failed to open gzip stream: %s\n", out_path);
        return EXIT_FAILURE;
    }
    if (gzbuffer(gz, 65536) != 0) {
        std::fprintf(stderr, "ERROR: Failed to configure gzip buffer\n");
        gzclose(gz);
        return EXIT_FAILURE;
    }

    const char* header = "id,category,trust_tier,prompt_text\n";
    const unsigned header_size = static_cast<unsigned>(std::strlen(header));
    if (gzwrite(gz, header, header_size) != static_cast<int>(header_size)) {
        std::fprintf(stderr, "ERROR: Failed writing CSV header\n");
        gzclose(gz);
        return EXIT_FAILURE;
    }

    char row_buf[256];
    for (long offset = 0; offset < max_records; ++offset) {
        const long record_id = offset + 1;
        const int len = std::snprintf(
            row_buf, sizeof(row_buf),
            "%ld,LLM_Security,Level_30_Untrusted,Evaluate isolation boundary for node %ld\\n",
            record_id, record_id
        );
        if (len <= 0 || static_cast<std::size_t>(len) >= sizeof(row_buf)
                || gzwrite(gz, row_buf, static_cast<unsigned>(len)) != len) {
            std::fprintf(stderr, "ERROR: gzwrite failed at record %ld\n", record_id);
            gzclose(gz);
            return EXIT_FAILURE;
        }
    }

    const int close_status = gzclose(gz);
    if (close_status != Z_OK) {
        std::fprintf(stderr, "ERROR: gzclose returned non-zero status: %d\n", close_status);
        return EXIT_FAILURE;
    }
    std::printf("{\"records_written\": %ld, \"status\": \"OK\"}\n", max_records);
    return EXIT_SUCCESS;
}
