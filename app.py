import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import hashlib

st.set_page_config(
    page_title="CEIMA • Sistema de Pagos",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

:root {
    --verde-oscuro: #1a5c2a;
    --verde-medio: #2d7a3e;
    --verde-claro: #4a9e5c;
    --verde-bg: #f0f7f1;
    --verde-borde: #c8e6c9;
    --dorado: #c8a52a;
    --dorado-claro: #f0d060;
    --blanco: #ffffff;
    --gris-texto: #2c2c2c;
    --gris-muted: #6b7280;
    --gris-bg: #f8faf8;
    --rojo: #c0392b;
    --amarillo: #d97706;
    --verde-ok: #1a5c2a;
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    color: var(--gris-texto);
    background-color: var(--gris-bg);
}

.main { background: var(--gris-bg); }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--verde-oscuro) !important;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stRadio label { color: white !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }

/* HEADINGS */
h1, h2, h3 {
    font-family: 'Merriweather', serif;
    color: var(--verde-oscuro);
}

/* BUTTONS */
.stButton > button {
    background: var(--verde-oscuro) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--verde-medio) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(26,92,42,0.25) !important;
}

/* INPUTS */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background: white !important;
    border: 1.5px solid var(--verde-borde) !important;
    color: var(--gris-texto) !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus {
    border-color: var(--verde-medio) !important;
    box-shadow: 0 0 0 3px rgba(45,122,62,0.15) !important;
}

/* METRICS */
div[data-testid="metric-container"] {
    background: white;
    border: 1.5px solid var(--verde-borde);
    border-radius: 10px;
    padding: 1.2rem;
    border-left: 4px solid var(--verde-oscuro) !important;
}
div[data-testid="metric-container"] label {
    color: var(--gris-muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="metric-container"] div[data-testid="metric-value"] {
    color: var(--verde-oscuro) !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--verde-borde);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--gris-muted);
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: var(--verde-oscuro) !important;
    border-bottom: 2px solid var(--verde-oscuro) !important;
    font-weight: 700 !important;
}

/* DATAFRAME */
.stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid var(--verde-borde); }

/* CARDS */
.ceima-card {
    background: white;
    border: 1.5px solid var(--verde-borde);
    border-radius: 10px;
    padding: 1.4rem;
    margin-bottom: 1rem;
}
.ceima-header {
    background: var(--verde-oscuro);
    color: white;
    padding: 0.8rem 1.4rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.ceima-header h2 {
    color: white !important;
    margin: 0;
    font-size: 1.3rem;
}

/* BADGES */
.badge-green {
    background: #d4edda; color: #1a5c2a;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #a8d5b0;
}
.badge-yellow {
    background: #fff3cd; color: #856404;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #ffc107;
}
.badge-red {
    background: #f8d7da; color: #721c24;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #f5c6cb;
}

/* RESUMEN PAGO */
.resumen-pago {
    background: var(--verde-bg);
    border: 2px solid var(--verde-borde);
    border-radius: 10px;
    padding: 1.4rem;
}
.resumen-total {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--verde-oscuro);
    font-family: 'Merriweather', serif;
}

/* LOGIN */
.login-container {
    background: white;
    border: 1.5px solid var(--verde-borde);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px rgba(26,92,42,0.1);
}
.login-logo {
    text-align: center;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--verde-borde);
    margin-bottom: 1.5rem;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: var(--verde-bg) !important;
    border: 1px solid var(--verde-borde) !important;
    border-radius: 6px !important;
    color: var(--verde-oscuro) !important;
    font-weight: 600 !important;
}

/* ALERTS */
.stSuccess { border-left: 4px solid var(--verde-oscuro) !important; }
.stWarning { border-left: 4px solid var(--dorado) !important; }
.stError { border-left: 4px solid var(--rojo) !important; }

