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

    h1, h2, h3, h4, h5 {
        color: #1e3c72;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

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

    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
    }

    .css-1d391kg .css-1v3fvcr {
        color: white;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .stAlert {
        border-radius: 12px !important;
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
# DATABASE (SQLite)
# ============================================================================
DB_PATH = "kitesa_negasa_data.db"

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
    "National ID",
    "Lakk Bilbila Barataa",
    "Lakk Bilbila Maatii",
    "M/B Duraan Itti Barachaa Ture",
    "Avireejjii Qabxii",
    "Guyyaa Galmee (E.C)",
    "Barsiisaa Galmeessee",
    "Mana Barumsaa",
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

# ============================================================================
# SESSION STATE
# ============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_school" not in st.session_state:
    st.session_state.current_school = ""

# ============================================================================
# AUTHORIZED USERS
# ============================================================================
AUTHORIZED_USERS = {
    "kitesanegasa2012@gmail.com": "kitesanegasa2012password",
    "barsiisaa1@gmail.com": "pass1234",
    "bulchaa@gmail.com": "admin2026",
    "feyisamililu23@gmail.com": "20481092F",
}

REPORT_PASSWORDS = ["kitesanegasa2012password", "kitesa2019", "admin123"]
ADMIN_PASSWORD = "KitesaAdmin@2026"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
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
    try:
        if target and float(target) > 0:
            return f"{(float(actual) / float(target) * 100):.1f}%"
    except (ValueError, TypeError):
        pass
    return "-"


def report_header(title):
    school_name = get_setting("saved_school_name", ".................")
    academic_year = get_setting("bara_barnootaa", "2019")
    return f"#### 📄 {title} - 🏫 {school_name} — Bara {academic_year} / Academic Year {academic_year}"

# ============================================================================
# EMIS DATA UPLOAD FUNCTIONS
# ============================================================================
def load_emis_data(uploaded_file, template_type):
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            df = pd.read_excel(uploaded_file, engine='xlrd')
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def parse_student_basic_data(df):
    try:
        parsed_data = {
            'National ID': df.iloc[:, 0].astype(str).str.strip() if df.shape[1] > 0 else '',
            'Maqaa Guutuu': df.iloc[:, 2].astype(str).str.strip() if df.shape[1] > 2 else '',
            'Maqaa Abbaa': df.iloc[:, 3].astype(str).str.strip() if df.shape[1] > 3 else '',
            'Maqaa Akaakayyu': df.iloc[:, 4].astype(str).str.strip() if df.shape[1] > 4 else '',
            'Koorniyaa': df.iloc[:, 6].astype(str).str.strip() if df.shape[1] > 6 else '',
            'Bara Dhalootaa': df.iloc[:, 9].astype(str).str.strip() if df.shape[1] > 9 else '',
            'Umurii': df.iloc[:, 10] if df.shape[1] > 10 else '',
            'FAN ID': df.iloc[:, 12].astype(str).str.strip() if df.shape[1] > 12 else ''
        }
        return pd.DataFrame(parsed_data)
    except Exception as e:
        st.error(f"Error parsing basic data: {e}")
        return None


def parse_student_result_data(df):
    try:
        parsed_data = {
            'National ID': df.iloc[:, 0].astype(str).str.strip() if df.shape[1] > 0 else '',
            'Student ID': df.iloc[:, 0].astype(str).str.strip() if df.shape[1] > 0 else '',
            'Kutaa': df.iloc[:, 2].astype(str).str.strip() if df.shape[1] > 2 else '',
            'Avireejjii Qabxii': df.iloc[:, 3] if df.shape[1] > 3 else ''
        }
        return pd.DataFrame(parsed_data)
    except Exception as e:
        st.error(f"Error parsing result data: {e}")
        return None


def compare_with_emis(emis_data, app_data):
    mismatches = []
    matches = []
    emis_not_in_app = []
    app_not_in_emis = []
    
    emis_dict = {}
    for _, row in emis_data.iterrows():
        national_id = str(row.get('National ID', '')).strip()
        fan_id = str(row.get('FAN ID', '')).strip()
        full_name = str(row.get('Maqaa Guutuu', '')).strip()
        
        key = national_id if national_id and national_id != 'nan' else (fan_id if fan_id and fan_id != 'nan' else full_name)
        if key and key != 'nan':
            emis_dict[key] = {
                'data': row.to_dict(),
                'national_id': national_id,
                'fan_id': fan_id,
                'full_name': full_name
            }
    
    app_dict = {}
    for _, row in app_data.iterrows():
        fan_id = str(row.get('FAN ID', '')).strip()
        full_name = str(row.get('Maqaa Guutuu', '')).strip()
        
        key = fan_id if fan_id and fan_id != 'nan' else full_name
        if key and key != 'nan':
            app_dict[key] = {
                'data': row.to_dict(),
                'fan_id': fan_id,
                'full_name': full_name
            }
    
    for key, emis_item in emis_dict.items():
        emis_row = emis_item['data']
        emis_national_id = emis_item['national_id']
        
        found = False
        match_key = None
        
        for app_key, app_item in app_dict.items():
            if app_item.get('fan_id', '') == emis_national_id:
                found = True
                match_key = app_key
                break
        
        if not found:
            for app_key, app_item in app_dict.items():
                if app_item.get('fan_id', '') == emis_item.get('fan_id', ''):
                    found = True
                    match_key = app_key
                    break
        
        if not found:
            for app_key, app_item in app_dict.items():
                if app_item.get('full_name', '').lower() == emis_item.get('full_name', '').lower():
                    found = True
                    match_key = app_key
                    break
        
        if found and match_key:
            app_row = app_dict[match_key]['data']
            mismatch = {}
            is_match = True
            
            compare_fields = ['Maqaa Guutuu', 'Koorniyaa', 'Bara Dhalootaa', 'Umurii', 'Avireejjii Qabxii', 'FAN ID']
            for field in compare_fields:
                emis_val = str(emis_row.get(field, '')).strip()
                app_val = str(app_row.get(field, '')).strip()
                if emis_val != app_val:
                    mismatch[field] = {
                        'emis': emis_val,
                        'app': app_val
                    }
                    is_match = False
            
            if is_match:
                matches.append({
                    'key': key, 
                    'data': emis_row,
                    'national_id': emis_national_id
                })
            else:
                mismatches.append({
                    'key': key,
                    'emis_data': emis_row,
                    'app_data': app_row,
                    'mismatch_fields': mismatch,
                    'national_id': emis_national_id
                })
        else:
            emis_not_in_app.append({
                'key': key, 
                'data': emis_row,
                'national_id': emis_national_id
            })
    
    for key, app_item in app_dict.items():
        found = False
        for emis_key, emis_item in emis_dict.items():
            if app_item.get('fan_id', '') == emis_item.get('fan_id', ''):
                found = True
                break
            if app_item.get('full_name', '').lower() == emis_item.get('full_name', '').lower():
                found = True
                break
        
        if not found:
            app_not_in_emis.append({
                'key': key, 
                'data': app_item['data']
            })
    
    return {
        'matches': matches,
        'mismatches': mismatches,
        'emis_not_in_app': emis_not_in_app,
        'app_not_in_emis': app_not_in_emis
    }


def update_student_from_emis(student_id, emis_data):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE students SET 
                "Maqaa Guutuu" = ?,
                "Koorniyaa" = ?,
                "Bara Dhalootaa" = ?,
                "Umurii" = ?,
                "Avireejjii Qabxii" = ?,
                "FAN ID" = ?
            WHERE id = ?
        """, (
            emis_data.get('Maqaa Guutuu', ''),
            emis_data.get('Koorniyaa', ''),
            emis_data.get('Bara Dhalootaa', ''),
            emis_data.get('Umurii', ''),
            emis_data.get('Avireejjii Qabxii', ''),
            emis_data.get('FAN ID', ''),
            student_id
        ))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating student: {e}")
        return False
    finally:
        conn.close()

# ============================================================================
# LOGIN SCREEN
# ============================================================================
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
                    st.success("Baga nagaan dhufte! Welcome!")
                    st.rerun()
                else:
                    st.error("Gmail ykn Password sirrii miti! Invalid credentials!")

        st.markdown("---")
        st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
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
        "3. Reports & Dashboard | Gabaasa (Password Needed)",
        "4. Admin Dashboard | Bulchiinsaa (Password Needed)",
        "5. Login History | Seenaa Seensaa",
        "6. Multi-School Dashboard | Manneen Barnootaa",
        "7. EMIS Data Upload | Ragaa EMIS Fe'uu",
        "8. Logout | Baasi",
    ],
)

# ============================================================================
# 8. LOGOUT
# ============================================================================
if menu == "8. Logout | Baasi":
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# ============================================================================
# 1. COVER PAGE
# ============================================================================
elif menu == "1. Cover Page | Fuula Jalqabaa":
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
            """
        )

    st.write("---")

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
# 2. STUDENT REGISTRATION FORM (SIMPLIFIED)
# ============================================================================
elif menu == "2. Student Registration | Galmee Barataa":
    st.subheader("📝 Student Registration Form | Foormii Galmee Barattootaa")
    st.info("Please use the student registration form to add new students.")
    st.markdown("---")
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

# ============================================================================
# 3. REPORTS & DASHBOARD (SIMPLIFIED)
# ============================================================================
elif menu == "3. Reports & Dashboard | Gabaasa (Password Needed)":
    st.subheader("🔐 Reports & Dashboard | Gabaasa fi Kuusaa")

    password = st.text_input("Enter Password | Password Galchi", type="password")

    if password in REPORT_PASSWORDS:
        st.success("✅ Access Granted! Seensa Milkaa'e!")

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

        db = load_students()
        if not db.empty:
            st.dataframe(db, use_container_width=True)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                db.to_excel(writer, sheet_name="Students", index=False)
            st.download_button(
                label="📥 Download Report | Gabaasa Buqqisaa",
                data=buffer.getvalue(),
                file_name=f"Student_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.info("No students found.")
    else:
        if password:
            st.error("Incorrect password! Password sirrii miti!")

# ============================================================================
# 4. ADMIN DASHBOARD
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
                db.to_excel(writer, sheet_name="Data", index=False)
            st.download_button(
                label="📥 Full Data Backup (Excel) | Deetaa Guutuu Backup",
                data=buffer_admin.getvalue(),
                file_name=f"Backup_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.info("No students in database.")
    else:
        if admin_password:
            st.error("Incorrect admin password!")

# ============================================================================
# 5. LOGIN HISTORY
# ============================================================================
elif menu == "5. Login History | Seenaa Seensaa":
    st.subheader("📋 Login History | Seenaa Seensaa Appii")

    hist_df = load_login_history()

    if not hist_df.empty:
        st.dataframe(hist_df, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🗑️ Delete Login History Records | Seenaa Seensaa Haquu")

        records_to_delete = st.multiselect(
            "Select records to delete | Seenaa haquuf filadhu:",
            hist_df["id"].tolist(),
            format_func=lambda x: f"ID: {x} - {hist_df[hist_df['id']==x]['Gmail'].values[0]}"
        )

        if st.button("🗑️ Delete Selected Records | Seenaa Filatame Haqi"):
            if records_to_delete:
                for rec_id in records_to_delete:
                    delete_login_record(int(rec_id))
                st.success(f"{len(records_to_delete)} record(s) deleted.")
                st.rerun()
            else:
                st.warning("Please select records to delete.")
    else:
        st.info("No login history yet.")

# ============================================================================
# 6. MULTI-SCHOOL DASHBOARD
# ============================================================================
elif menu == "6. Multi-School Dashboard | Manneen Barnootaa":
    st.subheader("🏫 Multi-School Dashboard | Kuusaa Manneen Barnootaa Biroo")

    all_schools = get_all_schools()

    if all_schools:
        st.markdown(f"### 📚 Schools Registered: **{len(all_schools)}**")

        school_stats = []
        for school in all_schools:
            school_df = get_students_by_school(school)
            count = len(school_df)
            school_stats.append({
                "School | Mana Barumsaa": school,
                "Total Students | Barattoota": count,
                "Last Registration": school_df["Guyyaa Galmee (E.C)"].iloc[-1] if not school_df.empty else "N/A"
            })

        st.dataframe(pd.DataFrame(school_stats), use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔍 View School Data")

        selected_school_view = st.selectbox(
            "Select School to View | Mana Barumsaa Filadhu",
            all_schools
        )

        if selected_school_view:
            school_data = get_students_by_school(selected_school_view)
            st.dataframe(school_data, use_container_width=True)
    else:
        st.info("No schools registered yet.")

    st.markdown("---")
    st.markdown(CONTACT_INFO_HTML, unsafe_allow_html=True)

# ============================================================================
# 7. EMIS DATA UPLOAD
# ============================================================================
elif menu == "7. EMIS Data Upload | Ragaa EMIS Fe'uu":
    st.subheader("📤 EMIS Data Upload & Validation | Ragaa EMIS Fe'uu fi Mirkaneessuu")
    
    st.info("""
    **📋 EMIS Data Requirements:**
    - **Student Basic Data**: Column A (National ID), C (Full Name), D (Father), E (Grandfather), G (Gender), J (DOB), K (Age), M (FAN ID)
    - **Student Result Data**: Column A (National ID), C (Grade), D (Average Score)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        basic_file = st.file_uploader(
            "📄 Student Basic Data (Column A = National ID)",
            type=['xlsx', 'xls'],
            key="emis_basic"
        )
    
    with col2:
        result_file = st.file_uploader(
            "📄 Student Result Data (Column A = National ID)",
            type=['xlsx', 'xls'],
            key="emis_result"
        )
    
    if basic_file and result_file:
        with st.spinner("Processing EMIS data..."):
            basic_df = load_emis_data(basic_file, "basic")
            result_df = load_emis_data(result_file, "result")
            
            if basic_df is not None and result_df is not None:
                parsed_basic = parse_student_basic_data(basic_df)
                parsed_result = parse_student_result_data(result_df)
                
                if parsed_basic is not None and parsed_result is not None:
                    emis_data = pd.merge(parsed_basic, parsed_result, on=['National ID'], how='left')
                    
                    st.markdown("#### 📊 EMIS Data Preview")
                    st.dataframe(emis_data.head(10), use_container_width=True)
                    
                    app_db = load_students()
                    
                    if not app_db.empty:
                        comparison_result = compare_with_emis(emis_data, app_db)
                        
                        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                        with col_m1:
                            st.metric("✅ Matches", len(comparison_result['matches']))
                        with col_m2:
                            st.metric("⚠️ Mismatches", len(comparison_result['mismatches']))
                        with col_m3:
                            st.metric("📤 EMIS Only", len(comparison_result['emis_not_in_app']))
                        with col_m4:
                            st.metric("📥 App Only", len(comparison_result['app_not_in_emis']))
                    else:
                        st.warning("No data found in the app database.")
