import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64
from pathlib import Path

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Validador Corporativo de NF | MSE",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# FUNÇÃO PARA CARREGAR LOGO
# =====================================================
def carregar_logo_base64(caminho_logo):
    try:
        with open(caminho_logo, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except FileNotFoundError:
        return None

logo_path = "assets/logo_mse.png"
logo_base64 = carregar_logo_base64(logo_path)

# =====================================================
# CSS CORPORATIVO MSE
# =====================================================
st.markdown("""
<style>
    .main {
        background-color: #F7F9FC;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .mse-header {
        background: linear-gradient(135deg, #111111 0%, #2A2A2A 100%);
        padding: 28px 34px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        display: flex;
        align-items: center;
        gap: 28px;
    }

    .mse-logo {
        background-color: white;
        padding: 14px 18px;
        border-radius: 14px;
        width: 210px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .mse-logo img {
        max-width: 170px;
        height: auto;
    }

    .mse-title h1 {
        font-size: 34px;
        margin-bottom: 6px;
        font-weight: 700;
    }

    .mse-title p {
        font-size: 15px;
        color: #E5E7EB;
        margin-bottom: 0;
    }

    .info-card {
        background-color: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        border-top: 5px solid #C91F1F;
        min-height: 128px;
    }

    .info-card h3 {
        color: #111111;
        font-size: 18px;
        margin-bottom: 10px;
    }

    .info-card p {
        color: #4B5563;
        font-size: 14px;
        margin-bottom: 0;
    }

    .upload-box {
        background-color: white;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        margin-top: 18px;
        margin-bottom: 18px;
        border-left: 5px solid #C91F1F;
    }

    .result-box {
        background-color: white;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #7A869A;
        font-size: 12px;
        margin-top: 40px;
    }

    div[data-testid="stMetricValue"] {
        color: #C91F1F;
        font-weight: 700;
    }

    .stButton>button {
        background-color: #C91F1F;
        color: white;
        border-radius: 10px;
        height: 46px;
        border: none;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #A61717;
        color: white;
        border: none;
    }

    section[data-testid="stSidebar"] {
        background-color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONFIGURAÇÃO DA API
# =====================================================
api_configurada = False

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    api_configurada = True

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    if logo_base64:
        st.image(logo_path, width=180)

    st.markdown("## ⚙️ Configurações")
    st.markdown("**Sistema:** Validador de Nota Fiscal de Serviço")
    st.markdown("**Empresa:** MSE Engenharia")
    st.markdown("**Modelo:** Gemini 2.5 Flash")
    st.markdown("**Formato aceito:** PDF")

    st.divider()

    st.markdown("## 📌 Itens analisados")
    st.markdown("""
    - Dados do tomador  
    - Dados do prestador  
    - Local da prestação  
    - Código de serviço  
    - ISS retido  
    - INSS retido  
    - Valor bruto e líquido  
    - Retenções  
    - Divergências fiscais  
    """)

    st.divider()

    if api_configurada:
        st.success("API configurada")
    else:
        st.error("API não configurada")

# =====================================================
# CABEÇALHO COM LOGO
# =====================================================
if logo_base64:
    st.markdown(f"""
    <div class="mse-header">
        <div class="mse-logo">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        <div class="mse-title">
            <h1>Validador Corporativo de Nota Fiscal</h1>
            <p>Análise inteligente de NFS-e com foco em retenções, tomador, local da prestação, valores e conformidade fiscal.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="mse-header">
        <div class="mse-title">
            <h1>Validador Corporativo de Nota Fiscal</h1>
            <p>Análise inteligente de NFS-e com foco em retenções, tomador, local da prestação, valores e conformidade fiscal.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.warning("Logo não encontrada. Verifique se o arquivo está em assets/logo_mse.png")

# =====================================================
# CARDS INICIAIS
# =====================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>📄 Leitura da NF</h3>
        <p>Extração automática dos principais dados da nota fiscal enviada em PDF.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>🧮 Validação Tributária</h3>
        <p>Conferência de ISS, INSS, valor bruto, valor líquido e demais retenções.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3>🚦 Quadro Resumo</h3>
        <p>Classificação visual dos itens como OK, Alerta ou Pendente de correção.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# UPLOAD
# =====================================================
st.markdown('<div class="upload-box">', unsafe_allow_html=True)

st.subheader("📤 Envio da Nota Fiscal")

uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo PDF da Nota Fiscal",
    type=["pdf"],
    help="Envie uma NFS-e em PDF para iniciar a análise."
)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PROCESSAMENTO
# =====================================================
if uploaded_file is not None:

    file_size_mb = uploaded_file.size / (1024 * 1024)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Arquivo", uploaded_file.name)

    with col_b:
        st.metric("Tamanho", f"{file_size_mb:.2f} MB")

    with col_c:
        st.metric("Data da análise", datetime.now().strftime("%d/%m/%Y"))

    if not api_configurada:
        st.error("A chave GEMINI_API_KEY não está configurada no Streamlit Secrets.")
        st.stop()

    if file_size_mb > 50:
        st.error("O arquivo ultrapassa o limite recomendado de 50 MB.")
        st.stop()

    if st.button("🔎 Iniciar validação da NF", use_container_width=True):

        with st.spinner("Analisando a nota fiscal. Aguarde alguns instantes..."):

            try:
                bytes_data = uploaded_file.read()

                pdf_part = {
                    "mime_type": "application/pdf",
                    "data": bytes_data
                }

                prompt_validacao = """
Você é um analista fiscal sênior da área de Gestão Documental/Fiscal da MSE Engenharia.

Analise o PDF da Nota Fiscal de Serviço Eletrônica - NFS-e enviado.

OBJETIVO:
Validar a nota fiscal de forma corporativa, objetiva e visual, apontando o que está correto, o que exige atenção e o que precisa de correção.

REGRAS IMPORTANTES:
- Não invente informações.
- Use apenas dados visíveis no PDF.
- Quando um dado não for localizado, informe "Não identificado".
- Não aprove automaticamente uma nota com dados ausentes relevantes.
- A análise é uma triagem documental/fiscal e deve apoiar a validação do fiscal responsável.
- Seja direto, profissional e objetivo.

VALIDAÇÕES OBRIGATÓRIAS:

1. DADOS DA NOTA
- Número da nota fiscal
- Data de emissão
- Competência ou período da medição, se houver
- Município emissor
- Prestador: razão social e CNPJ
- Tomador: razão social e CNPJ
- Endereço do tomador, se houver
- Local da prestação do serviço
- Obra, contrato, pedido ou medição mencionada, se houver

2. SERVIÇO
- Descrição do serviço
- Código de serviço/código de tributação
- Coerência entre descrição e código
- Indicação de mão de obra, material, equipamento ou medição
- Identificação se há discriminação de materiais/equipamentos

3. VALORES E RETENÇÕES
- Valor bruto da NF
- Valor de deduções, se houver
- Base de cálculo do ISS
- Alíquota do ISS
- Valor do ISS
- Indicação se o ISS foi retido
- Base do INSS, se houver
- Valor do INSS retido, se houver
- Outras retenções, se houver
- Valor líquido da NF

4. CONFERÊNCIA MATEMÁTICA
- Verificar se Valor Líquido = Valor Bruto - Retenções
- Verificar se ISS = Base do ISS x Alíquota
- Verificar se INSS informado possui base e valor compatíveis
- Apontar divergências de cálculo

5. CONFERÊNCIA FISCAL/DOCUMENTAL
- Verificar se o tomador está identificado corretamente
- Verificar se o local da prestação está claro
- Verificar se há indício de retenção correta ou ausência de retenção
- Apontar quando ISS ou INSS exigirem validação do fiscal
- Indicar se a NF deve seguir, seguir com ressalva ou ser devolvida ao fornecedor

FORMATO OBRIGATÓRIO DA RESPOSTA:

# Resultado da Validação da Nota Fiscal

## 1. Quadro Resumo Executivo

Monte obrigatoriamente uma tabela com as colunas:

| Item Validado | Status | Evidência/Comentário |

Use apenas estes status:
- ✅ OK
- ⚠️ ALERTA
- ❌ PENDENTE/CORRIGIR
- ➖ NÃO IDENTIFICADO

Itens obrigatórios do quadro:
- Dados do prestador
- Dados do tomador
- Local da prestação
- Código de serviço
- Descrição do serviço
- Valor bruto
- Valor líquido
- ISS
- INSS
- Outras retenções
- Conferência matemática
- Indicação de obra/medição/pedido
- Conclusão para pagamento

## 2. Status Geral

Informe apenas um dos status abaixo:
- ✅ NF SEM DIVERGÊNCIA APARENTE
- ⚠️ NF COM PONTOS DE ATENÇÃO
- ❌ NF PENDENTE DE CORREÇÃO

Depois explique o motivo em até 3 linhas.

## 3. Dados Identificados na NF

Monte uma tabela com as colunas:

| Campo | Informação Identificada | Observação |

## 4. Conferência de Valores e Retenções

Monte uma tabela com as colunas:

| Item | Base/Valor Identificado | Alíquota | Resultado da Conferência |

## 5. Inconsistências ou Pontos de Atenção

Liste de forma objetiva:
- Dados ausentes
- Divergências de valor
- Retenções que exigem validação
- Informações que devem ser corrigidas pelo fornecedor

## 6. Recomendação Final

Informe uma das recomendações:
- Pode seguir para pagamento
- Pode seguir somente após validação fiscal
- Solicitar correção/cancelamento e nova emissão da NF

Finalize com uma justificativa curta.
"""

                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                response = model.generate_content([pdf_part, prompt_validacao])

                st.success("Análise concluída com sucesso!")

                st.markdown('<div class="result-box">', unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs([
                    "📊 Validação da NF",
                    "📎 Dados do Arquivo",
                    "ℹ️ Observações"
                ])

                with tab1:
                    st.markdown(response.text)

                with tab2:
                    st.write("**Nome do arquivo:**", uploaded_file.name)
                    st.write("**Tamanho:**", f"{file_size_mb:.2f} MB")
                    st.write("**Data e hora da análise:**", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

                with tab3:
                    st.info(
                        "Esta análise é uma triagem automatizada. "
                        "A decisão final sobre retenções, correções e pagamento deve ser validada pela área fiscal responsável."
                    )

                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error("Ocorreu um erro ao processar a nota fiscal.")
                st.exception(e)

else:
    st.info("Envie uma Nota Fiscal em PDF para iniciar a validação.")

# =====================================================
# RODAPÉ
# =====================================================
st.markdown("""
<div class="footer">
    MSE Engenharia • Validador Corporativo de Nota Fiscal • Apoio à análise fiscal e documental
</div>
""", unsafe_allow_html=True)
