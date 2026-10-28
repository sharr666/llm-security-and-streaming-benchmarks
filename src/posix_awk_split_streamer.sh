#!/usr/bin/env bash
# Author: Mehrdad Poorhassan (ORCID: 0009-0004-9269-3912)
# Zero-Python POSIX awk + GNU split Constant-Memory Streamer (666MB shards)
set -euo pipefail
OUTPUT_DIR="${1:-./prompts_200b_666mb_parts}"
TOTAL_ROWS="${2:-1000000}"
mkdir -p "$OUTPUT_DIR"
awk -v max="$TOTAL_ROWS" 'BEGIN {
    for(i=1; i<=max; i++) {
        printf "%d,Science_Tech,Analyze structural integrity of system node %d under load.,High\n", i, i
    }
}' | split -C 666m -d -a 5 --additional-suffix=.csv - "$OUTPUT_DIR/part_"
