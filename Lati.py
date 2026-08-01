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

def get_last_location(db, col_name):
    if not db.empty and col_name in db.columns and len(db[col_name].dropna()) > 0:
        return db[col_name].dropna().iloc[-1]
    return ""

def get_grade_rows(df, grade_list):
    sub = df[df["Kutaa"].isin([str(g) for g in grade_list])]
    d_count = len(sub[sub["Koorniyaa"] == "Dhiira"])
    dh_count = len(sub[sub["Koorniyaa"] == "Dhalaa"])
    return d_count, dh_count, d_count + dh_count

def generate_grouped_report(data_rows, title_col_name="Kutaa"):
    # Groupings: 1-6, 7-8, 1-8, 9-12, and Total (1-12)
    rows_1_6_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)
    rows_1_6_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) <= 6)
    
    rows_7_8_d = sum(r["Dhiira"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)
    rows_7_8_dh = sum(r["Dhalaa"] for r in data_rows if 7 <= int(r["Kutaa_Num"]) <= 8)
    
    rows_9_12_d = sum(r["Dhiira"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)
    rows_9_12_dh = sum(r["Dhalaa"] for r in data_rows if int(r["Kutaa_Num"]) >= 9)

    final_table = []
    
    # 1 to 6
    for r in data_rows:
        if int(r["Kutaa_Num"]) <= 6:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 1 - 6", "Dhiira": rows_1_6_d, "Dhalaa": rows_1_6_dh, "Ida'ama": rows_1_6_d + rows_1_6_dh})
    
    # 7 to 8
    for r in data_rows:
        if 7 <= int(r["Kutaa_Num"]) <= 8:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 7 - 8", "Dhiira": rows_7_8_d, "Dhalaa": rows_7_8_dh, "Ida'ama": rows_7_8_d + rows_7_8_dh})
    
    # Ida'ama 1 - 8
    final_table.append({title_col_name: "Ida'ama Waliigalaa (1 - 8)", "Dhiira": rows_1_6_d + rows_7_8_d, "Dhalaa": rows_1_6_dh + rows_7_8_dh, "Ida'ama": (rows_1_6_d + rows_7_8_d) + (rows_1_6_dh + rows_7_8_dh)})

    # 9 to 12
    for r in data_rows:
        if int(r["Kutaa_Num"]) >= 9:
            final_table.append({title_col_name: r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
    final_table.append({title_col_name: "Ida'ama Kutaa 9 - 12", "Dhiira": rows_9_12_d, "Dhalaa": rows_9_12_dh, "Ida'ama": rows_9_12_d + rows_9_12_dh})

    # Ida'ama Waliigalaa (1 - 12)
    tot_d = rows_1_6_d + rows_7_8_d + rows_9_12_d
    tot_dh = rows_1_6_dh + rows_7_8_dh + rows_9_12_dh
    final_table.append({title_col_name: "Waliigalaa (1 - 12)", "Dhiira": tot_d, "Dhalaa": tot_dh, "Ida'ama": tot_d + tot_dh})

    return pd.DataFrame(final_table)

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

            maqaa_haadhaa = st.text_input("10. Maqaa Guutuu Haadhaa ykn Guddistuu")
            fan_id = st.text_input("11. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID) - Dirqama miti")
            lakk_bilbila_barataa = st.text_input("12. Lakkoofsa Bilbila Barataa")
            lakk_bilbila_maatii = st.text_input("13. Lakkoofsa Bilbila Maatii")
            mb_duraan = st.text_input("14. Mana Barumsaa Duraan Itti Barachaa Ture")

            avireejjii = st.number_input(
                "15. Avireejjii Qabxii Bara Darbee (0 - 100)",
                min_value=0.0, max_value=100.0, value=75.0,
            )

            if avireejjii < 50:
                st.markdown(
                    '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu qaba!</p>',
                    unsafe_allow_html=True,
                )

            barsiisaa = st.text_input("16. Barsiisaa Galmeessee")
            guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018")

        submitted = st.form_submit_button("💾 Save (Enter)")

        if submitted:
            if not maqaa_guutuu:
                st.error("Maaloo Maqaa Guutuu barataa guuti!")
            else:
                # Duplicate Check Rule (Rule 3)
                existing_df = st.session_state.students_db
                duplicate_found = False
                if not existing_df.empty:
                    # Check by exact name match and grade
                    match_name = existing_df["Maqaa Guutuu"].str.strip().str.lower() == maqaa_guutuu.strip().lower()
                    match_grade = existing_df["Kutaa"] == kutaa
                    if fan_id.strip():
                        match_fan = existing_df["FAN ID"].str.strip().str.lower() == fan_id.strip().lower()
                        duplicate_found = ((match_name & match_grade) | (match_fan & (existing_df["FAN ID"] != ""))).any()
                    else:
                        duplicate_found = (match_name & match_grade).any()

                if duplicate_found:
                    st.error(f"⚠️ Galmawwiin hin danda'amne! Barataan '{maqaa_guutuu}' Kutaa {kutaa} keessatti duraanuu galmaa'eera (2 yeroo ta'uuf hin hayyamamu)!")
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

            # Download/Print Target Excel
            buffer_t = io.BytesIO()
            with pd.ExcelWriter(buffer_t, engine="openpyxl") as writer:
                target_df.to_excel(writer, sheet_name="Karoora_Galmee", index=False)
            st.download_button(
                label="📥 Karoora Excel-tti Download / Print Gochuu",
                data=buffer_t.getvalue(),
                file_name="Karoora_Galmee_Barattootaa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        with tabB:
            st.markdown("### B. Guca Gabaasaa Waligalaa Barataa (Excel Download)")
            if not db.empty:
                st.dataframe(db, use_container_width=True)
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
                st.download_button(
                    label="📥 Gabaasa Guutuu Excel-tti Download / Print Gochuu",
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
                selected_date = st.selectbox("Guyyaa Filadhu (E.C)", available_dates)
                day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]
                st.dataframe(day_df, use_container_width=True)

                buffer_c = io.BytesIO()
                with pd.ExcelWriter(buffer_c, engine="openpyxl") as writer:
                    day_df.to_excel(writer, sheet_name="Gabaasa_Guyyaa", index=False)
                st.download_button(
                    label="📥 Gabaasa Guyyaa Kanaa Excel-tti Download / Print",
                    data=buffer_c.getvalue(),
                    file_name=f"Gabaasa_Guyyaa_{selected_date.replace('/', '-')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("Deetaan hin jiru.")

        with tabD:
            st.markdown("### D. Gabaasa Galmee Hanga Ammaatti")
            if not db.empty:
                raw_summary = []
                for k in range(1, 13):
                    d, dh, tot = get_grade_rows(db, [k])
                    raw_summary.append({
                        "Kutaa_Num": str(k),
                        "Kutaa": f"Kutaa {k}",
                        "Dhiira": d,
                        "Dhalaa": dh,
                        "Ida'ama": tot
                    })
                summary_df = generate_grouped_report(raw_summary, title_col_name="Kutaa")
                st.dataframe(summary_df, use_container_width=True)

                buffer_d = io.BytesIO()
                with pd.ExcelWriter(buffer_d, engine="openpyxl") as writer:
                    summary_df.to_excel(writer, sheet_name="Gabaasa_Hanga_Ammaa", index=False)
                st.download_button(
                    label="📥 Gabaasa Hanga Ammaa Excel-tti Download / Print",
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
                        label="📥 Barattoota Miidhama Qaamaa Excel-tti Download",
                        data=buffer_e.getvalue(),
                        file_name="Barattoota_Miidhama_Qaamaa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan miidhama qaamaa qabu hin galmoofne.")

        with tabF:
            st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa")
            if not db.empty:
                disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
                if not disabled_df.empty:
                    count_df = disabled_df["Gosa Miidhamaa"].value_counts().reset_index(name="Baay'ina")
                    st.dataframe(count_df, use_container_width=True)

                    buffer_f = io.BytesIO()
                    with pd.ExcelWriter(buffer_f, engine="openpyxl") as writer:
                        count_df.to_excel(writer, sheet_name="Lakkoofsa_Miidhamaa", index=False)
                    st.download_button(
                        label="📥 Lakkoofsa Miidhamaa Excel-tti Download",
                        data=buffer_f.getvalue(),
                        file_name="Lakkoofsa_Gosa_Miidhamaa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

        with tabG:
            st.markdown("### G. Gabaasa Barattoota Irra Deebi'anii")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
                if not repeat_df.empty:
                    st.dataframe(repeat_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Haala Galmee"]], use_container_width=True)
                    
                    buffer_g = io.BytesIO()
                    with pd.ExcelWriter(buffer_g, engine="openpyxl") as writer:
                        repeat_df.to_excel(writer, sheet_name="Irra_Deebii", index=False)
                    st.download_button(
                        label="📥 Barattoota Irra Deebii Excel-tti Download",
                        data=buffer_g.getvalue(),
                        file_name="Barattoota_Irra_Deebii.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("Barataan irra deebii galmaa'e hin jiru.")

        with tabH:
            st.markdown("### H. Gabaasa Lakkoofsaa Irra Deebii")
            if not db.empty:
                repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
                if not repeat_df.empty:
                    pivot_rep = repeat_df.groupby(["Kutaa", "Koorniyaa"]).size().unstack(fill_value=0).reset_index()
                    st.dataframe(pivot_rep, use_container_width=True)

                    buffer_h = io.BytesIO()
                    with pd.ExcelWriter(buffer_h, engine="openpyxl") as writer:
                        pivot_rep.to_excel(writer, sheet_name="Lakkoofsa_Irra_Deebii", index=False)
                    st.download_button(
                        label="📥 Lakkoofsa Irra Deebii Excel-tti Download",
                        data=buffer_h.getvalue(),
                        file_name="Lakkoofsa_Irra_Deebii.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

        with tabI:
            st.markdown("### I. Gabaasa Waligalaa 2019 (Karoora vs Raawwii)")
            perf_raw = []
            for k in range(1, 13):
                t_d = st.session_state.targets[str(k)]["Dhiira"]
                t_dh = st.session_state.targets[str(k)]["Dhalaa"]
                r_d, r_dh, r_tot = get_grade_rows(db, [k])
                perf_raw.append({
                    "Kutaa_Num": str(k),
                    "Kutaa": f"Kutaa {k}",
                    "Karoora Dhiira": t_d,
                    "Raawwii Dhiira": r_d,
                    "Karoora Dhalaa": t_dh,
                    "Raawwii Dhalaa": r_dh,
                    "Karoora Ida'ama": t_d + t_dh,
                    "Raawwii Ida'ama": r_tot
                })
            
            perf_df = pd.DataFrame(perf_raw)
            st.dataframe(perf_df, use_container_width=True)

            buffer_i = io.BytesIO()
            with pd.ExcelWriter(buffer_i, engine="openpyxl") as writer:
                perf_df.to_excel(writer, sheet_name="Karoora_vs_Raawwii", index=False)
            st.download_button(
                label="📥 Karoora vs Raawwii Excel-tti Download / Print",
                data=buffer_i.getvalue(),
                file_name="Karoora_vs_Raawwii_2019.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        with tabJ:
            st.markdown("### J. Edit / Delete / Update Data Barattootaa")
            if not db.empty:
                search_query = st.text_input("Maqaa barataa ykn FAN ID barressii barbaadi:")
                filtered_edit = db[db["Maqaa Guutuu"].str.contains(search_query, case=False, na=False) | db["FAN ID"].str.contains(search_query, case=False, na=False)] if search_query else db
                
                if not filtered_edit.empty:
                    selected_idx = st.selectbox("Barataa jijjiiruf filadhu (Index)", filtered_edit.index.tolist())
                    row_data = db.loc[selected_idx]
                    
                    with st.form("edit_form"):
                        new_maqaa = st.text_input("Maqaa Guutuu", value=row_data["Maqaa Guutuu"])
                        col_save_edit, col_del_edit = st.columns(2)
                        do_update = col_save_edit.form_submit_button("🔄 Update / Save")
                        do_delete = col_del_edit.form_submit_button("🗑️ Delete Barataa")

                        if do_update:
                            st.session_state.students_db.at[selected_idx, "Maqaa Guutuu"] = new_maqaa
                            st.success("Odeeffannoon barataa milkaa'inaan *Update* ta'eera!")
                            st.rerun()

                        if do_delete:
                            st.session_state.students_db = db.drop(selected_idx).reset_index(drop=True)
                            st.success("Barataan kun haqameera!")
                            st.rerun()

    elif password != "":
        st.error("Password sirrii miti! Irra deebi'ii yaali.")
