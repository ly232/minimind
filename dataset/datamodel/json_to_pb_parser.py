'''Translation classes that maps json to pb.

Example usage:

    parser = JsonToProtoParser(
        filename,
        SchemaType.SUPERVISED_FINE_TUNING_SCHEMA,
    )
    samples_pb = sft_parser.parse()
'''

from google.protobuf.message import Message
from typing import Any

import enum
import logging
import json
import sys
import os

# Manually add root project folder to import path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from generated.dataset.datamodel import schema_pb2


class SchemaType(enum.Enum):
    '''Enumerates list of supported schema types.
    
    See dataset/minimind_dataset/*.jsonl for underlying data.
    '''
    SUPERVISED_FINE_TUNING_SCHEMA = "sft"
    PRETRAIN_SCHEMA = "pretrain"


class SupervisedFineTuningSampleParser:
    '''Parser for SFT samples.'''

    def __init__(self):
        pass

    def parse(self, jsons) -> list[Message]:
        '''Parses minimind SFT json samples into protos.'''
        samples_pb = []
        sample_pb = schema_pb2.SupervisedFineTuningSample()
        for sample_json in jsons:
            try:
                conversations_json = sample_json['conversations']
                for conversation_json in conversations_json:
                    conversation_pb = schema_pb2.SupervisedFineTuningSample.Conversation()
                    # print(type(conversation_json))
                    conversation_pb.role = conversation_json['role']
                    conversation_pb.content = conversation_json['content']
                    if 'reasoning_content' in conversation_json:
                        conversation_pb.reasoning_content = conversation_json['reasoning_content']
                    sample_pb.converstaions.append(conversation_pb)
            except KeyError as e:
                # Log an error but do not abort.
                logging.error(f'Missing key in json: {sample_json}; exception: {e}')
        samples_pb.append(sample_pb)

        return samples_pb


class PretrainSampleParser:
    '''Parser for pretrain samples.'''

    def __init__(self):
        pass

    def parse(self, jsons) -> list[Message]:
        '''Parses minimind pretrain json samples into protos.'''
        samples_pb = []
        sample_pb = schema_pb2.PretrainSample()
        for sample_json in jsons:
            sample_pb.text = sample_json['text']
        samples_pb.append(sample_pb)
        return samples_pb


class JsonToProtoParser:
    '''Facade parser that delegates to type-specific parsers.
    
    Attributes:
    - filename (str): path to jsonl file.
    - schema_type (enum): schema type of jsonl file.
    - num_lines (int): number of lines to read from jsonl file.
    '''

    def __init__(self, filename: str, schema_type: SchemaType, num_lines: int = 10):
        # Extract jsonl into raw arrays.
        self.jsons = []
        with open(filename, 'r') as f:
            while len(self.jsons) < num_lines:
                self.jsons.append(json.loads(f.readline()))

        self.schema_type = schema_type
        self.sft_parser = SupervisedFineTuningSampleParser()
        self.pt_parser = PretrainSampleParser()
        
    def parse(self) -> list[Message]:
        '''Routes to type specific parser to parse.'''
        if self.schema_type == SchemaType.SUPERVISED_FINE_TUNING_SCHEMA:
            return self.sft_parser.parse(self.jsons)
        elif self.schema_type == SchemaType.PRETRAIN_SCHEMA:
            return self.pt_parser.parse(self.jsons)
        else:
            raise ValueError(f'Unsupported schema type: {self.schema_type}')
