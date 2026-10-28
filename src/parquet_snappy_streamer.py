"""
Author: Mehrdad Poorhassan (ORCID: 0009-0004-9269-3912)
Description: Python script for generating Parquet (Snappy) shards using pyarrow.
"""

import os
import pyarrow as pa
import pyarrow.parquet as pq


def generate_parquet_shards(output_dir="shards", num_shards=5, rows_per_shard=1000):
    """
    Generates Parquet shards compressed with Snappy using PyArrow.
    """
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
