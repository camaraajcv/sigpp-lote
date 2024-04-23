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
            # Formata a coluna 'CPF' como número inteiro de 11 dígitos
            df['CPF'] = df['CPF'].astype(str).str.zfill(11)
            # Formata a coluna 'RUBRICA' como número inteiro de 6 dígitos
            df['RUBRICA'] = df['RUBRICA'].astype(str).str.zfill(6)
        else:
            st.error("Erro: O arquivo Excel deve ter exatamente 4 colunas.")

        # Exibindo os dados do arquivo Excel
        st.write("Dados do arquivo Excel:")
        st.write(df)

        # Formulário para informações adicionais
        st.header("Informações Adicionais")

        col1, col2 = st.columns(2)
        with col1:
            tipo_operacao = st.selectbox("Tipo de Operação", ["I - Inclusão", "A - Alteração", "E - Exclusão", "F - Finalização"])

            inicio_direito = st.text_input("Início do Direito (AAAAMM)", max_chars=6)

            fim_direito = st.text_input("Data Final do Direito (AAAAMM)", max_chars=6)

        with col2:
            num_parcelas = st.text_input("Número de Parcelas (dois dígitos)", max_chars=2)

            valor_coluna = st.selectbox("O Valor da Planilha é um:", ["Índice", "Valor"])

            documento = st.text_input("Documento (15 dígitos)", max_chars=15)

        # Gerar arquivo .txt
        if st.button("Gerar Arquivo .txt"):
            generate_txt_file(tipo_operacao, inicio_direito, fim_direito, num_parcelas, valor_coluna, documento, df)


def generate_txt_file(tipo_operacao, inicio_direito, fim_direito, num_parcelas, valor_coluna, documento, df):
    # Verifica se o campo de Data Final do Direito está vazio
    if fim_direito == "":
        fim_direito = " " * 6

    # Verifica se o campo de Número de Parcelas está vazio
    if num_parcelas == "":
        num_parcelas = " " * 2

    # Determina os valores dos campos de índice e valor do lançamento com base na seleção do usuário
    if valor_coluna == "Índice":
        # Formatando para 4 casas decimais e convertendo para string
        valor_formatado = '{:.4f}'.format(float(df["VALOR"]))

        # Removendo o ponto e completando com zeros à esquerda
        valor_indice = valor_formatado.replace('.', '').zfill(10)
        valor_lancamento = " " * 9  # Campo de valor do lançamento fica vazio
    else:  # Se valor_coluna for "Valor"
        valor_lancamento = '{:09.2f}'.format(float(df["VALOR"])).replace('.', '').zfill(9)  # Formata com 2 casas decimais sem vírgula e preenche com zeros à esquerda
        valor_indice = " " * 10  # Campo de valor do índice fica vazio

    # Formatação dos campos
    tipo_operacao = tipo_operacao.split(" ")[0]  # Pegar apenas a primeira letra do tipo de operação
    inicio_direito = inicio_direito.zfill(6)
    fim_direito = fim_direito.zfill(6)
    documento = documento.strip()  # Remove espaços em branco do documento

    # Criar o conteúdo do arquivo .txt
    txt_content = f"{tipo_operacao}1010{inicio_direito}{fim_direito}{df['Saram_vinculo'].iloc[0]}{df['CPF'].iloc[0]}{df['RUBRICA'].iloc[0]}01{num_parcelas}{valor_indice}{valor_lancamento}{documento}\n"

    # Escrever o conteúdo no arquivo
    with open("dados.txt", "w") as txt_file:
        txt_file.write(txt_content)
        st.success(valor_indice)
    # Botão de download
    download_button = st.download_button(
        label="Clique para baixar o arquivo .txt",
        data=open("dados.txt", "rb"),
        file_name="dados.txt",
        mime="text/plain"
    )

    if download_button:
        
        st.success("Arquivo .txt gerado e baixado com sucesso!")

if __name__ == "__main__":
    main()







