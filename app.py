"""Tela do AulaCerta. Rode com: streamlit run app.py"""
import json
import os

import streamlit as st

from cadeia_backup import ErroAulaCerta, gerar_plano, plano_em_markdown

st.set_page_config(page_title="AulaCerta", page_icon="📐", layout="centered")
st.title("📐 AulaCerta")
st.caption("Planos de aula de Matemática com habilidades da BNCC conferidas numa base oficial.")

if not os.getenv("OPENAI_API_KEY"):
    st.error("Chave da OpenAI não encontrada. Crie o arquivo .env com OPENAI_API_KEY=... (veja o README).")
    st.stop()

with st.form("pedido"):
    col1, col2 = st.columns(2)
    serie = col1.selectbox("Série", [6, 7, 8, 9], index=2, format_func=lambda s: f"{s}º ano")
    duracao = col2.number_input("Duração (minutos)", min_value=20, max_value=200, value=50, step=5)
    tema = st.text_input("Tema da aula", placeholder="Ex.: equações do 1º grau")
    perfil = st.text_area("Perfil da turma (opcional)", placeholder="Ex.: turma com dificuldade em frações")
    enviar = st.form_submit_button("Gerar plano de aula", type="primary")

if enviar:
    if not tema.strip():
        st.warning("Escreva o tema da aula.")
        st.stop()
    try:
        with st.status("Gerando o plano...", expanded=True) as status:
            resultado = gerar_plano(serie, tema, int(duracao), perfil, ao_avancar=st.write)
            status.update(label="Plano pronto!", state="complete", expanded=False)
    except ErroAulaCerta as erro:
        st.error(str(erro))
        st.stop()
    except Exception as erro:  # erro de rede, chave inválida, falta de crédito...
        st.error(f"Não foi possível falar com a OpenAI: {erro}")
        st.stop()
    st.session_state["resultado"] = resultado

resultado = st.session_state.get("resultado")
if resultado:
    aba_plano, aba_verificacao, aba_cadeia = st.tabs(["Plano de aula", "Verificação", "Cadeia de prompts"])

    with aba_plano:
        markdown = plano_em_markdown(resultado)
        st.markdown(markdown)
        st.download_button("Baixar plano (.md)", markdown, file_name="plano_de_aula.md")

    with aba_verificacao:
        st.subheader("Conferido pelo código")
        for v in resultado["verificacoes_codigo"]:
            icone = "✅" if v["resultado"] == "OK" else "⚠️"
            st.write(f"{icone} **{v['pergunta']}** {v['detalhe']}")
        st.subheader("Conferido pelo prompt 4 (CoVe)")
        for v in resultado["verificacoes_modelo"]:
            icone = "✅" if str(v.get("resultado", "")).upper() == "OK" else "✏️"
            st.write(f"{icone} **{v.get('pergunta', '')}** {v.get('detalhe', '')}")

    with aba_cadeia:
        st.caption(f"Log desta execução salvo em: {resultado['arquivo_log']}")
        st.markdown("**Prompt 1 – Análise do pedido**")
        st.json(resultado["analise"])
        st.markdown("**Busca na base – habilidades candidatas**")
        st.write(", ".join(resultado["candidatas"]))
        st.markdown("**Prompt 2 – Seleção de habilidades**")
        st.json(resultado["selecao"])
        st.markdown("**Prompts 3 e 4 – Plano final (JSON)**")
        st.code(json.dumps(resultado["plano"], ensure_ascii=False, indent=2), language="json")
