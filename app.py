import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página e Layout Expandido
st.set_page_config(
    page_title="Validador MSE - Gestão de Contratos",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Barra Lateral (Sidebar) - Identidade Visual Garantida
st.sidebar.markdown("### 🏢 Identidade Corporativa")
try:
    # Método nativo do Streamlit apontando para o arquivo que está na raiz do seu GitHub
    st.sidebar.image("logo mse.png", use_container_width=True)
except:
    # Fallback caso ocorra qualquer variação no nome do arquivo
    st.sidebar.subheader("MSE ENGENHARIA")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Escopo do Validador")
st.sidebar.info(
    "Este portal utiliza inteligência artificial avançada para automatizar a conferência fiscal de Notas Fiscais de Serviço, garantindo conformidade com a LC 116/2003 e eficiência no setor de Contratos."
)

# 3. Cabeçalho da Área Principal (Texto Puro de Alto Contraste)
st.title("Validador Inteligente de Notas Fiscais")
st.subheader("Contratos e Gestão Documental — MSE")
st.markdown("---")

# 4. Configuração de Segurança da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Chave de API não configurada nos 'Secrets' do Streamlit.")

# 5. Área de Upload Central
st.markdown("### 📥 Upload do Documento")
st.write("Arraste ou selecione o PDF da Nota Fiscal de Serviço (NFS-e) para iniciar a auditoria fiscal automática.")

uploaded_file = st.file_uploader("", type=["pdf"], help="Apenas arquivos PDF são suportados.")

if uploaded_file is not None:
    status_container = st.empty()
    status_container.info("⏳ Iniciando análise fiscal profunda... Por favor, aguarde.")
    
    with st.spinner("Decodificando dados e aplicando regras de Contratos MSE..."):
        try:
            bytes_data = uploaded_file.read()
            pdf_part = {"mime_type": "application/pdf", "data": bytes_data}
            
            # PROMPT EXECUTIVO DE ALTO PADRÃO (Garante títulos limpos e tabelas organizadas)
            prompt_mse = """
            Você é um Auditor Fiscal Sênior especializado em Contratos da MSE Engenharia. Analise este PDF de NFS-e e formate sua resposta exatamente seguindo esta estrutura corporativa em Markdown:

            # 📋 Relatório de Auditoria Fiscal Automatizada

            ---

            ### 1. QUADRO DE RESUMO EXECUTIVO
            Crie uma tabela Markdown rigorosa com as colunas: | Item de Validação | Status (✅ SUCONFORMIDADE / ⚠️ ALERTA / ❌ ERRO) | Observação Curta e Direta |
            Itens a validar: 
            1. Dados do Tomador (CNPJ/Endereço)
            2. Local da Prestação vs Faturamento
            3. Enquadramento do Código de Tributação
            4. Conferência do ISS Retido
            5. Conferência do INSS Retido
            6. Valor Total (Equação do Líquido: Bruto - Retenções Federais - ISS - INSS)

            ---

            ### 2. ANÁLISE TÉCNICA DETALHADA
            Abaixo da tabela, discorra profissionalmente sobre a análise, justificando cada ALERTA ou ERRO encontrado com base na legislação (LC 116/2003) e nas melhores práticas de conformidade fiscal. Se houver divergência matemática, apresente o cálculo correto. Use um tom executivo, sem termos coloquiais.
            """
            
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            response = model.generate_content([pdf_part, prompt_mse])
            
            status_container.success("✅ Análise Finalizada com Sucesso!")
            st.markdown(response.text)
            
        except Exception as e:
            if "429" in str(e):
                status_container.error("⚠️ Limite de requisições temporário atingido. Por favor, aguarde 30 segundos e tente reenviar o arquivo.")
            else:
                status_container.error(f"❌ Erro técnico no processamento do arquivo: {e}")

# Rodapé da Sidebar
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="text-align: center; color: #888; font-size: 11px; font-family: sans-serif;">
        Desenvolvido para MSE Engenharia<br>
        v1.3 Corporate Edition
    </div>
""", unsafe_allow_html=True)
