from datetime import datetime
import io
import sqlite3
import pandas as pd
import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Kitesa Negasa Feyisa - Student Registration System",
    page_icon="🎓",
    layout="wide",
)

# ============================================================================
# ENHANCED CSS - MODERN COVER PAGE & STYLING (FIX #1)
# ============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* === COVER CARD - Premium Design === */
    .cover-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #533483 100%);
        padding: 60px 40px;
        border-radius: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.5), 0 0 0 4px rgba(255,215,0,0.3), 0 0 0 8px rgba(255,215,0,0.1);
        border: 3px solid #ffd700;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease;
        animation: fadeInUp 0.8s ease;
    }

    .cover-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .cover-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 30px 70px rgba(0,0,0,0.6), 0 0 0 4px rgba(255,215,0,0.4);
    }

    .cover-card .icon {
        font-size: 72px;
        display: inline-block;
        background: rgba(255,215,0,0.15);
        padding: 20px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 3px solid #ffd700;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .cover-card h1 {
        color: #ffffff !important;
        font-size: 48px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 8px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .cover-card .subtitle {
        color: #f0e6ff !important;
        font-weight: 300;
        font-size: 22px;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }

    .cover-divider {
        height: 4px;
        width: 180px;
        background: linear-gradient(90deg, #ffd700, #ff6b6b, #ffd700);
        margin: 20px auto;
        border-radius: 2px;
        position: relative;
        z-index: 1;
    }

    .cover-card .description {
        font-size: 18px;
        opacity: 0.92;
        max-width: 700px;
        margin: 15px auto 0;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }

    /* === METRIC CARDS === */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f0f4ff);
        border: 2px solid #e3e6f0;
        padding: 25px 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(78,115,223,0.3);
        border-color: #4e73df;
        background: linear-gradient(145deg, #ffffff, #e8edff);
    }

    .metric-card h4 {
        color: #2e384d;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .metric-card h2 {
        color: #4e73df;
        font-weight: 800;
        font-size: 36px;
        margin: 5px 0;
    }

    .metric-card p {
        color: #6b7a8f;
        font-size: 13px;
        font-weight: 400;
    }

    /* === CONTACT CARD === */
    .contact-card {
        background: linear-gradient(135deg, #ffffff 0%, #eef2f9 100%);
        border: 2px solid #4e73df;
        border-radius: 16px;
        padding: 24px 30px;
        margin-top: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }

    .contact-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(78,115,223,0.2);
    }

    .contact-card h4 {
        color: #1e3c72;
        font-weight: 700;
        margin-bottom: 12px;
        font-size: 20px;
    }

    .contact-card p {
        margin: 6px 0;
        font-size: 15px;
        color: #2e384d;
        font-weight: 400;
    }

    .contact-card .contact-icon {
        display: inline-block;
        width: 32px;
        text-align: center;
    }

    /* === BUTTONS === */
    .stButton>button {
        background: linear-gradient(135deg, #4e73df 0%, #2e59d9 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(78,115,223,0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2e59d9 0%, #1e3c72 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(78,115,223,0.4);
    }

    /* === HEADINGS === */
    h1, h2, h3, h4, h5 {
        color: #1e3c72;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* === TAB STYLING === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f0f4ff;
        border-radius: 12px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        color: #4a5568;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4e73df, #2e59d9) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(78,115,223,0.3);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(78,115,223,0.1);
    }

    /* === SIDEBAR === */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
    }

    .css-1d391kg .css-1v3fvcr {
        color: white;
    }

    /* === DATA FRAME === */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* === INFO BOXES === */
    .stAlert {
        border-radius: 12px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# CONTACT INFO (FIX #2)
# ============================================================================
CONTACT_INFO_HTML = """
<div class="contact-card">
    <h4>📞 Contact Information | Odeeffannoo Qunnamtii</h4>
    <p>📱 <b>Phone &amp; Telegram:</b> +251969184005 / 910927936</p>
    <p>📧 <b>Gmail:</b> kitesanegasa2012@gmail.com</p>
    <p>📘 <b>Facebook:</b> Kitesa Negasa</p>
</div>
"""

# ============================================================================
# DATABASE (SQLite) - PERSISTENT STORAGE
# ============================================================================
DB_PATH = "kitesa_negasa_data.db"

# STUDENT COLUMNS - Fixed column names for consistency
STUDENT_COLUMNS = [
    "Maqaa Guutuu",           # Full Name
    "Koorniyaa",              # Gender
    "Kutaa",                  # Grade
    "Daree (Section)",        # Section
    "Bara Dhalootaa",         # Birth Date
    "Umurii",                 # Age
    "Haala Galmee",           # Registration Status
    "Bara Addaan Kute",       # Dropout Year
    "Haala Maatii",           # Family Status
    "Miidhama Qaamaa",        # Disability
    "Gosa Miidhamaa",         # Disability Type
    "Godina",                 # Zone
    "Aanaa",                  # District
    "Ganda",                  # Village
    "Maqaa Haadhaa/Guddistuu",# Mother/Guardian Name
    "FAN ID",                 # FAN ID
    "Lakk Bilbila Barataa",   # Student Phone
    "Lakk Bilbila Maatii",    # Family Phone
    "M/B Duraan Itti Barachaa Ture", # Previous School
    "Avireejjii Qabxii",      # Average Score
    "Guyyaa Galmee (E.C)",    # Registration Date
    "Barsiisaa Galmeessee",   # Teacher Registrar
    "Mana Barumsaa",          # School Name (NEW)
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
            'SELECT id, gmail AS Gmail, login_time AS "Login Time / Guyyaa Saatii" FROM login_history ORDER BY id DESC',
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


def delete_login_record(record_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM login_history WHERE id = ?", (record_id,))
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


def get_students_by_school(school_name):
    """Fetch students for a specific school"""
    conn = get_connection()
    try:
        df = pd.read_sql_query(
            'SELECT * FROM students WHERE "Mana Barumsaa" = ? ORDER BY id',
            conn,
            params=(school_name,)
        )
    finally:
        conn.close()
    return df


def get_all_schools():
    """Get list of all unique school names"""
    conn = get_connection()
    try:
        df = pd.read_sql_query(
            'SELECT DISTINCT "Mana Barumsaa" FROM students WHERE "Mana Barumsaa" IS NOT NULL AND "Mana Barumsaa" != "" ORDER BY "Mana Barumsaa"',
            conn
        )
        schools = df["Mana Barumsaa"].tolist() if not df.empty else []
    finally:
        conn.close()
    return schools


def delete_school_data(school_name):
    """Delete all students from a specific school"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE "Mana Barumsaa" = ?', (school_name,))
    conn.commit()
    conn.close()


init_db()

# ----------------- SESSION STATE -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_school" not in st.session_state:
    st.session_state.current_school = ""

# Authorized Users Database
AUTHORIZED_USERS = {
    "kitesanegasa2012@gmail.com": "kitesanegasa2012password",
    "barsiisaa1@gmail.com": "pass1234",
    "bulchaa@gmail.com": "admin2026",
    "feyisamililu23@gmail.com": "20481092F",
}

# Report Passwords
REPORT_PASSWORDS = ["kitesanegasa2012password", "kitesa2019", "admin123"]

# Admin Password
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
    """Calculate percentage - FIX #8"""
    try:
        if target and float(target) > 0:
            return f"{(float(actual) / float(target) * 100):.1f}%"
    except (ValueError, TypeError):
        pass
    return "-"


def report_header(title):
    """Generate report header with school name and academic year - FIX #6"""
    school_name = get_setting("saved_school_name", ".................")
    academic_year = get_setting("bara_barnootaa", "2019")
    return f"#### 📄 {title} - 🏫 {school_name} — Bara {academic_year} / Academic Year {academic_year}"


# ----------------- LOGIN SCREEN -----------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="cover-card" style="max-width: 550px; margin: 50px auto;">
            <div style="font-size:50px;">🔐</div>
            <h1 style="font-size:32px;">Login | Eeyyama</h1>
            <div class="cover-divider"></div>
            <p style="font-size:16px; opacity:0.9;">Please enter your Gmail and Password to access the system.</p>
            <p style="font-size:14px; opacity:0.7;">Maaloo Gmail fi Password galchi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            input_email = st.text_input("Gmail / Email")
            input_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("🔑 Seeni (Login)")

            if submit_login:
                if input_email in AUTHORIZED_USERS and AUTHORIZED_USERS[input_email] == input_password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = input_email
                    save_login(input_email)
                    st.success(f"Baga nagaan dhufte! Welcome {input_email}!")
                    st.rerun()
                else:
                    st.error("Gmail ykn Password sirrii miti! Invalid credentials!")

        st.markdown("---")
        st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

    st.stop()

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.markdown(f"👤 **User:** `{st.session_state.current_user}`")
st.sidebar.markdown("### 🏫 Kitesa Negasa Feyisa")

# --- School Selection for Multi-School Support (FIX #8) ---
all_schools = get_all_schools()
if all_schools:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏫 School Filter | Mana Barumsaa")
    school_filter = st.sidebar.selectbox(
        "Select School / Mana Barumsaa Filadhu",
        ["All Schools / Hunda"] + all_schools,
        key="school_filter"
    )
else:
    school_filter = "All Schools / Hunda"

menu = st.sidebar.selectbox(
    "📋 Navigation | Baafataa",
    [
        "1. Cover Page | Fuula Jalqabaa",
        "2. Student Registration | Galmee Barataa",
        "3. Reports & Dashboard | Gabaasa (Password Needed)",
        "4. Admin Dashboard | Bulchiinsaa (Password Needed)",
        "5. Login History | Seenaa Seensaa",
        "6. Multi-School Dashboard | Manneen Barnootaa",
        "7. Logout | Baasi",
    ],
)

if menu == "7. Logout | Baasi":
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# ============================================================================
# 1. COVER PAGE (FIX #1 & #2)
# ============================================================================
if menu == "1. Cover Page | Fuula Jalqabaa":
    st.markdown(
        """
        <div class="cover-card">
            <div class="icon">🎓</div>
            <h1>STUDENT REGISTRATION SYSTEM</h1>
            <h1 style="font-size:28px; color:#ffd700 !important;">SIRNA GALMEE BARATTOOTAA</h1>
            <div class="cover-divider"></div>
            <p class="subtitle">Created By / Kalaqame: <strong>Kitesa Negasa Feyisa</strong></p>
            <p class="description">
                This system helps schools register students, track attendance, generate reports, 
                and manage student data efficiently across multiple schools.<br>
                <span style="color:#ffd700;">Sirni kun barattoota galmeessuu, gabaasa qindeessuu fi 
                odeeffannoo barattootaa hordofuuf kan gargaaru.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # School Name Display
    school_name_cover = get_setting("saved_school_name", "")
    if school_name_cover:
        st.markdown(
            f"""
            <div style="text-align:center; margin-top:25px; padding:15px; 
                 background:linear-gradient(135deg, #4e73df, #2e59d9); 
                 border-radius:12px; color:white;">
                <h3 style="color:white; margin:0;">🏫 {school_name_cover}</h3>
                <p style="margin:5px 0 0; opacity:0.8;">Academic Year / Bara Barnootaa: {get_setting('bara_barnootaa', '2019')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("---")

    # Student Count by Grade - Filter by selected school
    db = load_students()
    if school_filter != "All Schools / Hunda" and not db.empty:
        db = db[db["Mana Barumsaa"] == school_filter]

    st.subheader("📊 Student Count by Grade | Lakkoofsa Barattootaa Kutaa Kutaan")

    cols = st.columns(4)
    for i in range(1, 13):
        count = len(db[db["Kutaa"] == str(i)]) if not db.empty else 0
        with cols[(i - 1) % 4]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>Kutaa {i} | Grade {i}</h4>
                    <h2>{count}</h2>
                    <p>Students | Barattoota</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("---")
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

# ============================================================================
# 2. STUDENT REGISTRATION FORM (FIX #4 - Haala Galmee outside form)
# ============================================================================
elif menu == "2. Student Registration | Galmee Barataa":
    st.subheader("📝 Student Registration Form | Foormii Galmee Barattootaa")

    db_existing = load_students()
    if school_filter != "All Schools / Hunda" and not db_existing.empty:
        db_existing = db_existing[db_existing["Mana Barumsaa"] == school_filter]

    default_godina = get_last_location(db_existing, "Godina")
    default_aanaa = get_last_location(db_existing, "Aanaa")
    default_ganda = get_last_location(db_existing, "Ganda")
    default_barsiisaa = st.session_state.current_user if st.session_state.current_user else get_last_location(db_existing, "Barsiisaa Galmeessee")
    default_guyyaa = get_last_location(db_existing, "Guyyaa Galmee (E.C)")
    if not default_guyyaa:
        default_guyyaa = "25/11/2018"

    saved_school_name = get_setting("saved_school_name", "")

    st.markdown("### 🏫 School Name | Maqaa Mana Barumsaa")
    school_input_col1, school_input_col2 = st.columns([3, 1])
    with school_input_col1:
        current_school_name = st.text_input(
            "Enter School Name / Maqaa Mana Barumsaa Galchi",
            value=saved_school_name,
        )
    with school_input_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save School | Save Godhi"):
            if current_school_name.strip():
                set_setting("saved_school_name", current_school_name.strip())
                st.success("School name saved! Maqaan mana barumsaa save ta'eera!")
                st.rerun()
            else:
                st.warning("Please enter a school name. Maaloo maqaa galchi.")

    saved_school_name = get_setting("saved_school_name", "")
    st.markdown("---")

    # --- Haala Galmee outside form (FIX #4) ---
    st.markdown("**5. Registration Status | Haala Galmee** _(Select this first / Kana dursaa filadhaa)_")
    haala_galmee = st.selectbox(
        "Registration Status / Haala Galmee",
        ["Haaraa | New", "Kan darbe | Previous", "Irra deebii (Kufe) | Repeat (Failed)", 
         "Irra deebii (Kute) | Repeat (Dropped)", "Irra deebii Mana Barumsaa Biroo | Transfer Repeat", 
         "Mana Barumsaa Biroo | From Other School"],
        key="haala_galmee_select",
    )
    st.markdown("---")

    # Session state for form persistence
    if "form_maqaa" not in st.session_state: st.session_state.form_maqaa = ""
    if "form_fan" not in st.session_state: st.session_state.form_fan = ""
    if "form_p_barataa" not in st.session_state: st.session_state.form_p_barataa = ""
    if "form_p_maatii" not in st.session_state: st.session_state.form_p_maatii = ""
    if "form_haadhaa" not in st.session_state: st.session_state.form_haadhaa = ""
    if "form_mb_biroo" not in st.session_state: st.session_state.form_mb_biroo = ""

    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            maqaa_guutuu = st.text_input("1. Full Name | Maqaa Guutuu", value=st.session_state.form_maqaa)
            koorniyaa = st.selectbox("2. Gender | Koorniyaa", ["Filadhu | Select", "Dhiira | Male", "Dhalaa | Female"])

            grade_col1, grade_col2 = st.columns(2)
            kutaa = grade_col1.selectbox("3. Grade | Kutaa", [str(i) for i in range(1, 13)])
            daree = grade_col2.selectbox("Section | Daree", [chr(65 + i) for i in range(11)])

            st.markdown("**4. Birth Date (Ethiopian Calendar) | Bara Dhalootaa (Akk. Itoophiyaatti)**")
            b_col1, b_col2, b_col3 = st.columns(3)
            b_guyyaa = b_col1.selectbox("Day | Guyyaa", [str(i) for i in range(1, 32)])
            b_jiia = b_col2.selectbox(
                "Month | Ji'a",
                [
                    "Fulbaana", "Onkololeessa", "Sadaasa", "Muddee",
                    "Amajjii", "Guraandhala", "Bitootessa", "Ebla", "Caamsaa",
                    "Waxabajjii", "Adoolessa", "Hagayya", "Pagumee",
                ],
            )
            b_bara = b_col3.number_input(
                "Year | Bara (e.g., 2011)", min_value=1990, max_value=2025, value=2011
            )
            current_et_year = 2018
            umurii = current_et_year - b_bara

            st.text_input("5. Registration Status | Haala Galmee (Selected / Filatame)", value=haala_galmee, disabled=True)

            bara_addaan_kute = st.selectbox(
                "Dropout Year | Bara Addaan Kute",
                ["Hin jiru | None", "2005", "2006", "2007", "2008", "2009", "2010"]
                + [str(y) for y in range(2011, 2027)],
            )

            haala_maatii = st.selectbox(
                "6. Family Status | Haala Maatii",
                ["Lachuu qaba | Both parents", "Abbaa qofa | Father only", 
                 "Haadha qofa | Mother only", "Lachuu hin qabu | Neither"],
            )

            miidhama_qaamaa = st.selectbox(
                "7. Disability | Miidhama Qaamaa", ["Hin jiru | No", "Jira | Yes"]
            )

            gosa_miidhamaa = st.selectbox(
                "8. Disability Type | Gosa Miidhamaa",
                [
                    "Hin qabu | None", "Arguu salphaa | Mild visual", "Arguu cimaa | Severe visual",
                    "Dhageettii salphaa | Mild hearing", "Dhageettii cimaa | Severe hearing",
                    "Dubbii salphaa | Mild speech", "Dubbii cimaa | Severe speech",
                    "Sochii salphaa | Mild physical", "Sochii cimaa | Severe physical",
                    "Saaleessa sammuu | Intellectual", "Currisa hawaasumaa | Social",
                    "Haadhaa fi abbaa dhabuu | Orphan"
                ]
            )

        with col2:
            st.markdown("**9. Birthplace | Bakka Dhalootaa**")
            godina = st.text_input("Zone | Godina", value=default_godina)
            aanaa = st.text_input("District | Aanaa", value=default_aanaa)
            ganda = st.text_input("Village | Ganda", value=default_ganda)

            maqaa_haadhaa = st.text_input(
                "10. Mother/Guardian Name | Maqaa Haadhaa/Guddistuu",
                value=st.session_state.form_haadhaa,
            )
            fan_id = st.text_input(
                "11. FAN ID (16 digits) | Lakkoofsa FAN ID (Digiti 16)",
                value=st.session_state.form_fan,
            )
            lakk_bilbila_barataa = st.text_input(
                "12. Student Phone | Lakk Bilbila Barataa (+251...)",
                value=st.session_state.form_p_barataa,
            )
            lakk_bilbila_maatii = st.text_input(
                "13. Family Phone | Lakk Bilbila Maatii (+251...)",
                value=st.session_state.form_p_maatii,
            )
            st.markdown("---")
            st.markdown("**14. Previous School | M/B Duraan Itti Barachaa Ture**")

            if haala_galmee not in [
                "Mana Barumsaa Biroo | From Other School",
                "Irra deebii Mana Barumsaa Biroo | Transfer Repeat",
            ]:
                if saved_school_name:
                    st.info(f"Current School automatically filled / Maqaan Mana Barumsaa ofumaan guutame: **{saved_school_name}**")
                    mb_duraan = saved_school_name
                else:
                    mb_duraan = st.text_input(
                        "Previous School Name | Maqaa Mana Barumsaa (Dursee kan barachaa ture)",
                        value=st.session_state.get("form_mb_biroo", ""),
                    )
            else:
                mb_duraan = st.text_input(
                    "Previous/Transfer School Name | Maqaa Mana Barumsaa Biroo",
                    value=st.session_state.get("form_mb_biroo", ""),
                )

            avireejjii = st.number_input(
                "15. Average Score | Avireejjii Qabxii (0 - 100)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
            )
            barsiisaa = st.text_input("16. Teacher Registrar | Barsiisaa Galmeessee", value=default_barsiisaa)
            guyyaa_galmee_ec = st.text_input("Registration Date (E.C) | Guyyaa Galmee (E.C)", value=default_guyyaa)

        submitted = st.form_submit_button("💾 Save Student | Barataa Save Godhi")

    if submitted:
        st.session_state.form_maqaa = maqaa_guutuu
        st.session_state.form_fan = fan_id
        st.session_state.form_p_barataa = lakk_bilbila_barataa
        st.session_state.form_p_maatii = lakk_bilbila_maatii
        st.session_state.form_haadhaa = maqaa_haadhaa
        st.session_state.form_mb_biroo = mb_duraan
        error_msgs = []

        if not maqaa_guutuu:
            error_msgs.append("Please enter student full name! Maaloo maqaa guutuu barataa galchi!")
        if koorniyaa == "Filadhu | Select":
            error_msgs.append("Please select gender! Maaloo koorniyaa filadhu!")

        if avireejjii < 50 and haala_galmee != "Irra deebii (Kufe) | Repeat (Failed)":
            error_msgs.append(
                'Student with score below 50 must be "Irra deebii (Kufe) | Repeat (Failed)"!'
            )

        clean_fan = fan_id.strip()
        if clean_fan and (not clean_fan.isdigit() or len(clean_fan) != 16):
            error_msgs.append("FAN ID must be exactly 16 digits! FAN ID dijiitii 16 qofa ta'uu qaba!")

        def validate_phone(phone_str, field_label):
            p = phone_str.strip()
            if p and not p.startswith("+251"):
                return f"{field_label}: Phone must start with +251! {field_label}: Lakkoofsi bilbilaa '+251' tiin jalqabuu qaba!"
            if p and len(p[4:]) != 9:
                return f"{field_label}: Phone must have 9 digits after +251! {field_label}: Koodii biyyaa itti aansuun lakkoofsi jiru dijiitii 9 qofa ta'uu qaba."
            return None

        if lakk_bilbila_barataa.strip():
            err_p1 = validate_phone(lakk_bilbila_barataa, "Student Phone | Bilbila Barataa")
            if err_p1:
                error_msgs.append(err_p1)

        if lakk_bilbila_maatii.strip():
            err_p2 = validate_phone(lakk_bilbila_maatii, "Family Phone | Bilbila Maatii")
            if err_p2:
                error_msgs.append(err_p2)

        if error_msgs:
            for err in error_msgs:
                st.markdown(
                    f'<p style="color:red; font-weight:bold;">⚠️ {err}</p>',
                    unsafe_allow_html=True,
                )
        else:
            # Get the actual school name from settings
            actual_school_name = get_setting("saved_school_name", saved_school_name)
            
            new_data = {
                "Maqaa Guutuu": maqaa_guutuu,
                "Koorniyaa": koorniyaa.replace(" | Male", "").replace(" | Female", ""),
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
                "Mana Barumsaa": actual_school_name,  # NEW field
            }

            insert_student(new_data)

            st.session_state.form_maqaa = ""
            st.session_state.form_fan = ""
            st.session_state.form_p_barataa = ""
            st.session_state.form_p_maatii = ""
            st.session_state.form_haadhaa = ""
            st.session_state.form_mb_biroo = ""

            st.success(f"Student {maqaa_guutuu} registered successfully! Galmeen barataa milkaa'inaan save ta'eera!")

# ============================================================================
# 3. REPORTS & DASHBOARD (FIX #3, #5, #6, #7)
# ============================================================================
elif menu == "3. Reports & Dashboard | Gabaasa (Password Needed)":
    st.subheader("🔐 Reports & Dashboard | Gabaasa fi Kuusaa")

    password = st.text_input("Enter Password | Password Galchi", type="password")

    if password in REPORT_PASSWORDS:
        st.success("✅ Access Granted! Seensa Milkaa'e!")

        # --- School Name and Academic Year Header (FIX #6) ---
        school_name_display = get_setting("saved_school_name", ".................")
        bara_barnootaa = st.text_input(
            "🗓️ Academic Year (E.C) | Bara Barnootaa",
            value=get_setting("bara_barnootaa", "2019"),
        )
        if st.button("Save Academic Year | Bara Barnootaa Save Godhi"):
            set_setting("bara_barnootaa", bara_barnootaa)
            st.success("Academic year saved! Bara barnootaa save ta'eera!")
            st.rerun()

        st.markdown("---")

        # Filter by school
        all_schools = get_all_schools()
        if all_schools:
            report_school_filter = st.selectbox(
                "🏫 Filter by School | Mana Barumsaa Filadhu",
                ["All Schools | Hunda"] + all_schools,
                key="report_school_filter"
            )
        else:
            report_school_filter = "All Schools | Hunda"

        tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
            [
                "📊 Karoora | Target",
                "📋 Guutuu | All",
                "📅 Guyyaa | Daily",
                "📈 Hanga Ammaa | YTD",
                "♿ Miidhamaa | Disability",
                "🔢 Lak. Miidhamaa | Disability Count",
                "🔄 Irra Deebii | Repeat",
                "🔢 Lak. Irra Deebii | Repeat Count",
                "📊 Karoora vs Raawwii | Target vs Actual",
                "✏️ Edit/Delete | Gulaali/Haqi",
            ]
        )

        # Load data with school filter
        db = load_students()
        if report_school_filter != "All Schools | Hunda" and not db.empty:
            db = db[db["Mana Barumsaa"] == report_school_filter]

        targets = load_targets()

        with tabA:
            st.markdown(report_header("Karoora Galmee Barataa | Student Registration Target"))
            st.markdown("### A. Target Report | Guca Karoora Galmee")

            with st.form("target_form"):
                selected_grade = st.selectbox(
                    "Select Grade | Kutaa Filadhu", [str(i) for i in range(1, 13)]
                )
                t_dhiira = st.number_input(
                    "Target Male | Karoora Dhiiraa",
                    min_value=0,
                    value=targets[selected_grade]["Dhiira"],
                )
                t_dhalaa = st.number_input(
                    "Target Female | Karoora Dhalaa",
                    min_value=0,
                    value=targets[selected_grade]["Dhalaa"],
                )
                save_target_btn = st.form_submit_button("💾 Save Target | Karoora Galchi")
                if save_target_btn:
                    save_target(selected_grade, t_dhiira, t_dhalaa)
                    st.success(f"Target for Grade {selected_grade} saved! Karoora Kutaa {selected_grade} galmeeffameera!")
                    st.rerun()

            raw_targets = []
            for k in range(1, 13):
                k_str = str(k)
                td = targets[k_str]["Dhiira"]
                tdh = targets[k_str]["Dhalaa"]
                raw_targets.append({
                    "Kutaa_Num": k_str,
                    "Kutaa": f"Kutaa {k} | Grade {k}",
                    "Dhiira": td,
                    "Dhalaa": tdh,
                    "Ida'ama": td + tdh
                })

            target_df = generate_grouped_report(raw_targets, title_col_name="Kutaa | Grade")
            st.dataframe(target_df, use_container_width=True)

            buffer_t = io.BytesIO()
            with pd.ExcelWriter(buffer_t, engine="openpyxl") as writer:
                target_df.to_excel(writer, sheet_name="Karoora_Galmee | Target", index=False)
            st.download_button(
                label="📥 Download Target Report | Karoora Print / Excel",
                data=buffer_t.getvalue(),
                file_name="Karoora_Galmee_Barattootaa_Target_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        with tabB:
            st.markdown(report_header("Gabaasa Galmee Waliigalaa | Full Student Report"))
            st.markdown("### B. Full Student Report | Gabaasaa Waligalaa")
            if not db.empty:
                st.dataframe(db, use_container_width=True)
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    db.to_excel(writer, sheet_name="Gabaasa_Guutuu | Full Report", index=False)
                st.download_button(
                    label="📥 Download Full Report | Gabaasa Guutuu Print / Excel",
                    data=buffer.getvalue(),
                    file_name="Gabaasa_Waligalaa_Barattootaa_Full_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("No students registered. Baratoonni hin galmoofne.")

        with tabC:
            st.markdown(report_header("Gabaasa Galmee Guyyaa Tokkoo | Daily Registration Report"))
            st.markdown("### C. Daily Registration Report | Gabaasa Galmee Guyyaa Tokkoo")
            if not db.empty:
                available_dates = db["Guyyaa Galmee (E.C)"].unique().tolist()
                selected_date = st.selectbox("Select Date (E.C) | Guyyaa Filadhu", available_dates, key="select_date_c")
                day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]

                if not day_df.empty:
                    raw_day = []
                    for k in range(1, 13):
                        sub_k = day_df[day_df["Kutaa"] == str(k)]
                        d_c = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                        dh_c = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                        raw_day.append({
                            "Kutaa_Num": str(k),
                            "Kutaa": f"Kutaa {k} | Grade {k}",
                            "Dhiira": d_c,
                            "Dhalaa": dh_c,
                            "Ida'ama": d_c + dh_c
                        })
                    grouped_day_df = generate_grouped_report(raw_day, title_col_name="Kutaa | Grade")
                    st.dataframe(grouped_day_df, use_container_width=True)

                    buffer_c = io.BytesIO()
                    with pd.ExcelWriter(buffer_c, engine="openpyxl") as writer:
                        grouped_day_df.to_excel(writer, sheet_name="Gabaasa_Guyyaa | Daily", index=False)
                    st.download_button(
                        label="📥 Download Daily Report | Gabaasa Guyyaa Print / Excel",
                        data=buffer_c.getvalue(),
                        file_name=f"Gabaasa_Guyyaa_{selected_date.replace('/', '-')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("No data for selected date. Guyyaa filatame kana deetaan hin jiru.")
            else:
                st.info("No students registered. Deetaan waligalaa hin jiru.")

        with tabD:
            st.markdown(report_header("Gabaasa Galmee Hanga Ammaatti | Year-to-Date Report"))
            st.markdown("### D. Year-to-Date Report | Gabaasa Galmee Hanga Ammaatti")
            if not db.empty:
                raw_summary = []
                for k in range(1, 13):
                    sub_k = db[db["Kutaa"] == str(k)]
                    d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                    dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                    raw_summary.append({
                        "Kutaa_Num": str(k),
                        "Kutaa": f"Kutaa {k} | Grade {k}",
                        "Dhiira": d,
                        "Dhalaa": dh,
                        "Ida'ama": d + dh
                    })
                summary_df = generate_grouped_report(raw_summary, title_col_name="Kutaa | Grade")
                st.dataframe(summary_df, use_container_width=True)

                buffer_d = io.BytesIO()
                with pd.ExcelWriter(buffer_d, engine="openpyxl") as writer:
                    summary_df.to_excel(writer, sheet_name="Gabaasa_Hanga_Ammaa | YTD", index=False)
                st.download_button(
                    label="📥 Download YTD Report | Gabaasa Hanga Ammaa Print / Excel",
                    data=buffer_d.getvalue(),
                    file_name="Gabaasa_Hanga_Ammaatti_YTD.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("No students registered. Deetaan hin jiru.")

        with tabE:
            st.markdown(report_header("Gabaasa Barattoota Miidhama Qaamaa Qaban | Students with Disabilities"))
            st.markdown("### E. Students with Disabilities Report | Gabaasa Barattoota Miidhama Qaamaa Qabanii")
            if not db.empty:
                disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
                if not disabled_df.empty:
                    st.dataframe(disabled_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Gosa Miidhamaa"]], use_container_width=True)

                    buffer_e = io.BytesIO()
                    with pd.ExcelWriter(buffer_e, engine="openpyxl") as writer:
                        disabled_df.to_excel(writer, sheet_name="Miidhama_Qaamaa | Disability", index=False)
                    st.download_button(
                        label="📥 Download Disability Report | Barattoota Miidhama Qaamaa Print / Excel",
                        data=buffer_e.getvalue(),
                        file_name="Barattoota_Miidhama_Qaamaa_Disability.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("No students with disabilities registered. Barataan miidhama qaamaa qabu hin galmoofne.")
            else:
                st.info("No students registered. Deetaan waligalaa hin jiru.")

        with tabF:
            st.markdown(report_header("Gabaasa Lakkoofsa Miidhama Qaamaa | Disability Count Report"))
            st.markdown("### F. Disability Count Report | Gabaasa Lakkoofsaa Miidhama Qaamaa")
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
                        dis_summary_df.to_excel(writer, sheet_name="Lakkoofsa_Miidhamaa | Disability Count", index=False)
                    st.download_button(
                        label="📥 Download Disability Count | Lakkoofsa Miidhamaa Print / Excel",
                        data=buffer_f.getvalue(),
                        file_name="Lakkoofsa_Gosa_Miidhamaa_Disability_Count.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("No students with disabilities registered. Barataan miidhama qaamaa qabu hin galmoofne.")
            else:
                st.info("No students registered. Deetaan waligalaa hin jiru.")

        with tabG:
            st.markdown(report_header("Gabaasa Barattoota Irra Deebi'anii | Repeat Students Report"))
            st.markdown("### G. Repeat Students Report | Gabaasa Barattoota Irra Deebi'anii")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
                if not repeat_df.empty:
                    display_repeat_df = repeat_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Umurii", "Haala Galmee", "Bara Addaan Kute"]].copy()
                    display_repeat_df.columns = ["Full Name | Maqaa Guutuu", "Gender | Saala", "Grade | Kutaa", "Age | Umurii", "Repeat Status | Haala Irra Deebii", "Dropout Year | Bara Irra Deebii"]
                    st.dataframe(display_repeat_df, use_container_width=True)

                    buffer_g = io.BytesIO()
                    with pd.ExcelWriter(buffer_g, engine="openpyxl") as writer:
                        display_repeat_df.to_excel(writer, sheet_name="Irra_Deebii | Repeat", index=False)
                    st.download_button(
                        label="📥 Download Repeat Report | Barattoota Irra Deebii Print / Excel",
                        data=buffer_g.getvalue(),
                        file_name="Barattoota_Irra_Deebii_Repeat_Report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("No repeat students registered. Barataan irra deebii galmaa'e hin jiru.")
            else:
                st.info("No students registered. Deetaan waligalaa hin jiru.")

        with tabH:
            st.markdown(report_header("Gabaasa Lakkoofsa Irra Deebii | Repeat Count Report"))
            st.markdown("### H. Repeat Count Report | Gabaasa Lakkoofsaa Irra Deebii")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
                if not repeat_df.empty:
                    raw_rep = []
                    for k in range(1, 13):
                        sub_k = repeat_df[repeat_df["Kutaa"] == str(k)]
                        d_c = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                        dh_c = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                        raw_rep.append({
                            "Kutaa_Num": str(k),
                            "Kutaa": f"Kutaa {k} | Grade {k}",
                            "Dhiira": d_c,
                            "Dhalaa": dh_c,
                            "Ida'ama": d_c + dh_c
                        })
                    grouped_rep_df = generate_grouped_report(raw_rep, title_col_name="Kutaa | Grade")
                    st.dataframe(grouped_rep_df, use_container_width=True)

                    buffer_h = io.BytesIO()
                    with pd.ExcelWriter(buffer_h, engine="openpyxl") as writer:
                        grouped_rep_df.to_excel(writer, sheet_name="Lakkoofsa_Irra_Deebii | Repeat Count", index=False)
                    st.download_button(
                        label="📥 Download Repeat Count | Lakkoofsa Irra Deebii Print / Excel",
                        data=buffer_h.getvalue(),
                        file_name="Lakkoofsa_Barattoota_Irra_Deebii_Repeat_Count.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("No repeat students registered. Barataan irra deebii galmaa'e hin jiru.")
            else:
                st.info("No students registered. Deetaan waligalaa hin jiru.")

        with tabI:
            st.markdown(report_header("Karoora vs Raawwii | Target vs Actual Comparison"))
            st.markdown("### I. Target vs Actual Report | Karoora fi Raawwii (FIX #3)")
            if not db.empty:
                raw_comparison = []
                for k in range(1, 13):
                    k_str = str(k)
                    t_d = targets[k_str]["Dhiira"]
                    t_dh = targets[k_str]["Dhalaa"]

                    sub_k = db[db["Kutaa"] == k_str]
                    a_d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                    a_dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])

                    raw_comparison.append({
                        "Kutaa_Num": k_str,
                        "Kutaa": f"Kutaa {k}",
                        "Karoora Dhiira": t_d,
                        "Karoora Dhalaa": t_dh,
                        "Karoora Ida'ama": t_d + t_dh,
                        "Raawwii Dhiira": a_d,
                        "Raawwii Dhalaa": a_dh,
                        "Raawwii Ida'ama": a_d + a_dh,
                        "Target_Dhiira": t_d,
                        "Target_Dhalaa": t_dh,
                        "Actual_Dhiira": a_d,
                        "Actual_Dhalaa": a_dh
                    })

                def fmt_val(t_val, a_val):
                    return f"Kar: {t_val} | Raw: {a_val}"

                t_1_6_d = sum(r["Target_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                t_1_6_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                a_1_6_d = sum(r["Actual_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                a_1_6_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)

                t_7_8_d = sum(r["Target_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                t_7_8_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                a_7_8_d = sum(r["Actual_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                a_7_8_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)

                t_9_12_d = sum(r["Target_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                t_9_12_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                a_9_12_d = sum(r["Actual_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                a_9_12_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)

                comp_final_table = []

                # Grades 1-6
                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) <= 6:
                        comp_final_table.append({
                            "Kutaa | Grade": r["Kutaa"],
                            "Karoora Dhiira | Target M": r["Karoora Dhiira"],
                            "Karoora Dhalaa | Target F": r["Karoora Dhalaa"],
                            "Karoora Ida'ama | Target Total": r["Karoora Ida'ama"],
                            "Raawwii Dhiira | Actual M": r["Raawwii Dhiira"],
                            "Raawwii Dhalaa | Actual F": r["Raawwii Dhalaa"],
                            "Raawwii Ida'ama | Actual Total": r["Raawwii Ida'ama"],
                            "Raawwii (%)": pct_str(r["Raawwii Ida'ama"], r["Karoora Ida'ama"])
                        })

                comp_final_table.append({
                    "Kutaa | Grade": "Ida'ama 1-6 | Total 1-6",
                    "Karoora Dhiira | Target M": t_1_6_d,
                    "Karoora Dhalaa | Target F": t_1_6_dh,
                    "Karoora Ida'ama | Target Total": t_1_6_d + t_1_6_dh,
                    "Raawwii Dhiira | Actual M": a_1_6_d,
                    "Raawwii Dhalaa | Actual F": a_1_6_dh,
                    "Raawwii Ida'ama | Actual Total": a_1_6_d + a_1_6_dh,
                    "Raawwii (%)": pct_str(a_1_6_d + a_1_6_dh, t_1_6_d + t_1_6_dh),
                })

                # Grades 7-8
                for r in raw_comparison:
                    if 7 <= int(r["Kutaa_Num"]) <= 8:
                        comp_final_table.append({
                            "Kutaa | Grade": r["Kutaa"],
                            "Karoora Dhiira | Target M": r["Karoora Dhiira"],
                            "Karoora Dhalaa | Target F": r["Karoora Dhalaa"],
                            "Karoora Ida'ama | Target Total": r["Karoora Ida'ama"],
                            "Raawwii Dhiira | Actual M": r["Raawwii Dhiira"],
                            "Raawwii Dhalaa | Actual F": r["Raawwii Dhalaa"],
                            "Raawwii Ida'ama | Actual Total": r["Raawwii Ida'ama"],
                            "Raawwii (%)": pct_str(r["Raawwii Ida'ama"], r["Karoora Ida'ama"])
                        })

                comp_final_table.append({
                    "Kutaa | Grade": "Ida'ama 7-8 | Total 7-8",
                    "Karoora Dhiira | Target M": t_7_8_d,
                    "Karoora Dhalaa | Target F": t_7_8_dh,
                    "Karoora Ida'ama | Target Total": t_7_8_d + t_7_8_dh,
                    "Raawwii Dhiira | Actual M": a_7_8_d,
                    "Raawwii Dhalaa | Actual F": a_7_8_dh,
                    "Raawwii Ida'ama | Actual Total": a_7_8_d + a_7_8_dh,
                    "Raawwii (%)": pct_str(a_7_8_d + a_7_8_dh, t_7_8_d + t_7_8_dh),
                })

                comp_final_table.append({
                    "Kutaa | Grade": "Ida'ama Waliigalaa (1-8) | Total (1-8)",
                    "Karoora Dhiira | Target M": t_1_6_d + t_7_8_d,
                    "Karoora Dhalaa | Target F": t_1_6_dh + t_7_8_dh,
                    "Karoora Ida'ama | Target Total": (t_1_6_d + t_7_8_d) + (t_1_6_dh + t_7_8_dh),
                    "Raawwii Dhiira | Actual M": a_1_6_d + a_7_8_d,
                    "Raawwii Dhalaa | Actual F": a_1_6_dh + a_7_8_dh,
                    "Raawwii Ida'ama | Actual Total": (a_1_6_d + a_7_8_d) + (a_1_6_dh + a_7_8_dh),
                    "Raawwii (%)": pct_str((a_1_6_d + a_7_8_d) + (a_1_6_dh + a_7_8_dh), (t_1_6_d + t_7_8_d) + (t_1_6_dh + t_7_8_dh)),
                })

                # Grades 9-12
                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) >= 9:
                        comp_final_table.append({
                            "Kutaa | Grade": r["Kutaa"],
                            "Karoora Dhiira | Target M": r["Karoora Dhiira"],
                            "Karoora Dhalaa | Target F": r["Karoora Dhalaa"],
                            "Karoora Ida'ama | Target Total": r["Karoora Ida'ama"],
                            "Raawwii Dhiira | Actual M": r["Raawwii Dhiira"],
                            "Raawwii Dhalaa | Actual F": r["Raawwii Dhalaa"],
                            "Raawwii Ida'ama | Actual Total": r["Raawwii Ida'ama"],
                            "Raawwii (%)": pct_str(r["Raawwii Ida'ama"], r["Karoora Ida'ama"])
                        })

                comp_final_table.append({
                    "Kutaa | Grade": "Ida'ama 9-12 | Total 9-12",
                    "Karoora Dhiira | Target M": t_9_12_d,
                    "Karoora Dhalaa | Target F": t_9_12_dh,
                    "Karoora Ida'ama | Target Total": t_9_12_d + t_9_12_dh,
                    "Raawwii Dhiira | Actual M": a_9_12_d,
                    "Raawwii Dhalaa | Actual F": a_9_12_dh,
                    "Raawwii Ida'ama | Actual Total": a_9_12_d + a_9_12_dh,
                    "Raawwii (%)": pct_str(a_9_12_d + a_9_12_dh, t_9_12_d + t_9_12_dh),
                })

                # Grand Total
                tot_t_d = t_1_6_d + t_7_8_d + t_9_12_d
                tot_t_dh = t_1_6_dh + t_7_8_dh + t_9_12_dh
                tot_a_d = a_1_6_d + a_7_8_d + a_9_12_d
                tot_a_dh = a_1_6_dh + a_7_8_dh + a_9_12_dh

                comp_final_table.append({
                    "Kutaa | Grade": "Waliigalaa (1-12) | Grand Total",
                    "Karoora Dhiira | Target M": tot_t_d,
                    "Karoora Dhalaa | Target F": tot_t_dh,
                    "Karoora Ida'ama | Target Total": tot_t_d + tot_t_dh,
                    "Raawwii Dhiira | Actual M": tot_a_d,
                    "Raawwii Dhalaa | Actual F": tot_a_dh,
                    "Raawwii Ida'ama | Actual Total": tot_a_d + tot_a_dh,
                    "Raawwii (%)": pct_str(tot_a_d + tot_a_dh, tot_t_d + tot_t_dh),
                })

                comp_df = pd.DataFrame(comp_final_table)
                st.dataframe(comp_df, use_container_width=True)

                buffer_i = io.BytesIO()
                with pd.ExcelWriter(buffer_i, engine="openpyxl") as writer:
                    comp_df.to_excel(writer, sheet_name="Karoora_vs_Raawwii | Target_vs_Actual", index=False)
                st.download_button(
                    label="📥 Download Target vs Actual Report | Karoora vs Raawwii Print / Excel",
                    data=buffer_i.getvalue(),
                    file_name="Karoora_vs_Raawwii_Target_Actual_Comparison.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("No students registered. Deetaan galmaa'e hin jiru.")

        with tabJ:
            st.markdown(report_header("Gulaali/Haqi Barattoota | Edit/Delete Students"))
            st.markdown("### J. Edit or Delete Students | Barattoota Gulaaluu ykn Haquu")
            if not db.empty:
                search_name = st.text_input("Search by Name | Maqaa Barataa Barbaadi")
                if search_name:
                    filtered_db = db[db["Maqaa Guutuu"].str.contains(search_name, case=False, na=False)]
                else:
                    filtered_db = db

                if not filtered_db.empty:
                    selected_idx = st.selectbox(
                        "Select Student to Edit/Delete | Barataa Gulaaluuf ykn Haquuf Filadhu:",
                        filtered_db["id"].tolist(),
                        format_func=lambda x: f"{db.loc[db['id']==x, 'Maqaa Guutuu'].values[0]} (Kutaa {db.loc[db['id']==x, 'Kutaa'].values[0]})",
                    )
                    record = db[db["id"] == selected_idx].iloc[0]

                    st.markdown("#### ✏️ Edit Student Data | Odeeffannoo Barataa Gulaali")
                    with st.form("edit_student_form"):
                        e_col1, e_col2 = st.columns(2)

                        daree_options = [chr(65 + i) for i in range(11)]
                        haala_options = ["Haaraa | New", "Kan darbe | Previous", "Irra deebii (Kufe) | Repeat (Failed)", 
                                        "Irra deebii (Kute) | Repeat (Dropped)", "Mana Barumsaa Biroo | From Other School"]

                        try:
                            kutaa_idx = int(record["Kutaa"]) - 1
                            if kutaa_idx < 0 or kutaa_idx > 11:
                                kutaa_idx = 0
                        except (ValueError, TypeError):
                            kutaa_idx = 0
                        try:
                            daree_idx = daree_options.index(record["Daree (Section)"])
                        except ValueError:
                            daree_idx = 0
                        try:
                            haala_idx = haala_options.index(record["Haala Galmee"])
                        except ValueError:
                            haala_idx = 0

                        with e_col1:
                            e_maqaa = st.text_input("Full Name | Maqaa Guutuu", value=record["Maqaa Guutuu"])
                            e_koorniyaa = st.selectbox("Gender | Koorniyaa", ["Dhiira | Male", "Dhalaa | Female"], index=0 if "Dhiira" in str(record["Koorniyaa"]) else 1)
                            e_kutaa = st.selectbox("Grade | Kutaa", [str(i) for i in range(1, 13)], index=kutaa_idx)
                            e_daree = st.selectbox("Section | Daree", daree_options, index=daree_idx)
                            e_bara_dhalootaa = st.text_input("Birth Date | Bara Dhalootaa", value=str(record["Bara Dhalootaa"]))
                            e_umurii = st.text_input("Age | Umurii", value=str(record["Umurii"]))
                            e_haala_galmee = st.selectbox("Registration Status | Haala Galmee", haala_options, index=haala_idx)
                            e_bara_addaan_kute = st.text_input("Dropout Year | Bara Addaan Kute", value=str(record["Bara Addaan Kute"]))
                            e_haala_maatii = st.text_input("Family Status | Haala Maatii", value=str(record["Haala Maatii"]))
                            e_miidhama = st.selectbox("Disability | Miidhama Qaamaa", ["Hin jiru | No", "Jira | Yes"], index=0 if "Hin jiru" in str(record["Miidhama Qaamaa"]) else 1)
                            e_gosa_miidhamaa = st.text_input("Disability Type | Gosa Miidhamaa", value=str(record["Gosa Miidhamaa"]))

                        with e_col2:
                            e_godina = st.text_input("Zone | Godina", value=str(record["Godina"]))
                            e_aanaa = st.text_input("District | Aanaa", value=str(record["Aanaa"]))
                            e_ganda = st.text_input("Village | Ganda", value=str(record["Ganda"]))
                            e_haadhaa = st.text_input("Mother/Guardian Name | Maqaa Haadhaa/Guddistuu", value=str(record["Maqaa Haadhaa/Guddistuu"]))
                            e_fan = st.text_input("FAN ID", value=str(record["FAN ID"]))
                            e_bilbila_barataa = st.text_input("Student Phone | Lakk Bilbila Barataa", value=str(record["Lakk Bilbila Barataa"]))
                            e_bilbila_maatii = st.text_input("Family Phone | Lakk Bilbila Maatii", value=str(record["Lakk Bilbila Maatii"]))
                            e_mb_duraan = st.text_input("Previous School | M/B Duraan Itti Barachaa Ture", value=str(record["M/B Duraan Itti Barachaa Ture"]))
                            e_avireejjii = st.text_input("Average Score | Avireejjii Qabxii", value=str(record["Avireejjii Qabxii"]))
                            e_guyyaa_galmee = st.text_input("Registration Date (E.C) | Guyyaa Galmee (E.C)", value=str(record["Guyyaa Galmee (E.C)"]))
                            e_barsiisaa = st.text_input("Teacher Registrar | Barsiisaa Galmeessee", value=str(record["Barsiisaa Galmeessee"]))
                            e_mana_barumsaa = st.text_input("School Name | Mana Barumsaa", value=str(record.get("Mana Barumsaa", get_setting("saved_school_name", ""))))

                        col_save, col_del = st.columns(2)
                        with col_save:
                            save_edit = st.form_submit_button("💾 Save Changes | Jijjiirama Save Godhi")
                        with col_del:
                            delete_edit = st.form_submit_button("🗑️ Delete Student | Barataa Kana Haqi")

                        if save_edit:
                            updated_data = {
                                "Maqaa Guutuu": e_maqaa,
                                "Koorniyaa": e_koorniyaa.replace(" | Male", "").replace(" | Female", ""),
                                "Kutaa": e_kutaa,
                                "Daree (Section)": e_daree,
                                "Bara Dhalootaa": e_bara_dhalootaa,
                                "Umurii": e_umurii,
                                "Haala Galmee": e_haala_galmee,
                                "Bara Addaan Kute": e_bara_addaan_kute,
                                "Haala Maatii": e_haala_maatii,
                                "Miidhama Qaamaa": e_miidhama.replace(" | No", "").replace(" | Yes", ""),
                                "Gosa Miidhamaa": e_gosa_miidhamaa,
                                "Godina": e_godina,
                                "Aanaa": e_aanaa,
                                "Ganda": e_ganda,
                                "Maqaa Haadhaa/Guddistuu": e_haadhaa,
                                "FAN ID": e_fan,
                                "Lakk Bilbila Barataa": e_bilbila_barataa,
                                "Lakk Bilbila Maatii": e_bilbila_maatii,
                                "M/B Duraan Itti Barachaa Ture": e_mb_duraan,
                                "Avireejjii Qabxii": e_avireejjii,
                                "Guyyaa Galmee (E.C)": e_guyyaa_galmee,
                                "Barsiisaa Galmeessee": e_barsiisaa,
                                "Mana Barumsaa": e_mana_barumsaa,
                            }
                            update_student(int(selected_idx), updated_data)
                            st.success("Student data updated successfully! Odeeffannoon barataa milkaa'inaan haaromfameera!")
                            st.rerun()

                        if delete_edit:
                            delete_student(int(selected_idx))
                            st.success("Student deleted successfully! Barataan milkaa'inaan haqameera!")
                            st.rerun()
                else:
                    st.warning("Student not found. Barataan argame hin jiru.")
            else:
                st.info("No students registered. Deetaan galmaa'e hin jiru.")
    else:
        if password:
            st.error("Incorrect password! Password sirrii miti!")

# ============================================================================
# 4. ADMIN DASHBOARD (FIX #10)
# ============================================================================
elif menu == "4. Admin Dashboard | Bulchiinsaa (Password Needed)":
    st.subheader("🛡️ Admin Dashboard | Dashboard Bulchiinsaa")
    st.caption("This page is for administrators to manage all data.")

    admin_password = st.text_input("Admin Password | Password Galchi", type="password")

    if admin_password == ADMIN_PASSWORD:
        st.success("✅ Admin Access Granted! Seensa Bulchiinsaa Milkaa'e!")

        db = load_students()
        st.markdown(f"#### 📊 Total Students | Waliigalaa Barattoota: **{len(db)}**")

        if not db.empty:
            st.dataframe(db, use_container_width=True)

            buffer_admin = io.BytesIO()
            with pd.ExcelWriter(buffer_admin, engine="openpyxl") as writer:
                db.to_excel(writer, sheet_name="Deetaa_Guutuu | Full_Data", index=False)
            st.download_button(
                label="📥 Full Data Backup (Excel) | Deetaa Guutuu Backup",
                data=buffer_admin.getvalue(),
                file_name=f"Backup_Deetaa_Barattootaa_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.markdown("---")
            st.markdown("#### 📋 Login History | Seenaa Seensa Hunda")
            hist_df = load_login_history()
            st.dataframe(hist_df, use_container_width=True)

            st.markdown("---")
            st.markdown("#### ⚠️ Delete All Data | Balleessuu Deetaa Hunda")
            st.warning("⚠️ This will delete ALL student records! Kan deetaa hundaa balleessa!")
            confirm_delete_all = st.text_input("Type 'DELETE ALL' to confirm | Mirkaneessuuf 'DELETE ALL' jedhii barreessi:")
            if st.button("🗑️ Delete All Students | Deetaa Hunda Balleessi"):
                if confirm_delete_all == "DELETE ALL":
                    conn = get_connection()
                    conn.execute("DELETE FROM students")
                    conn.commit()
                    conn.close()
                    st.success("All data deleted. Deetaan hundi haqameera.")
                    st.rerun()
                else:
                    st.error("Type 'DELETE ALL' to confirm. Mirkaneessa sirrii galchuu qabda.")
        else:
            st.info("No students in database. Deetaan hin jiru.")
    else:
        if admin_password:
            st.error("Incorrect admin password! Password sirrii miti!")

# ============================================================================
# 5. LOGIN HISTORY (FIX #5)
# ============================================================================
elif menu == "5. Login History | Seenaa Seensaa":
    st.subheader("📋 Login History | Seenaa Seensaa Appii")

    hist_df = load_login_history()

    if not hist_df.empty:
        st.dataframe(hist_df, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🗑️ Delete Login History Records | Seenaa Seensaa Haquu")

        # Option to delete individual records or all
        records_to_delete = st.multiselect(
            "Select records to delete | Seenaa haquuf filadhu:",
            hist_df["id"].tolist(),
            format_func=lambda x: f"ID: {x} - {hist_df[hist_df['id']==x]['Gmail'].values[0]} ({hist_df[hist_df['id']==x]['Login Time / Guyyaa Saatii'].values[0]})"
        )

        col_del1, col_del2 = st.columns(2)
        with col_del1:
            if st.button("🗑️ Delete Selected Records | Seenaa Filatame Haqi"):
                if records_to_delete:
                    for rec_id in records_to_delete:
                        delete_login_record(int(rec_id))
                    st.success(f"{len(records_to_delete)} record(s) deleted. Seenaa haqameera!")
                    st.rerun()
                else:
                    st.warning("Please select records to delete. Maaloo seenaa haquuf filadhu.")

        with col_del2:
            if st.button("🗑️ Delete ALL Login History | Seenaa Hunda Haqi"):
                confirm = st.text_input("Type 'DELETE ALL' to confirm | Mirkaneessuuf 'DELETE ALL' jedhii barreessi:")
                if confirm == "DELETE ALL":
                    conn = get_connection()
                    conn.execute("DELETE FROM login_history")
                    conn.commit()
                    conn.close()
                    st.success("All login history deleted. Seenaan hundi haqameera.")
                    st.rerun()
                else:
                    st.error("Type 'DELETE ALL' to confirm.")
    else:
        st.info("No login history yet. Seenaan seensaa hanga ammaatti hin jiru.")

# ============================================================================
# 6. MULTI-SCHOOL DASHBOARD (FIX #8 & #9)
# ============================================================================
elif menu == "6. Multi-School Dashboard | Manneen Barnootaa":
    st.subheader("🏫 Multi-School Dashboard | Kuusaa Manneen Barnootaa Biroo")
    st.caption("Track and manage students across multiple schools.")

    all_schools = get_all_schools()

    if all_schools:
        st.markdown(f"### 📚 Schools Registered | Manneen Barnootaa Galmaa'an: **{len(all_schools)}**")

        # Display all schools and their student counts
        school_stats = []
        for school in all_schools:
            school_df = get_students_by_school(school)
            count = len(school_df)
            # Get grade distribution
            grade_counts = school_df["Kutaa"].value_counts().sort_index().to_dict() if not school_df.empty else {}
            school_stats.append({
                "School | Mana Barumsaa": school,
                "Total Students | Barattoota": count,
                "Grades | Kutaalee": ", ".join([f"{k} ({v})" for k, v in grade_counts.items()]) if grade_counts else "None",
                "Last Registration | Galmee Dhumaa": school_df["Guyyaa Galmee (E.C)"].iloc[-1] if not school_df.empty else "N/A"
            })

        stats_df = pd.DataFrame(school_stats)
        st.dataframe(stats_df, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔍 View School Data | Deetaa Mana Barumsaa Ilaaluu")

        selected_school_view = st.selectbox(
            "Select School to View | Mana Barumsaa Filadhu",
            all_schools
        )

        if selected_school_view:
            school_data = get_students_by_school(selected_school_view)
            st.markdown(f"#### 📋 Students at **{selected_school_view}** | Barattoota Mana Barumsaa **{selected_school_view}**")
            st.dataframe(school_data, use_container_width=True)

            # Export school data
            buffer_school = io.BytesIO()
            with pd.ExcelWriter(buffer_school, engine="openpyxl") as writer:
                school_data.to_excel(writer, sheet_name=f"{selected_school_view[:30]}", index=False)
            st.download_button(
                label=f"📥 Download {selected_school_view} Data | Deetaa Mana Barumsaa kanaa",
                data=buffer_school.getvalue(),
                file_name=f"School_{selected_school_view.replace(' ', '_')}_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.markdown("---")
            st.markdown("#### ⚠️ Delete School Data | Deetaa Mana Barumsaa Haquu")
            confirm_delete_school = st.text_input(f"Type 'DELETE {selected_school_view}' to confirm deleting all data for this school:")
            if st.button(f"🗑️ Delete {selected_school_view} Data"):
                if confirm_delete_school == f"DELETE {selected_school_view}":
                    delete_school_data(selected_school_view)
                    st.success(f"All data for {selected_school_view} deleted. Deetaan mana barumsaa kanaa haqameera.")
                    st.rerun()
                else:
                    st.error("Please type the exact confirmation text.")
    else:
        st.info("No schools registered yet. Start registering students with the 'Student Registration' page.")

    st.markdown("---")
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)
