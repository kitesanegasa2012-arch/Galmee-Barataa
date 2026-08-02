from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="LATI APP",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Styling (Borders, Shapes, Colors, Font Sizes)
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .cover-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 3px solid #ffffff;
        margin-bottom: 25px;
    }
    .cover-card h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 15px;
        color: #ffffff;
    }
    .cover-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: #e3e6f0;
    }
    .cover-card p {
        font-size: 1.1rem;
        color: #f8f9fa;
    }
    .contact-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fc 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #4e73df;
        border-right: 2px solid #e3e6f0;
        border-top: 2px solid #e3e6f0;
        border-bottom: 2px solid #e3e6f0;
        box-shadow: 0 5px 15px rgba(78, 115, 223, 0.15);
        margin-top: 20px;
        text-align: center;
    }
    .contact-box h4 {
        color: #2e384d;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .contact-box p {
        color: #5a5c69;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 8px 0;
    }
    .metric-card {
        background-color: #ffffff;
        border: 2px solid #e3e6f0;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
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
    </style>
""",
    unsafe_allow_html=True,
)

# Lakkoofsa Eeyyamaa (Whitelist)
APPROVED_USERS = {
    "barsiisaa1@gmail.com": "keta1234",
    "barsiisaa2@gmail.com": "naga5678",
    "kitesanegasa2012@gmail.com": "39323713K",
}

# Session State Initialization
if "students_db" not in st.session_state:
    st.session_state.students_db = pd.DataFrame(
        columns=[
            "Maqaa Guutuu", "Koorniyaa", "Kutaa", "Daree (Section)", "Bara Dhalootaa",
            "Umurii", "Haala Galmee", "Bara Addaan Kute", "Haala Maatii", "Miidhama Qaamaa",
            "Gosa Miidhamaa", "Godina", "Aanaa", "Ganda", "Maqaa Haadhaa/Guddistuu",
            "FAN ID", "Lakk Bilbila Barataa", "Lakk Bilbila Maatii", "M/B Duraan Itti Barachaa Ture",
            "Avireejjii Qabxii", "Guyyaa Galmee (E.C)", "Barsiisaa Galmeessee"
        ]
    )

if "targets" not in st.session_state:
    st.session_state.targets = {
        str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)
    }

if "school_name" not in st.session_state:
    st.session_state.school_name = ""


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


# ----------------- LOGIN SYSTEM -----------------
st.sidebar.markdown("### 🏫 Kitesa Negasa")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="cover-card">
            <h1>🎓 LATI APP </h1>
            <h3>Baga Nagaan Gara App Galmee Barattootaa Kitesa Negasaatiin Kalaqaameetti Dhuftan!</h3>
            <p>Sirni kun odeeffannoo guutuu barattootaa galmeessuun, gabaasota addaa addaa qopheessuu fi hordoffii taasisuuf kan qophaa'eedha.</p>
        </div>
        
        <div class="contact-box">
            <h4>📞 Odaan Qunnamtii (Contact Information)</h4>
            <p>Itti fayyadama app kanaaf eeyyama argachuuf toora qunnamtii kana fayyadamaa!</p>
            <p>📱 <b>Telphone & Telegram:</b> +251969184005 / 910927936</p>
            <p>📧 <b>Gmail:</b> kitesanegasa2012@gmail.com</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("---")
    st.subheader("🔐 Seensa Appii (Login System)")
    st.write("Appii kana fayyadamuuf maaloo Email fi Jecha Darbii (Password) keessan galchaa.")
    
    with st.form("login_form"):
        email = st.text_input("Email Barsiisaa")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Seeni (Login)")
        
        if submit:
            if email in APPROVED_USERS and APPROVED_USERS[email] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = email
                st.success("Baga nagaan Gara Lati App tti dhuftan!")
                st.rerun()
            else:
                st.error("Email ykn Password sirrii miti, ykn eeyyama hin qabdu!")
                
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

else:
    st.sidebar.write(f"Seenteetta: {st.session_state.current_user}")
    if st.sidebar.button("Bahu (Logout)"):
        st.session_state.authenticated = False
        st.rerun()

    menu = st.sidebar.selectbox(
        "Filannoo Fuulaa (Navigation)",
        [
            "1. Fuula jalqabaa (Cover Page)",
            "2. Dashboard Galmee Barataa (Foormii)",
            "3. Dashboard Gabaasa Qinda'ee",
        ],
    )

    if menu == "1. Fuula jalqabaa (Cover Page)":
        st.markdown(
            """
            <div class="cover-card">
                <h1>🎓 APP GALMEE BARATTOOTAA</h1>
                <h3>Baga Nagaan Gara App Galmee Barattootaa Mana Barumsaa B/saa Kitesa Negasaatiin Kalaqaameetti Dhuftan!</h3>
                <p>Sirni kun odeeffannoo barattootaa qabaachuuf, gabaasa oomishuuf fi hordoffii taasisuuf kan qophaa'eedha.</p>
            </div>
            
            <div class="contact-box">
                <h4>📞 Odaan Qunnamtii (Contact Information)</h4>
                <p>Itti fayyadama app kanaaf eeyyama argachuuf toora qunnamtii kana fayyadamaa!</p>
                <p>📱 <b>Telphone & Telegram:</b> +251969184005 / 910927936</p>
                <p>📧 <b>Gmail:</b> kitesanegasa2012@gmail.com</p>
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

    elif menu == "2. Dashboard Galmee Barataa (Foormii)":
        st.subheader("📝 Foomii Galmee Barattootaa Haaraa")

        with st.form("school_name_form"):
            st.markdown("### Maqaa Mana Barumsaa Galmeessaa")
            input_school = st.text_input(
                "Maqaa Mana Barumsaa",
                value=st.session_state.school_name,
                placeholder="Fkn: M/B Sadarkaa 2ffaa Kitesa Negasa",
            )
            save_school_btn = st.form_submit_button("🏫 Maqaa Mana Barumsaa Save Gochuu")
            if save_school_btn:
                if input_school.strip():
                    st.session_state.school_name = input_school.strip()
                    st.success("Maqaa mana barumsaa milkaa'inaan save ta'eera!")
                else:
                    st.warning("Maaloo maqaa mana barumsaa galchi!")

        if st.session_state.school_name:
            st.info(f"📌 Mana Barumsaa Galmaa'e: **{st.session_state.school_name}**")
        else:
            st.warning("⚠️ Jalqaba maqaa mana barumsaa oliitti save godhaa!")

        st.write("---")

        db_existing = st.session_state.students_db
        default_godina = get_last_location(db_existing, "Godina")
        default_aanaa = get_last_location(db_existing, "Aanaa")
        default_ganda = get_last_location(db_existing, "Ganda")

        with st.form("registration_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa")
                koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])

                grade_col1, grade_col2 = st.columns(2)
                kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
                daree = grade_col2.selectbox("Daree (Section)", [chr(65 + i) for i in range(11)])

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

                maqaa_haadhaa = st.text_input("10. Maqaa Guutuu Haadhaa ykn Guddistuu")
                fan_id = st.text_input("11. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID - Digiti 16)")
                lakk_bilbila_barataa = st.text_input("12. Lakkoofsa Bilbila Barataa (+251...)")
                lakk_bilbila_maatii = st.text_input("13. Lakkoofsa Bilbila Maatii (+251...)")
                mb_duraan = st.text_input("14. Mana Barumsaa Duraan Itti Barachaa Ture")

                avireejjii = st.number_input(
                    "15. Avireejjii Qabxii Bara Darbee (0 - 100)",
                    min_value=0.0, max_value=100.0, value=75.0,
                )

                barsiisaa = st.text_input("16. Barsiisaa Galmeessee")
                guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018")

            submitted = st.form_submit_button("💾 Save (Enter)")

            if submitted:
                error_msgs = []
                warning_msgs = []

                if not st.session_state.school_name:
                    error_msgs.append("Maaloo jalqaba Maqaa Mana Barumsaa save godhaa!")
                if not maqaa_guutuu:
                    error_msgs.append("Maqaa Guutuu barataa guuti!")
                if koorniyaa == "Filadhu":
                    error_msgs.append("Maaloo Koorniyaa barataa filadhu!")

                saved_school_lower = st.session_state.school_name.strip().lower()
                input_mb_lower = mb_duraan.strip().lower()

                if input_mb_lower:
                    if input_mb_lower == saved_school_lower and haala_galmee == "Mana Barumsaa Biroo":
                        error_msgs.append('Halluu diimaan: M/B duraan itti barachaa ture maqaa mana barumsaa kanaa wajjin wal-qixxaachaa waan jiruuf, Haala Galmee "Mana Barumsaa Biroo" jechuu hin qabu!')
                    elif input_mb_lower != saved_school_lower and haala_galmee != "Mana Barumsaa Biroo":
                        error_msgs.append('Halluu diimaan: M/B duraan itti barachaa ture maqaa mana barumsaa kanaan ala waan ta\'eef, Haala Galmee "Mana Barumsaa Biroo" jechuu qaba!')

                if avireejjii < 50 and haala_galmee != "Irra deebii (Kufe)":
                    error_msgs.append('Halluu diimaan: Barataan avireejjii 50 gadi fide haala galmeen "Irra deebii (Kufe)" jedhuun walsimuu qaba!')

                clean_fan = fan_id.strip()
                if clean_fan and (not clean_fan.isdigit() or len(clean_fan) != 16):
                    error_msgs.append("FAN ID dijiitii 16 qofa ta'uu qaba!")

                def validate_phone(phone_str, field_label):
                    p = phone_str.strip()
                    if not p.startswith("+251"):
                        return f"{field_label}: Lakkoofsi bilbilaa '+251' tiin jalqabuu qaba!"
                    subscriber_part = p[4:]
                    if len(subscriber_part) < 9:
                        return f"{field_label}: Lakk. ni hanqata (dijiitii 9 guutuu qaba)."
                    elif len(subscriber_part) > 9:
                        return f"{field_label}: Irra darbe (dijiitii 9 qofa ta'uu qaba)."
                    elif not subscriber_part.isdigit():
                        return f"{field_label}: Koodii biyyaa itti aansuun lakkoofsi jiru dijiitii qofa ta'uu qaba."
                    return None

                if lakk_bilbila_barataa.strip():
                    err_p1 = validate_phone(lakk_bilbila_barataa, "Bilbila Barataa")
                    if err_p1:
                        error_msgs.append(err_p1)

                if lakk_bilbila_maatii.strip():
                    err_p2 = validate_phone(lakk_bilbila_maatii, "Bilbila Maatii")
                    if err_p2:
                        error_msgs.append(err_p2)

                if not aanaa.strip() or not godina.strip():
                    warning_msgs.append("Odeeffannoo bakka dhalootaa (Godina ykn Aanaa) guutuu miti.")

                if error_msgs:
                    for err in error_msgs:
                        st.markdown(f'<p style="color:red; font-weight:bold;">⚠️ {err}</p>', unsafe_allow_html=True)
                elif warning_msgs:
                    for warn in warning_msgs:
                        st.markdown(
                            f'<div style="background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; font-weight: bold;">⚠️ {warn} - Maqaa barataa: {maqaa_guutuu}</div>',
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
                    st.session_state.students_db = pd.concat(
                        [st.session_state.students_db, pd.DataFrame([new_data])],
                        ignore_index=True,
                    )
                    st.success(f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!")

    elif menu == "3. Dashboard Gabaasa Qinda'ee":
        st.subheader("🔐 Dashboard Barsiisaa / Gabaasaa")
        st.write("Maaloo gabaasota kana ilaaluuf Password galchaa.")
        
        password = st.text_input("Password Gabaasaa", type="password", key="dash_pass")

        if password == "kitesa2019" or password == "admin123":
            st.success("Seensa Milkaa'e! Gabaasotaa, Karoora, fi Sirreeffama (Edit/Delete) ilaaluu dandeessa.")

            school_display = st.session_state.school_name if st.session_state.school_name else "Mana Barumsaa"

            tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabEdit = st.tabs(
                [
                    "Karoora", "Guutuu", "Guyyaa", "Hanga Ammaa", "Miidhamaa",
                    "Lak. Miidhamaa", "Irra Deebii", "Lak. Irra Deebii", "✏️ Edit / Delete"
                ]
            )

            db = st.session_state.students_db

            with tabA:
                st.markdown(f"### A. Guca Karoora Galmee Barataa - {school_display}")
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
                    label="📥 Karoora Download Gochuu",
                    data=buffer_t.getvalue(),
                    file_name="Karoora_Galmee_Barattootaa.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            with tabB:
                st.markdown(f"### B. Guca Gabaasaa Waligalaa Barataa - {school_display}")
                if not db.empty:
                    st.dataframe(db, use_container_width=True)
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
                    st.download_button(
                        label="📥 Gabaasa Guutuu Download Gochuu",
                        data=buffer.getvalue(),
                        file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Deetaan barataa galmaa'e hin jiru.")

            with tabC:
                st.markdown(f"### C. Gabaasa Galmee Guyyaa Tokkoo - {school_display}")
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
                            label="📥 Gabaasa Guyyaa Download",
                            data=buffer_c.getvalue(),
                            file_name=f"Gabaasa_Guyyaa_{selected_date.replace('/', '-')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("Guyyaa filatame kana deetaan hin jiru.")
                else:
                    st.info("Deetaan waligalaa hin jiru.")

            with tabD:
                st.markdown(f"### D. Gabaasa Galmee Hanga Ammaatti - {school_display}")
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
                        label="📥 Gabaasa Hanga Ammaa Download",
                        data=buffer_d.getvalue(),
                        file_name="Gabaasa_Hanga_Ammaatti.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Deetaan hin jiru.")

            with tabE:
                st.markdown(f"### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii - {school_display}")
                if not db.empty:
                    disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
                    if not disabled_df.empty:
                        st.dataframe(disabled_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Gosa Miidhamaa"]], use_container_width=True)

                        buffer_e = io.BytesIO()
                        with pd.ExcelWriter(buffer_e, engine="openpyxl") as writer:
                            disabled_df.to_excel(writer, sheet_name="Miidhama_Qaamaa", index=False)
                        st.download_button(
                            label="📥 Barattoota Miidhama Qaamaa Download",
                            data=buffer_e.getvalue(),
                            file_name="Barattoota_Miidhama_Qaamaa.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("Barataan miidhama qaamaa qabu hin galmoofne.")
                else:
                    st.info("Deetaan waligalaa hin jiru.")

            with tabF:
                st.markdown(f"### F. Gabaasa Lakkoofsaa Miidhama Qaamaa - {school_display}")
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
                            label="📥 Lakkoofsa Miidhamaa Download",
                            data=buffer_f.getvalue(),
                            file_name="Lakkoofsa_Gosa_Miidhamaa.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("Barataan miidhama qaamaa qabu hin galmoofne.")
                else:
                    st.info("Deetaan waligalaa hin jiru.")

            with tabG:
                st.markdown(f"### G. Gabaasa Barattoota Irra Deebi'anii - {school_display}")
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
                            label="📥 Barattoota Irra Deebii Download",
                            data=buffer_g.getvalue(),
                            file_name="Barattoota_Irra_Deebii.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("Barataan irra deebii galmaa'e hin jiru.")
                else:
                    st.info("Deetaan waligalaa hin jiru.")

            with tabH:
                st.markdown(f"### H. Gabaasa Lakkoofsaa Irra Deebii - {school_display}")
                if not db.empty:
                    repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
                    if not repeat_df.empty:
                        repeat_summary_data = []
                        haala_types = repeat_df["Haala Galmee"].unique()
                        for h_type in haala_types:
                            row = {"Haala Galmee": h_type}
                            sub_h = repeat_df[repeat_df["Haala Galmee"] == h_type]
                            
                            tot_h = 0
                            for k in range(1, 13):
                                k_str = str(k)
                                cnt = len(sub_h[sub_h["Kutaa"] == k_str])
                                row[f"Kutaa {k}"] = cnt
                                tot_h += cnt
                            row["Ida'ama Waliigalaa"] = tot_h
                            repeat_summary_data.append(row)

                        rep_sum_df = pd.DataFrame(repeat_summary_data)
                        st.dataframe(rep_sum_df, use_container_width=True)

                        buffer_h = io.BytesIO()
                        with pd.ExcelWriter(buffer_h, engine="openpyxl") as writer:
                            rep_sum_df.to_excel(writer, sheet_name="Lakkoofsa_Irra_Deebii", index=False)
                        st.download_button(
                            label="📥 Lakkoofsa Irra Deebii Download",
                            data=buffer_h.getvalue(),
                            file_name="Lakkoofsa_Barattoota_Irra_Deebii.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("Barataan irra deebii galmaa'e hin jiru.")
                else:
                    st.info("Deetaan waligalaa hin jiru.")
                    Conversation with Gemini
Moosajii Galmee barattootaa uumuuf gargaaru Kami?

Moosajiiwwan ykn sagantaaleen galmee barattootaa (Student Registration Systems) saffisaan, karaa qindaa'aa fi ammayyaatiin qabachuuf gargaaran keessaa caalaatti beekamoo fi tajaajila gaarii kennan armaan gaditti dhiyaataniiru:

1. Moosajiiwwan Odeeffannoo Mana Barumsaa (School Management Systems - SMS)
Moosajiiwwan kun galmee barattootaa qofa odoo hin ta'in, hordoffii argammii (attendance), qabxii qormaataa, fi kaffaltii galchuu dabalatee tajaajila guutuu kennu:

OpenEduCat: Sirna mana barumsaa kan Odoo irratti hundaa'e fi hojii galmee barattootaaf baay'ee mijataa ta'e.

Fedena: Mana barumsaa sadarkaa garaa garaatiif kan qophaa'e fi galmee barattootaa fi odeeffannoo bulchiinsaa bulchuuf kan gargaaru.

Gibbon: Moosajii bilisaa fi banaa (open-source) kan mana barumsaa keessatti galmee barattootaa, daree fi barsiisota walitti fufuuf gargaaru.

2. Meeshaalee Deetaabaasii fi Lakkaa'ii (Spreadsheets & Databases)
Mana barumsaa xixiqqoof ykn karaa salphaa fi bilisaa ta'een hojjechuuf:

Microsoft Excel / Google Sheets: Akkaataa barbaadetti gabatee qopheessuun (Templates) maqaa, lakkoofsa galmee, umrii, kutaa fi teessoo barattootaa galchuuf baay'ee tajaajila. Google Sheets irratti immoo namoonni hedduu tokkummaan irra hojjechuun ni danda'ama.

Microsoft Access / Google Forms: Foomii galmee (Registration Form) intarneetiin guutamu qopheessuun deetaa barattootaa kallattiidhaan gara deetaabaasii (Database) tti walitti qabuuf.

3. Moosajiiwwan Ofiin Hojjetaman (Custom Apps / Web Apps)
Python (Flask/Django) ykn Android Studio: Wantoota mana barumsaaf addatti barbaadaman irratti hundaa'uun moosajii dhuunfaa (Custom App) saffisaan tolchuun ni danda'ama.

Yaada dabalataa: Mana barumsaa keessaniif moosajii isa kamiin fayyadamuun akka danda'amu yoo barbaaddan, haala rakkoo jiru (fakkeenyaaf: interneetiin kan qabu moo kan hin qabne, akkasumas baajetiirratti hundaa'ee) irratti mari'achuun ni danda'ama.

Ani kaniin barbaade,Jalqabbii barnootaa kana irratti yommuu maqaa barataa fi odeeffannoo isaa hunda galchinuu,kutaan,saalaan,umuriin(Bara dhalootaa/guyyaa,ji'a bara,haala galmeen(haaraa,irra deebii(kufaatii,kutittin),miidhaama qaamaa(ija,miila,harka,sammuu,currisa,hawaasummaa),Haala maatii(Lachuu qaba,abbaa qofaa,haadha qofa,lachuu hin qabu),Qabxii kutaa darbe,Lakk,bilbilaa barataa,lakk.bilbila maatii,FAN ID. Guyyaa galmee ,Barsiisaa Galmeessee qabu,kalaqee,Dashboard Mana barumsaaf immoo,Gabaasa Daataa barataa,kutaan,umuriin,Saalaan,Haala galmeen(Haaraa,kufe itti debi'e,kutee itti deebi'e) jedhee ,Gabaasa Guyyaa,torbee,ji'aa,kan waligalaa kan print fi download ta'u kalaquu barbaade.isaan armaan olii keessaa kamtuu naa mijata

Haala ibsa bal'aa kennite kanaan, gaaffiin kee odeeffannoo barataa gadi fageenya qabu (akka saala, bara dhalootaa, haala galmee [haaraa, kufe/kutee kan deebi'e], miidhaama qaamaa gosa addaddaa, haala maatii, FAN ID, guyyaa galmee, barsiisaa galmeesse, fi kkf) kan qabatuu fi gama Dashboard mana barumsaatiin gabaasa guutuu (guyyaa, torbee, ji'aa, waliigalaa) akkaataa kutaa, saalaa, umrii, fi haala galmeetiin filatee print ykn download gochuuf kan dandeessisu, akkasumas karaa salphaa fi ammayyaatiin ijaaruuf isa kamiitu siif mijata gaaffii jedhuuf deebiin:

Filannoowwan armaan olii keessaa kallattiidhaan siif mijatuu danda'u:

1. Moosajii Ofiin Hojjetaman (Custom Apps / Web Apps) — Filannoo Isa Caalaa Mijaatuu fi Guutuu
Odeeffannoowwan bal'aa fi bifa lakkoofsa cimaa (Complex data) akkasii walitti qabuuf moosajiiwwan lakkaa'ii salphaa (akka Excel idilee) yeroo dhiyootti si rakkisuu danda'u. Kanaafuu, Custom App hojjechuutu siif filatamaadha:

Sababni Isaa: Odeeffannoo akka miidhaama qaamaa gosa addaddaa, haala maatii, FAN ID, fi qabxii kutaa darbee sirriitti walitti qabuuf, akkasumas Dashboard dhuunfaa qopheessuun gabaasa print ykn download (PDF/Excel) gochuuf sagantaa ofiin ijaarametu barbaachisa.

Akkamiin hojjete?

Python (Django ykn Flask): Gama backend tiin odeeffannoo kana hunda deetaabaasii (Database) keessatti sirnaan qabuuf.

Streamlit (Python): Yoo saffisaan Dashboard gabbataa fi bifa miidhagina qabuun qopheessuu barbaadde, Streamlit fayyadamuun yeroo gabaabaa keessatti foomii galmee fi Dashboard gabaasaa (filter kan godhu) hojjechuun ni danda'ama (fakkeenyaaf deetaa kana qindeessuuf barmaatilee akkasii fayyadamuu dandeessa).

Frontend (HTML/CSS/Bootstrap): Foomiin galmee fi Dashboard kun bifa ammayyaatiin akka mul'atuu fi sirriitti print akka ta'uuf gargaara.

2. Google Sheets / Microsoft Excel (Fayyadamuu yoo barbaadde - Garuu Daangaa kan qabu)
Haala Inni Itti Mijatu: Odeeffannoo kana hunda Columns fi Rows godhuun galchuuf Excel ykn Google Sheets fayyadhuun ni danda'ama. Keessattuu Google Sheets irratti Data Validation (Filannoo akka haaraa, kufe/kutee deebi'e, haala maatii, fi kkf) diriirsuun salphaadha.

Hanqinni Isaa: Dashboard gabaasaa gabbataa ta'ee fi guyyaa, torbee, ji'aan gabaasa baasuuf Pivot Tables ykn Charts hedduu walitti qindeessuu gaafata. Akkasumas namoonni hedduu yeroo tokkotti irratti hojjechuuf yoo ta'e Google Sheets caalaatti mijata, garuu odeeffannoon miidhaama qaamaa fi haala maatii baay'achaa yoo deeme filtering godhuun yeroo tokko tokko ni ulfaata.

Guduunfaa / Gorsa:
Yoo dandeettii pirogaraamiingii (Programming) qabdu ykn namni si gargaaru jiraate, Python (Streamlit ykn Django) fayyadamuun Moosajii Ofiin Hojjetamu (Custom App) tolchuun fedhii kee kana 100% guuta. Sababni isaa Dashboard mataa kee danda'e kan gabaasa addaddaatiin (kutaan, saalaan, haala galmeetiin) filter godhuu danda'uu fi kallattiidhaan Print/Download gochuu dandeessisu salphaatti ijaaruuf si dandeessisa.

Yoo saffisaan osuma moosajii hin barreessiin guyyaa har'aa eegaluu barbaadde immoo, Google Sheets irratti foomii guuttannoo (Google Forms) wajjin walqabsiisuun jalqabuu dandeessa; garuu gabaasa gadi fagoo baasuuf Pivot Table fi Formula irratti hojjechuu qabda.

tole kooddii python streamlit naaf uumtaa foormii isaan siif kennaa

Tole, eeyyee siif nan uuma! Foomii galmee barattootaa guutuu fi Dashboard gabaasaa (filter fi print/download gochuu danda'u) kan of keessaa qabu kooddii Python Streamlit sirriitti hojjetu siif qopheessuuf qophii dha.

Foomii barattootaa fi odeeffannoo gaafatte hunda (kutaa, saala, umrii/bara dhalootaa, haala galmee, miidhaama qaamaa, haala maatii, qabxii, bilbila, FAN ID, guyyaa galmee, fi barsiisaa galmeesse) kan qabate fi gama Dashboard tiin immoo gabaasa guyyaa, torbee, ji'aa fi waliigalaa bifa filannoowwaniin dhiyeessu kooddii kana hojjechuuf ergaa; kanumaan walqabatee foomiin kee akkaataa ati feetuun akka ta'uuf maalfaatu irra jira? Foomicha gara kooddiitti jijjiiruuf ergi!

1,COVER page irratti

"Icon"APP GALMEE BARATTOOTAA

Baga Nagaan Gara App Galmee Barattootaa Mana Barumsaa B/saa Kitesa Neagasaatiin kalaqaameettii Dhuftan!

Dashoard Galmee Barataaa Dashboard Gabaasaa Mana barumsaa

bordeerii,background,Colour addaa addaa fi miidhagaan,fontsize fi style

2.Dashboard Galmee Barataa

a,Maqaa Guutuu b,koorniyaa(Dhiira,Dhalaa)-filannoo c,Kutaa(1-12)-filannoo d,Bara Dhalootaa(Guyyaa,Ji'a,bara )Akka lakkoofsa itoophiyyatti akka filatee enter jedhutti

E,Umurii ,mosajichi bara dhalootaa irraa akka shallagee argatuutti

F,Haala Galmee(Haaraa,irra deebii(kute,kufe,mana barumsaa biroo),bara adda kute)-barreessitee filannoo,barrii adda kutee(2005 irraa eegali)

G,Haala maatii(lachuu qaba,Abbaa qofa,Haadha qofa,lachuu hin qabu)-filannoo

H.Haala Miidhama qaamaa(jira,hin jiru)-filannoo,,yoo jiraate(arguu salphaa,arguu cimaa,dhageetti salphaa,dhageettii cimaa,sochii harkaa salphaa,sochii harkaa cimaa,sochii miilaa salphaa,sochii miilaa cimaa,rakkoo dubbii salphaa,rakkoo dubbii cimaa,saaleessa sammuu,Currisa hawaasummaa)filannoodha

I.Bakka dhalootaa(Godina,Aanaa,Ganda)

J.Maqaa Guutuu Haadhaa ykn guddistuu

K.Lakkoofsa Waraqaa EEnyummaa Dijitaalaa(FAN)

L.lakkofsa bilbilaa barataa

M.lakkoofsa bilbila maatii

N.Mana barumsaa Duraan itti barachaa turee

O.avireejjii Qabxii bara darbee(Kun 50 gadi taanaan,halluu diimaa akka agarsiisu) fi haala galmee keessatti Kan kufe jedhuun akka waldubbisu godhi

P.Guyyaa Galmee(Kalaandarii guyyichaan ofii akka galchuu guyyan,sa'aatii kan Itoophiyaan

Q.save(Enter)xuqee

3.Dashboard HMB

A.Guca Karoora Galmee barataa 2019,kutaan,hubadhu asitti kutaan 1,umurii 7 fi waligala jedhamuun,bakka 2tti qodamu,saalaan karoorfate jalqaba asitti akka mosajji kanaaf kennu qophheessita

B,Guca Gabaasaa Waligalaa barataa odeeffannoo Guutuu baratan guutee sana excell bakka tokkotti tartiiba barataan galma'een walitti kuusee save godhe qabatu(edit,save,delete)ta'uu danda'u

C.Gucaa Gabaasaa Galmee Guyyaa daata lakkoofsaa qofaa kutaa,saalaa,umuriin kan kutaa 1 qofaa(umurii7+kutaa 1 waligala guyyicha galma'aanii,sababni isaa gabaasa barattoota umurii 7 qofaatti waan gaaffatamuufi

D.Guca Gabaasa excell Daataa lakkoofsaa qofaa kutaadhaan Dhiiraa fi dhalaan galma'aan(kutaan tokkoo umurii 7+Waligala kutaa 1) qinddeesse bifa Gbaasaaf ta'un

Hnaguma guyyaan galmee dabalaa deemuun dabalaa deemuu(kun kan waligalaati)

E.Gucaa Gabaasa Barattoota Miidhama Qaamaa qabanii Odeeffannoo barataan duraan guutee irraa dubbisee argatu excell maqaa,kutaan,umuriin,Gosa miidhamaa qaaama duraan barataan ibseen fi Barattootaa Haala maatii keessattii "Lachuu hin qabne dabalatee"Hnaguma bartaan dabalaa deemuun update ta'e baayina barataan dabalaa deemu qaba

F.Guca Gbaasa Barattoota miidhaama qaama qabanii Lakkoofsa qofaan kutaa,saalaa fi gosa miidhaama qaamaa qabanii,haala maatii keessatti "lachuu hin qabne dabalatee,kun gabaasa lakkoofsa qofa Kan option D irratti xiyyeefata

G.Guca Gbaasa Barattoota irra deebi'anii kuni maqaa,saala,kutaa,sababa irra deebii(kufaatii,kutee)bara irraa deebii(kana kan odeeffannoo barataa keessatti guutame fudhata

H.Guca Gabaasa barattoota irra deebi'anii lakkoofsa qofaan kutaa,saala,bara irra deebiin qindeessa

I.Gabaasa Galmee Waligalaa Bara 2019 excel qinddeessuu

karoora galmee bara darbee kutaa,saalaan kan dashboard barssisa jalaqaba option A irraatti guutame fudhachuun, Column 1 kutaa comun 2 karooraa Dhiiraa ,Dhalaa,Waligalaa ,column 3,raawwii Dhiiraa Dhalaa fi Waligalaa,column % parsantii raawwii Dhiiraa%,Dhalaa% fi Waligalaa%.kun karoorri guca A fi I kan walfakkatu ta'ee ragaa walirra fudhachh qaba.

J.Ragaan galma'ee save ta'ee yeroo dheeraaf kuufamuu,edit ta'uu fi kan hin barbaachifne delet akka ta'u godhi

Hubachiisa guddaa

1,Ragaan kun akka miidhaguufi fontsize fi style,halluu garaagaraan qulqullina isaa eegi qopheessi

2,Bakka ani fulduratti filannoo jedhe ofikee daata galchitee namni guutu filata jechuudha.

3.Daashboard barsiisaa pasward akka ta'u taasisi

4.Barataan yeroo galma'uu dashboard halluu garaagaraa qabu kan barataa hanga ammatti galma'ee baayina isaa qofa mullisuu kutaa kutaan agarsuu qopheessi fkn kutaa 1:60 jedhe icon bareedan golgamee kun cover page irratti haa ta'u

Kunoo kooddii Python Streamlit guutuu, kan haala miidhaginaa (UI), halluu, border, fontsize, font-style, akkasumas ulaagaawwan ati gaafatte hunda (Dashboard Barsiisaa password qabu, Cover Page icon fi lakkoofsa barattootaa agarsiisu, Dashboard galmee barataa bal'aa, fi Gucaalee Gabaasaa addaddaa Excel/Print gochuu danda'u) qabatamaatti hojjechuuf qophaa'e dha.

Kooddii kana faayilii kesessa (fakkeenyaaf app.py jechuun) kuusuun Terminal kee irratti streamlit run app.py jechuun hojjechuu dandeessa:

Python
from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="App Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Styling (Border, Background, Colors, Font size & styles)
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

# Session State Initialization for Database & Targets
if "students_db" not in st.session_state:
  st.session_state.students_db = pd.DataFrame(
      columns=[
          "Maqaa Guutuu",
          "Koorniyaa",
          "Kutaa",
          "Bara Dhalootaa",
          "Umurii",
          "Haala Galmee",
          "Bara Addaan Kute",
          "Haala Maatii",
          "Miidhama Qaamaa",
          "Gosa Miidhamaa",
          "Bakka Dhalootaa (Godina/Aanaa/Ganda)",
          "Maqaa Haadhaa/Guddistuu",
          "FAN ID",
          "Lakk Bilbila Barataa",
          "Lakk Bilbila Maatii",
          "M/B Duraan Itti Barachaa Ture",
          "Avireejjii Qabxii",
          "Guyyaa Galmee",
          "Barsiisaa Galmeessee",
      ]
  )

if "targets" not in st.session_state:
  # Default target structure for Grade 1-12
  st.session_state.targets = {
      str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)
  }

# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown(
    "### 🏫 Mana Barumsaa B/saa Kitesa Negasa"
)  # Updated teacher name reference
menu = st.sidebar.selectbox(
    "Filannoo Fuulaa (Navigation)",
    [
        "1. Cover Page",
        "2. Dashboard Galmee Barataa (Foomii)",
        "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)",
    ],
)

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

  # Display live student counts per grade in attractive metric cards
  db = st.session_state.students_db
  cols = st.columns(4)
  for i in range(1, 13):
    count = (
        len(db[db["Kutaa"] == str(i)]) if not db.empty else 0
    )  # Safe empty check
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

# ----------------- 2. DASHBOARD GALMEE BARATAA (FOOMII) -----------------
elif menu == "2. Dashboard Galmee Barataa (Foomii)":
  st.subheader("📝 Foomii Galmee Barattootaa Haaraa")

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa")
      koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])
      kutaa = st.selectbox(
          "3. Kutaa", [str(i) for i in range(1, 13)]
      )  # Grades 1 to 12

      st.markdown(
          "**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**"
      )  # Ethiopian calendar date options
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox(
          "Guyyaa", [str(i) for i in range(1, 31)]
      )  # Standard range
      b_ji'a = b_col2.selectbox(
          "Ji'a",
          [
              "Meskerem",
              "Tikimt",
              "Hidar",
              "Tahsas",
              "Tir",
              "Yekatit",
              "Megabit",
              "Meyazia",
              "Genbot",
              "Sene",
              "Hamle",
              "Nehase",
              "Pagume",
          ],
      )
      b_bara = b_col3.number_input(
          "Bara Dhalootaa (Fkn: 2005)", min_value=1980, max_value=2025, value=2010
      )
      # Calculate Age dynamically based on current Ethiopian year (~2018/2019)
      current_et_year = 2018
      umurii = current_et_year - b_bara

      haala_galmee = st.selectbox(
          "5. Haala Galmee",
          [
              "Haaraa",
              "Irra deebii (Kufe)",
              "Irra deebii (Kute)",
              "Mana Barumsaa Biroo",
          ],
      )
      bara_addaan_kute = (
          st.selectbox(
              "Bara Addaan Kute (Yoo jiraate)",
              ["On", "2005", "2006", "2007", "2008", "2009", "2010"]
              + [str(y) for y in range(2011, 2027)],
          )
          if "deebii" in haala_galmee
          else "Hin jiru"
      )

      haala_maatii = st.selectbox(
          "6. Haala Maatii",
          ["Lachuu qaba", "Abbaa qofa", "Haadha qofa", "Lachuu hin qabu"],
      )
      miidhama_qaamaa = st.selectbox(
          "7. Haala Miidhama Qaamaa", ["Hin jiru", "Jira"]
      )
      gosa_miidhamaa = (
          st.selectbox(
              "Gosa Miidhama Qaamaa",
              [
                  "Arguu salphaa",
                  "Arguu cimaa",
                  "Dhageettii salphaa",
                  "Dhageettii cimaa",
                  "Sochii harkaa salphaa",
                  "Sochii harkaa cimaa",
                  "Sochii miilaa salphaa",
                  "Sochii miilaa cimaa",
                  "Rakkoo dubbii salphaa",
                  "Rakkoo dubbii cimaa",
                  "Saaleessa sammuu",
                  "Currisa hawaasummaa",
              ],
          )
          if miidhama_qaamaa == "Jira"
          else "Hin jiru"
      )

    with col2:
      bakka_dhalootaa = st.text_input(
          "8. Bakka Dhalootaa (Godina, Aanaa, Ganda)"
      )
      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID)")
      lakk_bilbila_barataa = st.text_input("11. Lakkoofsa Bilbila Barataa")
      lakk_bilbila_maatii = st.text_input("12. Lakkoofsa Bilbila Maatii")
      mb_duraan = st.text_input("13. Mana Barumsaa Duraan Itti Barachaa Ture")

      avireejjii = st.number_input(
          "14. Avireejjii Qabxii Bara Darbee (0 - 100)",
          min_value=0.0,
          max_value=100.0,
          value=75.0,
      )

      # Automatic conditional check: If average < 50, flag red and map status alignment
      if avireejjii < 50:
        st.markdown(
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu qaba!</p>',
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee")
      guyyaa_galmee = str(datetime.now().date())  # Ethiopian calendar tracker layout

    submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
      if not maqaa_guutuu or not fan_id:
        st.error("Maaloo Maqaa Guutuu fi FAN ID guuti!")
      else:
        new_data = {
            "Maqaa Guutuu": maqaa_guutuu,
            "Koorniyaa": koorniyaa,
            "Kutaa": kutaa,
            "Bara Dhalootaa": f"{b_guyyaa}/{b_ji'a}/{b_bara}",
            "Umurii": umurii,
            "Haala Galmee": haala_galmee,
            "Bara Addaan Kute": bara_addaan_kute,
            "Haala Maatii": haala_maatii,
            "Miidhama Qaamaa": miidhama_qaamaa,
            "Gosa Miidhamaa": gosa_miidhamaa,
            "Bakka Dhalootaa (Godina/Aanaa/Ganda)": bakka_dhalootaa,
            "Maqaa Haadhaa/Guddistuu": maqaa_haadhaa,
            "FAN ID": fan_id,
            "Lakk Bilbila Barataa": lakk_bilbila_barataa,
            "Lakk Bilbila Maatii": lakk_bilbila_maatii,
            "M/B Duraan Itti Barachaa Ture": mb_duraan,
            "Avireejjii Qabxii": avireejjii,
            "Guyyaa Galmee": guyyaa_galmee,
            "Barsiisaa Galmeessee": barsiisaa,
        }
        # Append data safely
        st.session_state.students_db = pd.concat(
            [st.session_state.students_db, pd.DataFrame([new_data])],
            ignore_index=True,
        )
        st.success(
            f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!"
        )

# ----------------- 3. DASHBOARD BARSIIKAA / GABAASAA (PASSWORD PROTECTED) -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)":
  st.subheader("🔐 Dashboard Barsiisaa (Seensa Eeyyamame)")

  password = st.text_input("Password Galchi", type="password")

  # Simple secure teacher password check
  if password == "kitesa2019" or password == "admin123":
    st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa.")

    tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
        [
            "A. Karoora",
            "B. Guutuu (Excel)",
            "C. Guyyaa (Kutaa 1)",
            "D. Lakkoofsaa",
            "E. Miidhamaa (Detail)",
            "F. Miidhamaa (Count)",
            "G. Irra-Deebii (Detail)",
            "H. Irra-Deebii (Count)",
            "I. Gabaasa 2019",
            "J. Edit/Delete",
        ]
    )

    db = st.session_state.students_db

    with tabA:
      st.markdown("### A. Guca Karoora Galmee Barataa 2019")
      st.write(
          "Kutaa 1 (Umurii 7) fi kutaa birooaf karoora Dhiiraa fi Dhalaa galchi:"
      )
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

    with tabB:
      st.markdown("### B. Guca Gabaasaa Waligalaa Barataa (Excel Download)")
      if not db.empty:
        st.dataframe(db)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
        st.download_button(
            label="📥 Excel-tti Download Gochuu",
            data=buffer.getvalue(),
            file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
      else:
        st.info("Deetaan galmaa'e hin jiru.")

    with tabC:
      st.markdown("### C. Guca Gabaasaa Galmee Guyyaa (Kutaa 1, Umurii 7)")
      if not db.empty:
        filtered_c = db[(db["Kutaa"] == "1") & (db["Umurii"] == 7)]
        st.write(f"Baay'ina Barattoota Kutaa 1 (Umurii 7): {len(filtered_c)}")
        st.dataframe(filtered_c)
      else:
        st.info("Deetaan hin jiru.")

    with tabD:
      st.markdown(
          "### D. Gabaasa Lakkoofsaa Kutaa, Saalaa fi Umuriin (Fkn Umurii 7 + Kutaa 1)"
      )
      if not db.empty:
        summary_d = (
            db.groupby(["Kutaa", "Umurii", "Koorniyaa"])
            .size()
            .reset_index(name="Baay'ina")
        )
        st.dataframe(summary_d)
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown(
          "### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii (Odeeffannoo Guutuu)"
      )
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(disabled_df)
      else:
        st.info("Deetaan hin jiru.")

    with tabF:
      st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa & Haala Maatii")
      if not db.empty:
        st.write("**Miidhama Qaamaa Gosaan:**")
        st.dataframe(db[db["Miidhama Qaamaa"] == "Jira"]["Gosa Miidhamaa"].value_counts())
        st.write("**Haala Maatii (Lachuu hin qabne dabalatee):**")
        st.dataframe(db["Haala Maatii"].value_counts())

    with tabG:
      st.markdown(
          "### G. Gabaasa Barattoota Irra Deebi'anii (Maqaa, Saala, Kutaa, Sababa)"
      )
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(repeat_df[
            ["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Haala Galmee", "Bara Addaan Kute"]
        ])
      else:
        st.info("Deetaan hin jiru.")

    with tabH:
      st.markdown(
          "### H. Gabaasa Lakkoofsaa Barattoota Irra Deebi'anii (Kutaa & Saalaan)"
      )
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(
            repeat_df.groupby(["Kutaa", "Koorniyaa", "Haala Galmee"]).size().reset_index(name="Baay'ina")
        )
      else:
        st.info("Deetaan hin jiru.")

    with tabI:
      st.markdown("### I. Gabaasa Galmee Waligalaa Bara 2019 (Karoora vs Raawwii)")
      # Mapping target vs actual execution summary table
      perf_data = []
      for k in range(1, 13):
        k_str = str(k)
        t_d = st.session_state.targets[k_str]["Dhiira"]
        t_dh = st.session_state.targets[k_str]["Dhalaa"]
        t_tot = t_d + t_dh

        r_d = (
            len(db[(db["Kutaa"] == k_str) & (db["Koorniyaa"] == "Dhiira")])
            if not db.empty
            else 0
        )
        r_dh = (
            len(db[(db["Kutaa"] == k_str) & (db["Koorniyaa"] == "Dhalaa")])
            if not db.empty
            else 0
        )
        r_tot = r_d + r_dh

        p_d = (r_d / t_d * 100) if t_d > 0 else 0
        p_dh = (r_dh / t_dh * 100) if t_dh > 0 else 0
        p_tot = (r_tot / t_tot * 100) if t_tot > 0 else 0

        perf_data.append({
            "Kutaa": f"Kutaa {k}",
            "Karoora Dhiira": t_d,
            "Karoora Dhalaa": t_dh,
            "Karoora Waligalaa": t_tot,
            "Raawwii Dhiira": r_d,
            "Raawwii Dhalaa": r_dh,
            "Raawwii Waligalaa": r_tot,
            "% Dhiira": round(p_d, 1),
            "% Dhalaa": round(p_dh, 1),
            "% Waligalaa": round(p_tot, 1),
        })
      st.dataframe(pd.DataFrame(perf_data))

    with tabJ:
      st.markdown("### J. Edit / Delete Data Barattootaa")
      if not db.empty:
        idx_to_modify = st.number_input(
            "Lakk. Index Barataa jijjiiruu/haquu barbaadde (0 irraa eegala)",
            min_value=0,
            max_value=max(0, len(db) - 1),
            step=1,
        )
        st.write(db.iloc[idx_to_modify])

        col_del, col_edit = st.columns(2)
        if col_del.button("🗑️ Barataa Kana Haquu (Delete)"):
          st.session_state.students_db = db.drop(idx_to_modify).reset_index(
              drop=True
          )
          st.success("Deetaan barataa haqameera!")
          st.rerun()
      else:
        st.info("Deetaan jijjiiramu hin jiru.")

  elif password != "":
    st.error("Password sirrii miti! Irra deebi'ii yaali.")
File "/mount/src/galmee-barataa/Lati.py", line 157

b_ji'a = b_col2.selectbox(

^

SyntaxError: unterminated string literal (detected at line 157)

Kooddii armaan olii keessatti dogoggorri SyntaxError (unterminated string literal) uumameef sababni jecha Afaan Oromoo keessatti mallattoo ciccitaa ykn apostrophe (') fayyadamne (fkn: b_ji'a) jechuun Python keessatti string cufuuf itti fayyadamamtiif walitti buutuufi.

Rakkoo kana sirreesuuf, qubee ji'a jedhu keessaa mallattoo san baasuun ykn backslash itti fayyadamuun qajeelchuu qabda. Kunoo kooddii sirreeffame bifa guutuu ta'een bakka kanaatti galchuu dandeessa:

Python
from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="App Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Styling (Border, Background, Colors, Font size & styles)
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

# Session State Initialization for Database & Targets
if "students_db" not in st.session_state:
  st.session_state.students_db = pd.DataFrame(
      columns=[
          "Maqaa Guutuu",
          "Koorniyaa",
          "Kutaa",
          "Bara Dhalootaa",
          "Umurii",
          "Haala Galmee",
          "Bara Addaan Kute",
          "Haala Maatii",
          "Miidhama Qaamaa",
          "Gosa Miidhamaa",
          "Bakka Dhalootaa (Godina/Aanaa/Ganda)",
          "Maqaa Haadhaa/Guddistuu",
          "FAN ID",
          "Lakk Bilbila Barataa",
          "Lakk Bilbila Maatii",
          "M/B Duraan Itti Barachaa Ture",
          "Avireejjii Qabxii",
          "Guyyaa Galmee",
          "Barsiisaa Galmeessee",
      ]
  )

if "targets" not in st.session_state:
  st.session_state.targets = {
      str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)
  }

# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown("### 🏫 Mana Barumsaa B/saa Kitesa Negasa")
menu = st.sidebar.selectbox(
    "Filannoo Fuulaa (Navigation)",
    [
        "1. Cover Page",
        "2. Dashboard Galmee Barataa (Foomii)",
        "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)",
    ],
)

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

# ----------------- 2. DASHBOARD GALMEE BARATAA (FOOMII) -----------------
elif menu == "2. Dashboard Galmee Barataa (Foomii)":
  st.subheader("📝 Foomii Galmee Barattootaa Haaraa")

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa")
      koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])
      kutaa = st.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])

      st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**")
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
      b_jiia = b_col2.selectbox(
          "Ji'a",
          [
              "Meskerem",
              "Tikimt",
              "Hidar",
              "Tahsas",
              "Tir",
              "Yekatit",
              "Megabit",
              "Meyazia",
              "Genbot",
              "Sene",
              "Hamle",
              "Nehase",
              "Pagume",
          ],
      )
      b_bara = b_col3.number_input(
          "Bara Dhalootaa (Fkn: 2005)", min_value=1980, max_value=2025, value=2010
      )
      current_et_year = 2018
      umurii = current_et_year - b_bara

      haala_galmee = st.selectbox(
          "5. Haala Galmee",
          [
              "Haaraa",
              "Irra deebii (Kufe)",
              "Irra deebii (Kute)",
              "Mana Barumsaa Biroo",
          ],
      )
      bara_addaan_kute = (
          st.selectbox(
              "Bara Addaan Kute (Yoo jiraate)",
              ["Hin jiru", "2005", "2006", "2007", "2008", "2009", "2010"]
              + [str(y) for y in range(2011, 2027)],
          )
          if "deebii" in haala_galmee
          else "Hin jiru"
      )

      haala_maatii = st.selectbox(
          "6. Haala Maatii",
          ["Lachuu qaba", "Abbaa qofa", "Haadha qofa", "Lachuu hin qabu"],
      )
      miidhama_qaamaa = st.selectbox(
          "7. Haala Miidhama Qaamaa", ["Hin jiru", "Jira"]
      )
      gosa_miidhamaa = (
          st.selectbox(
              "Gosa Miidhama Qaamaa",
              [
                  "Arguu salphaa",
                  "Arguu cimaa",
                  "Dhageettii salphaa",
                  "Dhageettii cimaa",
                  "Sochii harkaa salphaa",
                  "Sochii harkaa cimaa",
                  "Sochii miilaa salphaa",
                  "Sochii miilaa cimaa",
                  "Rakkoo dubbii salphaa",
                  "Rakkoo dubbii cimaa",
                  "Saaleessa sammuu",
                  "Currisa hawaasummaa",
              ],
          )
          if miidhama_qaamaa == "Jira"
          else "Hin jiru"
      )

    with col2:
      bakka_dhalootaa = st.text_input(
          "8. Bakka Dhalootaa (Godina, Aanaa, Ganda)"
      )
      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID)")
      lakk_bilbila_barataa = st.text_input("11. Lakkoofsa Bilbila Barataa")
      lakk_bilbila_maatii = st.text_input("12. Lakkoofsa Bilbila Maatii")
      mb_duraan = st.text_input("13. Mana Barumsaa Duraan Itti Barachaa Ture")

      avireejjii = st.number_input(
          "14. Avireejjii Qabxii Bara Darbee (0 - 100)",
          min_value=0.0,
          max_value=100.0,
          value=75.0,
      )

      if avireejjii < 50:
        st.markdown(
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu qaba!</p>',
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee")
      guyyaa_galmee = str(datetime.now().date())

    submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
      if not maqaa_guutuu or not fan_id:
        st.error("Maaloo Maqaa Guutuu fi FAN ID guuti!")
      else:
        new_data = {
            "Maqaa Guutuu": maqaa_guutuu,
            "Koorniyaa": koorniyaa,
            "Kutaa": kutaa,
            "Bara Dhalootaa": f"{b_guyyaa}/{b_jiia}/{b_bara}",
            "Umurii": umurii,
            "Haala Galmee": haala_galmee,
            "Bara Addaan Kute": bara_addaan_kute,
            "Haala Maatii": haala_maatii,
            "Miidhama Qaamaa": miidhama_qaamaa,
            "Gosa Miidhamaa": gosa_miidhamaa,
            "Bakka Dhalootaa (Godina/Aanaa/Ganda)": bakka_dhalootaa,
            "Maqaa Haadhaa/Guddistuu": maqaa_haadhaa,
            "FAN ID": fan_id,
            "Lakk Bilbila Barataa": lakk_bilbila_barataa,
            "Lakk Bilbila Maatii": lakk_bilbila_maatii,
            "M/B Duraan Itti Barachaa Ture": mb_duraan,
            "Avireejjii Qabxii": avireejjii,
            "Guyyaa Galmee": guyyaa_galmee,
            "Barsiisaa Galmeessee": barsiisaa,
        }
        st.session_state.students_db = pd.concat(
            [st.session_state.students_db, pd.DataFrame([new_data])],
            ignore_index=True,
        )
        st.success(
            f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!"
        )

# ----------------- 3. DASHBOARD BARSIIKAA / GABAASAA (PASSWORD PROTECTED) -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)":
  st.subheader("🔐 Dashboard Barsiisaa (Seensa Eeyyamame)")

  password = st.text_input("Password Galchi", type="password")

  if password == "kitesa2019" or password == "admin123":
    st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa.")

    tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
        [
            "A. Karoora",
            "B. Guutuu (Excel)",
            "C. Guyyaa (Kutaa 1)",
            "D. Lakkoofsaa",
            "E. Miidhamaa (Detail)",
            "F. Miidhamaa (Count)",
            "G. Irra-Deebii (Detail)",
            "H. Irra-Deebii (Count)",
            "I. Gabaasa 2019",
            "J. Edit/Delete",
        ]
    )

    db = st.session_state.students_db

    with tabA:
      st.markdown("### A. Guca Karoora Galmee Barataa 2019")
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

    with tabB:
      st.markdown("### B. Guca Gabaasaa Waligalaa Barataa (Excel Download)")
      if not db.empty:
        st.dataframe(db)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
        st.download_button(
            label="📥 Excel-tti Download Gochuu",
            data=buffer.getvalue(),
            file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
      else:
        st.info("Deetaan galmaa'e hin jiru.")

    with tabC:
      st.markdown("### C. Guca Gabaasaa Galmee Guyyaa (Kutaa 1, Umurii 7)")
      if not db.empty:
        filtered_c = db[(db["Kutaa"] == "1") & (db["Umurii"] == 7)]
        st.write(f"Baay'ina Barattoota Kutaa 1 (Umurii 7): {len(filtered_c)}")
        st.dataframe(filtered_c)
      else:
        st.info("Deetaan hin jiru.")

    with tabD:
      st.markdown(
          "### D. Gabaasa Lakkoofsaa Kutaa, Saalaa fi Umuriin (Fkn Umurii 7 +"
          " Kutaa 1)"
      )
      if not db.empty:
        summary_d = (
            db.groupby(["Kutaa", "Umurii", "Koorniyaa"])
            .size()
            .reset_index(name="Baay'ina")
        )
        st.dataframe(summary_d)
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown(
          "### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii (Odeeffannoo"
          " Guutuu)"
      )
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(disabled_df)
      else:
        st.info("Deetaan hin jiru.")

    with tabF:
      st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa & Haala Maatii")
      if not db.empty:
        st.write("**Miidhama Qaamaa Gosaan:**")
        st.dataframe(
            db[db["Miidhama Qaamaa"] == "Jira"]["Gosa Miidhamaa"].value_counts()
        )
        st.write("**Haala Maatii (Lachuu hin qabne dabalatee):**")
        st.dataframe(db["Haala Maatii"].value_counts())

    with tabG:
      st.markdown(
          "### G. Gabaasa Barattoota Irra Deebi'anii (Maqaa, Saala, Kutaa,"
          " Sababa)"
      )
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(repeat_df[
            [
                "Maqaa Guutuu",
                "Koorniyaa",
                "Kutaa",
                "Haala Galmee",
                "Bara Addaan Kute",
            ]
        ])
      else:
        st.info("Deetaan hin jiru.")

    with tabH:
      st.markdown(
          "### H. Gabaasa Lakkoofsaa Barattoota Irra Deebi'anii (Kutaa &"
          " Saalaan)"
      )
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(
            repeat_df.groupby(["Kutaa", "Koorniyaa", "Haala Galmee"])
            .size()
            .reset_index(name="Baay'ina")
        )
      else:
        st.info("Deetaan hin jiru.")

    with tabI:
      st.markdown("### I. Gabaasa Galmee Waligalaa Bara 2019 (Karoora vs Raawwii)")
      perf_data = []
      for k in range(1, 13):
        k_str = str(k)
        t_d = st.session_state.targets[k_str]["Dhiira"]
        t_dh = st.session_state.targets[k_str]["Dhalaa"]
        t_tot = t_d + t_dh

        r_d = (
            len(db[(db["Kutaa"] == k_str) & (db["Koorniyaa"] == "Dhiira")])
            if not db.empty
            else 0
        )
        r_dh = (
            len(db[(db["Kutaa"] == k_str) & (db["Koorniyaa"] == "Dhalaa")])
            if not db.empty
            else 0
        )
        r_tot = r_d + r_dh

        p_d = (r_d / t_d * 100) if t_d > 0 else 0
        p_dh = (r_dh / t_dh * 100) if t_dh > 0 else 0
        p_tot = (r_tot / t_tot * 100) if t_tot > 0 else 0

        perf_data.append({
            "Kutaa": f"Kutaa {k}",
            "Karoora Dhiira": t_d,
            "Karoora Dhalaa": t_dh,
            "Karoora Waligalaa": t_tot,
            "Raawwii Dhiira": r_d,
            "Raawwii Dhalaa": r_dh,
            "Raawwii Waligalaa": r_tot,
            "% Dhiira": round(p_d, 1),
            "% Dhalaa": round(p_dh, 1),
            "% Waligalaa": round(p_tot, 1),
        })
      st.dataframe(pd.DataFrame(perf_data))

    with tabJ:
      st.markdown("### J. Edit / Delete Data Barattootaa")
      if not db.empty:
        idx_to_modify = st.number_input(
            "Lakk. Index Barataa jijjiiruu/haquu barbaadde (0 irraa eegala)",
            min_value=0,
            max_value=max(0, len(db) - 1),
            step=1,
        )
        st.write(db.iloc[idx_to_modify])

        col_del, col_edit = st.columns(2)
        if col_del.button("🗑️ Barataa Kana Haquu (Delete)"):
          st.session_state.students_db = db.drop(idx_to_modify).reset_index(
              drop=True
          )
          st.success("Deetaan barataa haqameera!")
          st.rerun()
      else:
        st.info("Deetaan jijjiiramu hin jiru.")

  elif password != "":
    st.error("Password sirrii miti! Irra deebi'ii yaali.")
Wantoota sirreeffaman

1.dashboard barataa keessatti Haala galmee kan jedhutti,"Kan darbe"kan jedhu itti dabalta

2.daashboard barsiisaa keessatti bara adda kute (hin jiru) jedha garuu kan barataa keessatti bakki bara adda kute itti guutamu hin jiruu itti dabali

3.Haala miidhamaa qaamaa keessatti,filannoo" jiraa" dhiyaatu jalatti warreen kun haa galan(arguu salphaa,arguu cimaa,dhageettii salphaa,dhageettii cimaa,dubbii salphaa,dubbii cimaa,sochii salphaa,sochii cimaa,saaleessa sammuu,currisa hawaasumaa,Haadhaa fi abbaa dhabuu)kun galuu qaba.jiraa jalatti listi ta'anii dhiyaachuu qabu

4.ji'ootni Waggaa Afaan oromoon barreeffamuu qabu

5.Guyyaan galmee E.C barreeffamuu qaba fkn 2026 ,/01/08 osoo hin hin taanee 25/11/2018 ta'uu qaba.Maqaan mana barumsaa,Godinaa,Aanaa fi Gandaa yeroo Baayee walfakkatuu,kanaaf kan barataa hundaa ta'ee barreessurra yeroo godina barreessuf ka'e maqaa godina duran barra'e jiru akka ofii bakka taasisi

5,Kutaa itti Ansee Daree(section) itti Dabalii hanga(A,B,C,D,E,F,G,H,I,J,K)tti barreessi

Dasboard barsisaa immoo

1,karoora kan jedhu irratti Dhiira ,Dhalaa,Ida'ama) jechuu qaba ida'ama itti dabalai

2,akkasuma raw kutaalee jalatti kutaa 6 xumuree ida'ama kutaa 1-6 itti dabali,ammas raw 7,8 boodaa ida'ama 7-8,fi ida'ama 1-8, 9-12 karooraafis raawaais kaa'i

3.Gucni "C" irra jiruu guca gabaasa galmee guyyaa guyyaadhaan barataan galma'ee addatti gabaasaa deemuu jechuudha.fknf barataa kutaa 1 gaafa guyyaa 25/9/2018 galma'e dhiira 40 dubara 50 ida'ama 90 jedhe kutaa kutaan daata laakkofsa qofa fayyadamee qindeessa excel irratti jechuudha.inni kun kan guyyaa galme qofa ykn kan guyyaa tokkoo qofaa qabataa jechuudha

4.Kan"D irraa jiru immoo gbaasa Galmee Hanaga ammattii ykn waliglaa erga galmeen eegalee jechudha.kunis,qabiyyeen isaa,T/L,kutaa,dhiira, dubara ida'ama(kutaan 1,2,3,4,5,6,1-6,7,8,7-8,1-8

5.Guucni Gabaasa baratoota miidhama qaamaa qabanii kan "F" irra jiru maqaadhaan,warreen qaban sun,maqaa,saala,kutaa,umurii,Gosa miidhama qaama.qabaachuu qaba.kuni,dashboard bartaa sanaan waldubbisuu qaba.ragaa achirra fudhatee gabasa naaf kennu qaba

6.Gucni gabaasa barattoota irra deebi'anii "G" irra jiru (maqaadhan ,kutaa,saala,sababa irra deebi'ani(kufaatii,adda kutuun),bara irra deebi'ame) kun maqaa dabalatee jechhuudha

7.kAN " H " immoo Barattoota irra debi'ani lakkoofsa qofaan gabateen garuu kanini ibsu kutaa,Dhiira,dhalaa,ida'ama qinda'aa

8.Gabaasne galmee waligaalaa "I" irra jiru foormii karoora galmee sanaan walfakkatee garuu coloumn itti dabaltee kutaan,dhiira,dhalaa,ida,ama) raawwii Dhiira,Dhalaa,Ida'ama,parsantii raawwii dhiira,dhalaa,ida'ama karoora sanarra parsantii baasa,kanas guca koora sana fayyadamta fkn kutaa 1,2,3,4,5,6,1-6,7,8,7-8,1-8 ,9-12 akkasittin qinda'uu qaba

