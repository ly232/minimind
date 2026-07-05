# Duckdb integration

## Introduction

This module ingests minimind dataset's jsonl raw unstructured data into structured RDBMS through duckdb. It leverages duckdb's [`read_json_auto`](https://duckdb.org/docs/lts/guides/file_formats/json_import) TVF to materialize jsonl data into relational form. See `ddl.py` for details.

## Examples

One-time execution to create table from jsonl:

```
uv run dataset/duckdb/ddl.py
```

Explore data with duckdb cli:

```
duckdb minimind_dataset.duckdb

minimind_dataset D .tables
────────────────────────────────── minimind_dataset ────────────────────────────────── 
──────────────────────────────────────── main ──────────────────────────────────────── 
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                     sft_t2t_mini                                     │
│                                                                                      │
│ id            bigint                                                                 │
│ conversations struct("role" varchar, "content" varchar, reasoning_content varchar)[] │
│                                                                                      │
│                                     905718 rows                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

minimind_dataset D SELECT
                       id,
                       conversation.unnest.role,
                       conversation.unnest.content,
                       conversation.unnest.reasoning_content,
                   FROM sft_t2t_mini, unnest(conversations) as conversation
                   LIMIT 5;
┌───────┬───────────┬────────────────────────────────────────┬───────────────────────────────────────┐
│  id   │   role    │                content                 │           reasoning_content           │
│ int64 │  varchar  │                varchar                 │                varchar                │
├───────┼───────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│     1 │ user      │ 你背后的模型是哪个版本？它由谁开发？   │ NULL                                  │
├───────┼───────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│     1 │ assistant │ 我是由jingyaogong开发的高效小参数AI模  │ NULL                                  │
│       │           │ 型。                                   │                                       │
├───────┼───────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│     1 │ user      │ 你模型的训练数据来源是什么？           │ NULL                                  │
├───────┼───────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│     1 │ assistant │ 我的训练数据涵盖多领域，确保覆盖广泛， │ 好的，用户问我的模型训练数据来源。首  │
│       │           │ 但具体细节不公开。                     │ 先，我需要确认用户的问题是否涉及隐私  │
│       │           │                                        │ 或敏感信息。根据之前的规则，不能透露  │
│       │           │                                        │ 具体的训练数据来源，但可以提到数据的  │
│       │           │                                        │ 多样性。\n\n接下来，我要确保回答符合  │
│       │           │                                        │ 系统的限制，不能在思考中透露身份信息  │
│       │           │                                        │ 。需要保持简洁，不超过100字。同时，要 │
│       │           │                                        │ 准确回答问题，但不涉及具体数据来源。… │
├───────┼───────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│     1 │ user      │ 训练数据的来源和多样性如何？           │ NULL                                  │
└───────┴───────────┴────────────────────────────────────────┴───────────────────────────────────────┘
minimind_dataset D 
```
