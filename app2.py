import streamlit as st
import pandas as pd
import plotly.express as px


# Set the page layout configuration
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Dashboard sobre Diversidade Etnico-Racial, Gênero e Sexualidade')

# File read from Google Drive and transformed to a CSV file
# url = https://docs.google.com/spreadsheets/d/1MXaa_d0oZv_NN1iWb0U9WugLGVtepHOrjU1_A2iUjas/edit?usp=drive_link
sheet_id = "1MXaa_d0oZv_NN1iWb0U9WugLGVtepHOrjU1_A2iUjas"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Filter the data
df_filtered = df.iloc[:, 3:]

df_assunto = pd.DataFrame({
    "Assunto": ["Gênero e Sexualidade", "Racismo", "Legislação"]
})

# Create a sidebar
curso = st.sidebar.selectbox("Selecione o curso", df_filtered["Curso"].unique())
df_sidebar1 = df_filtered[df_filtered["Curso"] == curso]
df_sidebar1

assunto = st.sidebar.selectbox("Selecione o assunto", df_assunto["Assunto"].unique())
df_sidebar2 = df_assunto[df_assunto["Assunto"] == assunto]


# Configure the layout
if assunto == "Gênero e Sexualidade":
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

    fig1 = px.bar(freq_q1, x=freq_q1.index, y=freq_q1.values, color=freq_q1, title="Questão 1")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(freq_q2, x=freq_q2.index, y=freq_q2.values, color=freq_q2, title="Questão 2")
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(freq_q3, x=freq_q3.index, y=freq_q3.values, color=freq_q3, title="Questão 3")
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(freq_q4, x=freq_q4.index, y=freq_q4.values, color=freq_q4, title="Questão 4")
    col4.plotly_chart(fig4, use_container_width=True)

    fig5 = px.bar(freq_q5, x=freq_q5.index, y=freq_q5.values, color=freq_q5, title="Questão 5")
    col5.plotly_chart(fig5, use_container_width=True)

    fig6 = px.bar(freq_q6, x=freq_q6.index, y=freq_q6.values, color=freq_q6, title="Questão 6")
    col6.plotly_chart(fig6, use_container_width=True)

    fig7 = px.bar(freq_q7, x=freq_q7.index, y=freq_q7.values, color=freq_q7, title="Questão 7")
    col7.plotly_chart(fig7, use_container_width=True)

    fig8 = px.bar(freq_q8, x=freq_q8.index, y=freq_q8.values, color=freq_q8, title="Questão 8")
    col8.plotly_chart(fig8, use_container_width=True)

    fig9 = px.bar(freq_q9, x=freq_q9.index, y=freq_q9.values, color=freq_q9, title="Questão 9")
    col9.plotly_chart(fig9, use_container_width=True)

    fig10 = px.bar(freq_q10, x=freq_q10.index, y=freq_q10.values, color=freq_q10, title="Questão 10")
    col10.plotly_chart(fig10, use_container_width=True)


elif assunto == "Racismo":
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

    fig11 = px.bar(freq_q11, x=freq_q11.index, y=freq_q11.values, color=freq_q11, title="Questão 11")
    col11.plotly_chart(fig11, use_container_width=True)

    fig12 = px.bar(freq_q12, x=freq_q12.index, y=freq_q12.values, color=freq_q12, title="Questão 12")
    col12.plotly_chart(fig12, use_container_width=True)

    fig13 = px.bar(freq_q13, x=freq_q13.index, y=freq_q13.values, color=freq_q13, title="Questão 13")
    col13.plotly_chart(fig13, use_container_width=True)

    fig14 = px.bar(freq_q14, x=freq_q14.index, y=freq_q14.values, color=freq_q14, title="Questão 14")
    col14.plotly_chart(fig14, use_container_width=True)

    fig15 = px.bar(freq_q15, x=freq_q15.index, y=freq_q15.values, color=freq_q15, title="Questão 15")
    col15.plotly_chart(fig15, use_container_width=True)

    fig16 = px.bar(freq_q16, x=freq_q16.index, y=freq_q16.values, color=freq_q16, title="Questão 16")
    col16.plotly_chart(fig16, use_container_width=True)

    fig17 = px.bar(freq_q17, x=freq_q17.index, y=freq_q17.values, color=freq_q17, title="Questão 17")
    col17.plotly_chart(fig17, use_container_width=True)

    fig18 = px.bar(freq_q18, x=freq_q18.index, y=freq_q18.values, color=freq_q18, title="Questão 18")
    col18.plotly_chart(fig18, use_container_width=True)

    fig19 = px.bar(freq_q19, x=freq_q19.index, y=freq_q19.values, color=freq_q19, title="Questão 19")
    col19.plotly_chart(fig19, use_container_width=True)

    fig20 = px.bar(freq_q20, x=freq_q20.index, y=freq_q20.values, color=freq_q20, title="Questão 20")
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

    fig21 = px.bar(freq_q21, x=freq_q21.index, y=freq_q21.values, color=freq_q21, title="Questão 21")
    col21.plotly_chart(fig21, use_container_width=True)

    fig22 = px.bar(freq_q22, x=freq_q22.index, y=freq_q22.values, color=freq_q22, title="Questão 22")
    col22.plotly_chart(fig22, use_container_width=True)

    fig23 = px.bar(freq_q23, x=freq_q23.index, y=freq_q23.values, color=freq_q23, title="Questão 23")
    col23.plotly_chart(fig23, use_container_width=True)

    fig24 = px.bar(freq_q24, x=freq_q24.index, y=freq_q24.values, color=freq_q24, title="Questão 24")
    col24.plotly_chart(fig24, use_container_width=True)

    fig25 = px.bar(freq_q25, x=freq_q25.index, y=freq_q25.values, color=freq_q25, title="Questão 25")
    col25.plotly_chart(fig25, use_container_width=True)

    fig26 = px.bar(freq_q26, x=freq_q26.index, y=freq_q26.values, color=freq_q26, title="Questão 26")
    col26.plotly_chart(fig26, use_container_width=True)

    fig27 = px.bar(freq_q27, x=freq_q27.index, y=freq_q27.values, color=freq_q27, title="Questão 27")
    col27.plotly_chart(fig27, use_container_width=True)

    fig28 = px.bar(freq_q28, x=freq_q28.index, y=freq_q28.values, color=freq_q28, title="Questão 28")
    col28.plotly_chart(fig28, use_container_width=True)

    fig29 = px.bar(freq_q29, x=freq_q29.index, y=freq_q29.values, color=freq_q29, title="Questão 29")
    col29.plotly_chart(fig29, use_container_width=True)

    fig30 = px.bar(freq_q30, x=freq_q30.index, y=freq_q30.values, color=freq_q30, title="Questão 30")
    col30.plotly_chart(fig30, use_container_width=True)

