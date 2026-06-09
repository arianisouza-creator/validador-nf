import streamlit as st
import google.generativeai as genai
from datetime import datetime

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Validador Corporativo de NF",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS CORPORATIVO
# =====================================================
st.markdown("""
<style>
    .main {
        background-color: #F7F9FC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .top-header {
        background: linear-gradient(135deg, #0B1F3A 0%, #123C69 100%);
        padding: 28px 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .top-header h1 {
        font-size: 34px;
        margin-bottom: 6px;
        font-weight: 700;
    }

    .top-header p {
        font-size: 16px;
        color: #DDE7F3;
        margin-bottom: 0;
    }

    .info-card {
        background-color: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        border-left: 5px solid #123C69;
        min-height: 130px;
    }

    .info-card h3 {
        color: #0B1F3A;
        font-size: 18px;
        margin-bottom: 10px;
    }

    .info-card p {
        color: #44546A;
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
        color: #123C69;
        font-weight: 700;
    }

    .stButton>button {
        background-color: #123C69;
        color: white;
        border-radius: 10px;
        height: 44px;
        border: none;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #0B1F3A;
        color: white;
        border: none;
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
else:
    api_configurada = False

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    st.markdown("**Sistema:** Validador de Nota Fiscal de Serviço")
    st.markdown("**Modelo:** Gemini 2.5 Flash")
    st.markdown("**Formato aceito:** PDF")
    st.markdown("**Limite recomendado:** até 50 MB")

    st.divider()

    st.markdown("## 📌 Conferências realizadas")
    st.markdown("""
    - Dados do tomador  
    - Local da prestação  
    - Código de serviço  
    - ISS retido  
    - INSS retido  
    - Valor bruto e líquido  
    - Retenções informadas  
    - Inconsistências fiscais  
    """)

    st.divider()

    if api_configurada:
        st.success("API configurada")
    else:
        st.error("API não configurada")

# =====================================================
# CABEÇALHO
# =====================================================
st.markdown("""
<div class="top-header">
    <h1>🧾 Validador Corporativo de Nota Fiscal</h1>
    <p>Análise inteligente de NFS-e com foco em retenções, tomador, local da prestação e conformidade fiscal.</p>
</div>
""", unsafe_allow_html=True)

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
        <h3>⚠️ Alertas Fiscais</h3>
        <p>Indicação de possíveis divergências para análise do fiscal responsável.</p>
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
        st.error("O arquivo ultrapassa o limite recomendado de 50 MB para análise pelo Gemini.")
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
Você é um analista fiscal sênior especializado na conferência de Notas Fiscais de Serviço Eletrônicas - NFS-e.

Analise o PDF da nota fiscal enviado e retorne uma conferência objetiva, profissional e estruturada.

IMPORTANTE:
- Não invente informações que não estejam no PDF.
- Quando algum dado não estiver visível, informe "Não identificado".
- Não aprove automaticamente uma NF com dados ausentes.
- A análise deve auxiliar a área fiscal, mas não substitui a validação final do responsável fiscal.

VALIDAÇÕES OBRIGATÓRIAS:

1. DADOS GERAIS DA NF
- Número da nota
- Data de emissão
- Competência, se houver
- Município emissor
- Prestador: razão social e CNPJ
- Tomador: razão social e CNPJ
- Endereço do tomador, se houver
- Local da prestação do serviço
- Obra, contrato, pedido ou medição mencionada, se houver

2. DESCRIÇÃO DO SERVIÇO
- Descrição do serviço prestado
- Código de serviço ou código de tributação
- Verificar se a descrição é coerente com o código informado
- Identificar se há menção a mão de obra, materiais, equipamentos ou medição

3. VALORES
- Valor bruto da NF
- Valor de deduções, se houver
- Base de cálculo do ISS
- Valor do ISS
- Alíquota do ISS
- Valor do INSS retido, se houver
- Base do INSS, se houver
- Outras retenções, se houver
- Valor líquido da NF

4. CONFERÊNCIA MATEMÁTICA
- Conferir se o valor líquido corresponde ao valor bruto menos as retenções
- Conferir se o ISS calculado está compatível com a base e a alíquota informadas
- Conferir se o INSS, quando informado, possui base e valor compatíveis
- Apontar divergências numéricas, mesmo que pequenas

5. CONFERÊNCIA FISCAL
- Verificar se há indício de ISS retido ou não retido
- Avaliar se o local da prestação está claro
- Avaliar se a retenção de ISS parece coerente com o município/local informado
- Avaliar se a retenção de INSS deve ser verificada quando houver cessão de mão de obra, empreitada ou serviços relacionados

FORMATO DE RESPOSTA:

# Resultado da Validação da Nota Fiscal

## Status Geral
Informe apenas um dos status abaixo:
- ✅ APROVADA PARA ANÁLISE FISCAL
- ⚠️ APROVADA COM RESSALVAS
- ❌ PENDENTE DE CORREÇÃO

Em seguida, explique o motivo em até 3 linhas.

## Resumo da NF
Monte uma tabela com as colunas:
Campo | Informação Identificada | Observação

## Conferência de Valores
Monte uma tabela com as colunas:
Item | Valor/Base | Alíquota | Resultado da Conferência

## Pontos de Atenção
Liste os pontos que precisam ser verificados pelo fiscal ou pelo fornecedor.

## Inconsistências Encontradas
Liste apenas divergências reais ou dados ausentes relevantes.

## Recomendação Final
Informe de forma objetiva se a nota pode seguir para pagamento, se precisa de validação fiscal ou se deve ser recusada/corrigida.
"""

                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                response = model.generate_content([pdf_part, prompt_validacao])

                st.success("Análise concluída com sucesso!")

                st.markdown('<div class="result-box">', unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs([
                    "📋 Resultado da Validação",
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
    Validador Corporativo de NF • Desenvolvido para apoio à análise fiscal e documental
</div>
""", unsafe_allow_html=True)
