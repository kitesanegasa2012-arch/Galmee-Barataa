from datetime import datetime
import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Appii Galmee Barattootaa - B/saa Kitesa Negasa",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
        background-image:
            radial-gradient(circle at top right, rgba(78,115,223,0.08), transparent 45%),
            radial-gradient(circle at bottom left, rgba(28,200,138,0.08), transparent 45%);
    }

    /* ---------- Cover / Hero card ---------- */
    .cover-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 55%, #4e73df 100%);
        padding: 50px 40px;
        border-radius: 22px;
        border: 3px solid rgba(255,255,255,0.25);
        color: white;
        text-align: center;
        box-shadow: 0 12px 30px rgba(30,60,114,0.35);
    }
    .cover-card::before {
        content: "";
        position: absolute;
        top: -70px; right: -70px;
        width: 190px; height: 190px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .cover-card::after {
        content: "";
        position: absolute;
        bottom: -90px; left: -50px;
        width: 230px; height: 230px;
        background: rgba(255,255,255,0.07);
        border-radius: 50%;
    }
    .cover-card h1 {
        color: #ffffff !important;
        font-size: 2.5rem;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.25);
        margin-bottom: 6px;
    }
    .cover-card h3 {
        color: #eaf0ff !important;
        font-weight: 500;
        margin-top: 0;
    }
    .cover-card p {
        color: #dce4f7;
        font-size: 1.05rem;
        max-width: 720px;
        margin: 10px auto 0 auto;
    }
    .badge-row {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 18px;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    .badge-pill {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.35);
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.85rem;
        color: #ffffff;
    }

    /* ---------- Contact card ---------- */
    .contact-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #f6c23e 0%, #e8590c 100%);
        padding: 22px 30px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 8px 20px rgba(232,89,12,0.28);
        margin-top: 18px;
        border: 2px solid rgba(255,255,255,0.3);
    }
    .contact-card h3 {
        color: #ffffff !important;
        margin-top: 0;
        margin-bottom: 6px;
    }
    .contact-card p {
        color: #fff6ea;
        margin: 4px 0;
        font-size: 0.98rem;
    }
    .contact-card b { color: #ffffff; }

    /* ---------- Metric cards ---------- */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e3e6f0;
        border-top: 5px solid #4e73df;
        border-radius: 14px;
        padding: 16px 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    }
    .metric-card h4 { margin: 0 0 4px 0; font-size: 1rem; }
    .metric-card h2 { margin: 2px 0; }
    .metric-card p { margin: 0; }

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

    /* ---------- Compact, space-saving field labels ---------- */
    .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stTextArea label, .stRadio label, .stDateInput label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #2e384d !important;
        line-height: 1.25 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13.5px;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Color palette used to give each grade card its own accent color
CARD_COLORS = [
    "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e",
    "#e74a3b", "#858796", "#6f42c1", "#fd7e14",
    "#20c997", "#00b4d8", "#ef476f", "#118ab2",
]

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
        "1. Fuula Duraa (Cover Page)",
        "2. Dashboard Galmee Barataa (Foormii/Form)",
        "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)",
    ],
)

