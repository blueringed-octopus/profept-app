import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page layout configuration
st.set_page_config(layout="wide")

@st.cache_data # Add cache_data decorator to avoid loading the data every time the page is refreshed
def load_data(url):
    df = pd.read_csv(url)
    return df

sheet_id = "1MXaa_d0oZv_NN1iWb0U9WugLGVtepHOrjU1_A2iUjas"
df = load_data(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

@st.cache_data
def transform(df):
    df = df.iloc[:, 3:]
    return df

def Geral():
    st.write("")

st.write("## Visão Geral dos Resultados")
st.write("Esta página apresenta uma visão geral dos resultados obtidos a partir das respostas dos(as) estudantes, permitindo uma análise abrangente das percepções de diversidade étnico-racial, gênero e sexualidade.")
st.write("Aqui, você pode explorar os resultados de forma agregada, sem filtrar por curso ou ano específico. Isso permite uma visão geral do conhecimento dos alunos sobre os temas abordados no questionário.")
st.write("Estão apresentados aqui um quadro geral com a frequência das respostas por pergunta e um gráfico de barras que mostra a frequência das respostas para cada pergunta, permitindo uma análise visual clara dos dados coletados.")
st.write("Além disso, são apresentados os índices de conhecimento geral, bem como os índices de conhecimento sobre Gênero e Sexualidade, Racismo e Legislação. Esses índices fornecem uma visão quantitativa do nível de conhecimento dos(as) estudantes sobre esses temas.")

# Filtering data

st.write("### Quadro Geral")
df_filtered = transform(df)

df_questions = df_filtered.iloc[:, 2:]

df_questions_rnm = df_filtered.iloc[:, 2:]

df_questions_rnm.columns = range(1, len(df_questions.columns) + 1)

freq_questions = df_questions.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

st.write(freq_questions)


# Creting a DataFrame to calculate the Index of Knowledge

q_df_filtered = df_filtered
q_column_names = {old_name: f"Q{new_name}" for old_name, new_name in zip(q_df_filtered.columns[2:], range(1, len(q_df_filtered.columns)))}
q_df_filtered = q_df_filtered.rename(columns=q_column_names)

q_df_questions = q_df_filtered.iloc[:, 2:]

q_df_questions_rnm = q_df_filtered.iloc[:, 2:]

q_df_questions_rnm.columns = range(1, len(q_df_questions.columns) + 1)

q_freq_questions = q_df_questions.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

# Creating a DataFrame with the questions list
df_questions_list = pd.DataFrame({
    "Questões": [list(df_filtered.columns[2:].values.tolist())]
    })

df_questions_list = df_questions_list["Questões"].apply(pd.Series).T.rename(columns={0: "Questões"})

questions = df_questions_list["Questões"].unique()


# Displaying general answers frequency to the questions

st.write("### Frequência geral das respostas")

freq_questions_rnm = df_questions_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_questions_melted = freq_questions_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_questions_melted = freq_questions_melted.rename(columns={"index": "Questões"})


# Mapping the values of 'Questões' to numbers from 1 to 30
questoes_mapping = {questao: i+1 for i, questao in enumerate(freq_questions_melted['Questões'].unique())}
freq_questions_melted['Questões_Num'] = freq_questions_melted['Questões'].map(questoes_mapping)



# Creating the bar chart
fig_questions = px.bar(freq_questions_melted, x='Questões', y='Frequência', color='Respostas', title="Frequência das Respostas por Questão", width=1000, height=600)
fig_questions.update_xaxes(tickvals=list(range(0, 31)))
st.plotly_chart(fig_questions)

# Indexes of the Level of Knowledge
st.write("### Índices de Nível de Conhecimento")
st.write("Os índices foram calculados considerando que a resposta esperada para as questões 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 15, 16, 17, 18, 19, 22 e 23 é 'Discordo totalmente' e para as questões 8, 9, 10, 14, 20, 21, 24, 25, 26, 27, 28, 29 e 30 a resposta esperada é 'Concordo totalmente'.")

# Function to calculate the index of general knowledge
@st.cache_data
def calcular_indice_conhecimento(q_freq_questions):
    """
    Calculates the general knowledge index and generates a frequency chart.
    Returns the average percentage value.
    """
    # Lists of questions for "Discordo totalmente" and "Concordo totalmente"
    # These lists are used to calculate the percentages for each question
    # based on the responses in the DataFrame q_freq_questions
    discordo_questions = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q11', 'Q12', 'Q13', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q22', 'Q23']
    concordo_questions = ['Q8', 'Q9', 'Q10', 'Q14', 'Q20', 'Q21', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29', 'Q30']
    percentuais = []
    questoes = []
    respostas = []
    percentuais_individuais = []

    # To calculate the percentage of "Discordo totalmente" for each question
    for q in discordo_questions:
        valor = q_freq_questions.loc[q, 'Discordo totalmente']
        soma = q_freq_questions.loc[q].sum()
        percentual = (valor / soma) * 100 if soma != 0 else 0
        percentuais.append(percentual)
        questoes.append(q)
        respostas.append("Discordo totalmente")
        percentuais_individuais.append(percentual)

    # To calculate the percentage of "Concordo totalmente" for each question
    for q in concordo_questions:
        valor = q_freq_questions.loc[q, 'Concordo totalmente']
        soma = q_freq_questions.loc[q].sum()
        percentual = (valor / soma) * 100 if soma != 0 else 0
        percentuais.append(percentual)
        questoes.append(q)
        respostas.append("Concordo totalmente")
        percentuais_individuais.append(percentual)

    # Sum of percentages divided by 30
    # (30 is the total number of questions)
    resultado_final = sum(percentuais) / 30

    # DataFrame for the chart
    # Create a DataFrame with the questions, answers, and individual percentages
    df_grafico = pd.DataFrame({
        "Questão": questoes,
        "Resposta": respostas,
        "Percentual": percentuais_individuais
    })

    fig = px.bar(
        df_grafico,
        x="Questão",
        y="Percentual",
        color="Resposta",
        barmode="group",
        title="Percentual de Respostas por Questão - Conhecimento Geral"
    )

    return resultado_final, fig

# Function to calculate the index of knowledge for Gender and Sexuality
@st.cache_data
def calcular_indice_genero_sexualidade(q_freq_questions):
    """
    Calculates the index of knowledge about Gender and Sexuality and generates a frequency chart.
    Returns the average percentage value and the Plotly chart.
    """
    gs_discordo_questions = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7']
    gs_concordo_questions = ['Q8', 'Q9', 'Q10']
    gs_percentuais = []
    questoes = []
    respostas = []
    percentuais_individuais = []

    # To calculate the percentage of "Discordo totalmente" for each question
    # (10 is the total number of questions)
    for q in gs_discordo_questions:
        gs_valor = q_freq_questions.loc[q, 'Discordo totalmente']
        gs_soma = q_freq_questions.loc[q].sum()
        gs_percentual = (gs_valor / gs_soma) * 100 if gs_soma != 0 else 0
        gs_percentuais.append(gs_percentual)
        questoes.append(q)
        respostas.append("Discordo totalmente")
        percentuais_individuais.append(gs_percentual)

    # To calculate the percentage of "Concordo totalmente" for each question
    # (10 is the total number of questions)
    for q in gs_concordo_questions:
        gs_valor = q_freq_questions.loc[q, 'Concordo totalmente']
        gs_soma = q_freq_questions.loc[q].sum()
        gs_percentual = (gs_valor / gs_soma) * 100 if gs_soma != 0 else 0
        gs_percentuais.append(gs_percentual)
        questoes.append(q)
        respostas.append("Concordo totalmente")
        percentuais_individuais.append(gs_percentual)

    # Sum of percentages divided by 10
    # (10 is the total number of questions)
    gs_resultado_final = sum(gs_percentuais) / 10  # 10 questões no total

    # DataFrame for the chart
    # Create a DataFrame with the questions, answers, and individual percentages
    df_grafico = pd.DataFrame({
        "Questão": questoes,
        "Resposta": respostas,
        "Percentual": percentuais_individuais
    })

    fig = px.bar(
        df_grafico,
        x="Questão",
        y="Percentual",
        color="Resposta",
        barmode="group",
        title="Percentual de Respostas por Questão - Gênero e Sexualidade"
    )

    return gs_resultado_final, fig

# Function to calculate the index of knowledge for Racism
@st.cache_data
def calcular_indice_racismo(q_freq_questions):
    """
    Calculates the index of knowledge about Racism and generates a frequency chart.
    Returns the average percentage value and the Plotly chart.
    """
    r_discordo_questions = ['Q11', 'Q12', 'Q13', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19']
    r_concordo_questions = ['Q14', 'Q20']
    r_percentuais = []
    questoes = []
    respostas = []
    percentuais_individuais = []

    # To calculate the percentage of "Discordo totalmente" for each question
    for q in r_discordo_questions:
        r_valor = q_freq_questions.loc[q, 'Discordo totalmente']
        r_soma = q_freq_questions.loc[q].sum()
        r_percentual = (r_valor / r_soma) * 100 if r_soma != 0 else 0
        r_percentuais.append(r_percentual)
        questoes.append(q)
        respostas.append("Discordo totalmente")
        percentuais_individuais.append(r_percentual)

    # To calculate the percentage of "Concordo totalmente" for each question
    # (10 is the total number of questions)
    for q in r_concordo_questions:
        r_valor = q_freq_questions.loc[q, 'Concordo totalmente']
        r_soma = q_freq_questions.loc[q].sum()
        r_percentual = (r_valor / r_soma) * 100 if r_soma != 0 else 0
        r_percentuais.append(r_percentual)
        questoes.append(q)
        respostas.append("Concordo totalmente")
        percentuais_individuais.append(r_percentual)

    # Sum of percentages divided by 10
    # (10 is the total number of questions)
    r_resultado_final = sum(r_percentuais) / 10  # 10 questões no total

    # DataFrame for the chart
    # Create a DataFrame with the questions, answers, and individual percentages
    df_r_grafico = pd.DataFrame({
        "Questão": questoes,
        "Resposta": respostas,
        "Percentual": percentuais_individuais
    })

    fig_r = px.bar(
        df_r_grafico,
        x="Questão",
        y="Percentual",
        color="Resposta",
        barmode="group",
        title="Percentual de Respostas por Questão - Racismo"
    )

    return r_resultado_final, fig_r

# Function to calculate the index of knowledge for Legislation
@st.cache_data
def calcular_indice_legislacao(q_freq_questions):
    """
    Calculates the index of knowledge about Gender and Sexuality and generates a frequency chart.
    Returns the average percentage value and the Plotly chart.
    """
    l_discordo_questions = ['Q22', 'Q23']
    l_concordo_questions = ['Q21', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29', 'Q30']
    l_percentuais = []
    l_questoes = []
    l_respostas = []
    l_percentuais_individuais = []

    # To calculate the percentage of "Discordo totalmente" for each question
    # (10 is the total number of questions)
    for q in l_discordo_questions:
        l_valor = q_freq_questions.loc[q, 'Discordo totalmente']
        l_soma = q_freq_questions.loc[q].sum()
        l_percentual = (l_valor / l_soma) * 100 if l_soma != 0 else 0
        l_percentuais.append(l_percentual)
        l_questoes.append(q)
        l_respostas.append("Discordo totalmente")
        l_percentuais_individuais.append(l_percentual)

    # To calculate the percentage of "Concordo totalmente" for each question
    # (10 is the total number of questions)
    for q in l_concordo_questions:
        l_valor = q_freq_questions.loc[q, 'Concordo totalmente']
        l_soma = q_freq_questions.loc[q].sum()
        l_percentual = (l_valor / l_soma) * 100 if l_soma != 0 else 0
        l_percentuais.append(l_percentual)
        l_questoes.append(q)
        l_respostas.append("Concordo totalmente")
        l_percentuais_individuais.append(l_percentual)

    # Sum of percentages divided by 10
    # (10 is the total number of questions)
    l_resultado_final = sum(l_percentuais) / 10

    # DataFrame for the chart
    # Create a DataFrame with the questions, answers, and individual percentages
    df_l_grafico = pd.DataFrame({
        "Questão": l_questoes,
        "Resposta": l_respostas,
        "Percentual": l_percentuais_individuais
    })

    fig_l = px.bar(
        df_l_grafico,
        x="Questão",
        y="Percentual",
        color="Resposta",
        barmode="group",
        title="Percentual de Respostas por Questão - Legislação"
    )
    return l_resultado_final, fig_l

resultado_final, fig = calcular_indice_conhecimento(q_freq_questions)
st.plotly_chart(fig)
st.write(f"**Índice de Conhecimento Geral: {resultado_final:.2f}%**")

gs_resultado_final, gs_fig = calcular_indice_genero_sexualidade(q_freq_questions)
st.plotly_chart(gs_fig)
st.write(f"**Índice de Conhecimento Geral sobre Gênero e Sexualidade: {gs_resultado_final:.2f}%**")

r_resultado_final, r_fig = calcular_indice_racismo(q_freq_questions)
st.plotly_chart(r_fig)
st.write(f"**Índice de Conhecimento Geral sobre Racismo: {r_resultado_final:.2f}%**")

l_resultado_final, l_fig = calcular_indice_legislacao(q_freq_questions)
st.plotly_chart(l_fig)
st.write(f"**Índice de Conhecimento Geral sobre Legislação: {l_resultado_final:.2f}%**")

