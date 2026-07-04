'''A simple main to demonstrate jsonl -> proto parser.

Example usage:

  # pretrain_t2t_mini.jsonl
  uv run dataset/datamodel/parser_demo.py \
    --filename=dataset/minimind_dataset/pretrain_t2t_mini.jsonl \
    --num_lines=10 \
    --schema_type=pretrain

  # sft_t2t_mini.jsonl
  uv run dataset/datamodel/parser_demo.py \
    --filename=dataset/minimind_dataset/sft_t2t_mini.jsonl \
    --num_lines=10 \
    --schema_type=sft
'''

import argparse
import logging
import sys
import os

# Manually add root project folder to import path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dataset.datamodel import json_to_pb_parser

def main():
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument("--filename", type=str)
    parser.add_argument("--num_lines", type=int, default=float('inf'))
    parser.add_argument(
        "--schema_type",
        type=json_to_pb_parser.SchemaType,
        choices=list(json_to_pb_parser.SchemaType),
        default=json_to_pb_parser.SchemaType.SUPERVISED_FINE_TUNING_SCHEMA,
        help="Execution mode, e.g. sft or pretrain."
    )
    args = parser.parse_args()

    parser = json_to_pb_parser.JsonToProtoParser(
        filename=args.filename,
        schema_type=args.schema_type,
        num_lines=args.num_lines,
    )

    samples_pb2 = parser.parse()
    print(samples_pb2)

if __name__ == '__main__':
    main()