ragaan barataa galma'ee dogoggora yoo godhatee,edit,save fi delet ta'uu akka danda'utti dasboard qofaatti qopheessii kan odeeffannoo hunda barataa of keessati qabatu ta'e erga barataan save godhe achittimmoo debi'ani edt godhamu

Konowruu fi gaaffiiwwan keessan hunda irratti hundaa'uun Applikeeshinii Galmee Barattootaa fi Dashboardii Barsiisaa (Streamlit Python App) guutuu qopheesseera. Haala armaan gadiitiin sirreeffamni fi dabaliinsi taasifameera:

Dashboard Barataa (Foomii Galmee):

Haala galmee jalatti "Kan darbe" kan jedhu dabalameera.

Bara addaan kute (Hin jiru, ykn bara adda kute yeroo filatamu akka guutamu) dabaleera.

Haala miidhamaa qaamaa jalatti "Jira" yeroo filatamu gosti miidhamaa akka armaan gadiitti listii ta'ee dhufeera: (Arguu salphaa, arguu cimaa, dhageettii salphaa, dhageettii cimaa, dubbii salphaa, dubbii cimaa, sochii salphaa, sochii cimaa, saaleessa sammuu, currisa hawaasumaa, haadhaa fi abbaa dhabuu).

Ji'ootni waggaa Afaan Oromootiin (Fulbaana, Onkololeessa, Hacaaluu/Hidar, Tamsaasa/Tahsas, Amajjii, Guraandhala, Bitootessa, Ebla, Caamsaa, Waxabajjii, Aoleessa/Hamle, Hagayya, Pagume) dhiyaataniiru.

