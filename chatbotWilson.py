#instalar e importar streamlit e openai

#passo 1: arrumar com o streamlit o título do chatbot. para modificar o tamanho do título, colocar ##, estudar mais sobre edição no streamlit.
#passo 2: colocar caixa de texto com streamlit com input
#passo 3: quando o usuário mandar uma mensagem: 
    # mostrar mensagem do user na tela
    # mandar para a ia responder, conectar com a gemini gratuita de última versão. chave api
    # mostrar mensagem de resposta da IA.
    # criar memória de mensagens e deixar elas aparecendo na tela
    # laço de repetição
import streamlit as st
from openai import OpenAI

modelo_ia = OpenAI(api_key=st.secrets["GEMINI_API_KEY"],
                   base_url="https://generativelanguage.googleapis.com/v1beta/openai")

#Título e configuração da página
st.title("🚗 Assistente do Consultor de Vendas Wilson Luis")
st.caption("Especialista em veículos, financiamentos, marketing automotivo e negociação")
#1.Definição do Prompt do Sistema (A "personalidade do Chatbot")
PROMPT_SISTEMA = """
Você é o Copiloto do Wilson, um especialista de elite em consultoria de vendas de veículos, 
estudante de Gestão de Vendas e entusiasta do mercado financeiro e investimentos.

Seu objetivo é ajudá-lo a ser um vendedor de extrema alta performance, cobrindo:

1. **Conhecimento Automotivo e Avaliação:**
   - Detalhes técnicos, prós e contras de modelos populares aos de luxo.
   - Dicas de inspeção, mecânica rápida e pontos de atenção para compra/troca.

2. **Financiamentos e Estratégias Financeiras:**
   - Dicas sobre taxas de juros, amortização, entrada, parcelamento, CDC, Leasing e Consórcios.
   - Estratégias ocultas e argumentos para ajudar o cliente a entender o custo-benefício da compra.
   - Noções de investimentos para ajudar o Wilson e orientar clientes sobre planejamento financeiro.

3. **Marketing Automotivo e Conteúdo:**
   - Criação de roteiros para Reels, TikTok, Stories e fotos de anúncios.
   - Textos persuasivos (Copywriting) para marketplaces (OLX, Webmotors, Facebook Marketplace).
   - Técnicas de gatilhos mentais para vendas no Instagram.

4. **Técnicas de Vendas e Negociação:**
   - Quebra de objeções (ex: "está caro", "vou falar com a esposa", "o juro está alto").
   - Técnicas de contorno e fechamento rápido com foco na máxima assertividade.

**Diretrizes de Resposta:**
- Mantenha um tom profissional, encorajador, direto ao ponto e focado em resultados de vendas.
- Sempre que criar um roteiro ou texto de anúncio, use formatos prontos para copiar e colar.
"""
#2. Inicialização do histórico na sessão:
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []
#3. Exibir histórico de conversas na tela:
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)
#4.Campo para o usuário mandar mensagem:
mensagem_usuario = st.chat_input("Digite sua mensagem aqui")

if mensagem_usuario: 
#Exibe e salva a mensagem do usuário
    st.chat_message("user").write(mensagem_usuario)
    mensagem1 = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem1)
#Monta a estrutura enviada para IA incluindo o contexto do sistema
    mensagens_para_envio = [{"role": "system", "content": PROMPT_SISTEMA}] + st.session_state["lista_mensagens"]
#Chamada à API    
    resposta_modelo = modelo_ia.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gemini-2.5-flash"
    )
    resposta_ia = resposta_modelo.choices[0].message.content
#Exibe e salva a resposta da IA
    st.chat_message("assistant").write(resposta_ia)    
    mensagem2 = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem2)