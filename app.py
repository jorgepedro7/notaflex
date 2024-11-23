import streamlit as st
from utils.xml_processing import process_xml_batch
import pandas as pd
import io

# Configuações do app
st.set_page_config(
    page_title='NotaFlex',
    page_icon='📄',
)
st.header("Nota Flex - Cálculo de ICMS em Lote")
st.subheader("Adicione seus arquivos .XML ao lado")

# Upload de múltiplos arquivos
st.sidebar.title("Upload de Arquivos 📄")
files = st.sidebar.file_uploader("Selecione arquivos XML", type=["xml"], accept_multiple_files=True)

# Processar arquivos em lote
if files and st.sidebar.button("Processar Notas Fiscais"):
    resultados = []  # Lista para armazenar os DataFrames válidos
    for file in files:
        # Processar apenas XMLs
        resultado = process_xml_batch(file)
        if isinstance(resultado, pd.DataFrame):
            resultados.append(resultado)
        else:
            st.error(f"Erro ao processar {file.name}: {resultado.get('Erro', 'Erro desconhecido.')}")

    # Consolidar resultados em um único DataFrame
    if resultados:
        df_consolidado = pd.concat(resultados, ignore_index=True)
        st.write("Resultados Consolidados:")
        st.dataframe(df_consolidado, use_container_width=True)

        # Botão para download do Excel consolidado
        buffer = io.BytesIO()
        df_consolidado.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="Baixar Resultado em Excel",
            data=buffer,
            file_name="resultado_calculos_lote.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