Guyyaan galmee Ethopian Calendar (E.C) akka bifa 25/11/2018 barreeffamu fooyya'eera. Godina, Aanaa fi Ganda irratti bifa default ta'een maqaa godina duraan barreeffame akka ofumaan qabatu taasifameera.

Kutaan itti ansee Dareen (Section) A, B, C, D, E, F, G, H, I, J, K hanga ta'etti filannoon dabalameera.

Ragaan barataa galmaa'e dogoggora yoo qabaate Edit, Save, fi Delete gochuun akka danda'amu Tab J jalatti guutummaatti qindaa'eera.

Dashboard Barsiisaa / Gabaasaa:

Guca A (Karoora): Dhiira, Dhalaa, fi Ida'ama of keessatti qabatee qindaa'eera.

Guca B (Excel): Gabaasa guutuu Excel-tti buusuuf dandeessisa.

Guca C (Guyyaa Tokkoo): Ragaa galmee guyyaa tokkoo qofa (fkn: gaafa 25/9/2018) qofaatiin lakkoofsa dhiira, dubara, ida'aman qindeessa.

Guca D (Waliigalaa / Hanga Ammaatti): Kutaa 1-6, 7-8, 1-8, 9-12 fi kkf ida'ama isaa waliin agarsiisa.

Guca E & F (Miidhama Qaamaa): Barattoota miidhama qaamaa qaban maqaa, saala, kutaa, umurii fi gosa miidhamaatiin qindeessuun dashboard barataa waliin walqunnamsiisa.

