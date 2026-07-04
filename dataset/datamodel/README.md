# Minimind dataset data model

## JSON to Protobuf parser

This package is a companion of [minimind-dataset](https://www.modelscope.cn/datasets/gongjy/minimind_dataset/files). It examines the `.jsonl` structure to infer schema, declare such schema in `protobuf`, and implements a data processing tool to translate `.jsonl` into a structured datastore with `protobuf` serving as the schema.

In particular, `schema.proto` defines the inferred schema. Python proto APIs are generated under generated/ directory, by running:

```python
python -m grpc_tools.protoc -I. \
    --python_out=./generated \
    ./dataset/datamodel/schema.proto
```
