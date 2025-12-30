# ==============================================================================
# PROJETO AR LIMPO GV - APLICATIVO DASHBOARD FINAL
# ==============================================================================

import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Ar Limpo GV",
    page_icon="🍃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- LÓGICA DE SAÚDE ---
SAUDE_AR_INFO = {
    "Bom": {"significado": "Qualidade do ar considerada boa. 👍", "cor": "green", "recomendacoes": ["Atividades ao ar livre liberadas.", "Sem restrições para grupos sensíveis."]},
    "Moderada": {"significado": "Qualidade do ar aceitável. ⚠️", "cor": "orange", "recomendacoes": ["Grupos sensíveis devem reduzir atividades intensas.", "Mantenha-se hidratado."]},
    "Ruim": {"significado": "Qualidade do ar ruim. 🚨", "cor": "red", "recomendacoes": ["Evite atividades físicas ao ar livre.", "Grupos sensíveis podem ter agravamento de sintomas."]},
    "Muito Ruim": {"significado": "Qualidade do ar muito ruim. 😷", "cor": "darkred", "recomendacoes": ["Use máscara PFF2 se precisar sair.", "Cancele atividades ao ar livre."]},
    "Péssima": {"significado": "ALERTA GERAL! Risco extremo. 🚫", "cor": "darkred", "recomendacoes": ["Permaneça em casa com janelas fechadas.", "Risco sério para toda a população."]},
    "Indisponível": {"significado": "Dados indisponíveis. 🤷‍♀️", "cor": "gray", "recomendacoes": ["Sem dados."]}
}

def get_info_qualidade_ar(iqar_valor):
    try:
        iqar = int(iqar_valor)
        if 0 <= iqar <= 50: nivel = "Bom"
        elif 51 <= iqar <= 100: nivel = "Moderada"
        elif 101 <= iqar <= 150: nivel = "Ruim"
        elif 151 <= iqar <= 200: nivel = "Muito Ruim"
        else: nivel = "Péssima"
        return nivel, SAUDE_AR_INFO[nivel]
    except (ValueError, TypeError):
        return "Indisponível", SAUDE_AR_INFO["Indisponível"]

# --- COLETA DE DADOS ---
@st.cache_data(ttl=600)
def carregar_dados():
    try:
        # --- ATENÇÃO: CHAVE DE API REMOVIDA PARA SEGURANÇA ---
        # O usuário deve inserir sua chave ao rodar localmente
        SUA_CHAVE_API = "INSIRA_SUA_CHAVE_AQUI" 
        
        cidade = "Vitoria" 
        url_aqicn_api = f"https://api.waqi.info/feed/{cidade}/?token={SUA_CHAVE_API}"
        response_ar = requests.get(url_aqicn_api, timeout=15)
        dados_ar_json = response_ar.json()
        
        # Coleta Clima
        latitude = -20.31; longitude = -40.33
        url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        response_clima = requests.get(url_clima, timeout=10)
        dados_clima_json = response_clima.json()

        if dados_ar_json.get("status") == "ok":
            df_final = pd.DataFrame([{'IQAr': dados_ar_json['data']['aqi'], 
                                    'Estacao': dados_ar_json['data']['city']['name'], 
                                    'DataHora': dados_ar_json['data']['time']['s'], 
                                    'lat': dados_ar_json['data']['city']['geo'][0], 
                                    'lon': dados_ar_json['data']['city']['geo'][1]}])
            df_final['temperatura'] = dados_clima_json['current']['temperature_2m']
            df_final['umidade'] = dados_clima_json['current']['relative_humidity_2m']
            
            df_final['NivelRisco'], df_final['InfoSaude'] = zip(*df_final['IQAr'].apply(get_info_qualidade_ar))
            return df_final
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# --- DASHBOARD ---
st.title("🍃 Ar Limpo GV: Qualidade do Ar")
st.markdown(f"**Atualizado em:** _{datetime.now().strftime('%d/%m/%Y %H:%M')}_")

if st.button("🔄 Atualizar"):
    st.cache_data.clear()
    st.rerun()

dados = carregar_dados()

if dados is not None and not dados.empty:
    dados_atuais = dados.iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("IQAr", dados_atuais['IQAr'])
    col2.metric("Temp", f"{dados_atuais['temperatura']} °C")
    col3.metric("Umidade", f"{dados_atuais['umidade']} %")
    
    st.markdown("---")
    st.subheader(f"Status: {dados_atuais['NivelRisco']}")
    
    info = dados_atuais['InfoSaude']
    if info['cor'] == 'green': st.success(info['significado'])
    elif info['cor'] == 'orange': st.warning(info['significado'])
    else: st.error(info['significado'])
    
    st.write("**Recomendações:**")
    for rec in info['recomendacoes']:
        st.markdown(f"- {rec}")

    st.markdown("---")
    mapa = folium.Map(location=[dados_atuais['lat'], dados_atuais['lon']], zoom_start=12)
    folium.Marker([dados_atuais['lat'], dados_atuais['lon']], popup=dados_atuais['Estacao']).add_to(mapa)
    st_folium(mapa, width=700, height=300)
    
else:
    st.warning("Para ver os dados reais, clone o repositório e insira sua chave de API no código.")

st.caption("Projeto de Extensão Estácio - Nota 10")