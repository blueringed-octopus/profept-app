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
df_filtered = transform(df)

df_subject = pd.DataFrame({
    "Assunto": ["Gênero e Sexualidade", "Racismo", "Legislação"]
})

df_questions_list = pd.DataFrame({
    "Questões": [list(df_filtered.columns[1:].values.tolist())]
})

df_questions_list = df_questions_list["Questões"].apply(pd.Series).T.rename(columns={0: "Questões"})

questions = df_questions_list["Questões"].unique()

# Create a sidebar
st.sidebar.title("Filtros")

course = st.sidebar.selectbox("Selecione o curso", df_filtered["Curso"].unique())

st.sidebar.write("###### *DCC = Técnico em Desenho de Construção Civil")
st.sidebar.write("###### **EDI = Técnico em Edificações")

df_sidebar1 = df_filtered[df_filtered["Curso"] == course]
st.write(df_sidebar1)

subject = st.sidebar.selectbox("Selecione o assunto", df_subject["Assunto"].unique())
df_sidebar2 = df_subject[df_subject["Assunto"] == subject]

# Displaying general answers frequency to the questions
st.write("## Frequência geral das respostas por pergunta")
df_questions = df_sidebar1.iloc[:, 1:]
freq_questions = df_questions.apply(pd.Series.value_counts).fillna(0)
st.write(freq_questions)

# Configuring the layout
if subject == "Gênero e Sexualidade":
    st.write("## Gênero e Sexualidade")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col9, col10 = st.columns(2)

    # Graphs
    df_q1 = df_sidebar1.iloc[:, 1]
    df_q2 = df_sidebar1.iloc[:, 2]
    df_q3 = df_sidebar1.iloc[:, 3]
    df_q4 = df_sidebar1.iloc[:, 4]
    df_q5 = df_sidebar1.iloc[:, 5]
    df_q6 = df_sidebar1.iloc[:, 6]
    df_q7 = df_sidebar1.iloc[:, 7]
    df_q8 = df_sidebar1.iloc[:, 8]
    df_q9 = df_sidebar1.iloc[:, 9]
    df_q10 = df_sidebar1.iloc[:, 10]

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

    fig1 = px.pie(freq_q1, values=freq_q1.values, names=freq_q1.index, title="Questão 1")
    fig1.update_layout(title = df_questions_list["Questões"][0])
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(freq_q2, values=freq_q2.values, names=freq_q2.index, title="Questão 2")
    fig2.update_layout(title = df_questions_list["Questões"][1])
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = px.pie(freq_q3, values=freq_q3.values, names=freq_q3.index, title="Questão 3")
    fig3.update_layout(title = df_questions_list["Questões"][2])
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.pie(freq_q4, values=freq_q4.values, names=freq_q4.index, title="Questão 4")
    fig4.update_layout(title = df_questions_list["Questões"][3])
    col4.plotly_chart(fig4, use_container_width=True)

    fig5 = px.pie(freq_q5, values=freq_q5.values, names=freq_q5.index, title="Questão 5")
    fig5.update_layout(title = df_questions_list["Questões"][4])
    col5.plotly_chart(fig5, use_container_width=True)

    fig6 = px.pie(freq_q6, values=freq_q6.values, names=freq_q6.index, title="Questão 6")
    fig6.update_layout(title = df_questions_list["Questões"][5])
    col6.plotly_chart(fig6, use_container_width=True)

    fig7 = px.pie(freq_q7, values=freq_q7.values, names=freq_q7.index, title="Questão 7")
    fig7.update_layout(title = df_questions_list["Questões"][6])
    col7.plotly_chart(fig7, use_container_width=True)

    fig8 = px.pie(freq_q8, values=freq_q8.values, names=freq_q8.index, title="Questão 8")
    fig8.update_layout(title = df_questions_list["Questões"][7])
    col8.plotly_chart(fig8, use_container_width=True)

    fig9 = px.pie(freq_q9, values=freq_q9.values, names=freq_q9.index, title="Questão 9")
    fig9.update_layout(title = df_questions_list["Questões"][8])
    col9.plotly_chart(fig9, use_container_width=True)

    fig10 = px.pie(freq_q10, values=freq_q10.values, names=freq_q10.index, title="Questão 10")
    fig10.update_layout(title = df_questions_list["Questões"][9])
    col10.plotly_chart(fig10, use_container_width=True)


