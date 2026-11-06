"""
Author: Mehrdad Poorhassan (ORCID: 0009-0004-9269-3912)
Description: Python script for generating Parquet (Snappy) shards using pyarrow.
"""

import os
import pyarrow as pa
import pyarrow.parquet as pq


def generate_parquet_shards(output_dir="shards", num_shards=5, rows_per_shard=1000):
    """Generate Snappy-compressed Parquet shards; memory scales with one full shard."""
    if not isinstance(output_dir, (str, os.PathLike)) or not os.fspath(output_dir):
        raise ValueError("output_dir must be a non-empty path")
    if type(num_shards) is not int or num_shards < 0:
        raise ValueError("num_shards must be a non-negative integer")
    if type(rows_per_shard) is not int or rows_per_shard < 0:
        raise ValueError("rows_per_shard must be a non-negative integer")
    os.makedirs(output_dir, exist_ok=True)

    schema = pa.schema([
        ('id', pa.int64()),
        ('text', pa.string()),
        ('score', pa.float64())
    ])

    for shard_idx in range(num_shards):
        ids = list(range(shard_idx * rows_per_shard, (shard_idx + 1) * rows_per_shard))
        texts = [f"Sample document content for row {i}" for i in ids]
        scores = [float(i % 100) / 100.0 for i in ids]

        table = pa.Table.from_arrays([ids, texts, scores], schema=schema)
        file_path = os.path.join(output_dir, f"shard_{shard_idx:04d}.parquet")

        pq.write_table(table, file_path, compression='SNAPPY')
        print(f"Generated {file_path} with {len(table)} rows.")


if __name__ == "__main__":
    generate_parquet_shards()
