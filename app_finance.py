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

st.subheader("🛵 Operação & Guarda")
c1, c2, c3 = st.columns(3)

with c1:
    st.error(f"🔴 **iFood (Retido)**: R$ {dados['balances']['apps']['ifood']:.2f}")
    ifood_val = st.number_input("Ganhos iFood", min_value=0.0, step=1.0, key="ifood_in")
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("Somar iFood"):
        if ifood_val > 0:
            dados["balances"]["apps"]["ifood"] += ifood_val
            registrar_historico(dados, "Ganhos iFood", ifood_val, "Corrida", True)
            salvar_dados(dados)
            st.rerun()
    if col_btn2.button("Repasse iFood", type="primary"):
        val = dados["balances"]["apps"]["ifood"]
        if val > 0:
            dados["balances"]["apps"]["ifood"] = 0
            dados["balances"]["cc"] += val
            registrar_historico(dados, "Repasse iFood", val, "Transferência", True)
            salvar_dados(dados)
            st.rerun()

with c2:
    st.warning(f"🟡 **99 Entrega (Retido)**: R$ {dados['balances']['apps']['ninenine']:.2f}")
    ninenine_val = st.number_input("Ganhos 99", min_value=0.0, step=1.0, key="nine_in")
    col_btn3, col_btn4 = st.columns(2)
    if col_btn3.button("Somar 99"):
        if ninenine_val > 0:
            dados["balances"]["apps"]["ninenine"] += ninenine_val
            registrar_historico(dados, "Ganhos 99", ninenine_val, "Corrida", True)
            salvar_dados(dados)
            st.rerun()
    if col_btn4.button("Repasse 99", type="primary"):
        val = dados["balances"]["apps"]["ninenine"]
        if val > 0:
            dados["balances"]["apps"]["ninenine"] = 0
            dados["balances"]["cc"] += val
            registrar_historico(dados, "Repasse 99", val, "Transferência", True)
            salvar_dados(dados)
            st.rerun()

with c3:
    st.info("🟣 **Enviar para o Cofre**")
    vault_val = st.number_input("Valor para guardar", min_value=0.0, step=1.0, key="vault_in")
    if st.button("Guardar (Tira da CC)"):
        if 0 < vault_val <= dados["balances"]["cc"]:
            dados["balances"]["cc"] -= vault_val
            dados["balances"]["cofre"] += vault_val
            registrar_historico(dados, "Enviado p/ Cofre", vault_val, "Guarda", False)
            salvar_dados(dados)
            st.rerun()
        else:
            st.error("Saldo na CC insuficiente!")

st.divider()

st.subheader("📊 Raio-X do Rombo")
m1, m2, m3 = st.columns(3)
m1.metric("Buraco Atual (A Pagar)", f"R$ {total_pagar:.2f}")
m2.metric("Esperança (A Receber)", f"R$ {total_receber:.2f}")
m3.metric("Saldo Pós-Dívidas (Liquidez)", f"R$ {sobrevivencia:.2f}", delta="Cuidado!" if sobrevivencia < 0 else "Estável")

st.divider()

col_caixa, col_lanc = st.columns([1, 2])
with col_caixa:
    st.subheader("Caixas Principais")
    nova_cc = st.number_input("Conta Corrente", value=float(dados["balances"]["cc"]), step=10.0)
    novo_din = st.number_input("Dinheiro Físico", value=float(dados["balances"]["dinheiro"]), step=10.0)
    if st.button("Atualizar Saldos Manuais"):
        dados["balances"]["cc"] = nova_cc
        dados["balances"]["dinheiro"] = novo_din
        registrar_historico(dados, "Ajuste Manual", 0, "Atualização", True)
        salvar_dados(dados)
        st.rerun()

with col_lanc:
    st.subheader("Novo Lançamento Futuro")
    with st.form("form_novo"):
        c_desc, c_val, c_tipo = st.columns([2, 1, 1])
        desc = c_desc.text_input("Descrição")
        val = c_val.number_input("Valor", min_value=0.01, step=1.0)
        tipo_str = c_tipo.selectbox("Tipo", ["A Pagar", "A Receber"])
        tipo = "pay" if tipo_str == "A Pagar" else "receive"
        
        if st.form_submit_button("Inserir Lançamento"):
            dados["transactions"].append({"id": dados["nextId"], "desc": desc, "val": val, "type": tipo})
            dados["nextId"] += 1
            salvar_dados(dados)
            st.rerun()

st.divider()

st.subheader("📅 Linha do Tempo (Pendentes)")
if not dados["transactions"]:
    st.write("Nenhum lançamento pendente.")
else:
    for t in sorted(dados["transactions"], key=lambda x: x["type"]):
        col_txt, col_val, col_act = st.columns([3, 2, 2])
        is_rec = t["type"] == "receive"
        cor = "🟢" if is_rec else "🔴"
        
        col_txt.write(f"**{t['desc']}**")
        col_val.write(f"{cor} R$ {t['val']:.2f}")
        
        with col_act:
            c_b1, c_b2 = st.columns(2)
            if c_b1.button("✔️ Baixar", key=f"bx_{t['id']}"):
                if is_rec:
                    dados["balances"]["cc"] += t["val"]
                    registrar_historico(dados, t["desc"], t["val"], "Recebido", True)
                else:
                    if dados["balances"]["cc"] < t["val"]:
                        st.warning("Aviso: CC ficou negativa!")
                    dados["balances"]["cc"] -= t["val"]
                    registrar_historico(dados, t["desc"], t["val"], "Pago", False)
                
                dados["transactions"] = [x for x in dados["transactions"] if x["id"] != t["id"]]
                salvar_dados(dados)
                st.rerun()
                
            if c_b2.button("🗑️ Excluir", key=f"ex_{t['id']}"):
                dados["transactions"] = [x for x in dados["transactions"] if x["id"] != t["id"]]
                salvar_dados(dados)
                st.rerun()

st.divider()

st.subheader("📖 Livro Caixa (Histórico Recente)")
for h in dados["history"]:
    cor_texto = "green" if h["positivo"] else "red"
    sinal = "+" if h["positivo"] else "-"
    st.markdown(f"`{h['time']}` | **{h['acao']}**: {h['desc']} | :{cor_texto}[{sinal} R$ {h['val']:.2f}]")
