"""🦄 El Reino de los Números Romanos
App Streamlit para aprender números romanos (3.º de Primaria):
  📖 Aprende  ·  ✏️ Ejercicios de la libreta  ·  🎮 Juego por niveles  ·  🔮 Conversor
"""
import random

import streamlit as st

st.set_page_config(
    page_title="El Reino de los Números Romanos",
    page_icon="🦄",
    layout="centered",
)

# ───────────────────────── Lógica ─────────────────────────
SIMBOLOS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
VALORES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

# Ejercicios de la libreta (29/09/2026)
EJERCICIOS = ["XXII", "LXXI", "VIII", "XXXVII", "MCCLXI",
              "IX", "MXI", "MMCIV", "XXIV", "MDCCXXIV"]

NIVELES = {
    "🌱 Nivel 1: hasta 20": (1, 20),
    "🌼 Nivel 2: hasta 100": (1, 100),
    "🌈 Nivel 3: hasta 500": (1, 500),
    "👑 Nivel 4: hasta 2000": (1, 2000),
    "🦄 Nivel 5: hasta 3999": (1, 3999),
}
R2N, N2R, MIX = "Romano → número", "Número → romano", "Mezcla"


def a_romano(n: int) -> str:
    res = ""
    for v, s in VALORES:
        while n >= v:
            res += s
            n -= v
    return res


def a_numero(texto: str):
    """Devuelve el valor si es un romano bien escrito; si no, None."""
    t = texto.strip().upper()
    if not t or any(c not in SIMBOLOS for c in t):
        return None
    total = 0
    for i, c in enumerate(t):
        v = SIMBOLOS[c]
        if i + 1 < len(t) and SIMBOLOS[t[i + 1]] > v:
            total -= v
        else:
            total += v
    return total if total > 0 and a_romano(total) == t else None


def trozos(t: str):
    res, i = [], 0
    while i < len(t):
        if i + 1 < len(t) and SIMBOLOS[t[i + 1]] > SIMBOLOS[t[i]]:
            res.append((t[i:i + 2], SIMBOLOS[t[i + 1]] - SIMBOLOS[t[i]]))
            i += 2
        else:
            res.append((t[i], SIMBOLOS[t[i]]))
            i += 1
    return res


def explicar_romano(t: str) -> str:
    partes = trozos(t)
    suma = " + ".join(f"{s} ({v})" for s, v in partes)
    return f"**{t}** = {suma} = **{sum(v for _, v in partes)}**"


def explicar_numero(n: int) -> str:
    partes, resto = [], n
    for v, s in VALORES:
        while resto >= v:
            partes.append((v, s))
            resto -= v
    nums = " + ".join(str(v) for v, _ in partes)
    rom = " ".join(s for _, s in partes)
    return f"**{n}** = {nums} → {rom} → **{a_romano(n)}**"


def es_numero_correcto(resp: str, n: int) -> bool:
    try:
        return int(resp.strip()) == n
    except ValueError:
        return False