div[data-testid="stForm"] {
    background: white;
    border: 1.5px solid var(--verde-borde);
    border-radius: 10px;
    padding: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── DATABASE ──────────────────────────────────────────────────────────────────
DB = "ceima.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT
    );
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        nivel TEXT NOT NULL,
        grado TEXT NOT NULL,
        grupo TEXT NOT NULL,
        tutor TEXT,
        contacto TEXT,
        email TEXT,
        activo INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        monto REAL NOT NULL,
        meses_pagados TEXT NOT NULL,
        fecha_pago TEXT NOT NULL,
        forma_pago TEXT DEFAULT 'Efectivo',
        pronto_pago INTEGER DEFAULT 0,
        descuento REAL DEFAULT 0,
        monto_original REAL,
        folio TEXT UNIQUE,
        registrado_por TEXT,
        notas TEXT,
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id)
    );
    """)
    pw = hashlib.sha256("ceima2024".encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO usuarios (username, password, nombre) VALUES (?,?,?)",
              ("admin", pw, "Administrador"))
    conn.commit()
    conn.close()

init_db()

# ── HELPERS ───────────────────────────────────────────────────────────────────
COLEGIATURAS = {"Secundaria": 3780, "Bachillerato": 3850}
PRONTO_PAGO_DIAS = 10
DESCUENTO_PP = 0.15

def es_pronto_pago(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").day <= PRONTO_PAGO_DIAS
    except:
        return False

def generar_folio():
    import random, string
    ts = datetime.now().strftime("%y%m%d%H%M")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CEIMA-{ts}-{rand}"

def get_alumnos():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM alumnos WHERE activo=1 ORDER BY nivel, grado, grupo, nombre", conn)
    conn.close()
    return df

def get_pagos_alumno(alumno_id):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM pagos WHERE alumno_id={alumno_id} ORDER BY fecha_pago DESC", conn)
    conn.close()
    return df

def semaforo_alumno(alumno_id):
    conn = get_conn()
    pagos = conn.execute(
        "SELECT meses_pagados FROM pagos WHERE alumno_id=?", (alumno_id,)).fetchall()
    conn.close()
    meses_pagados = set()
    for p in pagos:
        for m in p[0].split(","):
            meses_pagados.add(m.strip())
    hoy = date.today()
    adeudo = 0
    for i in range(3):
        d = hoy.replace(day=1)
        for _ in range(i):
            d = (d - timedelta(days=1)).replace(day=1)
        clave = d.strftime("%Y-%m")
        if clave not in meses_pagados:
            adeudo += 1
    if adeudo == 0:
        return "Al corriente", "green"
    elif adeudo == 1:
        return "1 mes de adeudo", "yellow"
    elif adeudo == 2:
        return "Llamar al tutor", "yellow"
    else:
        return "⚠ Restricción próxima", "red"

# ── AUTH ──────────────────────────────────────────────────────────────────────
def check_login(username, password):
    conn = get_conn()
    pw = hashlib.sha256(password.encode()).hexdigest()
    row = conn.execute("SELECT nombre FROM usuarios WHERE username=? AND password=?",
                       (username, pw)).fetchone()
    conn.close()
    return row[0] if row else None

def login_screen():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">
                <div style="font-size:3rem;">🌳</div>
                <div style="font-family:'Merriweather',serif; font-size:1.5rem; color:#1a5c2a; font-weight:700; margin-top:0.3rem;">CEIMA</div>
                <div style="font-size:0.8rem; color:#6b7280; letter-spacing:0.08em; text-transform:uppercase; margin-top:0.2rem;">Centro Educativo Integral México Americano</div>
                <div style="font-size:0.75rem; color:#4a9e5c; margin-top:0.4rem;">Sistema de Gestión de Pagos</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        if st.button("Iniciar sesión →", use_container_width=True):
            nombre = check_login(username, password)
            if nombre:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["nombre"] = nombre
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

# ── PÁGINAS ───────────────────────────────────────────────────────────────────
def pagina_dashboard():
    st.markdown("""
    <div class="ceima-header">
        <span style="font-size:1.4rem;">📊</span>
        <h2>Dashboard General</h2>
    </div>
    """, unsafe_allow_html=True)

    conn = get_conn()
    mes_actual = date.today().strftime("%Y-%m")
    total_alumnos = conn.execute("SELECT COUNT(*) FROM alumnos WHERE activo=1").fetchone()[0]
    pagos_mes = conn.execute(
        "SELECT COUNT(*) FROM pagos WHERE strftime('%Y-%m', fecha_pago)=?", (mes_actual,)).fetchone()[0]
    ingresos_mes = conn.execute(
        "SELECT COALESCE(SUM(monto),0) FROM pagos WHERE strftime('%Y-%m', fecha_pago)=?", (mes_actual,)).fetchone()[0]
    pp_mes = conn.execute(
        "SELECT COUNT(*) FROM pagos WHERE strftime('%Y-%m', fecha_pago)=? AND pronto_pago=1", (mes_actual,)).fetchone()[0]
    conn.close()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Alumnos activos", total_alumnos)
    c2.metric("Pagos este mes", pagos_mes)
    c3.metric("Ingresos del mes", f"${ingresos_mes:,.0f}")
    c4.metric("Pronto pagos", pp_mes)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Estado de cuenta — alumnos activos")

    alumnos = get_alumnos()
    if alumnos.empty:
        st.info("Aún no hay alumnos registrados.")
        return

    filas = []
    for _, a in alumnos.iterrows():
        estado, color = semaforo_alumno(a["id"])
        filas.append({
            "Nombre": a["nombre"],
            "Nivel": a["nivel"],
            "Grado": f"{a['grado']} {a['grupo']}",
            "Tutor": a["tutor"] or "—",
            "Estado": f"<span class='badge-{color}'>{estado}</span>"
        })
    df_show = pd.DataFrame(filas)
    st.write(df_show.to_html(escape=False, index=False), unsafe_allow_html=True)

def pagina_alumnos():
    st.markdown("""
    <div class="ceima-header">
        <span style="font-size:1.4rem;">👨‍🎓</span>
        <h2>Alumnos</h2>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋  Lista de alumnos", "➕  Registrar nuevo alumno"])

    with tab1:
        df = get_alumnos()
        if df.empty:
            st.info("No hay alumnos registrados todavía.")
        else:
            col1, col2 = st.columns([1, 3])
            filtro = col1.selectbox("Filtrar por nivel", ["Todos", "Secundaria", "Bachillerato"])
            if filtro != "Todos":
                df = df[df["nivel"] == filtro]
            cols = ["nombre","nivel","grado","grupo","tutor","contacto","email"]
            st.dataframe(df[cols].rename(columns={
                "nombre":"Nombre","nivel":"Nivel","grado":"Grado",
                "grupo":"Grupo","tutor":"Tutor","contacto":"Contacto","email":"Email"
            }), use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df)} alumnos")

    with tab2:
        with st.form("form_alumno", clear_on_submit=True):
            st.markdown("**Datos del alumno**")
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre completo *")
            nivel = c2.selectbox("Nivel *", ["Secundaria", "Bachillerato"])
            c3, c4 = st.columns(2)
            grado = c3.selectbox("Grado", ["1°","2°","3°"])
            grupo = c4.selectbox("Grupo", ["A","B","C","D"])
            st.markdown("**Datos del tutor**")
            c5, c6 = st.columns(2)
            tutor = c5.text_input("Nombre del tutor")
            contacto = c6.text_input("Teléfono / WhatsApp")
            email = st.text_input("Correo electrónico del tutor")
            submitted = st.form_submit_button("✓ Registrar alumno", use_container_width=True)
            if submitted:
                if not nombre.strip():
                    st.error("El nombre del alumno es obligatorio.")
                else:
                    conn = get_conn()
                    conn.execute(
                        "INSERT INTO alumnos (nombre,nivel,grado,grupo,tutor,contacto,email) VALUES (?,?,?,?,?,?,?)",
                        (nombre.strip(), nivel, grado, grupo, tutor, contacto, email))
                    conn.commit()
                    conn.close()
                    st.success(f"✓ Alumno '{nombre}' registrado correctamente.")

