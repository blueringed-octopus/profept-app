import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page layout configuration
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Dashboard sobre Diversidade Etnico-Racial, Gênero e Sexualidade')

# File read from Google Drive and transformed to a CSV file
# url = https://docs.google.com/spreadsheets/d/1MXaa_d0oZv_NN1iWb0U9WugLGVtepHOrjU1_A2iUjas/edit?usp=drive_link

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

# Filtering data

st.write("## Quadro Geral")
df_filtered = transform(df)
st.write(df_filtered)


df_subject = pd.DataFrame({
    "Assunto": ["Gênero e Sexualidade", "Racismo", "Legislação"]
})

df_questions_list = pd.DataFrame({
    "Questões": [list(df_filtered.columns[2:].values.tolist())]
})

df_questions_list = df_questions_list["Questões"].apply(pd.Series).T.rename(columns={0: "Questões"})

questions = df_questions_list["Questões"].unique()

# Displaying the questions
#st.write("## Lista de questões do questionário")
#st.write(df_questions_list)

# Displaying general answers frequency to the questions

st.write("## Frequência geral das respostas por pergunta")
df_questions = df_filtered.iloc[:, 2:]

df_questions_rnm = df_filtered.iloc[:, 2:]

df_questions_rnm.columns = range(1, len(df_questions.columns) + 1)

freq_questions = df_questions.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})

st.write(freq_questions)

freq_questions_rnm = df_questions_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Questões"})
#freq_questions_rnm = freq_questions_rnm.reset_index().rename(columns={"index": "Questões"})
#st.write(freq_questions_rnm)

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_questions_melted = freq_questions_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_questions_melted = freq_questions_melted.rename(columns={"index": "Questões"})
#freq_questions_melted

# Mapping the values of 'Questões' to numbers from 1 to 30
questoes_mapping = {questao: i+1 for i, questao in enumerate(freq_questions_melted['Questões'].unique())}
freq_questions_melted['Questões_Num'] = freq_questions_melted['Questões'].map(questoes_mapping)

# Creating the bar chart
fig_questions = px.bar(freq_questions_melted, x='Questões', y='Frequência', color='Respostas', title="Frequência das Respostas por Questão", width=1000, height=600)
fig_questions.update_xaxes(tickvals=list(range(0, 31)))
st.plotly_chart(fig_questions)


# Displaying the answers frequency to the questions by course, year and subject
# Create a sidebar
st.sidebar.title("Filtros")

course = st.sidebar.selectbox("Selecione o curso", df_filtered["Curso"].unique())

st.sidebar.write("###### *DCC = Técnico em Desenho de Construção Civil")
st.sidebar.write("###### **EDI = Técnico em Edificações")

df_sidebar1 = df_filtered[df_filtered["Curso"] == course]

new_column_names = {old_name: f"Q{new_name}" for old_name, new_name in zip(df_sidebar1.columns[2:], range(1, len(df_sidebar1.columns)))}
df_sidebar1 = df_sidebar1.rename(columns=new_column_names)

st.write("## Quadro de Respostas por Curso")
st.write(df_sidebar1)

# Displaying general answers frequency by course
st.write("## Frequência geral das respostas por curso")

# Creating a new DataFrame without the column "Em qual ano você está?"
df_without_year = df_sidebar1.drop(columns=["Em qual ano você está?"])

df_courses = df_without_year.iloc[:, 1:]
#df_courses
df_courses_rnm = df_without_year.iloc[:, 1:]
#df_courses_rnm
df_courses_rnm.columns = range(1, len(df_courses.columns) + 1)

# Calculating the frequency of answers by course
freq_courses = df_courses.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Cursos"})

st.write(freq_courses)

freq_courses_rnm = df_courses_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Cursos"})

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_courses_melted = freq_courses_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_courses_melted = freq_courses_melted.rename(columns={"index": "Cursos"})

# Mapping the values of 'Cursos' to numbers from 1 to 30
cursos_mapping = {curso: i+1 for i, curso in enumerate(freq_courses_melted['Cursos'].unique())}
freq_courses_melted['Cursos_Num'] = freq_courses_melted['Cursos'].map(cursos_mapping)

# Creating the bar chart
fig_courses = px.bar(freq_courses_melted, x='Cursos', y='Frequência', color='Respostas', title="Frequência das Respostas por Curso", width=1000, height=600)
fig_courses.update_xaxes(tickvals=list(range(0, 31)))
st.plotly_chart(fig_courses)

