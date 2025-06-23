# indices.py
import pandas as pd
import plotly.express as px

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

    return percentuais_individuais, resultado_final, fig

# Function to calculate the index of knowledge for Gender and Sexuality

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

    return percentuais_individuais, gs_resultado_final, fig

# Function to calculate the index of knowledge for Racism

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

    return percentuais_individuais, r_resultado_final, fig_r

# Function to calculate the index of knowledge for Legislation

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
    return l_percentuais_individuais, l_resultado_final, fig_l
