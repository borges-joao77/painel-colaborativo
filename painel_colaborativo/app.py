import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Painel Colaborativo", layout="wide")
st.title("Painel Colaborativo")

DATA_FILE = "dados.json"

def gerar_dados_iniciais():
    return [
        {"ID": 1,  "Nome": "Ana Silva",       "Tarefa": "Tarefa A", "Prioridade": "Alta",   "Status": "Pendente",      "Responsável": "Time A", "Progresso (%)": 0,   "Observação": ""},
        {"ID": 2,  "Nome": "Carlos Souza",     "Tarefa": "Tarefa B", "Prioridade": "Média",  "Status": "Em andamento",  "Responsável": "Time B", "Progresso (%)": 40,  "Observação": ""},
        {"ID": 3,  "Nome": "Beatriz Lima",     "Tarefa": "Tarefa C", "Prioridade": "Baixa",  "Status": "Concluído",     "Responsável": "Time C", "Progresso (%)": 100, "Observação": ""},
        {"ID": 4,  "Nome": "Diego Rocha",      "Tarefa": "Tarefa D", "Prioridade": "Alta",   "Status": "Pendente",      "Responsável": "Time A", "Progresso (%)": 10,  "Observação": ""},
        {"ID": 5,  "Nome": "Fernanda Costa",   "Tarefa": "Tarefa E", "Prioridade": "Média",  "Status": "Em andamento",  "Responsável": "Time B", "Progresso (%)": 60,  "Observação": ""},
        {"ID": 6,  "Nome": "Gabriel Santos",   "Tarefa": "Tarefa F", "Prioridade": "Alta",   "Status": "Pendente",      "Responsável": "Time C", "Progresso (%)": 5,   "Observação": ""},
        {"ID": 7,  "Nome": "Helena Martins",   "Tarefa": "Tarefa G", "Prioridade": "Baixa",  "Status": "Concluído",     "Responsável": "Time A", "Progresso (%)": 100, "Observação": ""},
        {"ID": 8,  "Nome": "Igor Oliveira",    "Tarefa": "Tarefa H", "Prioridade": "Média",  "Status": "Em andamento",  "Responsável": "Time B", "Progresso (%)": 75,  "Observação": ""},
        {"ID": 9,  "Nome": "Julia Ferreira",   "Tarefa": "Tarefa I", "Prioridade": "Alta",   "Status": "Pendente",      "Responsável": "Time C", "Progresso (%)": 20,  "Observação": ""},
        {"ID": 10, "Nome": "Lucas Pereira",    "Tarefa": "Tarefa J", "Prioridade": "Baixa",  "Status": "Em andamento",  "Responsável": "Time A", "Progresso (%)": 50,  "Observação": ""},
    ]

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return gerar_dados_iniciais()

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# Carrega dados
dados = carregar_dados()
df = pd.DataFrame(dados)

st.markdown("Edite os campos diretamente na tabela e clique em **Salvar alterações**.")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Resetar dados originais"):
        dados = gerar_dados_iniciais()
        salvar_dados(dados)
        st.rerun()

with col2:
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Tabela editável
df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "ID": st.column_config.NumberColumn("ID", disabled=True, width="small"),
        "Nome": st.column_config.TextColumn("Nome", width="medium"),
        "Tarefa": st.column_config.TextColumn("Tarefa", width="medium"),
        "Prioridade": st.column_config.SelectboxColumn(
            "Prioridade",
            options=["Alta", "Média", "Baixa"],
            width="small"
        ),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Pendente", "Em andamento", "Concluído"],
            width="medium"
        ),
        "Responsável": st.column_config.SelectboxColumn(
            "Responsável",
            options=["Time A", "Time B", "Time C"],
            width="small"
        ),
        "Progresso (%)": st.column_config.NumberColumn(
            "Progresso (%)",
            min_value=0,
            max_value=100,
            step=5,
            width="small"
        ),
        "Observação": st.column_config.TextColumn("Observação", width="large"),
    },
    hide_index=True,
)

if st.button("Salvar alterações", type="primary"):
    salvar_dados(df_editado.to_dict(orient="records"))
    st.success("Dados salvos com sucesso!")
    st.rerun()

# Resumo
st.divider()
st.subheader("Resumo")
col1, col2, col3 = st.columns(3)

status_counts = df_editado["Status"].value_counts()
with col1:
    st.metric("Pendente", status_counts.get("Pendente", 0))
with col2:
    st.metric("Em andamento", status_counts.get("Em andamento", 0))
with col3:
    st.metric("Concluído", status_counts.get("Concluído", 0))