# Showing the answers frequency to the questions by year
st.write("## Quadro de Respostas por Ano")
year = st.sidebar.selectbox("Selecione o ano", df_filtered["Em qual ano você está?"].unique())
df_sidebar3 = df_sidebar1[df_sidebar1["Em qual ano você está?"] == year]

# Creating a new DataFrame without the column "Curso"
df_without_course = df_sidebar3.drop(columns=["Curso"])

df_years = df_without_course.iloc[:, 1:]

df_years_rnm = df_without_course.iloc[:, 1:]

df_years_rnm.columns = range(1, len(df_years.columns) + 1)

# Calculating the frequency of answers by year
freq_years = df_years.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Anos"})

st.write(freq_years)

freq_years_rnm = df_years_rnm.apply(pd.Series.value_counts).fillna(0).T.rename(columns={0: "Anos"})

# Filtering the columns, transforming them into rows and renaming the new column to "Respostas"
freq_years_melted = freq_years_rnm.reset_index().melt(id_vars=["index"], var_name="Respostas", value_name="Frequência")
freq_years_melted = freq_years_melted.rename(columns={"index": "Anos"})

# Mapping the values of 'Anos' to numbers from 1 to 30
anos_mapping = {ano: i+1 for i, ano in enumerate(freq_years_melted['Anos'].unique())}
freq_years_melted['Anos_Num'] = freq_years_melted['Anos'].map(anos_mapping)

# Creating the bar chart
fig_years = px.bar(freq_years_melted, x='Anos', y='Frequência', color='Respostas', title="Frequência das Respostas por Ano", width=1000, height=600)
fig_years.update_xaxes(tickvals=list(range(0, 31)))
st.plotly_chart(fig_years)

# Showing the answers frequency to the questions by subject
st.write("## Gráficos de Respostas por Assunto")
subject = st.sidebar.selectbox("Selecione o assunto", df_subject["Assunto"].unique())
df_sidebar2 = df_subject[df_subject["Assunto"] == subject]


# Configuring the layout
if subject == "Gênero e Sexualidade":
    st.write("## Gênero e Sexualidade")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col9, col10 = st.columns(2)

    # Graphs
    df_q1 = df_sidebar1.iloc[:, 2]
    df_q2 = df_sidebar1.iloc[:, 3]
    df_q3 = df_sidebar1.iloc[:, 4]
    df_q4 = df_sidebar1.iloc[:, 5]
    df_q5 = df_sidebar1.iloc[:, 6]
    df_q6 = df_sidebar1.iloc[:, 7]
    df_q7 = df_sidebar1.iloc[:, 8]
    df_q8 = df_sidebar1.iloc[:, 9]
    df_q9 = df_sidebar1.iloc[:, 10]
    df_q10 = df_sidebar1.iloc[:, 11]

    freq_q1 = df_q1.value_counts()
    freq_q2 = df_q2.value_counts()
    freq_q3 = df_q3.value_counts()
    freq_q4 = df_q4.value_counts()
    freq_q5 = df_q5.value_counts()
    freq_q6 = df_q6.value_counts()
    freq_q7 = df_q7.value_counts()
    freq_q8 = df_q8.value_counts()
    freq_q9 = df_q9.value_counts()
    freq_q10 = df_q10.value_counts()

    fig1 = px.pie(freq_q1, values=freq_q1.values, names=freq_q1.index)
    fig1.update_layout(title = dict(text=df_sidebar1.columns[2]), font=dict(size=12))
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(freq_q2, values=freq_q2.values, names=freq_q2.index)
    fig2.update_layout(title = dict(text=df_sidebar1.columns[3]), font=dict(size=12))
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = px.pie(freq_q3, values=freq_q3.values, names=freq_q3.index)
    fig3.update_layout(title = dict(text=df_sidebar1.columns[4]), font=dict(size=12))
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.pie(freq_q4, values=freq_q4.values, names=freq_q4.index)
    fig4.update_layout(title = dict(text=df_sidebar1.columns[5]), font=dict(size=12))
    col4.plotly_chart(fig4, use_container_width=True)

    fig5 = px.pie(freq_q5, values=freq_q5.values, names=freq_q5.index)
    fig5.update_layout(title = dict(text=df_sidebar1.columns[6]), font=dict(size=12))
    col5.plotly_chart(fig5, use_container_width=True)

    fig6 = px.pie(freq_q6, values=freq_q6.values, names=freq_q6.index)
    fig6.update_layout(title = dict(text=df_sidebar1.columns[7]), font=dict(size=12))
    col6.plotly_chart(fig6, use_container_width=True)

    fig7 = px.pie(freq_q7, values=freq_q7.values, names=freq_q7.index)
    fig7.update_layout(title = dict(text=df_sidebar1.columns[8]), font=dict(size=12))
    col7.plotly_chart(fig7, use_container_width=True)

    fig8 = px.pie(freq_q8, values=freq_q8.values, names=freq_q8.index)
    fig8.update_layout(title = dict(text=df_sidebar1.columns[9]), font=dict(size=12))
    col8.plotly_chart(fig8, use_container_width=True)

    fig9 = px.pie(freq_q9, values=freq_q9.values, names=freq_q9.index)
    fig9.update_layout(title = dict(text=df_sidebar1.columns[10]), font=dict(size=12))
    col9.plotly_chart(fig9, use_container_width=True)

    fig10 = px.pie(freq_q10, values=freq_q10.values, names=freq_q10.index)
    fig10.update_layout(title = dict(text=df_sidebar1.columns[11]), font=dict(size=12))
    col10.plotly_chart(fig10, use_container_width=True)


