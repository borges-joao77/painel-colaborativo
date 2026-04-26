import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

st.set_page_config(page_title="Painel Colaborativo", layout="wide")
st.title("Painel Colaborativo")

DATA_FILE = "dados.json"

def gerar_dados_iniciais():
    nomes = ["Ana Silva", "Carlos Souza", "Beatriz Lima", "Diego Rocha", "Fernanda Costa",
             "Gabriel Santos", "Helena Martins", "Igor Oliveira", "Julia Ferreira", "Lucas Pereira"]
    status_opcoes = ["Pendente", "Em andamento", "Concluído"]
    responsaveis = ["Time A", "Time B", "Time C"]

    dados = []
    for i, nome in enumerate(nomes):
        dados.append({
            "ID": i + 1,
            "Nome": nome,
            "Tarefa": f"Tarefa {chr(65+i)}",
            "Prioridade": random.choice(["Alta", "Média", "Baixa"]),
            "Status": random.choice(status_opcoes),
            "Responsável": random.choice(responsaveis),
            "Progresso (%)": random.randint(0, 100),
            "Observação": ""
        })
    return dados

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
