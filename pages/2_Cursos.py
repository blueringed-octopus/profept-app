import streamlit as st
import pandas as pd
import plotly.express as px

def Cursos():
    st.write("## Quadro de Respostas por Curso")
    

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

st.write("## Visão dos resultados por Curso")
st.write("Esta página apresenta os resultados filtrados por curso. Dessa forma, é possível realizar uma análise mais detalhada, possibilitando identificar diferenças e semelhanças entre os cursos oferecidos no campus.")

# Filtering data

# st.write("## Quadro Geral")
df_filtered = transform(df)

# Displaying the answers frequency to the questions by course and year
# Create a sidebar
st.sidebar.title("Filtros")

course = st.sidebar.selectbox("Selecione o curso", df_filtered["Curso"].unique())

st.sidebar.write("###### *DCC = Técnico em Desenho de Construção Civil")
st.sidebar.write("###### **EDI = Técnico em Edificações")

df_sidebar1 = df_filtered[df_filtered["Curso"] == course]

new_column_names = {old_name: f"Q{new_name}" for old_name, new_name in zip(df_sidebar1.columns[2:], range(1, len(df_sidebar1.columns)))}
df_sidebar1 = df_sidebar1.rename(columns=new_column_names)

st.write("### Quadro de Respostas por Curso")
df_courses_filtered = df_filtered[df_filtered["Curso"] == course]

df_courses_filtered = df_courses_filtered.drop(columns=["Curso", "Em qual ano você está?"])

df_courses_filtered = df_courses_filtered.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

st.write(df_courses_filtered)

# Displaying general answers frequency by course
st.write("### Frequência das respostas por curso")

# Creating a new DataFrame without the column "Em qual ano você está?"
df_without_year = df_sidebar1.drop(columns=["Em qual ano você está?"])

df_courses = df_without_year.iloc[:, 1:]

df_courses_rnm = df_without_year.iloc[:, 1:]

df_courses_rnm.columns = range(1, len(df_courses.columns) + 1)

# Calculating the frequency of answers by course
freq_courses = df_courses.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

#st.write(freq_courses)


freq_courses_rnm = df_courses_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_courses_melted = freq_courses_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_courses_melted = freq_courses_melted.rename(columns={"index": "Questões"})

# Mapping the values of 'Questões' to numbers from 1 to 30
cursos_mapping = {curso: i+1 for i, curso in enumerate(freq_courses_melted['Questões'].unique())}
freq_courses_melted['Questões_Num'] = freq_courses_melted['Questões'].map(cursos_mapping)

# Creating the bar chart
fig_courses = px.bar(freq_courses_melted, x='Questões', y='Frequência', color='Respostas', title="Frequência das Respostas por Curso", width=1000, height=600)
fig_courses.update_xaxes(tickvals=list(range(0, 31)))

st.plotly_chart(fig_courses)