Guca G & H (Irra Deebii): Barattoota irra deebi'anii (kufaatii ykn addaan kutuun) maqaadhaan, akkasumas lakkoofsa qofaan kutaa, dhiira, dhalaa, ida'aman qindeessa.

Guca I (Gabaasa Waligalaa 2019): Karoora fi Raawwii walcinaa qabachuun Dhiira, Dhalaa, Ida'amaafi Parsantii (% raawwii) kutaa kutaan baasa.

Guca J (Edit / Delete / Update): Ragaa galmaa'e irratti dogoggora yoo jiraate yeroo barbaadameetti deebi'anii sirreessuu (Edit), save gochuu ykn haqchuu (Delete) ni dandeessisa.

Python Script (App) koodii guutuu qopheeffame kunoo kunoo kunooti:

Your Python file is ready
PY icon
app
 PY 
Open

File "/mount/src/galmee-barataa/Lati.py", line 9

Couldn't connect

^

SyntaxError: unterminated string literal (detected at line 9)

SyntaxError (unterminated string literal) kan uumameef sababa chatiin ykn kopshitoon kee yeroo koodii ergu "Couldn't connect" jedhu bifa sagalee (string) ykn ergaatiin koodii keessatti waan dabaleef. Python immoo mallattoo " ykn ' baneessee waan hin cufiniif rakkoo uuma.

