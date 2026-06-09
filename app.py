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

# 2. ESTILIZAÇÃO UI/UX PREMIUM (Customização Estética MSE)
st.markdown("""
    <style>
    /* Estilização do fundo geral */
    .stApp {
        background-color: #0B0E14;
    }
    
    /* Header Corporativo Integrado */
    .custom-header {
        background: linear-gradient(135deg, #161B25 0%, #0F131C 100%);
        border-left: 6px solid #C0392B;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Quadro de Resumo de Carga (Métricas) */
    div[data-testid="stMetric"] {
        background-color: #161B25 !important;
        border: 1px solid #232D3F !important;
        border-top: 4px solid #C0392B !important;
        border-radius: 6px !important;
        padding: 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    /* Títulos e Textos das Métricas */
    div[data-testid="stMetric"] label {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    /* Area do Parecer Técnico */
    .parecer-container {
        background-color: #111622;
        border: 1px solid #1F2635;
        padding: 30px;
        border-radius: 8px;
        color: #E2E8F0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONFIGURAÇÃO DA API DO GEMINI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API não configurada. Configure a GEMINI_API_KEY nas configurações do Streamlit.")

# 4. CABEÇALHO ESTRUTURADO COM LOGO
st.markdown("""
    <div class="custom-header">
        <table style="width:100%; border:none; border-collapse:collapse;">
            <tr style="border:none; background:none;">
                <td style="width:120px; border:none; padding:0; vertical-align:middle;">
                    <img src="app/static/logo_mse.png" width="110" onerror="this.src='https://placehold.co/110x50/161B25/FFFFFF?text=MSE';">
                </td>
                <td style="border:none; padding-left:20px; vertical-align:middle;">
                    <h1 style="color: #FFFFFF; margin:0; padding:0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight:700; letter-spacing: 0.5px;">
                        VALIDADOR INTELIGENTE DE NOTAS FISCAIS
                    </h1>
                    <p style="color: #94A3B8; margin: 5px 0 0 0; padding:0; font-size: 14px;">
                        Gestão de Contratos MSE & Auditoria do Compliance Fiscal Integrado (LC 116/2003)
                    </p>
                </td>
            </tr>
        </table>
    </div>
""", unsafe_allow_html=True)

# 5. ÁREA DE COMPLIANCE / CARREGAMENTO
st.markdown("<b style='color:#E2E8F0; font-family:Arial;'>Upload do Documento Fiscal</b>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Arraste e solte o PDF da NFS-e para validação automática", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    st.info("💡 Processando inteligência de dados e memórias de cálculo...")
    
    try:
        # Leitura dos bytes do PDF
        bytes_data = uploaded_file.read()
        
        pdf_part = {
            "mime_type": "application/pdf",
            "data": bytes_data
        }
        
        # PROMPT CORRIGIDO: Força a divisão clara para tratamento do Python
        prompt_validacao = """
        Você é o Auditor Fiscal Chefe da MSE Engenharia. Analise rigidamente este PDF de NFS-e sob os critérios abaixo:

        1. DADOS DO TOMADOR: CNPJ/CPF, Razão Social e Endereço corretos da MSE Engenharia.
        2. LOCAL DA PRESTAÇÃO VS FATURAMENTO: Consistência entre onde o serviço foi prestado e o faturamento (Regra ISS conforme LC 116).
        3. CÓDIGO DE TRIBUTAÇÃO VS SERVIÇO: Análise se a descrição do serviço bate com a atividade econômica/item da lei declarado.
        4. IMPOSTOS (ISS E INSS): Memória de cálculo matemática exata e aplicação legal das retenções de INSS (11%) e ISS (2-5%).
        5. VALOR TOTAL: Verificação de consistência da equação Valor Líquido = Valor Bruto - Retenções.

        Retorne EXATAMENTE as seções demarcadas por [QUADRO_RESUMO] e [PARECER_DETALHADO].

        Na seção [QUADRO_RESUMO], apresente estritamente este objeto JSON:
        {"conforme": X, "alerta": Y, "inconforme": Z}

        Na seção [PARECER_DETALHADO], discorra formal e tecnicamente sobre cada um dos pontos analisados em formato Markdown corporativo.
        """
        
        # Chamada utilizando o caminho completo do modelo estável para mitigar erro de API
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content([pdf_part, prompt_validacao])
        texto_resposta = response.text
        
        # 6. TRATAMENTO DE TEXTO (Separação Estrutural)
        try:
            quadro_part = re.search(r"\[QUADRO_RESUMO\](.*?)\[PARECER_DETALHADO\]", texto_resposta, re.DOTALL).group(1).strip()
            parecer_part = texto_resposta.split("[PARECER_DETALHADO]")[1].strip()
            
            quadro_part = quadro_part.replace("```json", "").replace("```", "").strip()
            dados_quadro = json.loads(quadro_part)
        except:
            dados_quadro = {"conforme": "-", "alerta": "-", "inconforme": "-"}
            parecer_part = texto_resposta

        # 7. QUADRO DE RESUMO (Métricas Executivas no Topo)
        st.markdown("<h3 style='color:#FFFFFF; font-family:Arial; font-size:18px; margin-bottom:15px;'>📊 Resumo de Compliance</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.metric(label="Módulos em Conformidade", value=dados_quadro.get("conforme", 0), delta="OK", delta_color="normal")
        with c2:
            st.metric(label="Alertas / Ambiguidade", value=dados_quadro.get("alerta", 0), delta="Atenção", delta_color="off")
        with c3:
            st.metric(label="Erros Críticos / Retenções", value=dados_quadro.get("inconforme", 0), delta="Crítico", delta_color="inverse")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 8. PARECER ANALÍTICO DISCORRIDO
        st.markdown("<h3 style='color:#FFFFFF; font-family:Arial; font-size:18px; margin-bottom:15px;'>📝 Parecer Técnico Detalhado</h3>", unsafe_allow_html=True)
        st.markdown(f'<div class="parecer-container">{parecer_part}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro crítico ao processar o arquivo: {e}")
