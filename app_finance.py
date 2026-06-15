import streamlit as st
import json
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="OtimizaMente Financeiro", page_icon="💸", layout="wide")

# --- 🔒 SISTEMA DE SEGURANÇA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 Acesso Restrito")
        st.markdown("Área de segurança máxima do OtimizaMente.")
        senha_digitada = st.text_input("Digite a senha", type="password")
        if st.button("Destrancar Painel"):
            # O sistema vai buscar a senha no arquivo secreto. Se não achar (rodando local sem configurar), usa "malta2026"
            senha_correta = st.secrets.get("senha_painel", "malta2026")
            
            if senha_digitada == senha_correta:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Senha incorreta. O acesso foi bloqueado.")
    st.stop() # Isso impede que o Python leia o resto do código abaixo. Genial, né?

# --- 🗄️ GERENCIAMENTO DE DADOS (Local por enquanto) ---
ARQUIVO_DADOS = 'dados_otimizamente.json'

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "balances": {"cc": 0.0, "dinheiro": 0.0, "cofre": 0.0, "apps": {"ifood": 0.0, "ninenine": 0.0}},
        "transactions": [
            {"id": 1, "desc": "Bolsa Estágio Whirlpool", "val": 1037.01, "type": "receive"},
            {"id": 2, "desc": "Fatura do Cartão", "val": 500.00, "type": "pay"},
            {"id": 3, "desc": "Parcela da Guitarra", "val": 190.00, "type": "pay"},
            {"id": 4, "desc": "Dívida Faculdade Descomplica", "val": 1004.68, "type": "pay"}
        ],
        "history": [],
        "nextId": 5
    }

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def registrar_historico(dados, desc, val, acao, positivo):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados["history"].insert(0, {"time": agora, "desc": desc, "val": val, "acao": acao, "positivo": positivo})
    if len(dados["history"]) > 15:
        dados["history"].pop()

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

dados = st.session_state.dados

# --- 📊 LÓGICA E INTERFACE (O resto do seu App) ---
real_cash = dados["balances"]["cc"] + dados["balances"]["dinheiro"]
total_receber = sum(t["val"] for t in dados["transactions"] if t["type"] == "receive")
total_pagar = sum(t["val"] for t in dados["transactions"] if t["type"] == "pay")
sobrevivencia = real_cash - total_pagar

col_t, col_b1, col_b2 = st.columns([2, 1, 1])
with col_t:
    st.title("OtimizaMente 🧠")
    st.caption("Visão Estratégica de Liquidez & Histórico")
with col_b1:
    st.info(f"**Cofre (Reserva Malta):**\n### R$ {dados['balances']['cofre']:.2f}")
with col_b2:
    st.success(f"**Poder de Fogo (Livre):**\n### R$ {real_cash:.2f}")

st.divider()

st.subheader("🛵 Operação