elif subject == "Racismo":
    st.write("## Racismo")
    col11, col12 = st.columns(2)
    col13, col14 = st.columns(2)
    col15, col16 = st.columns(2)
    col17, col18 = st.columns(2)
    col19, col20 = st.columns(2)

    # Graphs
    df_q11 = df_sidebar1.iloc[:, 12]
    df_q12 = df_sidebar1.iloc[:, 13]
    df_q13 = df_sidebar1.iloc[:, 14]
    df_q14 = df_sidebar1.iloc[:, 15]
    df_q15 = df_sidebar1.iloc[:, 16]
    df_q16 = df_sidebar1.iloc[:, 17]
    df_q17 = df_sidebar1.iloc[:, 18]
    df_q18 = df_sidebar1.iloc[:, 19]
    df_q19 = df_sidebar1.iloc[:, 20]
    df_q20 = df_sidebar1.iloc[:, 21]

    freq_q11 = df_q11.value_counts()
    freq_q12 = df_q12.value_counts()
    freq_q13 = df_q13.value_counts()
    freq_q14 = df_q14.value_counts()
    freq_q15 = df_q15.value_counts()
    freq_q16 = df_q16.value_counts()
    freq_q17 = df_q17.value_counts()
    freq_q18 = df_q18.value_counts()
    freq_q19 = df_q19.value_counts()
    freq_q20 = df_q20.value_counts()

    fig11 = px.pie(freq_q11, values=freq_q11.values, names=freq_q11.index, title="Questão 11")
    fig11.update_layout(title = dict(text=df_sidebar1.columns[12]), font=dict(size=12))
    col11.plotly_chart(fig11, use_container_width=True)

    fig12 = px.pie(freq_q12, values=freq_q12.values, names=freq_q12.index)
    fig12.update_layout(title = dict(text=df_sidebar1.columns[13]), font=dict(size=12))
    col12.plotly_chart(fig12, use_container_width=True)

    fig13 = px.pie(freq_q13, values=freq_q13.values, names=freq_q13.index)
    fig13.update_layout(title = dict(text=df_sidebar1.columns[14]), font=dict(size=12))
    col13.plotly_chart(fig13, use_container_width=True)

    fig14 = px.pie(freq_q14, values=freq_q14.values, names=freq_q14.index)
    fig14.update_layout(title = dict(text=df_sidebar1.columns[15]), font=dict(size=12))
    col14.plotly_chart(fig14, use_container_width=True)

    fig15 = px.pie(freq_q15, values=freq_q15.values, names=freq_q15.index)
    fig15.update_layout(title = dict(text=df_sidebar1.columns[16]), font=dict(size=12))
    col15.plotly_chart(fig15, use_container_width=True)

    fig16 = px.pie(freq_q16, values=freq_q16.values, names=freq_q16.index)
    fig16.update_layout(title = dict(text=df_sidebar1.columns[17]), font=dict(size=12))
    col16.plotly_chart(fig16, use_container_width=True)

    fig17 = px.pie(freq_q17, values=freq_q17.values, names=freq_q17.index)
    fig17.update_layout(title = dict(text=df_sidebar1.columns[18]), font=dict(size=12))
    col17.plotly_chart(fig17, use_container_width=True)

    fig18 = px.pie(freq_q18, values=freq_q18.values, names=freq_q18.index)
    fig18.update_layout(title = dict(text=df_sidebar1.columns[19]), font=dict(size=12))
    col18.plotly_chart(fig18, use_container_width=True)

    fig19 = px.pie(freq_q19, values=freq_q19.values, names=freq_q19.index)
    fig19.update_layout(title = dict(text=df_sidebar1.columns[20]), font=dict(size=12))
    col19.plotly_chart(fig19, use_container_width=True)

    fig20 = px.pie(freq_q20, values=freq_q20.values, names=freq_q20.index)
    fig20.update_layout(title = dict(text=df_sidebar1.columns[21]), font=dict(size=12))
    col20.plotly_chart(fig20, use_container_width=True)

