import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração da Página
st.set_page_config(
    page_title="MSE - Validador Fiscal Inteligente",
    page_icon="🧾",
    layout="wide"
)

# Estilização para as cores da MSE (Vermelho e Cinza Corporativo)
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        .stButton>button { background-color: #cc0000; color: white; border-radius: 5px; }
        .status-ok { color: #15803d; font-weight: bold; }
        .status-alert { color: #b91c1c; font-weight: bold; }
        div[data-testid="stMetricValue"] { color: #cc0000; }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho com a Logo MSE
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Substitua pelo caminho da imagem se estiver na mesma pasta do GitHub, 
    # ou use a URL direta que você me enviou.
    st.image("https://r2.community.elementor.com/wp-content/uploads/2024/11/mse-logo.png", width=150)

with col_title:
    st.title("Portal de Auditoria Fiscal Digital")
    st.caption("Tecnologia MSE para Compliance e Validação de NFS-e")

st.divider()

# 3. Configuração da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave API não encontrada. Adicione GEMINI_API_KEY nos Secrets do GitHub/Streamlit.")
    st.stop()

# 4. Upload do Arquivo
uploaded_file = st.file_uploader("Arraste o PDF da Nota Fiscal aqui", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analisando conformidade fiscal..."):
        try:
            bytes_data = uploaded_file.read()
            pdf_part = {"mime_type": "application/pdf", "data": bytes_data}
            
            # PROMPT com foco em JSON para gerar o quadro de resumo
            prompt = """
            Analise esta NFS-e conforme a LC 116/2003 e as melhores práticas de auditoria.
            Você deve responder estritamente em formato JSON para que eu possa montar um dashboard.
            
            Estrutura do JSON:
            {
                "resumo": [
                    {"item": "Dados do Tomador", "status": "OK" ou "ALERTA", "detalhe": "CNPJ/Endereço presente?"},
                    {"item": "Retenção de ISS", "status": "OK" ou "ALERTA", "detalhe": "Local de prestação vs faturamento"},
                    {"item": "Alíquota aplicada", "status": "OK" ou "ALERTA", "detalhe": "Cálculo 2% a 5%"},
                    {"item": "Cálculo Matemático", "status": "OK" ou "ALERTA", "detalhe": "Valor Bruto - Retenções = Líquido"}
                ],
                "analise_detalhada": "Texto completo em markdown explicando cada ponto de inconformidade encontrado.",
                "valor_total": "R$ Valor",
                "cnpj_identificado": "00.000... "
            }
            """
            
            model = genai.GenerativeModel(model_name="gemini-1.5-flash") # ou gemini-2.0-flash
            response = model.generate_content(
                [pdf_part, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            
            dados = json.loads(response.text)

            # --- PARTE 1: QUADRO DE RESUMO (O que você pediu) ---
            st.subheader("📊 Quadro de Resumo de Auditoria")
            
            # Criando colunas para métricas rápidas
            m1, m2, m3 = st.columns(3)
            m1.metric("Valor Identificado", dados["valor_total"])
            m2.metric("CNPJ Tomador", dados["cnpj_identificado"])
            m3.metric("Status Geral", "CONFORME" if all(x['status'] == 'OK' for x in dados['resumo']) else "ALERTA")

            # Tabela de Status
            def format_status(status):
                return "✅ OK" if status == "OK" else "⚠️ ALERTA"

            # Transformando o resumo do JSON em uma tabela visual
            tabela_resumo = []
            for item in dados["resumo"]:
                tabela_resumo.append({
                    "Item de Verificação": item["item"],
                    "Status": format_status(item["status"]),
                    "Observação": item["detalhe"]
                })
            
            st.table(tabela_resumo)

            # --- PARTE 2: DESCRIÇÕES DETALHADAS ---
            st.divider()
            st.subheader("🔍 Parecer Detalhado")
            with st.expander("Clique para ver os detalhes técnicos da análise", expanded=True):
                st.markdown(dados["analise_detalhada"])

            st.success("Auditoria concluída com sucesso!")

        except Exception as e:
            st.error(f"Erro ao processar PDF: {e}")

# Footer
st.markdown("---")
st.caption("© 2024 MSE - Inteligência em Auditoria Fiscal.")
