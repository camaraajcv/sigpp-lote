import streamlit as st
import pandas as pd

def main():
    st.title("App de Processamento de Dados")

    # Upload do arquivo Excel na página principal
    uploaded_file = st.file_uploader("Faça upload do arquivo Excel", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Lendo o arquivo Excel sem cabeçalhos de coluna
        df = pd.read_excel(uploaded_file, header=None)

        # Verifica se o DataFrame possui exatamente 4 colunas
        if len(df.columns) == 4:
            # Renomeia as colunas
            df.columns = ['Saram_vinculo', 'CPF', 'RUBRICA', 'VALOR']

            # Formata a coluna 'Saram_vinculo' como número inteiro de 10 dígitos
            df['Saram_vinculo'] = df['Saram_vinculo'].astype(str).str.zfill(10)
        else:
            st.error("Erro: O arquivo Excel deve ter exatamente 4 colunas.")

        # Exibindo os dados do arquivo Excel
        st.write("Dados do arquivo Excel:")
        st.write(df)

        # Processamento dos dados
        process_data(df)


def process_data(df):
    # Adicione aqui a lógica para processar os dados do arquivo Excel
    # Aqui você pode combinar os dados do Excel com os dados do formulário
    # e gerar o arquivo .txt conforme necessário
    # Por enquanto, vamos apenas mostrar uma mensagem de exemplo
    st.write("Aqui você pode adicionar a lógica para processar os dados e gerar o arquivo .txt")


if __name__ == "__main__":
    main()