# ───────────────────────── Estilo ─────────────────────────
st.markdown(
    """
<style>
.stApp {background: linear-gradient(160deg,#fdf2ff 0%,#eef6ff 55%,#fff7ec 100%);}
.titulo {text-align:center;padding:18px 10px;border-radius:24px;
  background:linear-gradient(90deg,#b388ff,#7dd3fc);color:white;
  box-shadow:0 6px 18px rgba(124,77,255,.25);margin-bottom:14px;}
.titulo h1 {color:white;margin:0;font-size:2rem;}
.titulo p {margin:4px 0 0;font-size:1.05rem;color:white;}
.tarjeta {background:white;border-radius:20px;padding:10px 4px;text-align:center;
  box-shadow:0 4px 12px rgba(0,0,0,.08);border:2px solid #e9d5ff;}
.tarjeta .rom {font-size:2rem;font-weight:800;color:#7c3aed;}
.tarjeta .num {font-size:1.15rem;color:#0ea5e9;font-weight:700;}
.grande {font-size:2.6rem;font-weight:800;color:#7c3aed;text-align:center;
  letter-spacing:5px;background:white;border-radius:24px;padding:12px;
  border:3px dashed #c4b5fd;margin:8px 0;}
.mini {font-size:1.7rem;font-weight:800;color:#7c3aed;background:white;
  border-radius:16px;padding:6px 12px;border:2px dashed #c4b5fd;margin-top:6px;}
.caja {background:white;color:#334155;border-left:8px solid #c4b5fd;
  border-radius:14px;padding:10px 16px;margin:8px 0;
  box-shadow:0 2px 8px rgba(0,0,0,.05);}
/* Pestañas: siempre en rojo (activas o no) */
.stApp button[data-baseweb="tab"] p,
.stApp button[data-baseweb="tab"] {color:#ef4444 !important;font-weight:700;}
.stApp button[data-baseweb="tab"][aria-selected="false"] {opacity:.75;}
/* Títulos y textos: legibles aunque el móvil esté en modo oscuro */
.stApp h2, .stApp h3, .stApp h4,
.stApp h2 *, .stApp h3 *, .stApp h4 * {color:#5b21b6 !important;}
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stCaptionContainer"],
.stApp label, .stApp label p {color:#334155 !important;}
.stApp [data-testid="stMetricLabel"] *, .stApp [data-testid="stMetricValue"] * {color:#5b21b6 !important;}
.stApp .titulo h1, .stApp .titulo p {color:white !important;}
.stApp .tarjeta .rom {color:#7c3aed !important;}
.stApp .tarjeta .num {color:#0ea5e9 !important;}
.stApp .grande, .stApp .mini {color:#7c3aed !important;}
/* Botones: fondo morado y texto blanco siempre */
.stApp .stButton button,
.stApp [data-testid="stFormSubmitButton"] button,
.stApp [data-testid^="stBaseButton"] {
  background:linear-gradient(90deg,#8b5cf6,#38bdf8) !important;
  border:none !important;border-radius:16px !important;
  box-shadow:0 4px 10px rgba(124,58,237,.25);}
.stApp .stButton button *,
.stApp [data-testid="stFormSubmitButton"] button *,
.stApp [data-testid^="stBaseButton"] * {color:#ffffff !important;font-weight:700;}
/* Campos de texto, listas y desplegables: fondo blanco y letra oscura */
.stApp input, .stApp textarea {background:#ffffff !important;color:#334155 !important;
  -webkit-text-fill-color:#334155 !important;}
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"],
.stApp [data-baseweb="select"] > div {background:#ffffff !important;color:#334155 !important;
  border-radius:12px;}
.stApp [data-baseweb="select"] * {color:#334155 !important;}
.stApp [data-testid="stNumberInput"] button {background:#f3e8ff !important;}
.stApp [data-testid="stNumberInput"] button * {color:#5b21b6 !important;}
.stApp [data-testid="stExpander"] {background:#ffffff;border-radius:14px;}
.stApp [data-testid="stExpander"] summary *,
.stApp [data-testid="stExpander"] p {color:#5b21b6 !important;}
.stApp [data-testid="stForm"] {background:rgba(255,255,255,.6);border-radius:18px;}
</style>
<div class="titulo">
  <h1>🦄 El Reino de los Números Romanos ✨</h1>
  <p>¡Aprende, practica y conviértete en Princesa de los Romanos! 🧚‍♀️</p>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📖 Aprende", "✏️ Mi libreta", "🎮 Juego", "🔮 Conversor"]
)

# ───────────────────────── 📖 Aprende ─────────────────────────
with tab1:
    st.subheader("🔤 Las 7 letras mágicas")
    cols = st.columns(7)
    for col, (s, v) in zip(cols, SIMBOLOS.items()):
        col.markdown(
            f'<div class="tarjeta"><div class="rom">{s}</div>'
            f'<div class="num">{v}</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="caja">🧠 <b>Truco para recordarlas</b> (de la más grande a la más pequeña):<br>'
        "<b>M</b>i <b>D</b>ulce <b>C</b>orcel <b>L</b>leva <b>X</b>ilófonos "
        "<b>V</b>erdes <b>I</b>ncreíbles 🦄</div>",
        unsafe_allow_html=True,
    )

    st.subheader("📜 Las reglas del reino")
    st.markdown(
        '<div class="caja">➕ <b>Regla 1 · Sumar.</b> Si una letra igual o más pequeña va '
        "<b>detrás</b>, se suma.<br>"
        "VI = 5 + 1 = <b>6</b> &nbsp;·&nbsp; XXII = 10 + 10 + 1 + 1 = <b>22</b></div>"
        '<div class="caja">3️⃣ <b>Regla 2 · Máximo tres.</b> I, X, C y M se pueden repetir '
        "hasta <b>3 veces</b> seguidas: III = 3, XXX = 30. "
        "<b>V, L y D nunca se repiten.</b></div>"
        '<div class="caja">➖ <b>Regla 3 · Restar.</b> Si una letra pequeña va '
        "<b>delante</b> de una más grande, se resta. Solo se puede restar:<br>"
        "<b>I</b> delante de V o X → IV = 4, IX = 9<br>"
        "<b>X</b> delante de L o C → XL = 40, XC = 90<br>"
        "<b>C</b> delante de D o M → CD = 400, CM = 900</div>"
        '<div class="caja">🧩 <b>Truco final · Descompón.</b> Separa el número en miles, '
        "centenas, decenas y unidades:<br>"
        "1724 = 1000 + 700 + 20 + 4 → <b>M</b> + <b>DCC</b> + <b>XX</b> + <b>IV</b> "
        "= <b>MDCCXXIV</b></div>",
        unsafe_allow_html=True,
    )

    st.subheader("🔢 Del 1 al 20")
    filas = st.columns(5)
    for n in range(1, 21):
        with filas[(n - 1) % 5]:
            st.markdown(
                f'<div class="tarjeta" style="margin-bottom:8px"><span class="num">{n}</span>'
                f' = <span class="rom" style="font-size:1.3rem">{a_romano(n)}</span></div>',
                unsafe_allow_html=True,
            )

# ───────────────────────── ✏️ Mi libreta ─────────────────────────
with tab2:
    st.subheader("✏️ Los ejercicios de mi libreta")
    st.caption("Escribe el número que corresponde a cada número romano.")

    with st.form("form_libreta"):
        c1, c2 = st.columns(2)
        for i, r in enumerate(EJERCICIOS):
            with (c1 if i < 5 else c2):
                st.markdown(f'<div class="mini">{i + 1}. {r}</div>', unsafe_allow_html=True)
                st.text_input(
                    f"Respuesta {i + 1}", key=f"ej_{i}",
                    label_visibility="collapsed", placeholder="= ?",
                )
        enviar = st.form_submit_button("Comprobar todo ✨", use_container_width=True)

    if enviar:
        aciertos = 0
        for i, r in enumerate(EJERCICIOS):
            n = a_numero(r)
            resp = st.session_state.get(f"ej_{i}", "")
            if es_numero_correcto(resp, n):
                aciertos += 1
                st.success(f"✅ {i + 1}. {explicar_romano(r)}")
            else:
                st.error(f"💡 {i + 1}. Casi… mira cómo se hace: {explicar_romano(r)}")
        st.markdown(f"### {'⭐' * aciertos}{'☆' * (10 - aciertos)}  {aciertos}/10")
        if aciertos == 10:
            st.balloons()
            st.success("🦄 ¡Perfecto! ¡Eres una Princesa de los Números Romanos! 👑")
        elif aciertos >= 7:
            st.info("🌈 ¡Muy bien! Repasa los que te han fallado y vuelve a intentarlo.")
        else:
            st.info("🧚‍♀️ ¡Ánimo! Mira las reglas en la pestaña 📖 y prueba otra vez.")

    def _limpiar():
        for j in range(len(EJERCICIOS)):
            st.session_state[f"ej_{j}"] = ""

    st.button("🔄 Borrar respuestas", on_click=_limpiar)

    with st.expander("🔎 Ver todas las soluciones paso a paso"):
        for i, r in enumerate(EJERCICIOS):
            st.markdown(f"{i + 1}. {explicar_romano(r)}")

# ───────────────────────── 🎮 Juego ─────────────────────────
with tab3:
    ss = st.session_state
    for k, v in dict(puntos=0, racha=0, mejor=0, hechas=0, fb=None, q=None, globos=False).items():
        ss.setdefault(k, v)

    c1, c2 = st.columns(2)
    nivel = c1.selectbox("Nivel", list(NIVELES), index=0)
    modo = c2.selectbox("¿Qué quieres practicar?", [R2N, N2R, MIX], index=2)

    def nueva_pregunta():
        lo, hi = NIVELES[nivel]
        tipo = modo if modo != MIX else random.choice([R2N, N2R])
        return {"n": random.randint(lo, hi), "tipo": tipo, "nivel": nivel, "modo": modo}

    if ss.q is None or ss.q["nivel"] != nivel or ss.q["modo"] != modo:
        ss.q = nueva_pregunta()

    m1, m2, m3 = st.columns(3)
    m1.metric("⭐ Estrellas", ss.puntos)
    m2.metric("🔥 Racha", ss.racha)
    m3.metric("🏆 Mejor racha", ss.mejor)

    if ss.fb:
        ok, msg = ss.fb
        (st.success if ok else st.error)(msg)
    if ss.globos:
        st.balloons()
        ss.globos = False

    q = ss.q
    with st.form("form_juego", clear_on_submit=True):
        if q["tipo"] == R2N:
            st.markdown(f'<div class="grande">{a_romano(q["n"])}</div>', unsafe_allow_html=True)
            st.markdown("**¿Qué número es?** 🔢")
        else:
            st.markdown(f'<div class="grande">{q["n"]}</div>', unsafe_allow_html=True)
            st.markdown("**Escríbelo en números romanos** 🏛️ (con letras: I, V, X, L, C, D, M)")
        resp = st.text_input("Tu respuesta", key="resp_juego", label_visibility="collapsed")
        ok_btn = st.form_submit_button("Comprobar ✨", use_container_width=True)

    if ok_btn:
        n = q["n"]
        if q["tipo"] == R2N:
            acierto = es_numero_correcto(resp, n)
            expl = explicar_romano(a_romano(n))
        else:
            acierto = a_numero(resp) == n
            expl = explicar_numero(n)
        ss.hechas += 1
        if acierto:
            ss.puntos += 1
            ss.racha += 1
            ss.mejor = max(ss.mejor, ss.racha)
            frase = random.choice(["¡Genial! 🦄", "¡Magia pura! ✨", "¡Bravo! 🌈", "¡Estupendo! 🧚‍♀️"])
            ss.fb = (True, f"{frase} {expl}")
            if ss.racha % 5 == 0:
                ss.globos = True
        else:
            ss.racha = 0
            ss.fb = (False, f"💡 Casi… se hace así: {expl}")
        ss.q = nueva_pregunta()
        st.rerun()

    if st.button("🔄 Empezar de cero"):
        for k in ("puntos", "racha", "mejor", "hechas"):
            ss[k] = 0
        ss.fb = None
        ss.q = nueva_pregunta()
        st.rerun()

# ───────────────────────── 🔮 Conversor ─────────────────────────
with tab4:
    st.subheader("🔮 El conversor mágico")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Romano → número**")
        t = st.text_input("Escribe un número romano", key="conv_r", placeholder="Ej.: MCMXC")
        if t.strip():
            if a_numero(t) is None:
                st.warning("🤔 Ese número romano no está bien escrito. Revisa las reglas.")
            else:
                st.markdown(explicar_romano(t.strip().upper()))
    with c2:
        st.markdown("**Número → romano**")
        num = st.number_input("Escribe un número (1 a 3999)", min_value=1, max_value=3999,
                              value=1724, step=1, key="conv_n")
        st.markdown(explicar_numero(int(num)))