elif subject == "Racismo":
    st.write("## Racismo")
    col11, col12 = st.columns(2)
    col13, col14 = st.columns(2)
    col15, col16 = st.columns(2)
    col17, col18 = st.columns(2)
    col19, col20 = st.columns(2)

    # Graphs
    df_q11 = df_sidebar1.iloc[:, 11]
    df_q12 = df_sidebar1.iloc[:, 12]
    df_q13 = df_sidebar1.iloc[:, 13]
    df_q14 = df_sidebar1.iloc[:, 14]
    df_q15 = df_sidebar1.iloc[:, 15]
    df_q16 = df_sidebar1.iloc[:, 16]
    df_q17 = df_sidebar1.iloc[:, 17]
    df_q18 = df_sidebar1.iloc[:, 18]
    df_q19 = df_sidebar1.iloc[:, 19]
    df_q20 = df_sidebar1.iloc[:, 20]

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
    fig11.update_layout(title = df_questions_list["Questões"][10])
    col11.plotly_chart(fig11, use_container_width=True)

    fig12 = px.pie(freq_q12, values=freq_q12.values, names=freq_q12.index, title="Questão 12")
    fig12.update_layout(title = df_questions_list["Questões"][11])
    col12.plotly_chart(fig12, use_container_width=True)

    fig13 = px.pie(freq_q13, values=freq_q13.values, names=freq_q13.index, title="Questão 13")
    fig13.update_layout(title = df_questions_list["Questões"][12])
    col13.plotly_chart(fig13, use_container_width=True)

    fig14 = px.pie(freq_q14, values=freq_q14.values, names=freq_q14.index, title="Questão 14")
    fig14.update_layout(title = df_questions_list["Questões"][13])
    col14.plotly_chart(fig14, use_container_width=True)

    fig15 = px.pie(freq_q15, values=freq_q15.values, names=freq_q15.index, title="Questão 15")
    fig15.update_layout(title = df_questions_list["Questões"][14])
    col15.plotly_chart(fig15, use_container_width=True)

    fig16 = px.pie(freq_q16, values=freq_q16.values, names=freq_q16.index, title="Questão 16")
    fig16.update_layout(title = df_questions_list["Questões"][15])
    col16.plotly_chart(fig16, use_container_width=True)

    fig17 = px.pie(freq_q17, values=freq_q17.values, names=freq_q17.index, title="Questão 17")
    fig17.update_layout(title = df_questions_list["Questões"][16])
    col17.plotly_chart(fig17, use_container_width=True)

    fig18 = px.pie(freq_q18, values=freq_q18.values, names=freq_q18.index, title="Questão 18")
    fig18.update_layout(title = df_questions_list["Questões"][17])
    col18.plotly_chart(fig18, use_container_width=True)

    fig19 = px.pie(freq_q19, values=freq_q19.values, names=freq_q19.index, title="Questão 19")
    fig19.update_layout(title = df_questions_list["Questões"][18])
    col19.plotly_chart(fig19, use_container_width=True)

    fig20 = px.pie(freq_q20, values=freq_q20.values, names=freq_q20.index, title="Questão 20")
    fig20.update_layout(title = df_questions_list["Questões"][19])
    col20.plotly_chart(fig20, use_container_width=True)

else:
    st.write("## Legislação")
    col21, col22 = st.columns(2)
    col23, col24 = st.columns(2)
    col25, col26 = st.columns(2)
    col27, col28 = st.columns(2)
    col29, col30 = st.columns(2)
    
    # Graphs
    df_q21 = df_sidebar1.iloc[:, 21]
    df_q22 = df_sidebar1.iloc[:, 22]
    df_q23 = df_sidebar1.iloc[:, 23]
    df_q24 = df_sidebar1.iloc[:, 24]
    df_q25 = df_sidebar1.iloc[:, 25]
    df_q26 = df_sidebar1.iloc[:, 26]
    df_q27 = df_sidebar1.iloc[:, 27]
    df_q28 = df_sidebar1.iloc[:, 28]
    df_q29 = df_sidebar1.iloc[:, 29]
    df_q30 = df_sidebar1.iloc[:, 30]

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

    fig21 = px.pie(freq_q21, values=freq_q21.values, names=freq_q21.index, title="Questão 21")
    fig21.update_layout(title = df_questions_list["Questões"][20])
    col21.plotly_chart(fig21, use_container_width=True)

    fig22 = px.pie(freq_q22, values=freq_q22.values, names=freq_q22.index, title="Questão 22")
    fig22.update_layout(title = df_questions_list["Questões"][21])
    col22.plotly_chart(fig22, use_container_width=True)

    fig23 = px.pie(freq_q23, values=freq_q23.values, names=freq_q23.index, title="Questão 23")
    fig23.update_layout(title = df_questions_list["Questões"][22])
    col23.plotly_chart(fig23, use_container_width=True)

    fig24 = px.pie(freq_q24, values=freq_q24.values, names=freq_q24.index, title="Questão 24")
    fig24.update_layout(title = df_questions_list["Questões"][23])
    col24.plotly_chart(fig24, use_container_width=True)

    fig25 = px.pie(freq_q25, values=freq_q25.values, names=freq_q25.index, title="Questão 25")
    fig25.update_layout(title = df_questions_list["Questões"][24])
    col25.plotly_chart(fig25, use_container_width=True)

    fig26 = px.pie(freq_q26, values=freq_q26.values, names=freq_q26.index, title="Questão 26")
    fig26.update_layout(title = df_questions_list["Questões"][25])
    col26.plotly_chart(fig26, use_container_width=True)

    fig27 = px.pie(freq_q27, values=freq_q27.values, names=freq_q27.index, title="Questão 27")
    fig27.update_layout(title = df_questions_list["Questões"][26])
    col27.plotly_chart(fig27, use_container_width=True)

    fig28 = px.pie(freq_q28, values=freq_q28.values, names=freq_q28.index, title="Questão 28")
    fig28.update_layout(title = df_questions_list["Questões"][27])
    col28.plotly_chart(fig28, use_container_width=True)

    fig29 = px.pie(freq_q29, values=freq_q29.values, names=freq_q29.index, title="Questão 29")
    fig29.update_layout(title = df_questions_list["Questões"][28])
    col29.plotly_chart(fig29, use_container_width=True)

    fig30 = px.pie(freq_q30, values=freq_q30.values, names=freq_q30.index, title="Questão 30")
    fig30.update_layout(title = df_questions_list["Questões"][29])
    col30.plotly_chart(fig30, use_container_width=True)

