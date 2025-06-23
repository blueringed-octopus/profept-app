import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
from scipy.stats import f_oneway, kruskal
from scipy.stats import mannwhitneyu
from indices import calcular_indice_conhecimento
from indices import calcular_indice_genero_sexualidade
from indices import calcular_indice_racismo
from indices import calcular_indice_legislacao

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

# Filtering data and generating a new DataFrame
df_filtered = transform(df)
q_df_filtered = df_filtered
q_column_names = {old_name: f"Q{new_name}" for old_name, new_name in zip(q_df_filtered.columns[2:], range(1, len(q_df_filtered.columns)))}
q_df_filtered = q_df_filtered.rename(columns=q_column_names)

st.write("## Análises Estatísticas dos Resultados") 

# Plotting the count of responses by 'Curso' and 'Em qual ano você está?'
st.subheader("Distribuição de Respostas por Curso e Ano")
count_df = q_df_filtered.groupby(['Curso', 'Em qual ano você está?']).size().reset_index(name='Quantidade de respostas')
st.write(count_df)

fig = px.bar(
    count_df,
    x='Curso',
    y='Quantidade de respostas',
    color='Em qual ano você está?',
    barmode='group',
    title='Quantidade de Respostas por Curso e Ano'
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Quadro Comparativo de Frequências das Respostas por Curso e Ano")

# Seleciona apenas as colunas de questões (começam com 'Q')
questoes = [col for col in q_df_filtered.columns if col.startswith('Q')]

# Agrupa por Curso, Ano e Resposta, contando as frequências
freq_df = q_df_filtered.melt(id_vars=['Curso', 'Em qual ano você está?'], value_vars=questoes,
                           var_name='Questão', value_name='Resposta')
freq_table = freq_df.groupby(['Curso', 'Em qual ano você está?', 'Questão', 'Resposta']).size().reset_index(name='Frequência')

freq_table['Questão'] = pd.Categorical(
    freq_table['Questão'],
    categories=[f"Q{i}" for i in range(1, 31)],
    ordered=True
)
freq_table = freq_table.sort_values(['Curso', 'Em qual ano você está?', 'Questão'])

# Cria uma tabela pivot para facilitar a visualização
freq_table_pivot = freq_table.pivot_table(
    index=['Curso', 'Em qual ano você está?', 'Questão'],
    columns='Resposta',
    values='Frequência',
    fill_value=0
).reset_index()
# Renomeia as colunas para facilitar a leitura
freq_table_pivot.columns.name = None  # Remove o nome da coluna
freq_table_pivot = freq_table_pivot.rename(columns=lambda x: x if isinstance(x, str) else f"Q{x}")
st.write(freq_table_pivot)

# Calcula estatísticas descritivas por Curso e Ano (somando todas as questões e respostas)
stats_df = freq_table.groupby(['Curso', 'Em qual ano você está?'])['Frequência'].agg(
    Média='mean',
    Mediana='median',
    Desvio_Padrão='std',
    Máximo='max',
    Mínimo='min'
).reset_index()

st.subheader("Quadro Comparativo de Estatísticas das Frequências por Curso e Ano")
st.dataframe(stats_df)

# Gráfico de barras: média com barra de erro (desvio padrão)
fig_stats = px.bar(
    stats_df,
    x='Curso',
    y='Média',
    color='Em qual ano você está?',
    barmode='group',
    error_y='Desvio_Padrão',
    title='Média das Frequências por Curso e Ano (com Desvio Padrão)'
)
st.plotly_chart(fig_stats, use_container_width=True)

# Análise de Tendência Central e Dispersão das Frequências por Questão, Curso e Ano
st.subheader("Tendência Central e Dispersão das Frequências por Questão, Curso e Ano")

# Calcula média, mediana e desvio padrão das frequências para cada questão, curso e ano
stats_questao = freq_table.groupby(['Curso', 'Em qual ano você está?', 'Questão'])['Frequência'].agg(
    Média='mean',
    Mediana='median',
    Desvio_Padrão='std'
).reset_index()

# Mostra o quadro comparativo
st.dataframe(stats_questao)

# Gráfico: barras agrupadas por questão, mostrando a média e barras de erro (desvio padrão)
# Ordena as questões de Q1 a Q30
stats_questao['Questão'] = pd.Categorical(
    stats_questao['Questão'],
    categories=[f"Q{i}" for i in range(1, 31)],
    ordered=True
)
stats_questao = stats_questao.sort_values('Questão')

# Gráficos separados por ano
# Ordena os anos corretamente, independente do formato
anos_unicos = list(stats_questao['Em qual ano você está?'].unique())
# Tenta ordenar por número se possível
try:
    anos_ordenados = sorted(anos_unicos, key=lambda x: int(str(x)[0]))
except Exception:
    anos_ordenados = sorted(anos_unicos)

for ano in anos_ordenados:
    st.subheader(f"Média e Desvio Padrão das Frequências por Questão e Curso - Ano: {ano}")
    dados_ano = stats_questao[stats_questao['Em qual ano você está?'] == ano]
    if not dados_ano.empty:
        fig_ano = px.bar(
            dados_ano,
            x='Questão',
            y='Média',
            color='Curso',
            barmode='group',
            error_y='Desvio_Padrão',
            category_orders={'Questão': [f"Q{i}" for i in range(1, 31)]},
            title=f'Média e Desvio Padrão das Frequências por Questão e Curso - Ano: {ano}'
        )
        st.plotly_chart(fig_ano, use_container_width=True)

# Teste de Kruskal-Wallis para verificar diferenças significativas entre cursos e anos
st.write("## Testes Estatísticos")

st.subheader("Teste de Kruskal-Wallis (diferença significativa) entre Cursos e Anos")

# Prepara os dados: média das frequências por resposta para cada Curso e para cada Ano
# Agrupa por Curso
cursos = stats_df['Curso'].unique()
anos = stats_df['Em qual ano você está?'].unique()

# Teste ANOVA/Kruskal-Wallis entre cursos
dados_cursos = [freq_table[freq_table['Curso'] == curso]['Frequência'].values for curso in cursos]
if all(len(arr) > 1 for arr in dados_cursos):
    stat_curso, p_curso = kruskal(*dados_cursos)
else:
    stat_curso, p_curso = np.nan, np.nan

# Teste ANOVA/Kruskal-Wallis entre anos
dados_anos = [freq_table[freq_table['Em qual ano você está?'] == ano]['Frequência'].values for ano in anos]
if all(len(arr) > 1 for arr in dados_anos):
    stat_ano, p_ano = kruskal(*dados_anos)
else:
    stat_ano, p_ano = np.nan, np.nan

# Monta quadro de resultados
resultados = pd.DataFrame({
    "Comparação": ["Cursos", "Anos"],
    "Estatística": [stat_curso, stat_ano],
    "p-valor": [p_curso, p_ano],
    "Diferença Significativa": ["Sim" if p < 0.05 else "Não" for p in [p_curso, p_ano]]
})

st.dataframe(resultados)

# Gráfico dos p-valores
fig_p = px.bar(
    resultados,
    x="Comparação",
    y="p-valor",
    color="Diferença Significativa",
    text_auto='.5f',
    title="p-valor dos Testes Kruskal-Wallis"
)
fig_p.update_layout(
    yaxis_title="p-valor",
    yaxis_tickformat=".5f"  # Força notação decimal, sem notação científica
)
st.plotly_chart(fig_p, use_container_width=True)

# Texto explicativo
texto = []
if p_curso < 0.05:
    texto.append("Há diferença significativa entre os cursos.")
else:
    texto.append("Não há diferença significativa entre os cursos.")
if p_ano < 0.05:
    texto.append("Há diferença significativa entre os anos.")
else:
    texto.append("Não há diferença significativa entre os anos.")

st.info(" ".join(texto))

# Teste de Kruskal-Wallis por questão entre cursos e anos
st.subheader("Questões com Diferença Significativa entre Cursos e entre Anos (Kruskal-Wallis por questão)")

# Por questão e por curso
resultados_questoes_curso = []
cursos = freq_table['Curso'].unique()
for questao in [f"Q{i}" for i in range(1, 31)]:
    dados = [freq_table[(freq_table['Questão'] == questao) & (freq_table['Curso'] == curso)]['Frequência'].values
             for curso in cursos]
    if all(len(arr) > 0 for arr in dados):
        stat, p = kruskal(*dados)
        resultados_questoes_curso.append({'Questão': questao, 'Estatística': stat, 'p-valor': p})
df_result_questoes_curso = pd.DataFrame(resultados_questoes_curso)
df_result_questoes_curso['Significativo'] = df_result_questoes_curso['p-valor'] < 0.05

st.write("**Por Curso:**")
st.dataframe(df_result_questoes_curso[df_result_questoes_curso['Significativo']])

# Por questão e por ano
resultados_questoes_ano = []
anos = freq_table['Em qual ano você está?'].unique()
for questao in [f"Q{i}" for i in range(1, 31)]:
    dados = [freq_table[(freq_table['Questão'] == questao) & (freq_table['Em qual ano você está?'] == ano)]['Frequência'].values
             for ano in anos]
    if all(len(arr) > 0 for arr in dados):
        stat, p = kruskal(*dados)
        resultados_questoes_ano.append({'Questão': questao, 'Estatística': stat, 'p-valor': p})
df_result_questoes_ano = pd.DataFrame(resultados_questoes_ano)
df_result_questoes_ano['Significativo'] = df_result_questoes_ano['p-valor'] < 0.05

st.write("**Por Ano:**")
st.dataframe(df_result_questoes_ano[df_result_questoes_ano['Significativo']])


# Sheirer-Ray-Hare test function
def scheirer_ray_hare(data, dv, factors):
    # data: DataFrame
    # dv: nome da coluna dependente (ex: 'Frequência')
    # factors: lista com os nomes dos fatores (ex: ['Curso', 'Ano'])
    from itertools import product

    # Rankeia os dados
    data = data.copy()
    data['rank'] = stats.rankdata(data[dv])

    # Soma total dos ranks
    grand_sum = data['rank'].sum()
    n = len(data)

    # Soma dos ranks por fator 1
    factor1 = factors[0]
    factor2 = factors[1]
    groups1 = data.groupby(factor1)['rank'].sum()
    groups2 = data.groupby(factor2)['rank'].sum()
    groups12 = data.groupby([factor1, factor2])['rank'].sum()

    # Número de níveis
    a = data[factor1].nunique()
    b = data[factor2].nunique()

    # Número de observações por grupo
    n_j = data.groupby(factor1).size()
    n_k = data.groupby(factor2).size()
    n_jk = data.groupby([factor1, factor2]).size()

    # Soma dos quadrados total
    ss_total = ((data['rank'] - (grand_sum / n)) ** 2).sum()

    # Soma dos quadrados fator 1
    ss_factor1 = ((groups1 ** 2) / n_j).sum() - (grand_sum ** 2) / n

    # Soma dos quadrados fator 2
    ss_factor2 = ((groups2 ** 2) / n_k).sum() - (grand_sum ** 2) / n

    # Soma dos quadrados interação
    ss_interaction = ((groups12 ** 2) / n_jk).sum() - ((groups1 ** 2) / n_j).sum() - ((groups2 ** 2) / n_k).sum() + (grand_sum ** 2) / n

    # Soma dos quadrados erro
    ss_error = ss_total - ss_factor1 - ss_factor2 - ss_interaction

    # Graus de liberdade
    df_factor1 = a - 1
    df_factor2 = b - 1
    df_interaction = (a - 1) * (b - 1)
    df_error = n - a * b

    # Estatísticas H
    h_factor1 = (ss_factor1 / ss_error) * df_error
    h_factor2 = (ss_factor2 / ss_error) * df_error
    h_interaction = (ss_interaction / ss_error) * df_error

    # p-valores
    p_factor1 = 1 - stats.chi2.cdf(h_factor1, df_factor1)
    p_factor2 = 1 - stats.chi2.cdf(h_factor2, df_factor2)
    p_interaction = 1 - stats.chi2.cdf(h_interaction, df_interaction)

    # Monta DataFrame de resultados
    result = pd.DataFrame({
        'Fonte': [factor1, factor2, f'{factor1}*{factor2}'],
        'H': [h_factor1, h_factor2, h_interaction],
        'df': [df_factor1, df_factor2, df_interaction],
        'p-valor': [p_factor1, p_factor2, p_interaction]
    })
    return result

# Renomeia a coluna para facilitar
df_srh = freq_table.rename(columns={'Em qual ano você está?': 'Ano'})

# Aplica o teste
srh_result = scheirer_ray_hare(df_srh, dv='Frequência', factors=['Curso', 'Ano'])

st.subheader("Teste Scheirer-Ray-Hare (bi-fatorial não paramétrico)")
st.dataframe(srh_result)

# Interpretação dos resultados do Scheirer-Ray-Hare
significativos = srh_result[srh_result['p-valor'] < 0.05]

if not significativos.empty:
    texto_srh = "Diferença significativa encontrada em: " + ", ".join(significativos['Fonte'].tolist()) + "."
else:
    texto_srh = "Não foi encontrada diferença significativa entre os fatores ou interação."

st.info(texto_srh)

fig_srh = px.bar(
    srh_result,
    x='Fonte',
    y='p-valor',
    color=(srh_result['p-valor'] < 0.05).map({True: 'Significativo', False: 'Não significativo'}),
    color_discrete_map={'Significativo': 'crimson', 'Não significativo': 'royalblue'},
    text_auto='.3f',
    title='p-valor do Teste Scheirer-Ray-Hare por Fator'
)
fig_srh.add_shape(
    type="line",
    x0=-0.5, x1=len(srh_result['Fonte'])-0.5,
    y0=0.05, y1=0.05,
    line=dict(color="black", dash="dash"),
)
fig_srh.add_annotation(
    x=len(srh_result['Fonte'])-1,
    y=0.05,
    text="p = 0.05",
    showarrow=False,
    yshift=10,
    font=dict(color="black")
)
fig_srh.update_layout(
    yaxis_title="p-valor",
    xaxis_title="Fator",
    legend_title="Significância",
    yaxis=dict(range=[0, max(0.06, srh_result['p-valor'].max() + 0.01)])
)
st.plotly_chart(fig_srh, use_container_width=True)

st.subheader("Questões com Diferença Significativa (Scheirer-Ray-Hare por questão)")

resultados_srh = []

for questao in [f"Q{i}" for i in range(1, 31)]:
    df_questao = freq_table[freq_table['Questão'] == questao]
    if df_questao['Curso'].nunique() > 1 and df_questao['Em qual ano você está?'].nunique() > 1:
        # Para cada questão, aplica o Scheirer-Ray-Hare
        srh_result = scheirer_ray_hare(
            df_questao.rename(columns={'Em qual ano você está?': 'Ano'}),
            dv='Frequência',
            factors=['Curso', 'Ano']
        )
        for _, row in srh_result.iterrows():
            resultados_srh.append({
                'Questão': questao,
                'Fonte': row['Fonte'],
                'H': row['H'],
                'df': row['df'],
                'p-valor': row['p-valor'],
                'Significativo': row['p-valor'] < 0.05
            })

df_result_srh = pd.DataFrame(resultados_srh)
st.dataframe(df_result_srh[df_result_srh['Significativo']])


# Calcula o índice de conhecimento para cada grupo 
st.write("## Testes Estatísticos para os Índices de Conhecimento")
cursos_disponiveis = q_df_filtered['Curso'].unique()
if len(cursos_disponiveis) >= 2:
    curso1, curso2 = cursos_disponiveis[:2]

    # Filtra os dados para cada curso
    q_freq_curso1 = q_df_filtered[q_df_filtered['Curso'] == curso1].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    q_freq_curso2 = q_df_filtered[q_df_filtered['Curso'] == curso2].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T

    # Calcula os percentuais para cada curso usando a função já importada
    percentuais1, _, _ = calcular_indice_conhecimento(q_freq_curso1)
    
    percentuais2, _, _ = calcular_indice_conhecimento(q_freq_curso2)

    # Se a função retorna apenas a média, adapte para retornar os percentuais individuais:
    # percentuais1 = lista de percentuais individuais do curso1
    # percentuais2 = lista de percentuais individuais do curso2

    # Para garantir, vamos supor que você tem acesso aos percentuais individuais:
    # (Se não, adapte a função para retornar também percentuais_individuais)
    # Exemplo:
    # percentuais1, _, _ = calcular_indice_conhecimento(q_freq_curso1, return_all=True)

    # Teste de Mann-Whitney U
    stat, p_value = mannwhitneyu(percentuais1, percentuais2, alternative='two-sided')

    # Monta tabela de resultados
    mann_df = pd.DataFrame({
        "Grupo": [curso1, curso2, "Teste"],
        "Estatística": [np.nan, np.nan, stat],
        "p-valor": [np.nan, np.nan, p_value]
    })

    st.subheader("Teste de Mann-Whitney U entre os cursos")
    st.dataframe(mann_df)

    # Gráfico dos percentuais individuais
    percentuais_plot = pd.DataFrame({
        "Percentual": percentuais1 + percentuais2,
        "Curso": [curso1]*len(percentuais1) + [curso2]*len(percentuais2)
    })
    fig_mann = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Conhecimento por Curso"
    )
    st.plotly_chart(fig_mann, use_container_width=True, key="mann_box")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Mann-Whitney U.")