Koodii guutuu kee keessaa sarara (line) 9 irratti rakkoon kun jira. Innis yeroo baayyee akkana ta'uu danda'a:

Akkamitti Sirreessuu Dandeenya?
File Lati.py (ykn app.py) keessii kee banatii sarara 9ffaa irra jiru sana balleessi (haqi). Ergasii koodii armaan olii siif dhihaate kana guutummaatti kopshitoo (copy) godhiitii galchi.

Yoo koodicha terminal irraa streamlit run Lati.py jechuun hojiirra oolchuu barbaaddus, fayila app.py jedhuun ykn maqaa duraan qabuuniin kuusuun ni danda'ama.

Ergan login system itti godhe,Gibee page malee daashboard barataa fi Gabaasa duraan qopha'ee naaf baasuu dideem

Rakkoon kun kan uumameef sababa Login System dabaltaniif caasaa st.sidebar.selectbox ykn if/elif logic fuulota (pages) irratti haguugamee ykn walirra buusee Dashboardiiwwan biroo dhoksuu isaatiini.

Rakkoo kana sirreessuuf, koodii kee keessatti Login System fi Sidebar Navigation walqixa akka qabatan fi barattoonnis ta'e barsiisonni akka itti danda'an taasisnee koodii guutuu fi qulqulluu armaan gadii siif qopheessineerra.

