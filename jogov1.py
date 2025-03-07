import streamlit as st
import re

# Função de validação de e-mail (verifica se contém "@" e um ponto)
def validar_email(email):
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email)

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Orientação Vocacional", layout="wide")

# --- DEFINIÇÃO DOS INTERESSES (80 CARTÕES) ---
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

# --- LISTA DE CURSOS DISPONÍVEIS ---
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

# --- DEFINIÇÃO DE PALAVRAS-CHAVE POR CURSO ---
# Foram adicionadas novas palavras-chave para que áreas como "Negócios", "Finanças" e afins contribuam também para "Gestão".
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

# --- GERENCIAMENTO DE PÁGINAS COM st.session_state ---
if "page" not in st.session_state:
    st.session_state.page = "selecao_interesses"

# Função para computar os cursos recomendados com base nos interesses selecionados
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

# --- PÁGINA 1: SELEÇÃO DE INTERESSES ---
if st.session_state.page == "selecao_interesses":
    st.title("Orientação Vocacional - Selecione os seus Interesses")
    st.markdown("Clique nos cartões abaixo para selecionar os seus hobbies e interesses:")

    if "selected_interesses" not in st.session_state:
        st.session_state.selected_interesses = []

    total_interesses = len(interesses)
    colunas_por_linha = 10
    linhas = total_interesses // colunas_por_linha

    # Cria a grid de 8 linhas e 10 colunas
    for i in range(linhas):
        cols = st.columns(colunas_por_linha)
        for j in range(colunas_por_linha):
            index = i * colunas_por_linha + j
            if index < total_interesses:
                inter = interesses[index]
                selecionado = cols[j].checkbox(inter, key=f"chk_{index}")
                if selecionado and inter not in st.session_state.selected_interesses:
                    st.session_state.selected_interesses.append(inter)
                elif not selecionado and inter in st.session_state.selected_interesses:
                    st.session_state.selected_interesses.remove(inter)

    st.write("### Interesses Selecionados:")
    st.write(st.session_state.selected_interesses)

    if st.button("Ver cursos compatíveis com os meus interesses"):
        st.session_state.page = "resultado_cursos"
        st.rerun()

# --- PÁGINA 2: RESULTADOS E CONTATO ---
elif st.session_state.page == "resultado_cursos":
    st.title("Cursos Compatíveis no ISMT")
    st.markdown("Com base nos seus interesses, recomendamos os seguintes cursos:")

    recomendados = obter_cursos_recomendados(st.session_state.selected_interesses)

    # Determina o máximo de pontos e define um threshold (50% do máximo)
    max_score = max(recomendados.values()) if recomendados else 0
    threshold = 0.5 * max_score

    # Exibe todos os cursos, destacando os compatíveis
    for curso in cursos:
        if curso in recomendados:
            score = recomendados[curso]
            # Se o curso atingir ou ultrapassar o threshold, destaca-o
            if score >= threshold:
                st.markdown(f"**:star: {curso} (compatibilidade: {score})**")
            else:
                st.markdown(f"{curso} (compatibilidade: {score})")
        else:
            st.markdown(curso)

    st.markdown("---")
    st.markdown("Para mais informações, por favor, indique o seu nome e e-mail:")

    nome = st.text_input("Nome")
    email = st.text_input("E-mail")

    if st.button("Enviar"):
        if nome and email:
            if not validar_email(email):
                st.error("Por favor, introduza um e-mail válido.")
            else:
                st.success("Obrigado! Em breve entraremos em contacto.")
                # Aqui, pode-se implementar o envio de e-mail ou o armazenamento dos dados.
        else:
            st.error("Por favor, preencha ambos os campos: nome e e-mail.")
