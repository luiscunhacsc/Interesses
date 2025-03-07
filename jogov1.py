import streamlit as st
import re

# ------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------

# Validação de e-mail
def validar_email(email):
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email)

# Função para obter um ícone para cada interesse
def get_icon(interest):
    i = interest.lower()
    if "cinema" in i:
        return "🎬"
    elif "música" in i:
        return "🎵"
    elif "fotografia" in i:
        return "📷"
    elif any(x in i for x in ["arte", "design", "ilustração", "pintura", "escultura", "moda", "animação", "publicidade", "comunicação visual", "arquitetura"]):
        return "🎨"
    elif any(x in i for x in ["programação", "software", "jogos", "robótica", "inteligência artificial", "cibersegurança", "hardware", "redes"]):
        return "💻"
    elif any(x in i for x in ["empreendedorismo", "negócios", "finanças", "investimentos", "marketing", "planeamento", "gestão"]):
        return "💼"
    elif any(x in i for x in ["psicologia", "comportamento", "neuro", "bem-estar", "autoconhecimento", "sociologia", "antropologia"]):
        return "🧠"
    elif any(x in i for x in ["serviço social", "direitos", "comunitário", "voluntariado", "sustentabilidade", "cidadania", "educação", "políticas"]):
        return "🤝"
    elif any(x in i for x in ["comunicação empresarial", "relações públicas", "mídias sociais", "eventos", "branding", "networking", "liderança"]):
        return "📢"
    elif any(x in i for x in ["reportagem", "investigação", "jornalismo", "redação", "telejornalismo", "entrevistas"]):
        return "📰"
    else:
        return "⭐"

# Função para alternar (toggle) um interesse ao clicar no cartão
def toggle_interest(interest):
    if interest in st.session_state.selected_interesses:
        st.session_state.selected_interesses.remove(interest)
    else:
        st.session_state.selected_interesses.append(interest)
    st.rerun()

# Função para calcular os cursos recomendados (lógica com pontuação ponderada)
def obter_cursos_recomendados(selecionados):
    recomendados = {}
    for curso, keywords in course_keywords.items():
        score = 0
        for inter in selecionados:
            inter_clean = inter.lower().strip()
            for kw in keywords:
                kw_clean = kw.lower().strip()
                if inter_clean == kw_clean:
                    score += 2  # correspondência exata
                elif kw_clean in inter_clean:
                    score += 1  # correspondência parcial
        if score > 0:
            recomendados[curso] = score
    return recomendados

# ------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------
st.set_page_config(page_title="Orientação Vocacional", layout="wide")

# Inicialização das variáveis de sessão
if "page" not in st.session_state:
    st.session_state.page = "selecao_interesses"
if "selected_interesses" not in st.session_state:
    st.session_state.selected_interesses = []
if "verInteressesDev" not in st.session_state:
    st.session_state.verInteressesDev = False  # por defeito, não mostra a lista de interesses

# Lista de interesses (80 cartões)
interesses = [
    # Linha 1
    "Arte Digital", "Design Gráfico", "Fotografia", "Cinema", "Música", "Literatura", "Teatro", "Dança", "Pintura", "Escultura",
    # Linha 2
    "Animação", "Moda", "Publicidade", "Comunicação Visual", "Arquitetura", "Ilustração", "Design de Interiores", "Artes Plásticas", "Escultura Contemporânea", "Artes Cênicas",
    # Linha 3
    "Programação", "Desenvolvimento de Software", "Jogos Digitais", "Realidade Virtual", "Robótica", "Inteligência Artificial", "Ciência de Dados", "Cibersegurança", "Hardware", "Redes de Computadores",
    # Linha 4
    "Empreendedorismo", "Startups", "Inovação", "Marketing Digital", "Negócios", "Finanças", "Investimentos", "Economia", "Planeamento Estratégico", "Gestão de Projectos",
    # Linha 5
    "Psicologia", "Sociologia", "Antropologia", "Comportamento Humano", "Saúde Mental", "Neurociência", "Psicoterapia", "Desenvolvimento Pessoal", "Bem-estar", "Autoconhecimento",
    # Linha 6
    "Ciências Sociais", "Serviço Social", "Ativismo", "Direitos Humanos", "Educação", "Políticas Públicas", "Engajamento Comunitário", "Voluntariado", "Sustentabilidade", "Cidadania",
    # Linha 7
    "Comunicação Empresarial", "Relações Públicas", "Assessoria de Imprensa", "Mídias Sociais", "Eventos", "Branding", "Marketing de Influência", "Comunicação Organizacional", "Liderança", "Networking",
    # Linha 8
    "Reportagem", "Investigação", "Redação Jornalística", "Mídia Digital", "Telejornalismo", "Edição de Vídeo", "Fotografia Jornalística", "Entrevistas", "Recrutamento", "Formação"
]

# Lista de cursos disponíveis
cursos = [
    "Design de Comunicação",
    "Multimédia",
    "Jornalismo",
    "Comunicação Empresarial",
    "Empreendedorismo",
    "Gestão",
    "Gestão de Recursos Humanos",
    "Psicologia",
    "Serviço Social",
    "Informática"
]