Koodii Sirraa'e (Copy godhiitii fayyadami):
Python
from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="App Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",
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

# Session State Initialization for Database & Targets
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

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False


# Helper function to get default location from existing db
def get_last_location(db, col_name):
  if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
    return db[col_name].dropna().iloc[-1]
  return ""


# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown("### 🏫 Mana Barumsaa B/saa Kitesa Negasa")
menu = st.sidebar.selectbox(
    "Filannoo Fuulaa (Navigation)",
    [
        "1. Cover Page",
        "2. Dashboard Galmee Barataa (Foomii)",
        "3. Dashboard Barsiisaa / Gabaasaa (Admin)",
    ],
)

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

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa")
      koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])

      grade_col1, grade_col2 = st.columns(2)
      kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
      daree = grade_col2.selectbox(
          "Daree (Section)", [chr(65 + i) for i in range(11)]
      )

      st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**")
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
      b_jiia = b_col2.selectbox(
          "Ji'a",
          [
              "Fulbaana",
              "Onkololeessa",
              "Hacaaluu/Hidar",
              "Tamsaasa/Tahsas",
              "Amajjii",
              "Guraandhala",
              "Bitootessa",
              "Ebla",
              "Caamsaa",
              "Waxabajjii",
              "Aoleessa/Hamle",
              "Hagayya",
              "Pagume",
          ],
      )
      b_bara = b_col3.number_input(
          "Bara Dhalootaa (Fkn: 2011)", min_value=1990, max_value=2025, value=2011
      )
      current_et_year = 2018
      umurii = current_et_year - b_bara

      haala_galmee = st.selectbox(
          "5. Haala Galmee",
          [
              "Haaraa",
              "Kan darbe",
              "Irra deebii (Kufe)",
              "Irra deebii (Kute)",
              "Mana Barumsaa Biroo",
          ],
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

      gosa_miidhamaa = (
          st.selectbox(
              "Gosa Miidhama Qaamaa / Haala Addaa",
              [
                  "Hin qabu",
                  "Arguu salphaa",
                  "Arguu cimaa",
                  "Dhageettii salphaa",
                  "Dhageettii cimaa",
                  "Dubbii salphaa",
                  "Dubbii cimaa",
                  "Sochii salphaa",
                  "Sochii cimaa",
                  "Saaleessa sammuu",
                  "Currisa hawaasummaa",
                  "Haadhaa fi abbaa dhabuu",
              ],
          )
          if miidhama_qaamaa == "Jira"
          else "Hin qabu"
      )

    with col2:
      st.markdown("**8. Bakka Dhalootaa**")
      godina = st.text_input("Godina", value=default_godina)
      aanaa = st.text_input("Aanaa", value=default_aanaa)
      ganda = st.text_input("Ganda", value=default_ganda)

      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID)")
      lakk_bilbila_barataa = st.text_input("11. Lakkoofsa Bilbila Barataa")
      lakk_bilbila_maatii = st.text_input("12. Lakkoofsa Bilbila Maatii")
      mb_duraan = st.text_input("13. Mana Barumsaa Duraan Itti Barachaa Ture")

      avireejjii = st.number_input(
          "14. Avireejjii Qabxii Bara Darbee (0 - 100)",
          min_value=0.0,
          max_value=100.0,
          value=75.0,
      )

      if avireejjii < 50:
        st.markdown(
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi'
            ' waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu'
            " qaba!</p>",
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee")
      guyyaa_galmee_ec = st.text_input(
          "Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018"
      )

    submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
      if not maqaa_guutuu or not fan_id:
        st.error("Maaloo Maqaa Guutuu fi FAN ID guuti!")
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
        st.success(
            f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!"
        )

# ----------------- 3. DASHBOARD BARSIIKAA / GABAASAA (PASSWORD PROTECTED) -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Admin)":
  st.subheader("🔐 Dashboard Barsiisaa (Seensa Eeyyamame)")

  if not st.session_state.logged_in:
    password = st.text_input("Password Galchi", type="password")
    if st.button("Seeni (Login)"):
      if password == "kitesa2019" or password == "admin123":
        st.session_state.logged_in = True
        st.rerun()
      else:
        st.error("Password sirrii miti! Irra deebi'ii yaali.")
  else:
    st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa.")
    if st.button("Ba'i (Logout)"):
      st.session_state.logged_in = False
      st.rerun()

    tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
        [
            "A. Karoora",
            "B. Guutuu (Excel)",
            "C. Guyyaa (Guyyaa Tokkoo)",
            "D. Waligalaa (Hanaga Ammaatti)",
            "E. Miidhamaa (Maqaa)",
            "F. Miidhamaa (Count)",
            "G. Irra-Deebii (Maqaa)",
            "H. Irra-Deebii (Count)",
            "I. Gabaasa Waligalaa 2019",
            "J. Edit/Delete Data",
        ]
    )

    db = st.session_state.students_db


    def get_grade_rows(df, grade_list):
      sub = df[df["Kutaa"].isin([str(g) for g in grade_list])]
      d_count = len(sub[sub["Koorniyaa"] == "Dhiira"])
      dh_count = len(sub[sub["Koorniyaa"] == "Dhalaa"])
      return d_count, dh_count, d_count + dh_count

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

      t_summary = []
      for k in range(1, 13):
        k_str = str(k)
        td = st.session_state.targets[k_str]["Dhiira"]
        tdh = st.session_state.targets[k_str]["Dhalaa"]
        t_summary.append(
            {"Kutaa": f"Kutaa {k}", "Dhiira": td, "Dhalaa": tdh, "Ida'ama": td + tdh}
        )
      st.dataframe(pd.DataFrame(t_summary))

    with tabB:
      st.markdown("### B. Guca Gabaasaa Waligalaa Barataa (Excel Download)")
      if not db.empty:
        st.dataframe(db)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
        st.download_button(
            label="📥 Excel-tti Download Gochuu",
            data=buffer.getvalue(),
            file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
      else:
        st.info("Deetaan galmaa'e hin jiru.")

    with tabC:
      st.markdown("### C. Gabaasa Galmee Guyyaa Tokkoo")
      if not db.empty:
        available_dates = db["Guyyaa Galmee (E.C)"].unique().tolist()
        selected_date = st.selectbox("Guyyaa Filadhu (E.C)", available_dates)
        day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]
        st.dataframe(day_df)
      else:
        st.info("Deetaan hin jiru.")

    with tabD:
      st.markdown("### D. Gabaasa Galmee Hanga Ammaatti")
      if not db.empty:
        summary_rows = []
        for k in range(1, 13):
          d, dh, tot = get_grade_rows(db, [k])
          summary_rows.append(
              {
                  "Kutaa": f"Kutaa {k}",
                  "Dhiira": d,
                  "Dhalaa": dh,
                  "Ida'ama": tot,
              }
          )
        st.dataframe(pd.DataFrame(summary_rows))
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown("### E. Gabaasa Barattoota Miidhama Qaamaa")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(disabled_df) if not disabled_df.empty else st.info(
            "Hin jiru."
        )
      else:
        st.info("Deetaan hin jiru.")

    with tabF:
      st.markdown("### F. Lakkoofsa Miidhama Qaamaa")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(
            disabled_df["Gosa Miidhamaa"].value_counts().reset_index(name="Baay'ina")
        ) if not disabled_df.empty else st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabG:
      st.markdown("### G. Barattoota Irra Deebi'anii")
      if not db.empty:
        repeat_df = db[
            db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)
        ]
        st.dataframe(repeat_df) if not repeat_df.empty else st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabH:
      st.markdown("### H. Lakkoofsa Irra Deebi'anii")
      if not db.empty:
        repeat_df = db[
            db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)
        ]
        if not repeat_df.empty:
          st.dataframe(
              repeat_df.groupby(["Kutaa", "Koorniyaa"])
              .size()
              .unstack(fill_value=0)
              .reset_index()
          )
        else:
          st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabI:
      st.markdown("### I. Gabaasa Waligalaa 2019 (Karoora vs Raawwii)")
      perf_data = []
      for k in range(1, 13):
        t_d = st.session_state.targets[str(k)]["Dhiira"]
        t_dh = st.session_state.targets[str(k)]["Dhalaa"]
        r_d, r_dh, r_tot = get_grade_rows(db, [k])
        perf_data.append(
            {
                "Kutaa": f"Kutaa {k}",
                "Karoora Dhiira": t_d,
                "Karoora Dhalaa": t_dh,
                "Raawwii Dhiira": r_d,
                "Raawwii Dhalaa": r_dh,
            }
        )
      st.dataframe(pd.DataFrame(perf_data))

    with tabJ:
      st.markdown("### J. Edit / Delete Data Barattootaa")
      if not db.empty:
        search_query = st.text_input("Maqaa barataa ykn FAN ID barressii:")
        filtered_edit = (
            db[
                db["Maqaa Guutuu"]
                .str.contains(search_query, case=False, na=False)
                | db["FAN ID"].str.contains(search_query, case=False, na=False)
            ]
            if search_query
            else db
        )
        if not filtered_edit.empty:
          selected_idx = st.selectbox(
              "Barataa jijjiiruf filadhu", filtered_edit.index.tolist()
          )
          row_data = db.loc[selected_idx]
          with st.form("edit_form"):
            new_maqaa = st.text_input(
                "Maqaa Guutuu", value=row_data["Maqaa Guutuu"]
            )
            new_kutaa = st.selectbox(
                "Kutaa",
                [str(i) for i in range(1, 13)],
                index=int(row_data["Kutaa"]) - 1,
            )
            do_update = st.form_submit_button("🔄 Update")
            do_delete = st.form_submit_button("🗑️ Delete")
            if do_update:
              st.session_state.students_db.at[selected_idx, "Maqaa Guutuu"] = (
                  new_maqaa
              )
              st.session_state.students_db.at[selected_idx, "Kutaa"] = new_kutaa
              st.success("Updated successfully!")
              st.rerun()
            if do_delete:
              st.session_state.students_db = db.drop(selected_idx).reset_index(
                  drop=True
              )
              st.success("Deleted successfully!")
              st.rerun()
        else:
          st.info("Hin argamne.")
      else:
        st.info("Deetaan hin jiru.")
