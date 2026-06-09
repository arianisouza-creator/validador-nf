import streamlit as st
import google.generativeai as genai
import base64

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Validador MSE", page_icon="🧾", layout="wide")

# CSS Customizado para visual Corporativo
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #b22222; color: white; border-radius: 5px; width: 100%; }
    h1 { color: #333; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Cabeçalho com Logo Convertida em Código e Título
col1, col2 = st.columns([1, 4])
with col1:
    # Sua logo MSE convertida em string de texto puro (Base64) para evitar erros de leitura de arquivo
    logo_base64 = "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"
    
    # Exibe a logo a partir do código direto
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" width="150">', unsafe_allow_html=True)
with col2:
    st.title("Validador Inteligente de Notas Fiscais - Contratos MSE")

st.markdown("---")

# 3. Configuração da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API não configurada nos Secrets.")

# 4. Upload do Arquivo
st.sidebar.header("Configurações")
uploaded_file = st.file_uploader("Arraste aqui o PDF da Nota Fiscal", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analisando Nota Fiscal sob as regras de Contratos MSE..."):
        try:
            bytes_data = uploaded_file.read()
            pdf_part = {"mime_type": "application/pdf", "data": bytes_data}
            
            # PROMPT ESTRUTURADO PARA O PADRÃO MSE
            prompt_mse = """
            Você é um Auditor Fiscal Sênior da MSE. Analise este PDF e siga este formato rigoroso de resposta:

            ### 1. QUADRO DE RESUMO EXECUTIVO
            Crie uma tabela Markdown com as colunas: | Item de Validação | Status (✅ OK / ⚠️ ALERTA / ❌ ERRO) | Observação Curta |
            Itens a validar: Dados do Tomador, Local da Prestação vs Faturamento, Código de Tributação, Cálculo ISS, Cálculo INSS, Valor Total (Equação do Líquido).

            ### 2. ANÁLISE DETALHADA (DISCORRER)
            Abaixo da tabela, escreva uma análise técnica detalhada discorrendo sobre:
            - Conformidade com a LC 116/2003.
            - Justificativa detalhada de cada alerta ou erro encontrado.
            - Conferência matemática exata dos impostos retidos.
            - Recomendação final para o setor de contratos.

            Use um tom profissional, corporativo e direto.
            """
            
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            response = model.generate_content([pdf_part, prompt_mse])
            
            # EXIBIÇÃO DOS RESULTADOS
            st.success("Análise Finalizada com Sucesso!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Erro técnico no processamento: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para Gestão de Contratos MSE.")