# Dicionário de palavras-chave para cada curso
course_keywords = {
    "Design de Comunicação": ["arte", "design", "fotografia", "ilustração", "pintura", "escultura", "moda", "publicidade", "comunicação visual"],
    "Multimédia": ["animação", "cinema", "música", "edição de vídeo", "multimédia", "design gráfico", "fotografia"],
    "Jornalismo": ["reportagem", "investigação", "redação", "entrevistas", "mídia digital", "telejornalismo"],
    "Comunicação Empresarial": ["comunicação empresarial", "marketing", "branding", "relações públicas", "mídias sociais", "eventos", "networking"],
    "Empreendedorismo": ["empreendedorismo", "startups", "inovação", "negócios", "planeamento estratégico"],
    "Gestão": ["gestão", "planeamento", "liderança", "gestão de projectos", "negócios", "finanças", "investimentos", "economia"],
    "Gestão de Recursos Humanos": ["recursos humanos", "formação", "desenvolvimento de talentos", "cultura organizacional", "diversidade", "inclusão"],
    "Psicologia": ["psicologia", "comportamento humano", "neurociência", "bem-estar", "autoconhecimento"],
    "Serviço Social": ["serviço social", "direitos humanos", "engajamento comunitário", "voluntariado", "sustentabilidade", "cidadania"],
    "Informática": ["programação", "desenvolvimento de software", "jogos digitais", "realidade virtual", "robótica", "inteligência artificial", "ciência de dados", "cibersegurança", "hardware", "redes de computadores"]
}

# Dicionário de ícones para os cursos
course_icons = {
    "Design de Comunicação": "🎨",
    "Multimédia": "🖥️",
    "Jornalismo": "📰",
    "Comunicação Empresarial": "📢",
    "Empreendedorismo": "💼",
    "Gestão": "📊",
    "Gestão de Recursos Humanos": "🤝",
    "Psicologia": "🧠",
    "Serviço Social": "🤝",
    "Informática": "💻"
}

# ------------------------------
# PÁGINA 1: SELEÇÃO DE INTERESSES
# ------------------------------
if st.session_state.page == "selecao_interesses":
    st.markdown(
        '<div class="main-header"><h1>Bem-vindo à Orientação Vocacional do ISMT</h1><p>Descobre os cursos que combinam com os teus interesses!</p></div>',
        unsafe_allow_html=True
    )
    st.markdown("### Seleciona os teus hobbies e interesses (clicando nos cartões):")
    
    total_interesses = len(interesses)
    # Ajusta o número de colunas para maximizar a visibilidade (ex: 10 colunas)
    colunas_por_linha = 10  
    linhas = total_interesses // colunas_por_linha
    
    # Organiza os cartões numa grelha
    for i in range(linhas):
        cols = st.columns(colunas_por_linha)
        for j in range(colunas_por_linha):
            index = i * colunas_por_linha + j
            if index < total_interesses:
                inter = interesses[index]
                icon = get_icon(inter)
                label = f"{icon} {inter}"
                if inter in st.session_state.selected_interesses:
                    label = f"✅ {label}"
                # Cada botão, ao ser clicado, alterna o interesse
                cols[j].button(label, key=f"card_{index}", on_click=lambda inter=inter: toggle_interest(inter))
    
    # Mostra a lista de interesses selecionados apenas se a flag verInteressesDev for True
    if st.session_state.verInteressesDev:
        st.markdown("### Interesses Selecionados:")
        st.write(st.session_state.selected_interesses)
    
    if st.button("Ver cursos compatíveis com os meus interesses"):
        st.session_state.page = "resultado_cursos"
        st.rerun()

# ------------------------------
# PÁGINA 2: RESULTADOS E CONTATO
# ------------------------------
elif st.session_state.page == "resultado_cursos":
    st.markdown(
        '<div class="main-header"><h1>Cursos Compatíveis</h1><p>Estes cursos combinam com os teus interesses!</p></div>',
        unsafe_allow_html=True
    )
    
    # Botão para voltar à seleção de interesses
    if st.button("Voltar à seleção de interesses"):
        st.session_state.page = "selecao_interesses"
        st.rerun()
    
    recomendados = obter_cursos_recomendados(st.session_state.selected_interesses)
    max_score = max(recomendados.values()) if recomendados else 0
    threshold = 0.5 * max_score

    for curso in cursos:
        if curso in recomendados:
            score = recomendados[curso]
            icon = course_icons.get(curso, "⭐")
            if score >= threshold:
                st.markdown(f"**:star: {icon} {curso} (compatibilidade: {score})**")
            else:
                st.markdown(f"{icon} {curso} (compatibilidade: {score})")
        else:
            st.markdown(curso)

    st.markdown("---")
    st.markdown("Para mais informações, indica o teu nome e e-mail:")
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")

    if st.button("Enviar"):
        if nome and email:
            if not validar_email(email):
                st.error("Por favor, introduz um e-mail válido.")
            else:
                st.success("Obrigado! Em breve entraremos em contacto.")
        else:
            st.error("Por favor, preenche ambos os campos: nome e e-mail.")