Guutummaan koodiichaa kana kanaaf akka inni qabiyyee daashboard barataa fi Gabaasa keessa jiru mullisu gidhi

Koodii guutuu fi sirrii ta'e, kan fuula jalqabaa (Cover Page), foomii galmee barataa (Dashboard Galmee Barataa), akkasumas daashboardii barsiisaa (Gabaasota fi Karoora hunda) sirriitti walqabsiisee qabatamaan hojjetu kunooti:

Python
from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="App Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",
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

# Session State Initialization for Database & Targets
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

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False


# Helper function to get default location from existing db
def get_last_location(db, col_name):
  if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
    return db[col_name].dropna().iloc[-1]
  return ""


# ----------------- NAVIGATION / PAGES -----------------
st.sidebar.markdown("### 🏫 Mana Barumsaa B/saa Kitesa Negasa")
menu = st.sidebar.selectbox(
    "Filannoo Fuulaa (Navigation)",
    [
        "1. Cover Page",
        "2. Dashboard Galmee Barataa (Foomii)",
        "3. Dashboard Barsiisaa / Gabaasaa (Admin)",
    ],
)

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

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa")
      koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])

      grade_col1, grade_col2 = st.columns(2)
      kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
      daree = grade_col2.selectbox(
          "Daree (Section)", [chr(65 + i) for i in range(11)]
      )

      st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**")
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
      b_jiia = b_col2.selectbox(
          "Ji'a",
          [
              "Fulbaana",
              "Onkololeessa",
              "Hacaaluu/Hidar",
              "Tamsaasa/Tahsas",
              "Amajjii",
              "Guraandhala",
              "Bitootessa",
              "Ebla",
              "Caamsaa",
              "Waxabajjii",
              "Aoleessa/Hamle",
              "Hagayya",
              "Pagume",
          ],
      )
      b_bara = b_col3.number_input(
          "Bara Dhalootaa (Fkn: 2011)", min_value=1990, max_value=2025, value=2011
      )
      current_et_year = 2018
      umurii = current_et_year - b_bara

      haala_galmee = st.selectbox(
          "5. Haala Galmee",
          [
              "Haaraa",
              "Kan darbe",
              "Irra deebii (Kufe)",
              "Irra deebii (Kute)",
              "Mana Barumsaa Biroo",
          ],
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

      gosa_miidhamaa = (
          st.selectbox(
              "Gosa Miidhama Qaamaa / Haala Addaa",
              [
                  "Hin qabu",
                  "Arguu salphaa",
                  "Arguu cimaa",
                  "Dhageettii salphaa",
                  "Dhageettii cimaa",
                  "Dubbii salphaa",
                  "Dubbii cimaa",
                  "Sochii salphaa",
                  "Sochii cimaa",
                  "Saaleessa sammuu",
                  "Currisa hawaasummaa",
                  "Haadhaa fi abbaa dhabuu",
              ],
          )
          if miidhama_qaamaa == "Jira"
          else "Hin qabu"
      )

    with col2:
      st.markdown("**8. Bakka Dhalootaa**")
      godina = st.text_input("Godina", value=default_godina)
      aanaa = st.text_input("Aanaa", value=default_aanaa)
      ganda = st.text_input("Ganda", value=default_ganda)

      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID)")
      lakk_bilbila_barataa = st.text_input("11. Lakkoofsa Bilbila Barataa")
      lakk_bilbila_maatii = st.text_input("12. Lakkoofsa Bilbila Maatii")
      mb_duraan = st.text_input("13. Mana Barumsaa Duraan Itti Barachaa Ture")

      avireejjii = st.number_input(
          "14. Avireejjii Qabxii Bara Darbee (0 - 100)",
          min_value=0.0,
          max_value=100.0,
          value=75.0,
      )

      if avireejjii < 50:
        st.markdown(
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi'
            ' waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu'
            " qaba!</p>",
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee")
      guyyaa_galmee_ec = st.text_input(
          "Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018"
      )

    submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
      if not maqaa_guutuu or not fan_id:
        st.error("Maaloo Maqaa Guutuu fi FAN ID guuti!")
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
        st.success(
            f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!"
        )

# ----------------- 3. DASHBOARD BARSIIKAA / GABAASAA (PASSWORD PROTECTED) -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Admin)":
  st.subheader("🔐 Dashboard Barsiisaa (Seensa Eeyyamame)")

  if not st.session_state.logged_in:
    password = st.text_input("Password Galchi", type="password")
    if st.button("Seeni (Login)"):
      if password == "kitesa2019" or password == "admin123":
        st.session_state.logged_in = True
        st.rerun()
      else:
        st.error("Password sirrii miti! Irra deebi'ii yaali.")
  else:
    st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa.")
    if st.button("Ba'i (Logout)"):
      st.session_state.logged_in = False
      st.rerun()

    tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
        [
            "A. Karoora",
            "B. Guutuu (Excel)",
            "C. Guyyaa (Guyyaa Tokkoo)",
            "D. Waligalaa (Hanaga Ammaatti)",
            "E. Miidhamaa (Maqaa)",
            "F. Miidhamaa (Count)",
            "G. Irra-Deebii (Maqaa)",
            "H. Irra-Deebii (Count)",
            "I. Gabaasa Waligalaa 2019",
            "J. Edit/Delete Data",
        ]
    )

    db = st.session_state.students_db


    def get_grade_rows(df, grade_list):
      sub = df[df["Kutaa"].isin([str(g) for g in grade_list])]
      d_count = len(sub[sub["Koorniyaa"] == "Dhiira"])
      dh_count = len(sub[sub["Koorniyaa"] == "Dhalaa"])
      return d_count, dh_count, d_count + dh_count

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

      t_summary = []
      for k in range(1, 13):
        k_str = str(k)
        td = st.session_state.targets[k_str]["Dhiira"]
        tdh = st.session_state.targets[k_str]["Dhalaa"]
        t_summary.append(
            {"Kutaa": f"Kutaa {k}", "Dhiira": td, "Dhalaa": tdh, "Ida'ama": td + tdh}
        )
      st.dataframe(pd.DataFrame(t_summary))

    with tabB:
      st.markdown("### B. Guca Gabaasaa Waligalaa Barataa (Excel Download)")
      if not db.empty:
        st.dataframe(db)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
        st.download_button(
            label="📥 Excel-tti Download Gochuu",
            data=buffer.getvalue(),
            file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
      else:
        st.info("Deetaan galmaa'e hin jiru.")

    with tabC:
      st.markdown("### C. Gabaasa Galmee Guyyaa Tokkoo")
      if not db.empty:
        available_dates = db["Guyyaa Galmee (E.C)"].unique().tolist()
        selected_date = st.selectbox("Guyyaa Filadhu (E.C)", available_dates)
        day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]
        st.dataframe(day_df)
      else:
        st.info("Deetaan hin jiru.")

    with tabD:
      st.markdown("### D. Gabaasa Galmee Hanga Ammaatti")
      if not db.empty:
        summary_rows = []
        for k in range(1, 13):
          d, dh, tot = get_grade_rows(db, [k])
          summary_rows.append(
              {
                  "Kutaa": f"Kutaa {k}",
                  "Dhiira": d,
                  "Dhalaa": dh,
                  "Ida'ama": tot,
              }
          )
        st.dataframe(pd.DataFrame(summary_rows))
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown("### E. Gabaasa Barattoota Miidhama Qaamaa")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(disabled_df) if not disabled_df.empty else st.info(
            "Hin jiru."
        )
      else:
        st.info("Deetaan hin jiru.")

    with tabF:
      st.markdown("### F. Lakkoofsa Miidhama Qaamaa")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(
            disabled_df["Gosa Miidhamaa"].value_counts().reset_index(name="Baay'ina")
        ) if not disabled_df.empty else st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabG:
      st.markdown("### G. Barattoota Irra Deebi'anii")
      if not db.empty:
        repeat_df = db[
            db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)
        ]
        st.dataframe(repeat_df) if not repeat_df.empty else st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabH:
      st.markdown("### H. Lakkoofsa Irra Deebi'anii")
      if not db.empty:
        repeat_df = db[
            db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)
        ]
        if not repeat_df.empty:
          st.dataframe(
              repeat_df.groupby(["Kutaa", "Koorniyaa"])
              .size()
              .unstack(fill_value=0)
              .reset_index()
          )
        else:
          st.info("Hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabI:
      st.markdown("### I. Gabaasa Waligalaa 2019 (Karoora vs Raawwii)")
      perf_data = []
      for k in range(1, 13):
        t_d = st.session_state.targets[str(k)]["Dhiira"]
        t_dh = st.session_state.targets[str(k)]["Dhalaa"]
        r_d, r_dh, r_tot = get_grade_rows(db, [k])
        perf_data.append(
            {
                "Kutaa": f"Kutaa {k}",
                "Karoora Dhiira": t_d,
                "Karoora Dhalaa": t_dh,
                "Raawwii Dhiira": r_d,
                "Raawwii Dhalaa": r_dh,
            }
        )

            with tabEdit:
                st.markdown("### ✏️ Sirreeffama (Edit) ykn Haquu (Delete) Deetaa Barattootaa")
                if not db.empty:
                    student_names = db["Maqaa Guutuu"].tolist()
                    selected_student = st.selectbox("Barataa Sirreessuu ykn Haquu barbaaddu filadhu", student_names)
                    
                    student_row = db[db["Maqaa Guutuu"] == selected_student].iloc[0]
                    idx = db[db["Maqaa Guutuu"] == selected_student].index[0]

                    with st.form("edit_student_form"):
                        e_name = st.text_input("Maqaa Guutuu", value=student_row["Maqaa Guutuu"])
                        e_grade = st.selectbox("Kutaa", [str(i) for i in range(1, 13)], index=int(student_row["Kutaa"])-1)
                        e_gender = st.selectbox("Koorniyaa", ["Dhiira", "Dhalaa"], index=0 if student_row["Koorniyaa"] == "Dhiira" else 1)
                        e_phone = st.text_input("Lakk Bilbila Barataa", value=student_row["Lakk Bilbila Barataa"])
                        
                        col_update, col_delete = st.columns(2)
                        update_btn = col_update.form_submit_button("💾 Jijjiirama Save Gochuu")
                        delete_btn = col_delete.form_submit_button("🗑️ Barataa Kana Haquu (Delete)")

                        if update_btn:
                            st.session_state.students_db.at[idx, "Maqaa Guutuu"] = e_name
                            st.session_state.students_db.at[idx, "Kutaa"] = e_grade
                            st.session_state.students_db.at[idx, "Koorniyaa"] = e_gender
                            st.session_state.students_db.at[idx, "Lakk Bilbila Barataa"] = e_phone
                            st.success(f"Odeeffannoon barataa {e_name} milkaa'inaan haaromfameera (Updated)!")
                            st.rerun()

                        if delete_btn:
                            st.session_state.students_db = st.session_state.students_db.drop(idx).reset_index(drop=True)
                            st.warning(f"Barataan {selected_student} galmee keessaa haqameera!")
                            st.rerun()
                else:
                    st.info("Deetaan barataa galmaa'e hin jiru.")                                                     
