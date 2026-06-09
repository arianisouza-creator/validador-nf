import streamlit as st
import google.generativeai as genai
import json
import re

# 1. CONFIGURAÇÃO DA PÁGINA (Tema Amplo e Corporativo)
st.set_page_config(
    page_title="Validador de Notas Fiscais | MSE Engenharia", 
    page_icon="🧾", 
    layout="wide"
)

# 2. ESTILIZAÇÃO CSS (Customização de Cores e Design MSE)
st.markdown("""
    <style>
    /* Estilização do fundo e container principal */
    .stApp {
        background-color: #0E1117;
    }
    /* Estilização dos blocos de métricas (Quadro de Resumo) */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 15px 20px;
    }
    /* Alinhamento do título da métrica */
    div[data-testid="stMetric"] label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.9rem !important;
        font-weight: bold !important;
        color: #8B949E !important;
    }
    /* Cor do valor principal da métrica */
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #F0F6FC !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONFIGURAÇÃO DA API DO GEMINI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API não configurada. Configure a GEMINI_API_KEY nas configurações do Streamlit.")

# 4. CABEÇALHO CORPORATIVO (Logo + Título)
col1, col2 = st.columns([1, 4])
with col1:
    # IMPORTANTE: Garanta que o arquivo 'logo mse.png' esteja na mesma pasta do projeto no GitHub
    try:
        st.image("logo mse.png", width=140)
    except:
        # Fallback caso a imagem não seja encontrada temporariamente
        st.subheader("🔹 MSE")

with col2:
    st.markdown("<h1 style='color: #F0F6FC; margin-top: 10px; font-family: Arial;'>VALIDADOR INTELIGENTE DE NOTAS FISCAIS - CONTRATOS MSE</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: #8B949E;'>Auditoria automatizada de conformidade tributária, retenções e dados cadastrais de NFS-e.</p>", unsafe_allow_html=True)
st.divider()

# 5. ÁREA DE UPLOAD
uploaded_file = st.file_uploader("Arraste e solte o PDF da Nota Fiscal aqui", type=["pdf"])

if uploaded_file is not None:
    st.info("Processando e auditando o documento fiscal... Por favor, aguarde.")
    
    try:
        # Leitura dos bytes do PDF
        bytes_data = uploaded_file.read()
        
        pdf_part = {
            "mime_type": "application/pdf",
            "data": bytes_data
        }
        
        # PROMPT ESTRUTURADO: Força o Gemini a devolver um bloco JSON para o Quadro e o Markdown para o Discurso
        prompt_validacao = """
        Você é um Auditor Fiscal Master especializado em Contratos da MSE Engenharia. Analise esta Nota Fiscal de Serviço Eletrônica (NFS-e) e realize uma validação rigorosa com base na LC 116/2003 e nas regras abaixo:

        1. DADOS DO TOMADOR: Verifique se CNPJ/CPF, Razão Social e endereço do tomador estão presentes e preenchidos.
        2. LOCAL DA PRESTAÇÃO VS FATURAMENTO: Avalie se a cidade onde o serviço foi prestado coincide com a cidade de faturamento ou se a regra de retenção do ISS no local da prestação foi seguida corretamente.
        3. CÓDIGO DE TRIBUTAÇÃO VS SERVIÇO: Verifique se o código de serviço/CNAE/Item da LC 116 é perfeitamente coerente com a descrição dos serviços executados.
        4. IMPOSTOS (ISS E INSS): Calcule matematicamente se as alíquotas e valores de retenção de ISS (entre 2% e 5%) e INSS (11%, se aplicável) estão corretos sobre a base de cálculo.
        5. VALOR TOTAL: Valide a equação básica: Valor Líquido = Valor Bruto - Retenções.

        Você deve OBRIGATORIAMENTE retornar sua resposta dividida exatamente em duas partes usando as tags [QUADRO_RESUMO] e [PARECER_DETALHADO].

        Na parte [QUADRO_RESUMO], devolva APENAS um objeto JSON com o número de itens em cada status. Exemplo:
        {"conforme": 3, "alerta": 1, "inconforme": 1}

        Na parte [PARECER_DETALHADO], discorra detalhadamente em formato Markdown corporativo sobre cada um dos 5 pontos avaliados, explicando as memórias de cálculo, embasamentos legais ou inconsistências encontradas.
        """
        
        # Execução do modelo
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([pdf_part, prompt_validacao])
        texto_resposta = response.text
        
        # 6. PARSER DA RESPOSTA (Separação do Quadro de Resumo e do Discurso)
        try:
            quadro_part = re.search(r"\[QUADRO_RESUMO\](.*?)\[PARECER_DETALHADO\]", texto_resposta, re.DOTALL).group(1).strip()
            parecer_part = texto_resposta.split("[PARECER_DETALHADO]")[1].strip()
            
            # Limpa possíveis formatações de bloco de código que o LLM possa colocar no JSON
            quadro_part = quadro_part.replace("```json", "").replace("```", "").strip()
            dados_quadro = json.loads(quadro_part)
        except:
            # Fallback de segurança caso o LLM mude a estrutura do texto
            dados_quadro = {"conforme": "-", "alerta": "-", "inconforme": "-"}
            parecer_part = texto_resposta

        # 7. EXIBIÇÃO DO QUADRO DE RESUMO (Métricas no Topo)
        st.subheader("📊 Quadro de Resumo de Compliance")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.metric(label="ITENS CONFORMES", value=dados_quadro.get("conforme", 0), delta="OK", delta_color="normal")
        with c2:
            st.metric(label="ALERTAS / AMBIGUIDADES", value=dados_quadro.get("alerta", 0), delta="Atenção", delta_color="off")
        with c3:
            st.metric(label="INCONFORMIDADES CRÍTICAS", value=dados_quadro.get("inconforme", 0), delta="Crítico", delta_color="inverse")
            
        st.divider()
        
        # 8. EXIBIÇÃO DO DISCURSO DETALHADO (Abaixo do Quadro)
        st.subheader("📝 Parecer Técnico do Auditor")
        st.markdown(parecer_part)
        
    except Exception as e:
        st.error(f"Erro crítico ao processar o arquivo: {e}")
