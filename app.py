import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página e Título Profissional
st.set_page_config(
    page_title="Validador MSE - Gestão de Contratos",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Cabeçalho Corporativo com Logo e Título Alinhados via HTML/CSS
# Usando o link público da logo MSE para garantir o carregamento
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0; border-bottom: 2px solid #b22222; margin-bottom: 30px;">
        <img src="https://raw.githubusercontent.com/arianisouza-creator/validador-nf/main/logo-mse.png" width="120">
        <div>
            <h1 style="margin: 0; color: #333; font-family: 'Helvetica Neue', sans-serif; font-size: 32px;">
                Validador Inteligente de Notas Fiscais
            </h1>
            <h2 style="margin: 0; color: #b22222; font-family: 'Helvetica Neue', sans-serif; font-size: 20px; font-weight: normal;">
                Gestão de Contratos MSE
            </h2>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. Configuração de Segurança da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Chave de API não configurada nos 'Secrets' do Streamlit.")

# 4. Área Principal e Sidebar
st.markdown("### 📥 Upload do Documento")
st.write("Arraste ou selecione o PDF da Nota Fiscal de Serviço (NFS-e) para iniciar a auditoria fiscal automática.")

# Campo de upload centralizado e moderno
uploaded_file = st.file_uploader("", type=["pdf"], help="Apenas arquivos PDF são suportados.")

if uploaded_file is not None:
    # Mostra um status visual de processamento
    status_container = st.empty()
    status_container.info("⏳ Iniciando análise fiscal profunda... Por favor, aguarde.")
    
    with st.spinner("Decodificando dados e aplicando regras de Contratos MSE..."):
        try:
            bytes_data = uploaded_file.read()
            pdf_part = {"mime_type": "application/pdf", "data": bytes_data}
            
            # PROMPT ESTRUTURADO PARA O PADRÃO EXECUTIVO MSE (Baseado nos prints de sucesso)
            prompt_mse = """
            Você é um Auditor Fiscal Sênior especializado em Contratos da MSE Engenharia. Analise este PDF de NFS-e e formate sua resposta *exatamente* seguindo esta estrutura corporativa em Markdown:

            # 📋 Relatório de Auditoria Fiscal Automatizada

            ---

            ### 1. QUADRO DE RESUMO EXECUTIVO
            Crie uma tabela Markdown rigorosa com as colunas: | Item de Validação | Status (✅ OK / ⚠️ ALERTA / ❌ ERRO) | Observação Curta e Direta |
            Itens a validar (use exatamente estes nomes): 
            1. Dados do Tomador (CNPJ/Endereço)
            2. Local da Prestação vs Faturamento
            3. Enquadramento do Código de Tributação
            4. Conferência do ISS Retido
            5. Conferência do INSS Retido
            6. Valor Total (Equação do Líquido: Bruto - Retenções Federais - ISS - INSS)

            ---

            ### 2. ANÁLISE TÉCNICA DETALHADA
            Discorra profissionalmente sobre a análise, justificando *cada* ALERTA ou ERRO encontrado com base na legislação (LC 116/2003) e nas melhores práticas de conformidade fiscal. Se houver divergência matemática, apresente o cálculo correto. Use um tom executivo, sem termos coloquiais.
            """
            
            # Chamada ao modelo mais estável e rápido
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            response = model.generate_content([pdf_part, prompt_mse])
            
            # Atualiza o status e exibe o resultado
            status_container.success("✅ Análise Finalizada com Sucesso!")
            st.markdown(response.text)
            
        except Exception as e:
            status_container.error(f"❌ Erro técnico no processamento do arquivo: {e}")

# 5. Rodapé Profissional na Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 Gestão de Contratos MSE")
st.sidebar.info(
    "Este portal utiliza inteligência artificial avançada para automatizar a conferência fiscal de Notas Fiscais de Serviço, garantindo conformidade e eficiência."
)
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True) # Espaçador
st.sidebar.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px;">
        Desenvolvido internamente para a MSE Engenharia<br>
        v1.0 Corporate Edition
    </div>
""", unsafe_allow_html=True)
