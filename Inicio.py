import streamlit as st

# Title of the dashboard
st.title('Dashboard sobre Diversidade Etnico-Racial, Gênero e Sexualidade')

# Functions to the pages
def Geral():
    st.write("")

def Cursos():
    st.write("")
    
def Assuntos():
    st.write("")
    
def Anos():
    st.write("")

# Pages dictionary
pages = {
    "Resultado Geral": Geral,
    "Resultados por Curso": Cursos,
    "Resultados por Anos": Anos,
    "Resultados por Assunto": Assuntos
}

st.write(" Projeto de Pesquisa apresentado ao Programa de Pós-Graduação em Educação Profissional e Tecnológica em Rede Nacional (ProfEPT) Instituto Federal de Educação Ciência e Tecnologia de São Paulo como parte dos requisitos para a obtenção do Título de Mestre em Educação Profissional e Tecnológica.")
st.write(" Linha de pesquisa: Organização e Memórias de Espaços Pedagógicos na EPT")
st.write(" Resumo")
st.write(" Este projeto tem como objetivos subsidiar e direcionar as ações de conscientização, educação e enfrentamento a preconceitos, discriminações e racismos realizadas no Campus Ilha Solteira do IFSP para a Promoção dos Direitos Humanos, Igualdade Étnico-Racial e de Gênero e o desenvolvimento de uma ferramenta Web (Dashboard) que possa ser utilizada para auxiliar no desenvolvimento de ações de mitigação de conflitos baseadas em dados, obtidos a partir da aplicação de um questionário aos estudantes do Ensino Médio Integrado do campus Ilha Solteira do IFSP. Com isso, pretende-se diagnosticar o nível de conhecimento destes estudantes sobre Diversidade e como uma ferramenta que mostre dados sobre este tema poderia ser utilizada para auxiliar ou orientar as ações da instituição para conscientização, educação e enfrentamento a preconceitos, discriminações e racismos. Assim, para realizar esta investigação, serão adotados métodos tais como questionários, análise estatística dos dados e métodos de desenvolvimento de software para construção do Dashboard.")
