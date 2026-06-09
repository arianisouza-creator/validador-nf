import streamlit as st
import google.generativeai as genai

# Configuração da página do portal
st.set_page_config(page_title="Validador Inteligente de NF", page_icon="🧾", layout="centered")

st.title("🧾 Validador Inteligente de Notas Fiscais")
st.write("Faça o upload da sua NF em PDF para validar tomador, locais, impostos e alíquotas.")

# Configura a API do Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API não configurada. Configure a GEMINI_API_KEY nas configurações do Streamlit.")

# Campo para o usuário arrastar o PDF
uploaded_file = st.file_uploader("Escolha o arquivo PDF da Nota Fiscal", type=["pdf"])

if uploaded_file is not None:
    st.info("Processando e validando a nota... Por favor, aguarde.")
    
    try:
        # Lê os bytes do arquivo PDF diretamente
        bytes_data = uploaded_file.read()
        
        # Prepara o arquivo para o Gemini usando a estrutura correta
        pdf_part = {
            "mime_type": "application/pdf",
            "data": bytes_data
        }
        
        # O Prompt com todas as regras fiscais que combinamos
        prompt_validacao = """
        Você é um auditor fiscal de elite. Analise este PDF de Nota Fiscal de Serviço (NFS-e) e valide os seguintes pontos estritamente com base na legislação brasileira (LC 116/2003):
        
        1. DADOS DO TOMADOR: Verifique se CNPJ/CPF, Razão Social e endereço do tomador estão presentes.
        2. LOCAL DA PRESTAÇÃO VS FATURAMENTO: Avalie se a cidade de prestação e de faturamento batem, ou se a regra de retenção do ISS no local da prestação foi seguida corretamente conforme as exceções da lei.
        3. CÓDIGO DE TRIBUTAÇÃO VS SERVIÇO: Verifique se o código de serviço/tributação é coerente com a descrição do serviço prestado.
        4. IMPOSTOS (ISS E INSS): Calcule se a alíquota do ISS (entre 2% e 5%) e do INSS (se houver) estão matemáticas e legalmente corretas com base no valor bruto.
        5. VALOR TOTAL: Valide a equação básica: Valor Líquido = Valor Bruto - Retenções.
        
        Formate sua resposta em Markdown bem visual: Use um status geral (SUCESSO ou ALERTA) em destaque, uma tabela com o resumo dos dados encontrados e uma lista detalhada de inconformidades caso existam.
        """
        
        # Chamada corrigida usando a classe GenerativeModel correta
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([pdf_part, prompt_validacao])
        
        # Mostra o resultado na tela
        st.success("Análise Concluída!")
        st.markdown(response.text)
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
