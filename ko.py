from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="App Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",from datetime import datetime
import io
import sqlite3
import pandas as pd
import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Created By Kitesa Negasa Feyisa",
    page_icon="🎓",
    layout="wide",
)

# ============================================================================
# FIX #1: DIZAAYINII COVER PAGE / WALIIGALAA (nicer fonts, gradient, borders)
# ============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main { background-color: #f4f6f9; }

    .cover-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 55%, #4e73df 100%);
        padding: 50px 30px;
        border-radius: 22px;
        color: white;
        text-align: center;
        box-shadow: 0 12px 35px rgba(30, 60, 114, 0.35);
        border: 3px solid #ffd700;
    }
    .cover-card h1 {
        color: #ffffff !important;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .cover-card h3 {
        color: #f0f4ff !important;
        font-weight: 400;
        font-size: 20px;
    }
    .cover-divider {
        height: 4px;
        width: 130px;
        background: #ffd700;
        margin: 18px auto;
        border-radius: 2px;
    }

    .metric-card {
        background-color: #ffffff;
        border: 2px solid #e3e6f0;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(78,115,223,0.25);
        border-color: #4e73df;
    }

    .contact-card {
        background: linear-gradient(135deg, #ffffff 0%, #eef2f9 100%);
        border: 2px solid #4e73df;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .contact-card h4 { color: #1e3c72; margin-bottom: 10px; }
    .contact-card p { margin: 5px 0; font-size: 15px; color: #2e384d; }

    .stButton>button {
        background: linear-gradient(135deg, #4e73df 0%, #2e59d9 100%);
        color: white;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2e59d9 0%, #1e3c72 100%);
    }

    h1, h2, h3 {
        color: #2e384d;
        font-family: 'Poppins', sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# FIX #2: ODEEFFANNOO QUNNAMTII (phone/telegram, gmail, Facebook) - dabalata
# ============================================================================
CONTACT_INFO_HTML = """
<div class="contact-card">
    <h4>📞 Toora Odeeffannoo Qunnamtii</h4>
    <p>📱 <b>Bilbilaa &amp; Telegram:</b> +251969184005 / 910927936</p>
    <p>📧 <b>Gmail:</b> kitesanegasa2012@gmail.com</p>
    <p>📘 <b>Facebook:</b> Kitesa Negasa</p>
</div>
"""

# ============================================================================
# DATABASE (SQLite) - PERSISTENT STORAGE
# ============================================================================
DB_PATH = "kitesa_negasa_data.db"

# --- SIRREEFFAMA GUDDAA (rakkoo ijoo "save hin taane" sanaa) ---
# Duraan maqaan column kanaa (fkn "Maqaa Guutuu(students full name") fi
# maqaan "key" kan insert_student() itti fayyadamu (fkn "Maqaa Guutuu")
# WALHIN SIMNE ture. Sababa kanaan, yeroo galmeen save ta'u SQL dogoggora
# ("no such column") uumuun deetaan hunduu save ta'uu dhabuu danda'a ture.
# Amma maqaan column hundi, kan "new_data" keessatti fayyadamnu waliin
# walsimsiifamee jira.
STUDENT_COLUMNS = [
    "Maqaa Guutuu",
    "Koorniyaa",
    "Kutaa",
    "Daree (Section)",
    "Bara Dhalootaa",
    "Umurii",
    "Haala Galmee",
    "Bara Addaan Kute",
    "Haala Maatii",
    "Miidhama Qaamaa",
    "Gosa Miidhamaa",
    "Godina",
    "Aanaa",
    "Ganda",
    "Maqaa Haadhaa/Guddistuu",
    "FAN ID",
    "Lakk Bilbila Barataa",
    "Lakk Bilbila Maatii",
    "M/B Duraan Itti Barachaa Ture",
    "Avireejjii Qabxii",
    "Guyyaa Galmee (E.C)",
    "Barsiisaa Galmeessee",
]


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cols_sql = ", ".join([f'"{c}" TEXT' for c in STUDENT_COLUMNS])
    cur.execute(
        f'''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {cols_sql}
            )'''
    )
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS targets (
                kutaa TEXT PRIMARY KEY,
                dhiira INTEGER DEFAULT 0,
                dhalaa INTEGER DEFAULT 0
            )'''
    )
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gmail TEXT,
                login_time TEXT
            )'''
    )
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )'''
    )
    conn.commit()
    conn.close()


def load_students():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM students ORDER BY id", conn)
    finally:
        conn.close()
    return df


def insert_student(data: dict):
    conn = get_connection()
    cur = conn.cursor()
    cols = list(data.keys())
    placeholders = ", ".join(["?"] * len(cols))
    col_names = ", ".join([f'"{c}"' for c in cols])
    cur.execute(
        f'INSERT INTO students ({col_names}) VALUES ({placeholders})',
        list(data.values()),
    )
    conn.commit()
    conn.close()


def update_student(row_id: int, data: dict):
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ", ".join([f'"{c}" = ?' for c in data.keys()])
    values = list(data.values()) + [row_id]
    cur.execute(f'UPDATE students SET {set_clause} WHERE id = ?', values)
    conn.commit()
    conn.close()


def delete_student(row_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()


def load_targets():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM targets", conn)
    finally:
        conn.close()
    targets = {str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)}
    for _, r in df.iterrows():
        targets[str(r["kutaa"])] = {"Dhiira": int(r["dhiira"]), "Dhalaa": int(r["dhalaa"])}
    return targets


def save_target(kutaa, dhiira, dhalaa):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO targets (kutaa, dhiira, dhalaa) VALUES (?, ?, ?)
           ON CONFLICT(kutaa) DO UPDATE SET dhiira=excluded.dhiira, dhalaa=excluded.dhalaa''',
        (kutaa, dhiira, dhalaa),
    )
    conn.commit()
    conn.close()


def load_login_history():
    conn = get_connection()
    try:
        df = pd.read_sql_query(
            'SELECT gmail AS Gmail, login_time AS "Guyyaa/Saatii" FROM login_history ORDER BY id DESC',
            conn,
        )
    finally:
        conn.close()
    return df


def save_login(gmail):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO login_history (gmail, login_time) VALUES (?, ?)",
        (gmail, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_setting(key, default=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default


def set_setting(key, value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO settings (key, value) VALUES (?, ?)
           ON CONFLICT(key) DO UPDATE SET value=excluded.value''',
        (key, value),
    )
    conn.commit()
    conn.close()


init_db()

# ----------------- SESSION STATE (only for login + in-progress form) -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# Authorized Users Database (hin tuqamne - akkuma duraanii)
AUTHORIZED_USERS = {
    "kitesanegasa2012@gmail.com": "kitesanegasa2012password",
    "barsiisaa1@gmail.com": "pass1234",
    "bulchaa@gmail.com": "admin2026",
    "feyisamililu23@gmail.com": "20481092F",
}

# Password gabaasaa barsiisaa (Dashboard Barsiisaa)
REPORT_PASSWORDS = ["kitesanegasa2012password", "kitesa2019", "admin123"]

# FIX #10: Password addaa Dashboard Bulchiinsaa (Admin) - kana jijjiiruu dandeessa
ADMIN_PASSWORD = "KitesaAdmin@2026"


def get_last_location(db, col_name):
    if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
        return db[col_name].dropna().iloc[-1]
    return ""


def generate_grouped_report(data_rows, title_col_name="Kutaa"):
    rows_1_6_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)
    rows_1_6_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)

    rows_7_8_d = sum(r["Dhiira"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)
    rows_7_8_dh = sum(r["Dhalaa"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)

    rows_9_12_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)
    rows_9_12_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)

    final_table = []

    for r in data_rows:
        if int(r["Kutaa_Num"]) <= 6:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 1 - 6", "Dhiira": rows_1_6_d, "Dhalaa": rows_1_6_dh, "Ida'ama": rows_1_6_d + rows_1_6_dh})

    for r in data_rows:
        if 7 <= int(r["Kutaa_Num"]) <= 8:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 7 - 8", "Dhiira": rows_7_8_d, "Dhalaa": rows_7_8_dh, "Ida'ama": rows_7_8_d + rows_7_8_dh})

    final_table.append({title_col_name: "Ida'ama Waliigalaa (1 - 8)", "Dhiira": rows_1_6_d + rows_7_8_d, "Dhalaa": rows_1_6_dh + rows_7_8_dh, "Ida'ama": (rows_1_6_d + rows_7_8_d) + (rows_1_6_dh + rows_7_8_dh)})

    for r in data_rows:
        if int(r["Kutaa_Num"]) >= 9:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 9 - 12", "Dhiira": rows_9_12_d, "Dhalaa": rows_9_12_dh, "Ida'ama": rows_9_12_d + rows_9_12_dh})

    tot_d = rows_1_6_d + rows_7_8_d + rows_9_12_d
    tot_dh = rows_1_6_dh + rows_7_8_dh + rows_9_12_dh
    final_table.append({title_col_name: "Waliigalaa (1 - 12)", "Dhiira": tot_d, "Dhalaa": tot_dh, "Ida'ama": tot_d + tot_dh})

    return pd.DataFrame(final_table)


def pct_str(actual, target):
    """Raawwii dhibbeentaa (%) herregu - FIX #8"""
    try:
        if target and float(target) > 0:
            return f"{(float(actual) / float(target) * 100):.1f}%"
    except (ValueError, TypeError):
        pass
    return "-"


# ----------------- LOGIN SCREEN CHECK -----------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="cover-card" style="max-width: 550px; margin: 50px auto;">
            <h2>🔐 Sirna Eeyyamaa (Login System)</h2>
            <p>App kana fayyadamuuf Gmail fi Password hayyamame galchuun dirqama.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            input_email = st.text_input("Gmail")
            input_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Seeni (Login)")

            if submit_login:
                if input_email in AUTHORIZED_USERS and AUTHORIZED_USERS[input_email] == input_password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = input_email
                    save_login(input_email)
                    st.success(f"Baga nagaan dhufte, {input_email}!")
                    st.rerun()
                else:
                    st.error("Gmail ykn Password sirrii miti, ykn hayyama hin qabdu!")

        st.markdown("---")
        st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

    st.stop()

# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown(f"👤 **Seeneera:** `{st.session_state.current_user}`")
st.sidebar.markdown("### 🏫 Kitesa Negasa Feyisa")
menu = st.sidebar.selectbox(
    "Filannoo Baafataa (Navigation)",
    [
        "1. Cover Page",
        "2. Kutaa Galmee Barataa (Foormii)",
        "3. Kutaa Qophii Gabaasaa (Password Needed)",
        "4. Dashboard Bulchiinsaa (Admin - Password Needed)",
        "5. Seenaa Seensaa (Login History / Audit)",
        "6. Baasi (Logout)",
    ],
)

if menu == "6. Baasi (Logout)":
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# ----------------- 1. COVER PAGE (FIX #1 fi #2) -----------------
if menu == "1. Cover Page":
    st.markdown(
        """
        <div class="cover-card">
            <div style="font-size:60px;">🎓</div>
            <h1>APP SIRNA GALMEE BARATTOOTAA (STUDENT REGISTRATION SYSTEM)</h1>
            <div class="cover-divider"></div>
            <h3>Baga Nagaan Gara App Sirna Galmee Barattootaa Kitesa Nagasaatiin Kalaqameetti Dhuftan!</h3>
            <p style="font-size:16px; opacity:0.92;">Sirni kun odeeffannoo barattootaa galmeessuuf, gabaasa qindeessuu fi ragaa barattootaa hordoffii taasisuuf kan qophaa'eedha.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    school_name_cover = get_setting("saved_school_name", "")
    if school_name_cover:
        st.markdown(
            f"<h3 style='text-align:center; margin-top:18px;'>🏫 {school_name_cover}</h3>",
            unsafe_allow_html=True,
        )

    st.write("---")
    st.subheader("📊 Lakkoofsa Barattootaa Galmaa'anii (Kutaa Kutaan)")

    db = load_students()
    cols = st.columns(4)
    for i in range(1, 13):
        count = len(db[db["Kutaa"] == str(i)]) if not db.empty else 0
        with cols[(i - 1) % 4]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>Kutaa {i}</h4>
                    <h2 style="color: #4e73df;">{count}</h2>
                    <p>Barattoota Galmaa'an</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("---")
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

# ----------------- 2. DASHBOARD GALMEE BARATTOOTAA (FOOMII) -----------------
elif menu == "2. Kutaa Galmee Barataa (Foormii)":
    st.subheader("📝 Foormii Galmee Barattootaa")

    db_existing = load_students()
    default_godina = get_last_location(db_existing, "Godina")
    default_aanaa = get_last_location(db_existing, "Aanaa")
    default_ganda = get_last_location(db_existing, "Ganda")
    default_barsiisaa = st.session_state.current_user if st.session_state.current_user else get_last_location(db_existing, "Barsiisaa Galmeessee")
    default_guyyaa = get_last_location(db_existing, "Guyyaa Galmee (E.C)")
    if not default_guyyaa:
        default_guyyaa = "25/11/2018"

    saved_school_name = get_setting("saved_school_name", "")

    st.markdown("### 🏫 Maqaa Mana Barumsaa")
    school_input_col1, school_input_col2 = st.columns([3, 1])
    with school_input_col1:
        current_school_name = st.text_input(
            "Maqaa Mana Barumsaa Galmeessaa Jirtu Galchaa (Save Akka Ta'uuf)",
            value=saved_school_name,
        )
    with school_input_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save School Name"):
            if current_school_name.strip():
                set_setting("saved_school_name", current_school_name.strip())
                st.success("Maqaan mana barumsaa milkaa'inaan save ta'eera!")
                st.rerun()
            else:
                st.warning("Maaloo maqaa mana barumsaa galchaa.")

    # Erga jijjiirama dandeessisuun booda haaromsuu (refresh)
    saved_school_name = get_setting("saved_school_name", "")

    st.markdown("---")

    # ------------------------------------------------------------------
    # FIX #4: "Haala Galmee" form-icha ALAATTI kaa'ame - sababiin isaa,
    # yeroo isa filattu battaluma sana Tab 14 (M/B Duraan Itti Barachaa
    # Ture) ofumaan akka jijjiiramu gochuufi.
    # ------------------------------------------------------------------
    st.markdown("**5. Haala Galmee** _(kana dursaa filadhaa, ragaan kanarratti hunda'uu waan ta'uuf)_")
    haala_galmee = st.selectbox(
        "Haala Galmee Barataa",
        ["Haaraa", "Kan darbe", "Irra deebii (Kufe)", "Irra deebii (Kute)", "Irra deebii Mana Barumsaa Biroo", "Mana Barumsaa Biroo"],
        key="haala_galmee_select",
    )
    st.markdown("---")

    if "form_maqaa" not in st.session_state: st.session_state.form_maqaa = ""
    if "form_fan" not in st.session_state: st.session_state.form_fan = ""
    if "form_p_barataa" not in st.session_state: st.session_state.form_p_barataa = ""
    if "form_p_maatii" not in st.session_state: st.session_state.form_p_maatii = ""
    if "form_haadhaa" not in st.session_state: st.session_state.form_haadhaa = ""
    if "form_mb_biroo" not in st.session_state: st.session_state.form_mb_biroo = ""

    # --- SIRREEFFAMA (item #1): kutaa foormichaa kun DURAAN "elif" kana ALAA
    # ba'ee ture ("with st.form" fi wanti isa hordofu hundi indent hin qabu
    # ture) -- kanaafuu menu kamiyyuu keessatti ni mul'ata ture. Amma sirriitti
    # "elif menu == '2. ...'" kana JALA deebi'ee ida'ameera. ---
    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa", value=st.session_state.form_maqaa)
            koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])

            grade_col1, grade_col2 = st.columns(2)
            kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
            daree = grade_col2.selectbox("Daree (Section)", [chr(65 + i) for i in range(11)])

            st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyaatti)**")
            b_col1, b_col2, b_col3 = st.columns(3)
            b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
            b_jiia = b_col2.selectbox(
                "Ji'a",
                [
                    "Fulbaana", "Onkololeessa", "Sadaasa", "Muddee",
                    "Amajjii", "Guraandhala", "Bitootessa", "Ebla", "Caamsaa",
                    "Waxabajjii", "Adoolessa", "Hagayya", "Pagumee",
                ],
            )
            b_bara = b_col3.number_input(
                "Bara Dhalootaa (Fkn: 2011)", min_value=1990, max_value=2025, value=2011
            )
            current_et_year = 2018
            umurii = current_et_year - b_bara

            st.text_input("5. Haala Galmee (Filatame)", value=haala_galmee, disabled=True)

            bara_addaan_kute = st.selectbox(
                "Bara Addaan Kute (Yoo kute/kufe)",
                ["Hin jiru", "2005", "2006", "2007", "2008", "2009", "2010"]
                + [str(y) for y in range(2011, 2027)],
            )

            haala_maatii = st.selectbox(
                "6. Haala Maatii",
                ["Lachuu qaba", "Abbaa qofa", "Haadha qofa", "Lachuu hin qabu"],
            )

            miidhama_qaamaa = st.selectbox(
                "7. Haala Miidhama Qaamaa", ["Hin jiru", "Jira"]
            )

            gosa_miidhamaa = st.selectbox(
                "8. Gosa Miidhama Qaamaa (Yoo Jira ta'e filadhu)",
                [
                    "Hin qabu", "Arguu salphaa", "Arguu cimaa", "Dhageettii salphaa",
                    "Dhageettii cimaa", "Dubbii salphaa", "Dubbii cimaa", "Sochii salphaa",
                    "Sochii cimaa", "Saaleessa sammuu", "Currisa hawaasumaa", "Haadhaa fi abbaa dhabuu"
                ]
            )

        with col2:
            st.markdown("**9. Bakka Dhalootaa** _(galmee dabre irraa ofumaan bahe)_")
            godina = st.text_input("Godina", value=default_godina)
            aanaa = st.text_input("Aanaa", value=default_aanaa)
            ganda = st.text_input("Ganda", value=default_ganda)

            maqaa_haadhaa = st.text_input(
                "10. Maqaa Guutuu Haadhaa ykn Guddistuu",
                value=st.session_state.form_haadhaa,
            )
            fan_id = st.text_input(
                "11. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID - Digiti 16)",
                value=st.session_state.form_fan,
            )
            lakk_bilbila_barataa = st.text_input(
                "12. Lakkoofsa Bilbila Barataa (+251...)",
                value=st.session_state.form_p_barataa,
            )
            lakk_bilbila_maatii = st.text_input(
                "13. Lakkoofsa Bilbila Maatii (+251...)",
                value=st.session_state.form_p_maatii,
            )
            st.markdown("---")
            st.markdown("**14. Mana Barumsaa Duraan Itti Barachaa Ture / Biroo**")

            # --- SIRREEFFAMA (item #2): "saved_school_name" (session_state)
            # utuu hin taane, "saved_school_name" (kan gubbaatti get_setting()
            # irraa argame, database keessatti kan kaa'ame) fayyadamna --
            # kunis maqaa mana barumsaa kanaan walsimaadha. ---
            if haala_galmee not in [
                "Mana Barumsaa Biroo",
                "Irra deebii Mana Barumsaa Biroo",
            ]:
                if saved_school_name:
                    st.info(f"Maqaan Mana Barumsaa Ofumaan Guutame: **{saved_school_name}**")
                    mb_duraan = saved_school_name
                else:
                    mb_duraan = st.text_input(
                        "Maqaa Mana Barumsaa (Dursee kan barachaa ture)",
                        value=st.session_state.get("form_mb_biroo", ""),
                    )
            else:
                mb_duraan = st.text_input(
                    "Maqaa Mana Barumsaa Biroo (Mana barumsaa barataan irraa dhufe)",
                    value=st.session_state.get("form_mb_biroo", ""),
                )

            avireejjii = st.number_input(
                "15. Avireejjii Qabxii Bara Darbee (0 - 100)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
            )
            barsiisaa = st.text_input("16. Barsiisaa Galmeessee", value=default_barsiisaa)
            guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C)", value=default_guyyaa)

        submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
        st.session_state.form_maqaa = maqaa_guutuu
        st.session_state.form_fan = fan_id
        st.session_state.form_p_barataa = lakk_bilbila_barataa
        st.session_state.form_p_maatii = lakk_bilbila_maatii
        st.session_state.form_haadhaa = maqaa_haadhaa
        st.session_state.form_mb_biroo = mb_duraan
        error_msgs = []

        if not maqaa_guutuu:
            error_msgs.append("Maqaa Guutuu barataa guuti!")
        if koorniyaa == "Filadhu":
            error_msgs.append("Maaloo Koorniyaa barataa filadhu!")

        if avireejjii < 50 and haala_galmee != "Irra deebii (Kufe)":
            error_msgs.append(
                'Barataan avireejjii 50 gadi fide, haala galmeen "Irra deebii (Kufe)" jedhu wajjin walsimuu qaba!'
            )

        clean_fan = fan_id.strip()
        if clean_fan and (not clean_fan.isdigit() or len(clean_fan) != 16):
            error_msgs.append("FAN ID dijiitii 16 qofa ta'uu qaba!")

        def validate_phone(phone_str, field_label):
            p = phone_str.strip()
            if not p.startswith("+251"):
                return f"{field_label}: Lakkoofsi bilbilaa '+251' tiin jalqabuu qaba!"
            subscriber_part = p[4:]
            if len(subscriber_part) != 9 or not subscriber_part.isdigit():
                return f"{field_label}: Koodii biyyaa itti aansuun lakkoofsi jiru dijiitii 9 qofa ta'uu qaba."
            return None

        if lakk_bilbila_barataa.strip():
            err_p1 = validate_phone(lakk_bilbila_barataa, "Bilbila Barataa")
            if err_p1:
                error_msgs.append(err_p1)

        if lakk_bilbila_maatii.strip():
            err_p2 = validate_phone(lakk_bilbila_maatii, "Bilbila Maatii")
            if err_p2:
                error_msgs.append(err_p2)

        if error_msgs:
            for err in error_msgs:
                st.markdown(
                    f'<p style="color:red; font-weight:bold;">⚠️ {err}</p>',
                    unsafe_allow_html=True,
                )
        else:
            new_data = {
                "Maqaa Guutuu": maqaa_guutuu,
                "Koorniyaa": koorniyaa,
                "Kutaa": kutaa,
                "Daree (Section)": daree,
                "Bara Dhalootaa": f"{b_guyyaa}/{b_jiia}/{b_bara}",
                "Umurii": umurii,
                "Haala Galmee": haala_galmee,
                "Bara Addaan Kute": bara_addaan_kute,
                "Haala Maatii": haala_maatii,
                "Miidhama Qaamaa": miidhama_qaamaa,
                "Gosa Miidhamaa": gosa_miidhamaa,
                "Godina": godina,
                "Aanaa": aanaa,
                "Ganda": ganda,
                "Maqaa Haadhaa/Guddistuu": maqaa_haadhaa,
                "FAN ID": fan_id,
                "Lakk Bilbila Barataa": lakk_bilbila_barataa,
                "Lakk Bilbila Maatii": lakk_bilbila_maatii,
                "M/B Duraan Itti Barachaa Ture": mb_duraan,
                "Avireejjii Qabxii": avireejjii,
                "Guyyaa Galmee (E.C)": guyyaa_galmee_ec,
                "Barsiisaa Galmeessee": barsiisaa,
            }

            insert_student(new_data)

            st.session_state.form_maqaa = ""
            st.session_state.form_fan = ""
            st.session_state.form_p_barataa = ""
            st.session_state.form_p_maatii = ""
            st.session_state.form_haadhaa = ""
            st.session_state.form_mb_biroo = ""

            st.success(f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!")

# ----------------- 3, 4, 5: KUTAALEE AMMAAN TANA HIN ARGAMNE -----------------
# Kutaaleen kunneen (Gabaasaa, Admin Dashboard, Seenaa Seensaa) koodii ati
# naaf ergite keessatti hin argamne (ARGUMEENTOOTNI isaanii - generate_grouped_report,
# pct_str, save_target - qofti jiru). Bakka bu'aa yeroof kaa'e, akka fuulli
# duwwaa hin taaneef; garuu hojiin dhugaa isaanii ammaan tana hin qophoofne.
elif menu == "3. Kutaa Qophii Gabaasaa (Password Needed)":
    st.info("🚧 Kutaan Gabaasaa ammaan tana hin qophoofne. Koodii duraanii yoo qabaatte naaf ergi, yoo hin qabaatinis waan gaafatte (karoora galchuu-save, table raawwii %) siif ijaara.")

elif menu == "4. Dashboard Bulchiinsaa (Admin - Password Needed)":
    st.info("🚧 Dashboardiin Bulchiinsaa ammaan tana hin qophoofne.")

elif menu == "5. Seenaa Seensaa (Login History / Audit)":
    st.info("🚧 Fuulli Seenaa Seensaa ammaan tana hin qophoofne.")
    layout="wide",
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .cover-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: #ffffff;
        border: 2px solid #e3e6f0;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #4e73df;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2e59d9;
    }
    h1, h2, h3 {
        color: #2e384d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- SESSION STATE INITIALIZATION -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "login_history" not in st.session_state:
    st.session_state.login_history = []

if "students_db" not in st.session_state:
    st.session_state.students_db = pd.DataFrame(
        columns=[
            "Maqaa Guutuu",
            "Koorniyaa",
            "Kutaa",
            "Daree (Section)",
            "Bara Dhalootaa",
            "Umurii",
            "Haala Galmee",
            "Bara Addaan Kute",
            "Haala Maatii",
            "Miidhama Qaamaa",
            "Gosa Miidhamaa",
            "Godina",
            "Aanaa",
            "Ganda",
            "Maqaa Haadhaa/Guddistuu",
            "FAN ID",
            "Lakk Bilbila Barataa",
            "Lakk Bilbila Maatii",
            "M/B Duraan Itti Barachaa Ture",
            "Avireejjii Qabxii",
            "Guyyaa Galmee (E.C)",
            "Barsiisaa Galmeessee",
        ]
    )

if "targets" not in st.session_state:
    st.session_state.targets = {
        str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)
    }

if "saved_school_name" not in st.session_state:
    st.session_state.saved_school_name = ""

# Authorized Users Database
AUTHORIZED_USERS = {
    "kitesanegasa2012@gmail.com": "kitesanegasa2012password",
    "barsiisaa1@gmail.com": "pass1234",
    "bulchaa@gmail.com": "admin2026",
}

def get_last_location(db, col_name):
    if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
        return db[col_name].dropna().iloc[-1]
    return ""

def generate_grouped_report(data_rows, title_col_name="Kutaa"):
    rows_1_6_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)
    rows_1_6_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)
    
    rows_7_8_d = sum(r["Dhiira"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)
    rows_7_8_dh = sum(r["Dhalaa"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)
    
    rows_9_12_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)
    rows_9_12_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)

    final_table = []
    
    for r in data_rows:
        if int(r["Kutaa_Num"]) <= 6:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 1 - 6", "Dhiira": rows_1_6_d, "Dhalaa": rows_1_6_dh, "Ida'ama": rows_1_6_d + rows_1_6_dh})
    
    for r in data_rows:
        if 7 <= int(r["Kutaa_Num"]) <= 8:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 7 - 8", "Dhiira": rows_7_8_d, "Dhalaa": rows_7_8_dh, "Ida'ama": rows_7_8_d + rows_7_8_dh})
    
    final_table.append({title_col_name: "Ida'ama Waliigalaa (1 - 8)", "Dhiira": rows_1_6_d + rows_7_8_d, "Dhalaa": rows_1_6_dh + rows_7_8_dh, "Ida'ama": (rows_1_6_d + rows_7_8_d) + (rows_1_6_dh + rows_7_8_dh)})

    for r in data_rows:
        if int(r["Kutaa_Num"]) >= 9:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 9 - 12", "Dhiira": rows_9_12_d, "Dhalaa": rows_9_12_dh, "Ida'ama": rows_9_12_d + rows_9_12_dh})

    tot_d = rows_1_6_d + rows_7_8_d + rows_9_12_d
    tot_dh = rows_1_6_dh + rows_7_8_dh + rows_9_12_dh
    final_table.append({title_col_name: "Waliigalaa (1 - 12)", "Dhiira": tot_d, "Dhalaa": tot_dh, "Ida'ama": tot_d + tot_dh})

    return pd.DataFrame(final_table)

# ----------------- LOGIN SCREEN CHECK -----------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="cover-card" style="max-width: 500px; margin: 50px auto;">
            <h2>🔐 Seensa Eeyyamaa (Login System)</h2>
            <p>App kana fayyadamuuf Gmail fi Password hayyamame galchuun dirqama.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            input_email = st.text_input("Gmail")
            input_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Seeni (Login)")
            
            if submit_login:
                if input_email in AUTHORIZED_USERS and AUTHORIZED_USERS[input_email] == input_password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = input_email
                    
                    login_record = {
                        "Gmail": input_email,
                        "Guyyaa/Saatii": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if login_record not in st.session_state.login_history:
                        st.session_state.login_history.append(login_record)
                        
                    st.success(f"Baga nagaan dhufte, {input_email}!")
                    st.rerun()
                else:
                    st.error("Gmail ykn Password sirrii miti, ykn hayyama hin qabdu!")
        
        st.markdown("---")
        st.markdown("### 📌 Toora Odeeffannoo Qunnamtii")
        st.markdown("**Lakk Bilbilaa & Telegram:** +251969184005 / 910927936")
        st.markdown("**Gmail:** kitesanegasa2012@gmail.com")
    
    st.stop()

# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown(f"👤 **Seenteera:** `{st.session_state.current_user}`")
st.sidebar.markdown("### 🏫 Mana Barumsaa B/saa Kitesa Negasa")
menu = st.sidebar.selectbox(
    "Filannoo Fuulaa (Navigation)",
    [
        "1. Cover Page",
        "2. Dashboard Galmee Barataa (Foomii)",
        "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)",
        "4. Seenaa Seensaa (Login History / Audit)",
        "5. Baasii (Logout)",
    ],
)

if menu == "5. Baasii (Logout)":
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# ----------------- 1. COVER PAGE -----------------
if menu == "1. Cover Page":
    st.markdown(
        """
        <div class="cover-card">
            <h1>🎓 APP GALMEE BARATTOOTAA</h1>
            <h3>Baga Nagaan Gara App Galmee Barattootaa Mana Barumsaa B/saa Kitesa Negasaatiin Kalaqaameetti Dhuftan!</h3>
            <p>Sirni kun odeeffannoo barattootaa qabaachuuf, gabaasa oomishuuf fi hordoffii taasisuuf kan qophaa'eedha.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")
    st.subheader("📊 Lakkoofsa Barattootaa Galmaa'anii (Kutaa Kutaan)")

    db = st.session_state.students_db
    cols = st.columns(4)
    for i in range(1, 13):
        count = len(db[db["Kutaa"] == str(i)]) if not db.empty else 0
        with cols[(i - 1) % 4]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>Kutaa {i}</h4>
                    <h2 style="color: #4e73df;">{count}</h2>
                    <p>Barattoota Galmaa'an</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------- 2. DASHBOARD GALMEE BARATTOOTAA (FOOMII) -----------------
elif menu == "2. Dashboard Galmee Barataa (Foomii)":
    st.subheader("📝 Foomii Galmee Barattootaa Haaraa")

    db_existing = st.session_state.students_db
    default_godina = get_last_location(db_existing, "Godina")
    default_aanaa = get_last_location(db_existing, "Aanaa")
    default_ganda = get_last_location(db_existing, "Ganda")
    default_barsiisaa = st.session_state.current_user if st.session_state.current_user else get_last_location(db_existing, "Barsiisaa Galmeessee")
    default_guyyaa = get_last_location(db_existing, "Guyyaa Galmee (E.C)")
    if not default_guyyaa:
        default_guyyaa = "25/11/2018"

    st.markdown("### 🏫 Galmee Maqaa Mana Barumsaa Waliigalaa")
    school_input_col1, school_input_col2 = st.columns([3, 1])
    with school_input_col1:
        current_school_name = st.text_input("Maqaa Mana Barumsaa Kanaa (Save akka ta'uuf)", value=st.session_state.saved_school_name)
    with school_input_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save School Name"):
            if current_school_name.strip():
                st.session_state.saved_school_name = current_school_name.strip()
                st.success("Maqaan mana barumsaa milkaa'inaan save ta'eera!")
            else:
                st.warning("Maaloo maqaa mana barumsaa galchaa.")

    st.markdown("---")

    if "form_maqaa" not in st.session_state: st.session_state.form_maqaa = ""
    if "form_fan" not in st.session_state: st.session_state.form_fan = ""
    if "form_p_barataa" not in st.session_state: st.session_state.form_p_barataa = ""
    if "form_p_maatii" not in st.session_state: st.session_state.form_p_maatii = ""
    if "form_haadhaa" not in st.session_state: st.session_state.form_haadhaa = ""
    if "form_mb_biroo" not in st.session_state: st.session_state.form_mb_biroo = ""

    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa", value=st.session_state.form_maqaa)
            koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])
            
            grade_col1, grade_col2 = st.columns(2)
            kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
            daree = grade_col2.selectbox("Daree (Section)", [chr(65+i) for i in range(11)])

            st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**")
            b_col1, b_col2, b_col3 = st.columns(3)
            b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
            b_jiia = b_col2.selectbox(
                "Ji'a",
                [
                    "Fulbaana", "Onkololeessa", "Hacaaluu/Hidar", "Tamsaasa/Tahsas",
                    "Amajjii", "Guraandhala", "Bitootessa", "Ebla", "Caamsaa",
                    "Waxabajjii", "Aoleessa/Hamle", "Hagayya", "Pagume",
                ],
            )
            b_bara = b_col3.number_input(
                "Bara Dhalootaa (Fkn: 2011)", min_value=1990, max_value=2025, value=2011
            )
            current_et_year = 2018
            umurii = current_et_year - b_bara

            haala_galmee = st.selectbox(
                "5. Haala Galmee",
                ["Haaraa", "Kan darbe", "Irra deebii (Kufe)", "Irra deebii (Kute)", "Mana Barumsaa Biroo"],
            )
            
            bara_addaan_kute = st.selectbox(
                "Bara Addaan Kute (Yoo kute/kufe)",
                ["Hin jiru", "2005", "2006", "2007", "2008", "2009", "2010"]
                + [str(y) for y in range(2011, 2027)],
            )

            haala_maatii = st.selectbox(
                "6. Haala Maatii",
                ["Lachuu qaba", "Abbaa qofa", "Haadha qofa", "Lachuu hin qabu"],
            )
            
            miidhama_qaamaa = st.selectbox(
                "7. Haala Miidhama Qaamaa", ["Hin jiru", "Jira"]
            )
            
            gosa_miidhamaa = st.selectbox(
                "8. Gosa Miidhama Qaamaa (Yoo Jira ta'e filadhu)",
                [
                    "Hin qabu", "Arguu salphaa", "Arguu cimaa", "Dhageettii salphaa",
                    "Dhageettii cimaa", "Dubbii salphaa", "Dubbii cimaa", "Sochii salphaa",
                    "Sochii cimaa", "Saaleessa sammuu", "Currisa hawaasumaa", "Haadhaa fi abbaa dhabuu"
                ]
            )

        with col2:
            st.markdown("**9. Bakka Dhalootaa**")
            godina = st.text_input("Godina", value=default_godina)
            aanaa = st.text_input("Aanaa", value=default_aanaa)
            ganda = st.text_input("Ganda", value=default_ganda)

            maqaa_haadhaa = st.text_input("10. Maqaa Guutuu Haadhaa ykn Guddistuu", value=st.session_state.form_haadhaa)
            fan_id = st.text_input("11. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID - Digiti 16)", value=st.session_state.form_fan)
            lakk_bilbila_barataa = st.text_input("12. Lakkoofsa Bilbila Barataa (+251...)", value=st.session_state.form_p_barataa)
            lakk_bilbila_maatii = st.text_input("13. Lakkoofsa Bilbila Maatii (+251...)", value=st.session_state.form_p_maatii)
            
            st.markdown("---")
            st.markdown("**14. Mana Barumsaa Duraan Itti Barachaa Ture / Biroo**")
            school_mode = st.radio("Filannoo Mana Barumsaa:", ["Mana Barumsaa Duraan itti barachaa ture", "Mana barumsaa biroo"])
            
            if school_mode == "Mana Barumsaa Duraan itti barachaa ture":
                auto_school = st.session_state.saved_school_name if st.session_state.saved_school_name else "Hin jiru (Dursee Maqaa Mana Barumsaa Save Godhi)"
                st.info(f"Maqaa Mana Barumsaa Save ta'ee jiru: **{auto_school}**")
                mb_duraan = auto_school
            else:
                mb_duraan = st.text_input("Maqaa Mana Barumsaa Biroo (Mana barumsaa barataan irraa dhufe)", value=st.session_state.form_mb_biroo)

            avireejjii = st.number_input(
                "15. Avireejjii Qabxii Bara Darbee (0 - 100)",
                min_value=0.0, max_value=100.0, value=75.0,
            )

            barsiisaa = st.text_input("16. Barsiisaa Galmeessee", value=default_barsiisaa)
            guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C)", value=default_guyyaa)

        submitted = st.form_submit_button("💾 Save (Enter)")

        if submitted:
            st.session_state.form_maqaa = maqaa_guutuu
            st.session_state.form_fan = fan_id
            st.session_state.form_p_barataa = lakk_bilbila_barataa
            st.session_state.form_p_maatii = lakk_bilbila_maatii
            st.session_state.form_haadhaa = maqaa_haadhaa
            st.session_state.form_mb_biroo = mb_duraan

            error_msgs = []

            if not maqaa_guutuu:
                error_msgs.append("Maqaa Guutuu barataa guuti!")
            if koorniyaa == "Filadhu":
                error_msgs.append("Maaloo Koorniyaa barataa filadhu!")

            if avireejjii < 50 and haala_galmee != "Irra deebii (Kufe)":
                error_msgs.append('Barataan avireejjii 50 gadi fide haala galmeen "Irra deebii (Kufe)" jedhuun walsimuu qaba!')

            clean_fan = fan_id.strip()
            if clean_fan and (not clean_fan.isdigit() or len(clean_fan) != 16):
                error_msgs.append("FAN ID dijiitii 16 qofa ta'uu qaba!")

            def validate_phone(phone_str, field_label):
                p = phone_str.strip()
                if not p.startswith("+251"):
                    return f"{field_label}: Lakkoofsi bilbilaa '+251' tiin jalqabuu qaba!"
                subscriber_part = p[4:]
                if len(subscriber_part) != 9 or not subscriber_part.isdigit():
                    return f"{field_label}: Koodii biyyaa itti aansuun lakkoofsi jiru dijiitii 9 qofa ta'uu qaba."
                return None

            if lakk_bilbila_barataa.strip():
                err_p1 = validate_phone(lakk_bilbila_barataa, "Bilbila Barataa")
                if err_p1: error_msgs.append(err_p1)
            
            if lakk_bilbila_maatii.strip():
                err_p2 = validate_phone(lakk_bilbila_maatii, "Bilbila Maatii")
                if err_p2: error_msgs.append(err_p2)

            if error_msgs:
                for err in error_msgs:
                    st.markdown(f'<p style="color:red; font-weight:bold;">⚠️ {err}</p>', unsafe_allow_html=True)
            else:
                new_data = {
                    "Maqaa Guutuu": maqaa_guutuu,
                    "Koorniyaa": koorniyaa,
                    "Kutaa": kutaa,
                    "Daree (Section)": daree,
                    "Bara Dhalootaa": f"{b_guyyaa}/{b_jiia}/{b_bara}",
                    "Umurii": umurii,
                    "Haala Galmee": haala_galmee,
                    "Bara Addaan Kute": bara_addaan_kute,
                    "Haala Maatii": haala_maatii,
                    "Miidhama Qaamaa": miidhama_qaamaa,
                    "Gosa Miidhamaa": gosa_miidhamaa,
                    "Godina": godina,
                    "Aanaa": aanaa,
                    "Ganda": ganda,
                    "Maqaa Haadhaa/Guddistuu": maqaa_haadhaa,
                    "FAN ID": fan_id,
                    "Lakk Bilbila Barataa": lakk_bilbila_barataa,
                    "Lakk Bilbila Maatii": lakk_bilbila_maatii,
                    "M/B Duraan Itti Barachaa Ture": mb_duraan,
                    "Avireejjii Qabxii": avireejjii,
                    "Guyyaa Galmee (E.C)": guyyaa_galmee_ec,
                    "Barsiisaa Galmeessee": barsiisaa,
                }
                st.session_state.students_db = pd.concat(
                    [st.session_state.students_db, pd.DataFrame([new_data])],
                    ignore_index=True,
                )
                st.session_state.form_maqaa = ""
                st.session_state.form_fan = ""
                st.session_state.form_p_barataa = ""
                st.session_state.form_p_maatii = ""
                st.session_state.form_haadhaa = ""
                st.session_state.form_mb_biroo = ""
                
                st.success(f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!")

# ----------------- 3. DASHBOARD BARSIISAA / GABAASAA -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)":
    st.subheader("🔐 Dashboard Barsiisaa (Seensa Eeyyamame)")

    password = st.text_input("Password Galchi", type="password")

    if password == "kitesanegasa2012password" or password == "kitesa2019" or password == "admin123":
        st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa.")

        tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
            [
                "Karoora", "Guutuu", "Guyyaa", "Hanga Ammaa", "Miidhamaa", 
                "Lak. Miidhamaa", "Irra Deebii", "Lak. Irra Deebii", "Karoora vs Raawwii", "Edit/Delete"
            ]
        )

        db = st.session_state.students_db

        with tabA:
            st.markdown("### A. Guca Karoora Galmee Barataa (Dhiira, Dhalaa, Ida'ama)")
            with st.form("target_form"):
                selected_grade = st.selectbox(
                    "Kutaa Filadhu", [str(i) for i in range(1, 13)]
                )
                t_dhiira = st.number_input(
                    "Karoora Dhiiraa",
                    min_value=0,
                    value=st.session_state.targets[selected_grade]["Dhiira"],
                )
                t_dhalaa = st.number_input(
                    "Karoora Dhalaa",
                    min_value=0,
                    value=st.session_state.targets[selected_grade]["Dhalaa"],
                )
                save_target = st.form_submit_button("Karoora Galchi")
                if save_target:
                    st.session_state.targets[selected_grade]["Dhiira"] = t_dhiira
                    st.session_state.targets[selected_grade]["Dhalaa"] = t_dhalaa
                    st.success(f"Karoora Kutaa {selected_grade} galmeeffameera!")

            raw_targets = []
            for k in range(1, 13):
                k_str = str(k)
                td = st.session_state.targets[k_str]["Dhiira"]
                tdh = st.session_state.targets[k_str]["Dhalaa"]
                raw_targets.append({
                    "Kutaa_Num": k_str,
                    "Kutaa": f"Kutaa {k}",
                    "Dhiira": td,
                    "Dhalaa": tdh,
                    "Ida'ama": td + tdh
                })
            
            target_df = generate_grouped_report(raw_targets, title_col_name="Kutaa")
            st.dataframe(target_df, use_container_width=True)

            buffer_t = io.BytesIO()
            with pd.ExcelWriter(buffer_t, engine="openpyxl") as writer:
                target_df.to_excel(writer, sheet_name="Karoora_Galmee", index=False)
            st.download_button(
                label="📥 Karoora Print / Excel-tti Download Gochuu",
                data=buffer_t.getvalue(),
                file_name="Karoora_Galmee_Barattootaa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        with tabB:
            st.markdown("### B. Guca Gabaasaa Waligalaa Barataa")
            if not db.empty:
                st.dataframe(db, use_container_width=True)
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
                st.download_button(
                    label="📥 Gabaasa Guutuu Print / Excel-tti Download Gochuu",
                    data=buffer.getvalue(),
                    file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("Deetaan galmaa'e hin jiru.")

        with tabC:
            st.markdown("### C. Gabaasa Galmee Guyyaa Tokkoo")
            if not db.empty:
                available_dates = db["Guyyaa Galmee (E.C)"].unique().tolist()
                selected_date = st.selectbox("Guyyaa Filadhu (E.C)", available_dates, key="select_date_c")
                day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]
                
                if not day_df.empty:
                    raw_day = []
                    for k in range(1, 13):
                        sub_k = day_df[day_df["Kutaa"] == str(k)]
                        d_c = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                        dh_c = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                        raw_day.append({
                            "Kutaa_Num": str(k),
                            "Kutaa": f"Kutaa {k}",
                            "Dhiira": d_c,
                            "Dhalaa": dh_c,
                            "Ida'ama": d_c + dh_c
                        })
                    grouped_day_df = generate_grouped_report(raw_day, title_col_name="Kutaa")
                    st.dataframe(grouped_day_df, use_container_width=True)

                    buffer_c = io.BytesIO()
                    with pd.ExcelWriter(buffer_c, engine="openpyxl") as writer:
                        grouped_day_df.to_excel(writer, sheet_name="Gabaasa_Guyyaa", index=False)
                    st.download_button(
                        label="📥 Gabaasa Guyyaa Print / Excel",
                        data=buffer_c.getvalue(),
                        file_name=f"Gabaasa_Guyyaa_{selected_date.replace('/', '-')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Guyyaa filatame kana deetaan hin jiru.")
            else:
                st.info("Deetaan waligalaa hin jiru.")

        with tabD:
            st.markdown("### D. Gabaasa Galmee Hanga Ammaatti")
            if not db.empty:
                raw_summary = []
                for k in range(1, 13):
                    sub_k = db[db["Kutaa"] == str(k)]
                    d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                    dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                    raw_summary.append({
                        "Kutaa_Num": str(k),
                        "Kutaa": f"Kutaa {k}",
                        "Dhiira": d,
                        "Dhalaa": dh,
                        "Ida'ama": d + dh
                    })
                summary_df = generate_grouped_report(raw_summary, title_col_name="Kutaa")
                st.dataframe(summary_df, use_container_width=True)

                buffer_d = io.BytesIO()
                with pd.ExcelWriter(buffer_d, engine="openpyxl") as writer:
                    summary_df.to_excel(writer, sheet_name="Gabaasa_Hanga_Ammaa", index=False)
                st.download_button(
                    label="📥 Gabaasa Hanga Ammaa Print / Excel",
                    data=buffer_d.getvalue(),
                    file_name="Gabaasa_Hanga_Ammaatti.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("Deetaan hin jiru.")

        with tabE:
            st.markdown("### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii")
            if not db.empty:
                disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
                if not disabled_df.empty:
                    st.dataframe(disabled_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Gosa Miidhamaa"]], use_container_width=True)
                    
                    buffer_e = io.BytesIO()
                    with pd.ExcelWriter(buffer_e, engine="openpyxl") as writer:
                        disabled_df.to_excel(writer, sheet_name="Miidhama_Qaamaa", index=False)
                    st.download_button(
                        label="📥 Barattoota Miidhama Qaamaa Print / Excel",
                        data=buffer_e.getvalue(),
                        file_name="Barattoota_Miidhama_Qaamaa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan miidhama qaamaa qabu hin galmoofne.")
            else:
                st.info("Deetaan waligalaa hin jiru.")

        with tabF:
            st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa (Kutaa 1 - 8 fi Waliigalaa)")
            if not db.empty:
                disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
                if not disabled_df.empty:
                    pivot_data = []
                    disabilities = disabled_df["Gosa Miidhamaa"].unique()
                    for dis in disabilities:
                        row = {"Gosa Miidhamaa": dis}
                        sub_dis = disabled_df[disabled_df["Gosa Miidhamaa"] == dis]
                        
                        d_1_6, dh_1_6, d_7_8, dh_7_8 = 0, 0, 0, 0
                        for k in range(1, 13):
                            k_str = str(k)
                            sub_k = sub_dis[sub_dis["Kutaa"] == k_str]
                            cnt = len(sub_k)
                            row[f"Kutaa {k}"] = cnt
                            
                            if k <= 6:
                                d_1_6 += len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                                dh_1_6 += len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                            elif 7 <= k <= 8:
                                d_7_8 += len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                                dh_7_8 += len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                                
                        row["Ida'ama 1-6"] = d_1_6 + dh_1_6
                        row["Ida'ama 7-8"] = d_7_8 + dh_7_8
                        row["Ida'ama Waliigalaa"] = sum(row.get(f"Kutaa {k}", 0) for k in range(1, 13))
                        pivot_data.append(row)
                    
                    dis_summary_df = pd.DataFrame(pivot_data)
                    st.dataframe(dis_summary_df, use_container_width=True)

                    buffer_f = io.BytesIO()
                    with pd.ExcelWriter(buffer_f, engine="openpyxl") as writer:
                        dis_summary_df.to_excel(writer, sheet_name="Lakkoofsa_Miidhamaa", index=False)
                    st.download_button(
                        label="📥 Lakkoofsa Miidhamaa Print / Excel",
                        data=buffer_f.getvalue(),
                        file_name="Lakkoofsa_Gosa_Miidhamaa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan miidhama qaamaa qabu hin galmoofne.")
            else:
                st.info("Deetaan waligalaa hin jiru.")

        with tabG:
            st.markdown("### G. Gabaasa Barattoota Irra Deebi'anii (Repeat Table)")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
                if not repeat_df.empty:
                    display_repeat_df = repeat_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Umurii", "Haala Galmee", "Bara Addaan Kute"]].copy()
                    display_repeat_df.columns = ["Maqaa Guutuu", "Saala", "Kutaa", "Umurii", "Haala Irra Deebii", "Bara Irra Deebii"]
                    st.dataframe(display_repeat_df, use_container_width=True)
                    
                    buffer_g = io.BytesIO()
                    with pd.ExcelWriter(buffer_g, engine="openpyxl") as writer:
                        display_repeat_df.to_excel(writer, sheet_name="Irra_Deebii", index=False)
                    st.download_button(
                        label="📥 Barattoota Irra Deebii Print / Excel",
                        data=buffer_g.getvalue(),
                        file_name="Barattoota_Irra_Deebii.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan irra deebii galmaa'e hin jiru.")
            else:
                st.info("Deetaan waligalaa hin jiru.")

        with tabH:
            st.markdown("### H. Gabaasa Lakkoofsaa Irra Deebii (Tartiiba Kutaatiin)")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
                if not repeat_df.empty:
                    raw_rep = []
                    for k in range(1, 13):
                        sub_k = repeat_df[repeat_df["Kutaa"] == str(k)]
                        d_c = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                        dh_c = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                        raw_rep.append({
                            "Kutaa_Num": str(k),
                            "Kutaa": f"Kutaa {k}",
                            "Dhiira": d_c,
                            "Dhalaa": dh_c,
                            "Ida'ama": d_c + dh_c
                        })
                    grouped_rep_df = generate_grouped_report(raw_rep, title_col_name="Kutaa")
                    st.dataframe(grouped_rep_df, use_container_width=True)

                    buffer_h = io.BytesIO()
                    with pd.ExcelWriter(buffer_h, engine="openpyxl") as writer:
                        grouped_rep_df.to_excel(writer, sheet_name="Lakkoofsa_Irra_Deebii", index=False)
                    st.download_button(
                        label="📥 Lakkoofsa Irra Deebii Print / Excel",
                        data=buffer_h.getvalue(),
                        file_name="Lakkoofsa_Barattoota_Irra_Deebii.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan irra deebii galmaa'e hin jiru.")
            else:
                st.info("Deetaan waligalaa hin jiru.")

        with tabI:
            st.markdown("### I. Karoora vs Raawwii (Comparison - Tab A waliin wal fakkaatu)")
            if not db.empty:
                raw_comparison = []
                for k in range(1, 13):
                    k_str = str(k)
                    t_d = st.session_state.targets[k_str]["Dhiira"]
                    t_dh = st.session_state.targets[k_str]["Dhalaa"]
                    
                    sub_k = db[db["Kutaa"] == k_str]
                    a_d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                    a_dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                    
                    raw_comparison.append({
                        "Kutaa_Num": k_str,
                        "Kutaa": f"Kutaa {k}",
                        "Dhiira": f"Kar: {t_d} | Raw: {a_d}",
                        "Dhalaa": f"Kar: {t_dh} | Raw: {a_dh}",
                        "Ida'ama": f"Kar: {t_d+t_dh} | Raw: {a_d+a_dh}",
                        # Values for grouping calculation
                        "Dhiira_val": a_d,
                        "Dhalaa_val": a_dh
                    })
                
                # Custom comparison table following Tab A structure
                comp_rows_1_6_d = sum(r["Dhiira_val"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                comp_rows_1_6_dh = sum(r["Dhalaa_val"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                
                comp_rows_7_8_d = sum(r["Dhiira_val"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                comp_rows_7_8_dh = sum(r["Dhalaa_val"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                
                comp_rows_9_12_d = sum(r["Dhiira_val"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                comp_rows_9_12_dh = sum(r["Dhalaa_val"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)

                comp_final_table = []
                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) <= 6:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                comp_final_table.append({"Kutaa": "Ida'ama Kutaa 1 - 6", "Dhiira": str(comp_rows_1_6_d), "Dhalaa": str(comp_rows_1_6_dh), "Ida'ama": str(comp_rows_1_6_d + comp_rows_1_6_dh)})
                
                for r in raw_comparison:
                    if 7 <= int(r["Kutaa_Num"]) <= 8:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                comp_final_table.append({"Kutaa": "Ida'ama Kutaa 7 - 8", "Dhiira": str(comp_rows_7_8_d), "Dhalaa": str(comp_rows_7_8_dh), "Ida'ama": str(comp_rows_7_8_d + comp_rows_7_8_dh)})
                
                comp_final_table.append({"Kutaa": "Ida'ama Waliigalaa (1 - 8)", "Dhiira": str(comp_rows_1_6_d + comp_rows_7_8_d), "Dhalaa": str(comp_rows_1_6_dh + comp_rows_7_8_dh), "Ida'ama": str((comp_rows_1_6_d + comp_rows_7_8_d) + (comp_rows_1_6_dh + comp_rows_7_8_dh))})

                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) >= 9:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                comp_final_table.append({"Kutaa": "Ida'ama Kutaa 9 - 12", "Dhiira": str(comp_rows_9_12_d), "Dhalaa": str(comp_rows_9_12_dh), "Ida'ama": str(comp_rows_9_12_d + comp_rows_9_12_dh)})

                tot_d = comp_rows_1_6_d + comp_rows_7_8_d + comp_rows_9_12_d
                tot_dh = comp_rows_1_6_dh + comp_rows_7_8_dh + comp_rows_9_12_dh
                comp_final_table.append({"Kutaa": "Waliigalaa (1 - 12)", "Dhiira": str(tot_d), "Dhalaa": str(tot_dh), "Ida'ama": str(tot_d + tot_dh)})

                comp_df = pd.DataFrame(comp_final_table)
                st.dataframe(comp_df, use_container_width=True)
            else:
                st.info("Deetaan galmaa'e hin jiru.")

        with tabJ:
            st.markdown("### J. Barattoota Gulaaluu (Edit) ykn Haquu (Delete)")
            if not db.empty:
                search_name = st.text_input("Maqaa Barataa Barbaadi (Search by Name)")
                if search_name:
                    filtered_db = db[db["Maqaa Guutuu"].str.contains(search_name, case=False, na=False)]
                else:
                    filtered_db = db

                if not filtered_db.empty:
                    selected_idx = st.selectbox(
                        "Barataa Gulaaluuf ykn Haquuf Filadhu:",
                        filtered_db.index.tolist(),
                        format_func=lambda x: f"{db.loc[x, 'Maqaa Guutuu']} (Kutaa {db.loc[x, 'Kutaa']})"
                    )

                    col_j1, col_j2 = st.columns(2)
                    with col_j1:
                        if st.button("🗑️ Barataa Kana Haqi (Delete)"):
                            st.session_state.students_db = db.drop(selected_idx).reset_index(drop=True)
                            st.success("Barataan milkaa'inaan haqameera!")
                            st.rerun()
                else:
                    st.warning("Barataan argame hin jiru.")
            else:
                st.info("Deetaan galmaa'e hin jiru.")
    else:
        st.error("Password sirrii miti!")
