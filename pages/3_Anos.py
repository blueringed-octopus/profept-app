import streamlit as st
import pandas as pd
import plotly.express as px
from indices import calcular_indice_conhecimento

def Anos():
    st.write("## Quadro de Respostas por Anos")
    st.write("Este quadro apresenta as respostas dos alunos por ano, permitindo uma análise mais detalhada das percepções de diversidade étnico-racial, gênero e sexualidade em cada curso oferecido.")


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

st.write("## Visão dos resultados por Anos")
st.write("Esta página apresenta os resultados filtrados por ano, possibilitando uma análise mais detalhada das similaridades entre os anos dos cursos oferecidos no campus.")

# Filtering data

df_filtered = transform(df)
# st.write(df_filtered)

# Displaying the answers frequency to the questions by course and year
# Create a sidebar
st.sidebar.title("Filtros")

# Showing the answers frequency to the questions by year
st.write("### Quadro de Respostas por Ano")
year = st.sidebar.selectbox("Selecione o ano", df_filtered["Em qual ano você está?"].unique())

df_years_filtered = df_filtered[df_filtered["Em qual ano você está?"] == year]

df_years_filtered = df_years_filtered.drop(columns=["Curso", "Em qual ano você está?"])

df_years_filtered = df_years_filtered.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

st.write(df_years_filtered)

st.write("### Frequência geral das respostas por ano")

df_sidebar3 = df_filtered[df_filtered["Em qual ano você está?"] == year]

new_column_names = {old_name: f"Q{new_name}" for old_name, new_name in zip(df_sidebar3.columns[2:], range(1, len(df_sidebar3.columns)))}
df_sidebar3 = df_sidebar3.rename(columns=new_column_names)


# Creating a new DataFrame without the column "Curso"
df_without_course = df_sidebar3.drop(columns=["Curso"])

df_years = df_without_course.iloc[:, 1:]

df_years_rnm = df_without_course.iloc[:, 1:]

df_years_rnm.columns = range(1, len(df_years.columns) + 1)

# Calculating the frequency of answers by year
freq_years = df_years.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

freq_years_rnm = df_years_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_years_melted = freq_years_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_years_melted = freq_years_melted.rename(columns={"index": "Questões"})

# Mapping the values of 'Questões' to numbers from 1 to 30
anos_mapping = {ano: i+1 for i, ano in enumerate(freq_years_melted['Questões'].unique())}
freq_years_melted['Questões_Num'] = freq_years_melted['Questões'].map(anos_mapping)

# Creating the bar chart
fig_years = px.bar(freq_years_melted, x='Questões', y='Frequência', color='Respostas', title="Frequência das Respostas por Ano", width=1000, height=600)
fig_years.update_xaxes(tickvals=list(range(0, 31)))
st.plotly_chart(fig_years)

# Displaying the index of knowledge by course
st.write("### Índice de Conhecimento por Ano")
indice_conhecimento, resultado_final, fig = calcular_indice_conhecimento(freq_years)
st.write(f"Índice de Conhecimento: {resultado_final:.2f}%")
if resultado_final < 75:
    st.warning(f"#### O índice de conhecimento geral para o ano {year} é abaixo de 75%. Insatisfatório!")
else:
    st.success(f"#### O índice de conhecimento geral para o ano {year} é acima de 75%. Satisfatório!")

st.plotly_chart(fig)