def pagina_pagos():
    st.markdown("""
    <div class="ceima-header">
        <span style="font-size:1.4rem;">💳</span>
        <h2>Registrar Pago</h2>
    </div>
    """, unsafe_allow_html=True)

    alumnos = get_alumnos()
    if alumnos.empty:
        st.warning("Primero registra alumnos antes de registrar pagos.")
        return

    nombres_lista = alumnos["nombre"] + " — " + alumnos["nivel"] + " " + alumnos["grado"] + alumnos["grupo"]
    seleccion = st.selectbox("🔍 Buscar alumno", nombres_lista)
    idx = nombres_lista[nombres_lista == seleccion].index[0]
    alumno = alumnos.loc[idx]
    colegiatura_base = COLEGIATURAS[alumno["nivel"]]

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(f"""
        <div class="ceima-card">
            <p style="color:#6b7280;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">Datos del alumno</p>
            <p style="margin:0.2rem 0;"><b>{alumno['nombre']}</b></p>
            <p style="margin:0.2rem 0;color:#4a9e5c;">{alumno['nivel']} {alumno['grado']}{alumno['grupo']}</p>
            <p style="margin:0.2rem 0;">Tutor: {alumno['tutor'] or '—'}</p>
            <p style="margin:0.2rem 0;">Tel: {alumno['contacto'] or '—'}</p>
            <p style="margin:0;font-size:0.9rem;color:#1a5c2a;font-weight:600;">Colegiatura base: ${colegiatura_base:,.0f}/mes</p>
        </div>
        """, unsafe_allow_html=True)

        fecha_pago = st.date_input("📅 Fecha de pago", value=date.today())
        pp = es_pronto_pago(str(fecha_pago))
        if pp:
            st.markdown("<span class='badge-green'>✓ Pronto pago — se aplicará 15% de descuento</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#6b7280;font-size:0.85rem;'>Los primeros {PRONTO_PAGO_DIAS} días del mes aplica pronto pago (15% desc.)</span>", unsafe_allow_html=True)

        hoy = date.today()
        opciones_meses = []
        d = hoy.replace(day=1)
        prev = (d - timedelta(days=1)).replace(day=1)
        opciones_meses.append(prev.strftime("%Y-%m"))
        for i in range(4):
            m = hoy.month + i
            y = hoy.year + (m - 1) // 12
            m = ((m - 1) % 12) + 1
            opciones_meses.append(date(y, m, 1).strftime("%Y-%m"))

        meses_sel = st.multiselect("📆 Meses a cubrir", opciones_meses,
                                    default=[hoy.strftime("%Y-%m")])
        forma = st.selectbox("💰 Forma de pago", ["Efectivo", "Transferencia"])
        notas = st.text_input("Notas (opcional)")

    with col2:
        if meses_sel:
            n = len(meses_sel)
            monto_original = colegiatura_base * n
            descuento = round(monto_original * DESCUENTO_PP, 2) if pp else 0
            monto_final = monto_original - descuento

            st.markdown(f"""
            <div class="resumen-pago">
                <p style="color:#6b7280;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:1rem;">Resumen del pago</p>
                <table style="width:100%;border-collapse:collapse;">
                    <tr><td style="padding:4px 0;color:#6b7280;">Colegiatura</td><td style="text-align:right;">${colegiatura_base:,.0f}</td></tr>
                    <tr><td style="padding:4px 0;color:#6b7280;">Meses</td><td style="text-align:right;">{n}</td></tr>
                    <tr><td style="padding:4px 0;color:#6b7280;">Subtotal</td><td style="text-align:right;">${monto_original:,.0f}</td></tr>
                    <tr><td style="padding:4px 0;color:#1a5c2a;">Descuento PP</td><td style="text-align:right;color:#1a5c2a;">-${descuento:,.0f}</td></tr>
                </table>
                <hr style="border:1px solid #c8e6c9;margin:0.8rem 0;">
                <p style="margin:0;color:#6b7280;font-size:0.78rem;text-transform:uppercase;">Total a pagar</p>
                <p class="resumen-total">${monto_final:,.2f}</p>
                <p style="color:#6b7280;font-size:0.8rem;margin:0;">Forma: {forma}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✓ Registrar pago y generar recibo", use_container_width=True):
                folio = generar_folio()
                conn = get_conn()
                conn.execute("""
                    INSERT INTO pagos (alumno_id,monto,meses_pagados,fecha_pago,forma_pago,
                        pronto_pago,descuento,monto_original,folio,registrado_por,notas)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """, (alumno["id"], monto_final, ",".join(meses_sel), str(fecha_pago),
                      forma, 1 if pp else 0, descuento, monto_original,
                      folio, st.session_state["username"], notas))
                conn.commit()
                conn.close()

                st.success(f"✓ Pago registrado correctamente.")
                recibo = f"""
══════════════════════════════════════════════
   CEIMA — Centro Educativo Integral México Americano
   RECIBO DE PAGO DE COLEGIATURA
══════════════════════════════════════════════
Folio:            {folio}
Fecha de pago:    {fecha_pago.strftime('%d/%m/%Y')}
──────────────────────────────────────────────
ALUMNO
Nombre:           {alumno['nombre']}
Nivel:            {alumno['nivel']} {alumno['grado']}{alumno['grupo']}
Tutor:            {alumno['tutor'] or '—'}
──────────────────────────────────────────────
DETALLE DEL PAGO
Meses cubiertos:  {', '.join(meses_sel)}
Forma de pago:    {forma}
Colegiatura/mes:  ${colegiatura_base:,.0f}
Número de meses:  {n}
Subtotal:         ${monto_original:,.0f}
{'Pronto pago (15%):  -$' + f'{descuento:,.0f}' if pp else 'Sin descuento'}
──────────────────────────────────────────────
TOTAL PAGADO:     ${monto_final:,.2f}
══════════════════════════════════════════════
Registrado por:   {st.session_state['nombre']}
Tel. CEIMA: 2727247363 | 2722177036
══════════════════════════════════════════════
                """.strip()
                st.download_button("⬇ Descargar recibo", recibo,
                                   file_name=f"recibo_{folio}.txt", mime="text/plain")
        else:
            st.markdown("""
            <div style="background:white;border:1.5px dashed #c8e6c9;border-radius:10px;padding:2rem;text-align:center;color:#6b7280;">
                <p>Selecciona al menos un mes para ver el resumen</p>
            </div>
            """, unsafe_allow_html=True)

def pagina_estado_cuenta():
    st.markdown("""
    <div class="ceima-header">
        <span style="font-size:1.4rem;">📋</span>
        <h2>Estado de Cuenta</h2>
    </div>
    """, unsafe_allow_html=True)

    alumnos = get_alumnos()
    if alumnos.empty:
        st.info("Sin alumnos registrados.")
        return

    col1, col2 = st.columns([1, 1])
    filtro_nivel = col1.selectbox("Nivel", ["Todos", "Secundaria", "Bachillerato"])
    filtro_estado = col2.selectbox("Estado", ["Todos", "Al corriente", "Con adeudo", "Críticos"])

    if filtro_nivel != "Todos":
        alumnos = alumnos[alumnos["nivel"] == filtro_nivel]

    filas = []
    for _, a in alumnos.iterrows():
        estado, color = semaforo_alumno(a["id"])
        pagos = get_pagos_alumno(a["id"])
        ultimo = pagos.iloc[0]["fecha_pago"] if not pagos.empty else "—"
        total_pagado = pagos["monto"].sum() if not pagos.empty else 0
        filas.append({
            "Nombre": a["nombre"],
            "Nivel": a["nivel"],
            "Grado": f"{a['grado']}{a['grupo']}",
            "Tutor": a["tutor"] or "—",
            "Último pago": ultimo,
            "Total pagado": f"${total_pagado:,.0f}",
            "Estado": f"<span class='badge-{color}'>{estado}</span>",
            "_color": color
        })

    df_show = pd.DataFrame(filas)
    if filtro_estado == "Al corriente":
        df_show = df_show[df_show["_color"] == "green"]
    elif filtro_estado == "Con adeudo":
        df_show = df_show[df_show["_color"] == "yellow"]
    elif filtro_estado == "Críticos":
        df_show = df_show[df_show["_color"] == "red"]

    df_display = df_show.drop(columns=["_color"])
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.caption(f"Mostrando {len(df_show)} alumnos")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Historial de pagos por alumno")
    alumnos_all = get_alumnos()
    sel = st.selectbox("Seleccionar alumno", alumnos_all["nombre"].tolist())
    alumno_id = alumnos_all[alumnos_all["nombre"] == sel].iloc[0]["id"]
    pagos = get_pagos_alumno(alumno_id)
    if pagos.empty:
        st.info("Este alumno no tiene pagos registrados.")
    else:
        cols = ["folio","fecha_pago","meses_pagados","forma_pago","monto","pronto_pago","notas"]
        pagos_show = pagos[cols].copy()
        pagos_show["pronto_pago"] = pagos_show["pronto_pago"].apply(lambda x: "✓ Sí" if x else "No")
        pagos_show["monto"] = pagos_show["monto"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(pagos_show.rename(columns={
            "folio":"Folio","fecha_pago":"Fecha","meses_pagados":"Meses cubiertos",
            "forma_pago":"Forma","monto":"Monto","pronto_pago":"Pronto pago","notas":"Notas"
        }), use_container_width=True, hide_index=True)

def pagina_recordatorios():
    st.markdown("""
    <div class="ceima-header">
        <span style="font-size:1.4rem;">🔔</span>
        <h2>Recordatorios de Pago</h2>
    </div>
    """, unsafe_allow_html=True)

    alumnos = get_alumnos()
    criticos, aviso = [], []
    for _, a in alumnos.iterrows():
        estado, color = semaforo_alumno(a["id"])
        if color == "red":
            criticos.append({**a.to_dict(), "estado": estado})
        elif color == "yellow" and "Llamar" in estado:
            aviso.append({**a.to_dict(), "estado": estado})

    if not criticos and not aviso:
        st.success("✓ Todos los alumnos están al corriente. No hay recordatorios pendientes.")
        return

    if criticos:
        st.markdown(f"#### ⚠ Restricción próxima — {len(criticos)} alumno(s)")
        st.markdown("<small style='color:#721c24;'>Estos alumnos tienen 2.5 meses o más de adeudo. Se les restringirá el acceso próximamente.</small>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for a in criticos:
            with st.expander(f"📍 {a['nombre']} — {a['nivel']} {a['grado']}{a['grupo']}"):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Tutor:** {a['tutor'] or '—'}")
                col1.markdown(f"**Teléfono:** {a['contacto'] or '—'}")
                col2.markdown(f"**Email:** {a['email'] or '—'}")
                col2.markdown(f"**Estado:** <span class='badge-red'>{a['estado']}</span>", unsafe_allow_html=True)
                msg = f"Estimado(a) {a['tutor'] or 'tutor'}, le contactamos del CEIMA para informarle que el alumno(a) {a['nombre']} presenta un adeudo de colegiatura. Le pedimos regularizar su situación a la brevedad posible para evitar la restricción de acceso. Cualquier duda comuníquese al 2727247363. Gracias."
                st.markdown("**Mensaje listo para enviar:**")
                st.code(msg, language=None)
                if a["contacto"]:
                    tel = a["contacto"].replace(" ","").replace("-","")
                    st.markdown(f"[📱 Enviar por WhatsApp](https://wa.me/52{tel}?text={msg.replace(' ','%20').replace('(','%28').replace(')','%29')})")

    if aviso:
        st.markdown(f"#### 📞 Llamar esta semana — {len(aviso)} alumno(s)")
        st.markdown("<small style='color:#856404;'>Mes y medio de adeudo. Es momento de contactar al tutor.</small>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for a in aviso:
            with st.expander(f"📋 {a['nombre']} — {a['nivel']} {a['grado']}{a['grupo']}"):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Tutor:** {a['tutor'] or '—'}")
                col1.markdown(f"**Teléfono:** {a['contacto'] or '—'}")
                col2.markdown(f"**Email:** {a['email'] or '—'}")
                col2.markdown(f"**Estado:** <span class='badge-yellow'>{a['estado']}</span>", unsafe_allow_html=True)
                msg = f"Estimado(a) {a['tutor'] or 'tutor'}, le recordamos que la colegiatura del alumno(a) {a['nombre']} está pendiente de pago. Recuerde que pagando los primeros 10 días del mes aplica un descuento especial por pronto pago. Para cualquier aclaración comuníquese al 2727247363. ¡Gracias!"
                st.markdown("**Mensaje listo para enviar:**")
                st.code(msg, language=None)
                if a["contacto"]:
                    tel = a["contacto"].replace(" ","").replace("-","")
                    st.markdown(f"[📱 Enviar por WhatsApp](https://wa.me/52{tel}?text={msg.replace(' ','%20').replace('(','%28').replace(')','%29')})")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_screen()
else:
    with st.sidebar:
        st.markdown("""
        <div style="padding:1.2rem 0 1rem; text-align:center; border-bottom:1px solid rgba(255,255,255,0.2); margin-bottom:1rem;">
            <div style="font-size:2rem;">🌳</div>
            <div style="font-family:'Merriweather',serif; font-size:1.1rem; font-weight:700; color:white;">CEIMA</div>
            <div style="font-size:0.7rem; color:rgba(255,255,255,0.7); letter-spacing:0.05em;">Sistema de Pagos</div>
        </div>
        """, unsafe_allow_html=True)

        pagina = st.radio("", [
            "📊  Dashboard",
            "👨‍🎓  Alumnos",
            "💳  Registrar Pago",
            "📋  Estado de Cuenta",
            "🔔  Recordatorios"
        ])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding:0.8rem; background:rgba(255,255,255,0.1); border-radius:8px; margin-top:1rem;">
            <p style="margin:0; font-size:0.75rem; color:rgba(255,255,255,0.7);">Sesión activa</p>
            <p style="margin:0; font-weight:600; color:white; font-size:0.9rem;">{st.session_state['nombre']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    if "Dashboard" in pagina:
        pagina_dashboard()
    elif "Alumnos" in pagina:
        pagina_alumnos()
    elif "Registrar" in pagina:
        pagina_pagos()
    elif "Estado" in pagina:
        pagina_estado_cuenta()
    elif "Recordatorios" in pagina:
        pagina_recordatorios()
