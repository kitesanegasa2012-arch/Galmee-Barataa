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
# ENHANCED CSS - MODERN COVER PAGE & STYLING
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
    </style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# CONTACT INFO
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
# DATABASE (SQLite) - PERSISTENT STORAGE & EMIS COLUMNS INTEGRATION
# ============================================================================
DB_PATH = "kitesa_negasa_data.db"

# STUDENT COLUMNS - Integrated EMIS standard columns (Name, father_name, grandfather_name, date_of_birth)
STUDENT_COLUMNS = [
    "Name",                     # EMIS First Name
    "father_name",              # EMIS Father Name
    "grandfather_name",         # EMIS Grandfather Name
    "Maqaa Guutuu",             # Full Name (Combined)
    "Koorniyaa",                # Gender
    "Kutaa",                    # Grade
    "Daree (Section)",          # Section
    "date_of_birth",            # EMIS Date of Birth
    "Bara Dhalootaa",           # Birth Year
    "Umurii",                   # Age
    "Haala Galmee",             # Registration Status
    "Bara Addaan Kute",         # Dropout Year
    "Haala Maatii",             # Family Status
    "Miidhama Qaamaa",          # Disability
    "Gosa Miidhamaa",           # Disability Type
    "Godina",                   # Zone
    "Aanaa",                    # District
    "Ganda",                    # Village
    "Maqaa Haadhaa/Guddistuu",# Mother/Guardian Name
    "FAN ID",                   # FAN ID
    "Lakk Bilbila Barataa",     # Student Phone
    "Lakk Bilbila Maatii",      # Family Phone
    "M/B Duraan Itti Barachaa Ture", # Previous School
    "Avireejjii Qabxii",       # Average Score
    "Guyyaa Galmee (E.C)",      # Registration Date
    "Barsiisaa Galmeessee",     # Teacher Registrar
    "Mana Barumsaa",            # School Name
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


def get_last_location(db, col_name):
    if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
        return db[col_name].dropna().iloc[-1]
    return ""


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
        "3. Reports & Dashboard | Gabaasa",
        "4. Login History | Seenaa Seensaa",
        "5. Logout | Baasi",
    ],
)

if menu == "5. Logout | Baasi":
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# ============================================================================
# 1. COVER PAGE
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
                This system helps schools register students with EMIS standard records, track attendance, and generate reports.<br>
                <span style="color:#ffd700;">Sirni kun barattoota ragaa EMIS eeguun galmeessuuf kan gargaaru.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

