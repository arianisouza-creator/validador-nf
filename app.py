import streamlit as st
import google.generativeai as genai

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Validador MSE", page_icon="🧾", layout="wide")

# CSS Customizado para visual Corporativo (Correção aplicada aqui)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #b22222; color: white; border-radius: 5px; width: 100%; }
    h1 { color: #333; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Cabeçalho com Logo e Título
col1, col2 = st.columns([1, 4])
with col1:
    # URL da logo da MSE
    st.image("https://cdn.discordapp.com/attachments/1110300624388145223/1212818967837114368/mse_logo.png", width=150)
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