# ----------------- 1. COVER PAGE -----------------
if menu == "1. Fuula Duraa (Cover Page)":
  st.markdown(
      """
        <div class="cover-card">
            <h1>🎓 APPII GALMEE BARATTOOTAA</h1>
            <h3>Baga Nagaan Gara Appii Galmee Barattootaa Mana Barumsaa B/saa Kitesa Negasaa Dhuftan!</h3>
            <p>Sirni kun odeeffannoo barattootaa qabachuuf, gabaasa oomishuuf fi hordoffii taasisuuf kan qophaa'eedha.</p>
            <div class="badge-row">
                <span class="badge-pill">📚 Galmee Elektirooniksii</span>
                <span class="badge-pill">📊 Gabaasa Battalumaan</span>
                <span class="badge-pill">🔒 Nageenya Odeeffannoo</span>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div class="contact-card">
            <h3>📞 Toora Odeeffannoo fi Qunnamtii (Contact Information)</h3>
            <p>Eeyyama Appii kanatti fayyadamuu argachuuf ykn gaaffii kamiyyuu yoo qabaattan,
            karaalee qunnamtii armaan gadiitiin nu qunnamuu dandeessu:</p>
            <p>📱 <b>Bilbilaa fi Telegiraamii (Phone &amp; Telegram):</b> +251969184005 / 0910927936</p>
            <p>📧 <b>Imeelii (Gmail):</b> kitesanegasa2012@gmail.com</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.write("---")
  st.subheader("📊 Lakkoofsa Barattootaa Galmaa'anii Kutaadhaan (Number of Enrolled Students by Grade)")

  db = st.session_state.students_db
  cols = st.columns(4)
  for i in range(1, 13):
    count = len(db[db["Kutaa"] == str(i)]) if not db.empty else 0
    color = CARD_COLORS[(i - 1) % len(CARD_COLORS)]
    with cols[(i - 1) % 4]:
      st.markdown(
          f"""
                <div class="metric-card" style="border-top-color:{color};">
                    <h4>Kutaa {i} <span style="font-size:11px;color:#858796;">(Grade {i})</span></h4>
                    <h2 style="color:{color};">{count}</h2>
                    <p style="font-size:11px;color:#6b7280;">Barattoota Galmaa'an (Enrolled)</p>
                </div>
                """,
          unsafe_allow_html=True,
      )

# ----------------- 2. DASHBOARD GALMEE BARATTOOTAA (FOOMII) -----------------
elif menu == "2. Dashboard Galmee Barataa (Foormii/Form)":
  st.subheader("📝 Foormii Galmee Barattootaa Haaraa (New Student Registration Form)")

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa (Student Full Name)")
      koorniyaa = st.selectbox("2. Koorniyaa (Gender)", ["Filadhu", "Dhiira", "Dhalaa"])
      kutaa = st.selectbox("3. Kutaa (Grade)", [str(i) for i in range(1, 13)])

      st.markdown("**4. Bara Dhalootaa (Date of Birth - Akka Lakkoofsa Itoophiyaatti)**")
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox("Guyyaa (Day)", [str(i) for i in range(1, 31)])
      b_jiia = b_col2.selectbox(
          "Ji'a (Month)",
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
          "Bara (Year) (Fkn: 2005)", min_value=1980, max_value=2025, value=2010
      )
      current_et_year = 2018
      umurii = current_et_year - b_bara

      haala_galmee = st.selectbox(
          "5. Haala Galmee (Registration Status)",
          [
              "Haaraa",
              "Irra deebii (Kufe)",
              "Irra deebii (Kute)",
              "Mana Barumsaa Biroo",
          ],
      )
      bara_addaan_kute = (
          st.selectbox(
              "Bara Addaan Kute (Year Discontinued - Yoo jiraate)",
              ["Hin jiru", "2005", "2006", "2007", "2008", "2009", "2010"]
              + [str(y) for y in range(2011, 2027)],
          )
          if "deebii" in haala_galmee
          else "Hin jiru"
      )

      haala_maatii = st.selectbox(
          "6. Haala Maatii (Family Status)",
          ["Lachuu qaba", "Abbaa qofa", "Haadha qofa", "Lachuu hin qabu"],
      )
      miidhama_qaamaa = st.selectbox(
          "7. Haala Miidhama Qaamaa (Disability Status)", ["Hin jiru", "Jira"]
      )
      gosa_miidhamaa = (
          st.selectbox(
              "Gosa Miidhama Qaamaa (Type of Disability)",
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
          "8. Bakka Dhalootaa (Place of Birth - Godina, Aanaa, Ganda)"
      )
      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu (Mother/Guardian Full Name)")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID)")
      lakk_bilbila_barataa = st.text_input("11. Lakkoofsa Bilbila Barataa (Student Phone Number)")
      lakk_bilbila_maatii = st.text_input("12. Lakkoofsa Bilbila Maatii (Family Phone Number)")
      mb_duraan = st.text_input("13. Mana Barumsaa Duraan Itti Barachaa Ture (Previous School)")

      avireejjii = st.number_input(
          "14. Avireejjii Qabxii Bara Darbee (Average Score, 0 - 100)",
          min_value=0.0,
          max_value=100.0,
          value=75.0,
      )

      if avireejjii < 50:
        st.markdown(
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi waan ta\'eef, '
            '"Haala Galmee" jalatti "Kufe" jedhamee filatamuu qaba! '
            '(Score is below 50 — please select "Kufe/Failed" under Registration Status.)</p>',
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee (Registering Teacher)")
      guyyaa_galmee = str(datetime.now().date())

    submitted = st.form_submit_button("💾 Olkaa'i (Save)")

    if submitted:
      if not maqaa_guutuu or not fan_id:
        st.error("Maaloo Maqaa Guutuu fi FAN ID guuti! (Please fill in Full Name and FAN ID)")
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
            f"Galmeen barataa {maqaa_guutuu} milkaa'inaan galmeeffameera! (Successfully saved)"
        )

# ----------------- 3. DASHBOARD BARSIISAA / GABAASAA -----------------
elif menu == "3. Dashboard Barsiisaa / Gabaasaa (Password Needed)":
  st.subheader("🔐 Dashboard Barsiisaa (Teacher Dashboard - Seensa Eeyyamame)")

  password = st.text_input("Password Galchi (Enter Password)", type="password")

  if password == "kitesa2019" or password == "admin123":
    st.success("Seensa Milkaa'e! Gabaasotaa fi Karoora ilaaluu dandeessa. (Login successful — you can view reports and plans.)")

    tabA, tabB, tabC, tabD, tabE, tabF, tabG, tabH, tabI, tabJ = st.tabs(
        [
            "A. Karoora (Target)",
            "B. Gabaasa Guutuu (Full Report - Excel)",
            "C. Guyyaa - Kutaa 1 (Grade 1 Age Report)",
            "D. Lakkoofsa (Count Summary)",
            "E. Miidhamaa - Detail (Disability Detail)",
            "F. Miidhamaa - Lakkoofsa (Disability Count)",
            "G. Irra-Deebii - Detail (Repeaters Detail)",
            "H. Irra-Deebii - Lakkoofsa (Repeaters Count)",
            "I. Gabaasa 2019 (Annual Report)",
            "J. Sirreessi/Haqi (Edit/Delete)",
        ]
    )

    db = st.session_state.students_db

    with tabA:
      st.markdown("#### A. Gucaa Karoora Galmee Barattootaa 2019 (Student Registration Target Sheet)")
      with st.form("target_form"):
        selected_grade = st.selectbox(
            "Kutaa Filadhu (Select Grade)", [str(i) for i in range(1, 13)]
        )
        t_dhiira = st.number_input(
            "Karoora Dhiiraa (Male Target)",
            min_value=0,
            value=st.session_state.targets[selected_grade]["Dhiira"],
        )
        t_dhalaa = st.number_input(
            "Karoora Dhalaa (Female Target)",
            min_value=0,
            value=st.session_state.targets[selected_grade]["Dhalaa"],
        )
        save_target = st.form_submit_button("Karoora Galchi (Save Target)")
        if save_target:
          st.session_state.targets[selected_grade]["Dhiira"] = t_dhiira
          st.session_state.targets[selected_grade]["Dhalaa"] = t_dhalaa
          st.success(f"Karoora Kutaa {selected_grade} galmeeffameera! (Target saved)")

    with tabB:
      st.markdown("#### B. Gucaa Gabaasaa Waligalaa Barattootaa (Overall Report - Excel Download)")
      if not db.empty:
        st.dataframe(db)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          db.to_excel(writer, sheet_name="Gabaasa_Guutuu", index=False)
        st.download_button(
            label="📥 Excel-tti Buufadhu (Download as Excel)",
            data=buffer.getvalue(),
            file_name="Gabaasa_Waligalaa_Barattootaa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
      else:
        st.info("Deetaan galmaa'e hin jiru. (No data has been registered yet.)")

    with tabC:
      st.markdown("#### C. Gucaa Gabaasaa Kutaa 1, Umurii 7 (Grade 1 Students Aged 7)")
      if not db.empty:
        filtered_c = db[(db["Kutaa"] == "1") & (db["Umurii"] == 7)]
        st.write(f"Baay'ina Barattoota Kutaa 1 (Umurii 7): {len(filtered_c)}  *(Number of Grade 1 students aged 7)*")
        st.dataframe(filtered_c)
      else:
        st.info("Deetaan hin jiru. (No data available.)")

    with tabD:
      st.markdown("#### D. Gabaasa Lakkoofsaa Kutaa, Saalaa fi Umuriin (Count by Grade, Gender & Age)")
      if not db.empty:
        summary_d = (
            db.groupby(["Kutaa", "Umurii", "Koorniyaa"])
            .size()
            .reset_index(name="Baay'ina")
        )
        st.dataframe(summary_d)
      else:
        st.info("Deetaan hin jiru. (No data available.)")

    with tabE:
      st.markdown("#### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii (Students with Disabilities - Full Details)")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        st.dataframe(disabled_df)
      else:
        st.info("Deetaan hin jiru. (No data available.)")

    with tabF:
      st.markdown("#### F. Gabaasa Lakkoofsaa Miidhama Qaamaa & Haala Maatii (Disability & Family Status Count)")
      if not db.empty:
        st.write("**Miidhama Qaamaa Gosaan (By Disability Type):**")
        st.dataframe(
            db[db["Miidhama Qaamaa"] == "Jira"]["Gosa Miidhamaa"].value_counts()
        )
        st.write("**Haala Maatii (Family Status):**")
        st.dataframe(db["Haala Maatii"].value_counts())

    with tabG:
      st.markdown("#### G. Gabaasa Barattoota Irra Deebi'anii (Report of Repeating Students)")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(
            repeat_df[
                [
                    "Maqaa Guutuu",
                    "Koorniyaa",
                    "Kutaa",
                    "Haala Galmee",
                    "Bara Addaan Kute",
                ]
            ]
        )
      else:
        st.info("Deetaan hin jiru. (No data available.)")

    with tabH:
      st.markdown("#### H. Gabaasa Lakkoofsaa Barattoota Irra Deebi'anii (Count of Repeating Students)")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii", na=False)]
        st.dataframe(
            repeat_df.groupby(["Kutaa", "Koorniyaa", "Haala Galmee"])
            .size()
            .reset_index(name="Baay'ina")
        )
      else:
        st.info("Deetaan hin jiru. (No data available.)")

    with tabI:
      st.markdown("#### I. Gabaasa Galmee Waligalaa Bara 2019 (Overall Annual Registration Report)")
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
      st.markdown("#### J. Sirreessi ykn Haqi Deetaa Barataa (Edit / Delete Student Data)")
      if not db.empty:
        idx_to_modify = st.number_input(
            "Lakk. Index Barataa jijjiiruu/haquu barbaadde (Student Record Index)",
            min_value=0,
            max_value=max(0, len(db) - 1),
            step=1,
        )
        st.write(db.iloc[idx_to_modify])

        if st.button("🗑️ Barataa Kana Haquu (Delete)"):
          st.session_state.students_db = db.drop(idx_to_modify).reset_index(
              drop=True
          )
          st.success("Deetaan barataa haqameera! (Student data has been deleted.)")
          st.rerun()
      else:
        st.info("Deetaan jijjiiramu hin jiru. (No data available to edit.)")

  elif password != "":
    st.error("Password sirrii miti! Irra deebi'ii yaali. (Incorrect password — please try again.)")
