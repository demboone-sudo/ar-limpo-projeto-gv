# 🍃 Ar Limpo GV: Monitoramento da Qualidade do Ar

Este projeto é um Dashboard interativo desenvolvido em Python para o monitoramento em tempo real da qualidade do ar e condições climáticas na região da Grande Vitória (ES). Através da integração de APIs globais, a aplicação oferece dados precisos e recomendações de saúde para a população local.

## 🎯 Objetivo
O projeto visa democratizar o acesso a dados ambientais, auxiliando pessoas com problemas respiratórios, atletas e a comunidade em geral a tomarem decisões informadas sobre atividades ao ar livre baseadas no **IQAr (Índice de Qualidade do Ar)**.

## 🚀 Funcionalidades
- **Métricas em Tempo Real:** Exibição de IQAr, Temperatura e Umidade.
- **Lógica de Saúde:** Classificação automática com alertas visuais (Verde, Laranja, Vermelho) e recomendações específicas.
- **Geolocalização:** Mapa interativo mostrando a localização exata da estação de monitoramento.
- **Cache Inteligente:** Otimização de requisições de API para maior velocidade e economia de dados.

## 🛠️ Tecnologias e Bibliotecas
- **Python 3.x**
- **Streamlit:** Framework para a interface web.
- **Pandas:** Manipulação e estruturação dos dados.
- **Folium & Streamlit-Folium:** Visualização de mapas interativos.
- **Requests:** Consumo das APIs REST.
- **APIs Integradas:**
  - [AQICN (World Air Quality Index)](https://aqicn.org/api/): Dados de poluição atmosférica.
  - [Open-Meteo](https://open-meteo.com/): Dados climáticos de alta precisão.

## 📦 Como Rodar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/ar-limpo-gv.git](https://github.com/seu-usuario/ar-limpo-gv.git)

2. **Instalar as dependências:**
   Bashpip install streamlit pandas requests folium streamlit-folium
   
3. **Configurar a API Key:**
   Obtenha seu token em **waqi.info**.No código, substitua a variável SUA_CHAVE_API pelo seu token.
4. **Executar a aplicação:**
   Bashstreamlit run app.py
📊 Classificação do Ar (Escala Utilizada)
Índice      Nível            Ação Recomendada
0 - 50       Bom            Atividades normais.
51 - 100   Moderado        Grupos sensíveis devem ter cautela.
101 - 150   Ruim           Evitar esforço pesado ao ar livre.
151+       Crítico         Permanecer em locais fechados.





   
