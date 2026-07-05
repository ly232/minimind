'''DDL to transform minimind jsonl files into duckdb.'''

import duckdb


def create_table(table_name, conn):
    sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} AS (
            SELECT
                row_number() OVER () AS id,
                *
            FROM read_json_auto(
                'dataset/minimind_dataset/{table_name}.jsonl',
                sample_size=100000,
                union_by_name=true)
        );
    '''
    conn.execute(sql)


def main():
    conn = duckdb.connect('minimind_dataset.duckdb')

    create_table('pretrain_t2t_mini', conn)
    create_table('sft_t2t_mini', conn)


if __name__ == '__main__':
    main()