else:
    st.write("## Legislação")
    col21, col22 = st.columns(2)
    col23, col24 = st.columns(2)
    col25, col26 = st.columns(2)
    col27, col28 = st.columns(2)
    col29, col30 = st.columns(2)
    
    # Graphs
    df_q21 = df_sidebar1.iloc[:, 22]
    df_q22 = df_sidebar1.iloc[:, 23]
    df_q23 = df_sidebar1.iloc[:, 24]
    df_q24 = df_sidebar1.iloc[:, 25]
    df_q25 = df_sidebar1.iloc[:, 26]
    df_q26 = df_sidebar1.iloc[:, 27]
    df_q27 = df_sidebar1.iloc[:, 28]
    df_q28 = df_sidebar1.iloc[:, 29]
    df_q29 = df_sidebar1.iloc[:, 30]
    df_q30 = df_sidebar1.iloc[:, 31]

    freq_q21 = df_q21.value_counts()
    freq_q22 = df_q22.value_counts()
    freq_q23 = df_q23.value_counts()
    freq_q24 = df_q24.value_counts()
    freq_q25 = df_q25.value_counts()
    freq_q26 = df_q26.value_counts()
    freq_q27 = df_q27.value_counts()
    freq_q28 = df_q28.value_counts()
    freq_q29 = df_q29.value_counts()
    freq_q30 = df_q30.value_counts()

    fig21 = px.pie(freq_q21, values=freq_q21.values, names=freq_q21.index)
    fig21.update_layout(title = dict(text=df_sidebar1.columns[22]), font=dict(size=12))
    col21.plotly_chart(fig21, use_container_width=True)

    fig22 = px.pie(freq_q22, values=freq_q22.values, names=freq_q22.index)
    fig22.update_layout(title = dict(text=df_sidebar1.columns[23]), font=dict(size=12))
    col22.plotly_chart(fig22, use_container_width=True)

    fig23 = px.pie(freq_q23, values=freq_q23.values, names=freq_q23.index)
    fig23.update_layout(title = dict(text=df_sidebar1.columns[24]), font=dict(size=12))
    col23.plotly_chart(fig23, use_container_width=True)

    fig24 = px.pie(freq_q24, values=freq_q24.values, names=freq_q24.index)
    fig24.update_layout(title = dict(text=df_sidebar1.columns[25]), font=dict(size=12))
    col24.plotly_chart(fig24, use_container_width=True)

    fig25 = px.pie(freq_q25, values=freq_q25.values, names=freq_q25.index)
    fig25.update_layout(title = dict(text=df_sidebar1.columns[26]), font=dict(size=12))
    col25.plotly_chart(fig25, use_container_width=True)

    fig26 = px.pie(freq_q26, values=freq_q26.values, names=freq_q26.index)
    fig26.update_layout(title = dict(text=df_sidebar1.columns[27]), font=dict(size=12))
    col26.plotly_chart(fig26, use_container_width=True)

    fig27 = px.pie(freq_q27, values=freq_q27.values, names=freq_q27.index)
    fig27.update_layout(title = dict(text=df_sidebar1.columns[28]), font=dict(size=12))
    col27.plotly_chart(fig27, use_container_width=True)

    fig28 = px.pie(freq_q28, values=freq_q28.values, names=freq_q28.index)
    fig28.update_layout(title = dict(text=df_sidebar1.columns[29]), font=dict(size=12))
    col28.plotly_chart(fig28, use_container_width=True)

    fig29 = px.pie(freq_q29, values=freq_q29.values, names=freq_q29.index)
    fig29.update_layout(title = dict(text=df_sidebar1.columns[30]), font=dict(size=12))
    col29.plotly_chart(fig29, use_container_width=True)

    fig30 = px.pie(freq_q30, values=freq_q30.values, names=freq_q30.index)
    fig30.update_layout(title = dict(text=df_sidebar1.columns[31]), font=dict(size=12))
    col30.plotly_chart(fig30, use_container_width=True)

