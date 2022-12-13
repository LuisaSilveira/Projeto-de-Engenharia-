import streamlit as st
import pickle
import numpy as np


def loadModelo():
    with open('passos.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = loadModelo()

modelo = data['modelo']
leGen = data["leGen"]
leCurso = data['leCurso']
leFacul = data['leFacul']
leEc = data['leEc']


def exibePredict():
    st.title("Nível de atenção quando à saúde mental de estudantes.")
    st.write("""### Entre com as informações do indivíduo: """)

    faculs = ('PUC', 'Outro', 'UFRJ', 'UFF', 'Estácio')
    
    genero =('Masculino','Feminino')

    cursos = ('Engenharia', 'Outro', 'Medicina', 'Direito', 'Psicologia')
    
    estadoCivil = ('Solteiro','Casado','Em união estável')

    acomp =('Sim','Não')


    idade = st.number_input("Idade", min_value=18, max_value=30)
    gen = st.selectbox("Sexo",genero)
    curso = st.selectbox("Curso",cursos)
    facul = st.selectbox("Faculdade",faculs)
    periodo = st.number_input("Período de faculdade", min_value = 1, max_value = 15)
    cr = st.slider("Coeficiente de rendimento (nota media no curso)",0,10,5)
    ec = st.selectbox('Estado Civil', estadoCivil)
    psico = st.selectbox('Tem acompanhamento psicológico?',acomp)

    dSimNao = {'Sim':1,'Não':0}


    botao = st.button("Enviar")

    if botao:
        X = np.array([[idade,gen,curso,facul,periodo,cr,ec,psico]])
        X[:,1] = leGen.transform(X[:,1])
        X[:,2] = leCurso.transform(X[:,2])
        X[:,3] = leFacul.transform(X[:,3])
        X[:,6] = leEc.transform(X[:,6])
        X[:,7] = dSimNao.get(X[0][7] )
        X = X.astype(float)

        alarme = modelo.predict(X)[0]
        st.subheader("Situação estimada do aluno em questão: %s"%alarme, )
