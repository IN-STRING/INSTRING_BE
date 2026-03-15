import psycopg2

local = psycopg2.connect("postgresql://postgres:12qweras!@localhost:5432/Instring")
docker = psycopg2.connect("postgresql://postgres:12qweras!@localhost:5434/Instring")

tables = ['gstring', 'guitar', 'level', 'category', 'song', '"user"', 'userrecord', 'songcategorylink',
          'songuserclickedlink']

for table in tables:
    with local.cursor() as src, docker.cursor() as dst:
        clean_table = table.strip('"')

        # 로컬 DB에서 컬럼 가져오기 (search_vector 제외)
        src.execute(f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = '{clean_table}' 
            AND is_generated = 'NEVER'
            ORDER BY ordinal_position
        """)
        cols = [row[0] for row in src.fetchall()]
        col_str = ', '.join(cols)
        placeholders = ', '.join(['%s'] * len(cols))

        src.execute(f"SELECT {col_str} FROM {table}")
        rows = src.fetchall()
        if not rows:
            print(f"{table}: 데이터 없음")
            continue

        dst.executemany(f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING", rows)
        docker.commit()
        print(f"{table}: {len(rows)}건 완료")

local.close()
docker.close()