# Teste de Kruskal-Wallis para comparar os percentuais de conhecimento entre todos os cursos disponíveis
# Calcula o índice de conhecimento para cada curso disponível
cursos_disponiveis = q_df_filtered['Curso'].unique()
percentuais_por_curso = []
labels_curso = []

for curso in cursos_disponiveis:
    q_freq_curso = q_df_filtered[q_df_filtered['Curso'] == curso].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_conhecimento(q_freq_curso)
    percentuais_por_curso.append(percentuais)
    labels_curso.append(curso)

# Teste de Kruskal-Wallis (apenas se houver pelo menos 2 cursos)
if len(percentuais_por_curso) >= 2:
    stat, p_value = kruskal(*percentuais_por_curso)

    # Monta tabela de resultados
    kruskal_df = pd.DataFrame({
        "Grupo": labels_curso + ["Teste"],
        "Estatística": [np.nan]*len(labels_curso) + [stat],
        "p-valor": [np.nan]*len(labels_curso) + [p_value]
    })

    st.subheader("Teste de Kruskal-Wallis entre os cursos")
    st.dataframe(kruskal_df)

    # Gráfico dos percentuais individuais por curso
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_curso, []),
        "Curso": sum([[curso]*len(percentuais_por_curso[i]) for i, curso in enumerate(labels_curso)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Conhecimento por Curso"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos pelo teste de Kruskal-Wallis (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos pelo teste de Kruskal-Wallis (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Kruskal-Wallis.")


# Teste de Mann-Whitney U e Kruskal-Wallis para o índice de Gênero e Sexualidade

# Mann-Whitney U para os dois primeiros cursos
if len(cursos_disponiveis) >= 2:
    curso1, curso2 = cursos_disponiveis[:2]

    # Filtra os dados para cada curso
    q_freq_curso1 = q_df_filtered[q_df_filtered['Curso'] == curso1].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    q_freq_curso2 = q_df_filtered[q_df_filtered['Curso'] == curso2].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T

    # Calcula os percentuais para cada curso usando a função de gênero e sexualidade
    percentuais1, _, _ = calcular_indice_genero_sexualidade(q_freq_curso1)
    percentuais2, _, _ = calcular_indice_genero_sexualidade(q_freq_curso2)

    # Teste de Mann-Whitney U
    stat, p_value = mannwhitneyu(percentuais1, percentuais2, alternative='two-sided')

    # Monta tabela de resultados
    mann_df = pd.DataFrame({
        "Grupo": [curso1, curso2, "Teste"],
        "Estatística": [np.nan, np.nan, stat],
        "p-valor": [np.nan, np.nan, p_value]
    })

    st.subheader("Teste de Mann-Whitney U (Gênero e Sexualidade) entre os cursos")
    st.dataframe(mann_df)

    # Gráfico dos percentuais individuais
    percentuais_plot = pd.DataFrame({
        "Percentual": percentuais1 + percentuais2,
        "Curso": [curso1]*len(percentuais1) + [curso2]*len(percentuais2)
    })
    fig_mann = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Gênero e Sexualidade por Curso"
    )
    st.plotly_chart(fig_mann, use_container_width=True, key="mann_box_genero")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Gênero e Sexualidade (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Gênero e Sexualidade (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Mann-Whitney U para Gênero e Sexualidade.")

# Teste de Kruskal-Wallis para comparar os percentuais de Gênero e Sexualidade entre todos os cursos disponíveis
percentuais_por_curso = []
labels_curso = []

for curso in cursos_disponiveis:
    q_freq_curso = q_df_filtered[q_df_filtered['Curso'] == curso].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_genero_sexualidade(q_freq_curso)
    percentuais_por_curso.append(percentuais)
    labels_curso.append(curso)

if len(percentuais_por_curso) >= 2:
    stat, p_value = kruskal(*percentuais_por_curso)

    # Monta tabela de resultados
    kruskal_df = pd.DataFrame({
        "Grupo": labels_curso + ["Teste"],
        "Estatística": [np.nan]*len(labels_curso) + [stat],
        "p-valor": [np.nan]*len(labels_curso) + [p_value]
    })

    st.subheader("Teste de Kruskal-Wallis (Gênero e Sexualidade) entre os cursos")
    st.dataframe(kruskal_df)

    # Gráfico dos percentuais individuais por curso
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_curso, []),
        "Curso": sum([[curso]*len(percentuais_por_curso[i]) for i, curso in enumerate(labels_curso)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Gênero e Sexualidade por Curso"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_genero")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Gênero e Sexualidade (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Gênero e Sexualidade (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Kruskal-Wallis para Gênero e Sexualidade.")

# Teste de Mann-Whitney U e Kruskal-Wallis para o índice de Racismo

# Mann-Whitney U para os dois primeiros cursos
if len(cursos_disponiveis) >= 2:
    curso1, curso2 = cursos_disponiveis[:2]

    # Filtra os dados para cada curso
    q_freq_curso1 = q_df_filtered[q_df_filtered['Curso'] == curso1].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    q_freq_curso2 = q_df_filtered[q_df_filtered['Curso'] == curso2].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T

    # Calcula os percentuais para cada curso usando a função de racismo
    percentuais1, _, _ = calcular_indice_racismo(q_freq_curso1)
    percentuais2, _, _ = calcular_indice_racismo(q_freq_curso2)

    # Teste de Mann-Whitney U
    stat, p_value = mannwhitneyu(percentuais1, percentuais2, alternative='two-sided')

    # Monta tabela de resultados
    mann_df = pd.DataFrame({
        "Grupo": [curso1, curso2, "Teste"],
        "Estatística": [np.nan, np.nan, stat],
        "p-valor": [np.nan, np.nan, p_value]
    })

    st.subheader("Teste de Mann-Whitney U (Racismo) entre os cursos")
    st.dataframe(mann_df)

    # Gráfico dos percentuais individuais
    percentuais_plot = pd.DataFrame({
        "Percentual": percentuais1 + percentuais2,
        "Curso": [curso1]*len(percentuais1) + [curso2]*len(percentuais2)
    })
    fig_mann = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Racismo por Curso"
    )
    st.plotly_chart(fig_mann, use_container_width=True, key="mann_box_racismo")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Racismo (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Racismo (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Mann-Whitney U para Racismo.")

# Teste de Kruskal-Wallis para comparar os percentuais de Racismo entre todos os cursos disponíveis
percentuais_por_curso = []
labels_curso = []

for curso in cursos_disponiveis:
    q_freq_curso = q_df_filtered[q_df_filtered['Curso'] == curso].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_racismo(q_freq_curso)
    percentuais_por_curso.append(percentuais)
    labels_curso.append(curso)

if len(percentuais_por_curso) >= 2:
    stat, p_value = kruskal(*percentuais_por_curso)

    # Monta tabela de resultados
    kruskal_df = pd.DataFrame({
        "Grupo": labels_curso + ["Teste"],
        "Estatística": [np.nan]*len(labels_curso) + [stat],
        "p-valor": [np.nan]*len(labels_curso) + [p_value]
    })

    st.subheader("Teste de Kruskal-Wallis (Racismo) entre os cursos")
    st.dataframe(kruskal_df)

    # Gráfico dos percentuais individuais por curso
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_curso, []),
        "Curso": sum([[curso]*len(percentuais_por_curso[i]) for i, curso in enumerate(labels_curso)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Racismo por Curso"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_racismo")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Racismo (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Racismo (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Kruskal-Wallis para Racismo.")

# Teste de Mann-Whitney U e Kruskal-Wallis para o índice de Legislação

# Mann-Whitney U para os dois primeiros cursos
if len(cursos_disponiveis) >= 2:
    curso1, curso2 = cursos_disponiveis[:2]

    # Filtra os dados para cada curso
    q_freq_curso1 = q_df_filtered[q_df_filtered['Curso'] == curso1].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    q_freq_curso2 = q_df_filtered[q_df_filtered['Curso'] == curso2].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T

    # Calcula os percentuais para cada curso usando a função de legislação
    percentuais1, _, _ = calcular_indice_legislacao(q_freq_curso1)
    percentuais2, _, _ = calcular_indice_legislacao(q_freq_curso2)

    # Teste de Mann-Whitney U
    stat, p_value = mannwhitneyu(percentuais1, percentuais2, alternative='two-sided')

    # Monta tabela de resultados
    mann_df = pd.DataFrame({
        "Grupo": [curso1, curso2, "Teste"],
        "Estatística": [np.nan, np.nan, stat],
        "p-valor": [np.nan, np.nan, p_value]
    })

    st.subheader("Teste de Mann-Whitney U (Legislação) entre os cursos")
    st.dataframe(mann_df)

    # Gráfico dos percentuais individuais
    percentuais_plot = pd.DataFrame({
        "Percentual": percentuais1 + percentuais2,
        "Curso": [curso1]*len(percentuais1) + [curso2]*len(percentuais2)
    })
    fig_mann = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Legislação por Curso"
    )
    st.plotly_chart(fig_mann, use_container_width=True, key="mann_box_legislacao")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Legislação (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos ({curso1} vs {curso2}) pelo teste de Mann-Whitney U para o índice de Legislação (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Mann-Whitney U para Legislação.")

# Teste de Kruskal-Wallis para comparar os percentuais de Legislação entre todos os cursos disponíveis
percentuais_por_curso = []
labels_curso = []

for curso in cursos_disponiveis:
    q_freq_curso = q_df_filtered[q_df_filtered['Curso'] == curso].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_legislacao(q_freq_curso)
    percentuais_por_curso.append(percentuais)
    labels_curso.append(curso)

if len(percentuais_por_curso) >= 2:
    stat, p_value = kruskal(*percentuais_por_curso)

    # Monta tabela de resultados
    kruskal_df = pd.DataFrame({
        "Grupo": labels_curso + ["Teste"],
        "Estatística": [np.nan]*len(labels_curso) + [stat],
        "p-valor": [np.nan]*len(labels_curso) + [p_value]
    })

    st.subheader("Teste de Kruskal-Wallis (Legislação) entre os cursos")
    st.dataframe(kruskal_df)

    # Gráfico dos percentuais individuais por curso
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_curso, []),
        "Curso": sum([[curso]*len(percentuais_por_curso[i]) for i, curso in enumerate(labels_curso)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Curso",
        y="Percentual",
        points="all",
        title="Distribuição dos Índices de Legislação por Curso"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_legislacao")

    # Interpretação
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Legislação (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os cursos pelo teste de Kruskal-Wallis para o índice de Legislação (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois cursos para aplicar o teste de Kruskal-Wallis para Legislação.")

# Teste de Kruskal-Wallis para comparar os índices de conhecimento entre os anos (ordem do 1º ao 3º ano)

anos_disponiveis = q_df_filtered['Em qual ano você está?'].unique()

# Ordena os anos do 1º ao 3º (funciona para '1º', '2º', '3º' ou '1', '2', '3')
def ano_key(x):
    try:
        return int(str(x)[0])
    except Exception:
        return x

anos_ordenados = sorted(anos_disponiveis, key=ano_key)

# --- ÍNDICE DE CONHECIMENTO ---
percentuais_por_ano = []
labels_ano = []
for ano in anos_ordenados:
    q_freq_ano = q_df_filtered[q_df_filtered['Em qual ano você está?'] == ano].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_conhecimento(q_freq_ano)
    percentuais_por_ano.append(percentuais)
    labels_ano.append(ano)

if len(percentuais_por_ano) >= 2:
    stat, p_value = kruskal(*percentuais_por_ano)
    kruskal_df = pd.DataFrame({
        "Grupo": labels_ano + ["Teste"],
        "Estatística": [np.nan]*len(labels_ano) + [stat],
        "p-valor": [np.nan]*len(labels_ano) + [p_value]
    })
    st.subheader("Kruskal-Wallis: Índice de Conhecimento entre os anos")
    st.dataframe(kruskal_df)
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_ano, []),
        "Ano": sum([[ano]*len(percentuais_por_ano[i]) for i, ano in enumerate(labels_ano)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Ano",
        y="Percentual",
        category_orders={"Ano": labels_ano},
        points="all",
        title="Distribuição dos Índices de Conhecimento por Ano"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_conhecimento_ano")
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de conhecimento (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de conhecimento (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois anos para aplicar o teste de Kruskal-Wallis para o índice de conhecimento.")

# --- ÍNDICE DE GÊNERO E SEXUALIDADE ---
percentuais_por_ano = []
labels_ano = []
for ano in anos_ordenados:
    q_freq_ano = q_df_filtered[q_df_filtered['Em qual ano você está?'] == ano].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_genero_sexualidade(q_freq_ano)
    percentuais_por_ano.append(percentuais)
    labels_ano.append(ano)

if len(percentuais_por_ano) >= 2:
    stat, p_value = kruskal(*percentuais_por_ano)
    kruskal_df = pd.DataFrame({
        "Grupo": labels_ano + ["Teste"],
        "Estatística": [np.nan]*len(labels_ano) + [stat],
        "p-valor": [np.nan]*len(labels_ano) + [p_value]
    })
    st.subheader("Kruskal-Wallis: Índice de Gênero e Sexualidade entre os anos")
    st.dataframe(kruskal_df)
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_ano, []),
        "Ano": sum([[ano]*len(percentuais_por_ano[i]) for i, ano in enumerate(labels_ano)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Ano",
        y="Percentual",
        category_orders={"Ano": labels_ano},
        points="all",
        title="Distribuição dos Índices de Gênero e Sexualidade por Ano"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_genero_ano")
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de gênero e sexualidade (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de gênero e sexualidade (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois anos para aplicar o teste de Kruskal-Wallis para o índice de gênero e sexualidade.")

# --- ÍNDICE DE RACISMO ---
percentuais_por_ano = []
labels_ano = []
for ano in anos_ordenados:
    q_freq_ano = q_df_filtered[q_df_filtered['Em qual ano você está?'] == ano].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_racismo(q_freq_ano)
    percentuais_por_ano.append(percentuais)
    labels_ano.append(ano)

if len(percentuais_por_ano) >= 2:
    stat, p_value = kruskal(*percentuais_por_ano)
    kruskal_df = pd.DataFrame({
        "Grupo": labels_ano + ["Teste"],
        "Estatística": [np.nan]*len(labels_ano) + [stat],
        "p-valor": [np.nan]*len(labels_ano) + [p_value]
    })
    st.subheader("Kruskal-Wallis: Índice de Racismo entre os anos")
    st.dataframe(kruskal_df)
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_ano, []),
        "Ano": sum([[ano]*len(percentuais_por_ano[i]) for i, ano in enumerate(labels_ano)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Ano",
        y="Percentual",
        category_orders={"Ano": labels_ano},
        points="all",
        title="Distribuição dos Índices de Racismo por Ano"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_racismo_ano")
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de racismo (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de racismo (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois anos para aplicar o teste de Kruskal-Wallis para o índice de racismo.")

# --- ÍNDICE DE LEGISLAÇÃO ---
percentuais_por_ano = []
labels_ano = []
for ano in anos_ordenados:
    q_freq_ano = q_df_filtered[q_df_filtered['Em qual ano você está?'] == ano].iloc[:, 2:].apply(pd.Series.value_counts).fillna(0).T
    percentuais, _, _ = calcular_indice_legislacao(q_freq_ano)
    percentuais_por_ano.append(percentuais)
    labels_ano.append(ano)

if len(percentuais_por_ano) >= 2:
    stat, p_value = kruskal(*percentuais_por_ano)
    kruskal_df = pd.DataFrame({
        "Grupo": labels_ano + ["Teste"],
        "Estatística": [np.nan]*len(labels_ano) + [stat],
        "p-valor": [np.nan]*len(labels_ano) + [p_value]
    })
    st.subheader("Kruskal-Wallis: Índice de Legislação entre os anos")
    st.dataframe(kruskal_df)
    percentuais_plot = pd.DataFrame({
        "Percentual": sum(percentuais_por_ano, []),
        "Ano": sum([[ano]*len(percentuais_por_ano[i]) for i, ano in enumerate(labels_ano)], [])
    })
    fig_kruskal = px.box(
        percentuais_plot,
        x="Ano",
        y="Percentual",
        category_orders={"Ano": labels_ano},
        points="all",
        title="Distribuição dos Índices de Legislação por Ano"
    )
    st.plotly_chart(fig_kruskal, use_container_width=True, key="kruskal_box_legislacao_ano")
    if p_value < 0.05:
        st.info(f"Há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de legislação (p-valor = {p_value:.4f}).")
    else:
        st.info(f"Não há diferença significativa entre os anos pelo teste de Kruskal-Wallis para o índice de legislação (p-valor = {p_value:.4f}).")
else:
    st.warning("São necessários pelo menos dois anos para aplicar o teste de Kruskal-Wallis para o índice de legislação.")

