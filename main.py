import os

import pandas as pd

from utils import unzip_file
from api.router import app


if __name__ == "__main__":
    root_path = os.getcwd()
    root_path_files = os.listdir(root_path)
    for file in root_path_files:
        if file.endswith('.zip'):
            full_zip_path = os.path.join(root_path, file)
            unzip_file(
                zip_path=full_zip_path,
                extract_to=root_path,
            )
            break
        elif file == root_path_files[-1]:
            raise FileNotFoundError("File .zip not found")

    df_origin_data: pd.DataFrame = pd.read_csv(
        filepath_or_buffer='origem-dados.csv',
    )
    df_types: pd.DataFrame = pd.read_csv(
        filepath_or_buffer='tipos.csv',
    )
    df_origin_data_critical: pd.DataFrame = df_origin_data[df_origin_data['status'] == 'CRITICO'].sort_values(by='created_at')
    df_origin_data_critical["nome_tipo"] = df_origin_data_critical["tipo"].map(
        df_types.set_index('id')['nome']
    )

    if os.path.exists('insert-dados.sql'):
        os.remove('insert-dados.sql')
    with open('insert-dados.sql', 'w') as f:
        for index, row in df_origin_data_critical.iterrows():
            f.write(
                f"INSERT INTO dados_finais (created_at, product_code, customer_code, status, tipo, nome_tipo) "
                f"VALUES ('{row['created_at']}',{row['product_code']},{row['customer_code']},'{row['status']}',{row['tipo']},'{row['nome_tipo']}');\n"
            )

    query = """
SELECT 
    DATE(created_at) AS date,
    tipo,
    COUNT(*) AS item_count
FROM 
    dados_finais
GROUP BY 
    DATE(created_at), 
    tipo
ORDER BY 
    DATE(created_at), 
    tipo;
    """
    print(query)

    app.run()