# ============================================================================
# 2. STUDENT REGISTRATION FORM (Integrated with EMIS Name, father_name, grandfather_name, date_of_birth)
# ============================================================================
elif menu == "2. Student Registration | Galmee Barataa":
    st.subheader("📝 Student Registration Form (EMIS Standard)")

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
                st.warning("Please enter a school name.")

    saved_school_name = get_setting("saved_school_name", "")
    st.markdown("---")

    haala_galmee = st.selectbox(
        "Registration Status / Haala Galmee",
        ["Haaraa | New", "Kan darbe | Previous", "Irra deebii (Kufe) | Repeat (Failed)", 
         "Irra deebii (Kute) | Repeat (Dropped)", "Mana Barumsaa Biroo | From Other School"],
        key="haala_galmee_select",
    )
    st.markdown("---")

    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### **EMIS Name Information**")
            emis_name = st.text_input("1. Name (First Name) | Maqaa", value="")
            father_name = st.text_input("2. Father's Name | Maqaa Abbaa", value="")
            grandfather_name = st.text_input("3. Grandfather's Name | Maqaa Abbaa Abbaa", value="")
            
            # Auto-generate Full Name for consistency
            maqaa_guutuu = f"{emis_name} {father_name} {grandfather_name}".strip()

            koorniyaa = st.selectbox("4. Gender | Koorniyaa", ["Filadhu | Select", "Dhiira | Male", "Dhalaa | Female"])

            grade_col1, grade_col2 = st.columns(2)
            kutaa = grade_col1.selectbox("5. Grade | Kutaa", [str(i) for i in range(1, 13)])
            daree = grade_col2.selectbox("Section | Daree", [chr(65 + i) for i in range(11)])

            st.markdown("**6. Date of Birth | Guyyaa Dhalootaa (date_of_birth)**")
            date_of_birth_val = st.date_input("Date of Birth", value=datetime(2011, 9, 11))
            date_of_birth_str = date_of_birth_val.strftime("%Y-%m-%d")
            b_bara = str(date_of_birth_val.year)
            
            current_et_year = 2018
            umurii = str(current_et_year - date_of_birth_val.year)

            bara_addaan_kute = st.selectbox(
                "Dropout Year | Bara Addaan Kute",
                ["Hin jiru | None", "2005", "2006", "2007", "2008", "2009", "2010"]
                + [str(y) for y in range(2011, 2027)],
            )

            haala_maatii = st.selectbox(
                "7. Family Status | Haala Maatii",
                ["Lachuu qaba | Both parents", "Abbaa qofa | Father only", 
                 "Haadha qofa | Mother only", "Lachuu hin qabu | Neither"],
            )

        with col2:
            st.markdown("#### **Additional Student Details**")
            miidhama_qaamaa = st.selectbox("8. Disability | Miidhama Qaamaa", ["Hin jiru | No", "Jira | Yes"])
            gosa_miidhamaa = st.selectbox(
                "9. Disability Type | Gosa Miidhamaa",
                ["Hin qabu | None", "Arguu salphaa | Mild visual", "Arguu cimaa | Severe visual",
                 "Dhageettii salphaa | Mild hearing", "Dhageettii cimaa | Severe hearing", "Sochii | Physical"]
            )

            godina = st.text_input("Zone | Godina", value=default_godina)
            aanaa = st.text_input("District | Aanaa", value=default_aanaa)
            ganda = st.text_input("Village | Ganda", value=default_ganda)

            maqaa_haadhaa = st.text_input("10. Mother/Guardian Name | Maqaa Haadhaa/Guddistuu", value="")
            fan_id = st.text_input("11. FAN ID (16 digits)", value="")
            lakk_bilbila_barataa = st.text_input("12. Student Phone", value="")
            lakk_bilbila_maatii = st.text_input("13. Family Phone", value="")
            
            mb_duraan = st.text_input("14. Previous School", value=saved_school_name)
            avireejjii = st.number_input("15. Average Score", min_value=0.0, max_value=100.0, value=75.0)
            barsiisaa = st.text_input("16. Teacher Registrar", value=default_barsiisaa)
            guyyaa_galmee_ec = st.text_input("Registration Date (E.C)", value=default_guyyaa)

        submitted = st.form_submit_button("💾 Save Student | Barataa Save Godhi")

    if submitted:
        if not emis_name or not father_name or not grandfather_name:
            st.error("Maaloo Maqaa, Maqaa Abbaa, fi Maqaa Abbaa Abbaa guutuu galchaa!")
        else:
            data_dict = {
                "Name": emis_name,
                "father_name": father_name,
                "grandfather_name": grandfather_name,
                "Maqaa Guutuu": maqaa_guutuu,
                "Koorniyaa": koorniyaa,
                "Kutaa": kutaa,
                "Daree (Section)": daree,
                "date_of_birth": date_of_birth_str,
                "Bara Dhalootaa": b_bara,
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
                "Avireejjii Qabxii": str(avireejjii),
                "Guyyaa Galmee (E.C)": guyyaa_galmee_ec,
                "Barsiisaa Galmeessee": barsiisaa,
                "Mana Barumsaa": saved_school_name if saved_school_name else "Default School",
            }
            insert_student(data_dict)
            st.success("Barataan ragaa EMIS (Name, father_name, grandfather_name, date_of_birth) guutuun milkaa'inaan galmeeffameera!")

# ============================================================================
# 3. REPORTS & DASHBOARD
# ============================================================================
elif menu == "3. Reports & Dashboard | Gabaasa":
    st.subheader("📊 Registered Students Database & EMIS Export")
    db = load_students()
    if school_filter != "All Schools / Hunda" and not db.empty:
        db = db[db["Mana Barumsaa"] == school_filter]

    if not db.empty:
        st.dataframe(db, use_container_width=True)
    else:
        st.info("Ragaan barattootaa hin jiru.")

# ============================================================================
# 4. LOGIN HISTORY
# ============================================================================
elif menu == "4. Login History | Seenaa Seensaa":
    st.subheader("📋 Login History | Seenaa Seensaa")
    df_login = load_login_history()
    if not df_login.empty:
        st.dataframe(df_login, use_container_width=True)
    else:
        st.info("Seenaan seensaa hin jiru.")
