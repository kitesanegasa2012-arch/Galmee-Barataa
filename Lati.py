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
  # Targets dictionary for grades 1-12 with Dhiira, Dhalaa
  st.session_state.targets = {
      str(i): {"Dhiira": 0, "Dhalaa": 0} for i in range(1, 13)
  }

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
      daree = grade_col2.selectbox("Daree (Section)", [chr(65+i) for i in range(11)]) # A to K

      st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyyatti)**")
      b_col1, b_col2, b_col3 = st.columns(3)
      b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
      b_jiia = b_col2.selectbox(
          "Ji'a",
          [
              "Fulbaana",
              "Onkololeessa",
              "Hacaaluu/Hidar", # Traditional/Standard Ethiopian months in Afaan Oromoo
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
      
      gosa_miidhamaa = st.selectbox(
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
      ) if miidhama_qaamaa == "Jira" else "Hin qabu"

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
            '<p style="color:red; font-weight:bold;">⚠️ Qabxiin kun 50 gadi waan ta’eef, haala galmee irratti "Kufe" jedhamee walsimsiifamuu qaba!</p>',
            unsafe_allow_html=True,
        )

      barsiisaa = st.text_input("15. Barsiisaa Galmeessee")
      
      # Date in Ethiopian Calendar format requested: DD/MM/YYYY e.g., 25/11/2018
      guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018")

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

    # Helper function for grouping ranges
    def get_grade_rows(df, grade_list):
        sub = df[df["Kutaa"].isin([str(g) for g in grade_list])]
        d_count = len(sub[sub["Koorniyaa"] == "Dhiira"])
        dh_count = len(sub[sub["Koorniyaa"] == "Dhalaa"])
        return d_count, dh_count, d_count + dh_count

    with tabA:
      st.markdown("### A. Guca Karoora Galmee Barataa (Dhiira, Dhalaa, Ida'ama)")
      st.write("Kutaa 1-12ef karoora galmee galchi:")
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

      st.markdown("#### Lakkoofsa Karoora Waliigalaa (Kutaa Kutaan & Ida'ama)")
      t_summary = []
      for k in range(1, 13):
        k_str = str(k)
        td = st.session_state.targets[k_str]["Dhiira"]
        tdh = st.session_state.targets[k_str]["Dhalaa"]
        t_summary.append({"Kutaa": f"Kutaa {k}", "Dhiira": td, "Dhalaa": tdh, "Ida'ama": td + tdh})
      
      # Add sub-totals for 1-6, 7-8, 1-8, 9-12
      d_1_6 = sum(st.session_state.targets[str(i)]["Dhiira"] for i in range(1, 7))
      dh_1_6 = sum(st.session_state.targets[str(i)]["Dhalaa"] for i in range(1, 7))
      t_summary.append({"Kutaa": "Ida'ama (1-6)", "Dhiira": d_1_6, "Dhalaa": dh_1_6, "Ida'ama": d_1_6 + dh_1_6})

      d_7_8 = sum(st.session_state.targets[str(i)]["Dhiira"] for i in range(7, 9))
      dh_7_8 = sum(st.session_state.targets[str(i)]["Dhalaa"] for i in range(7, 9))
      t_summary.append({"Kutaa": "Ida'ama (7-8)", "Dhiira": d_7_8, "Dhalaa": dh_7_8, "Ida'ama": d_7_8 + dh_7_8})

      d_1_8 = d_1_6 + d_7_8
      dh_1_8 = dh_1_6 + dh_7_8
      t_summary.append({"Kutaa": "Ida'ama (1-8)", "Dhiira": d_1_8, "Dhalaa": dh_1_8, "Ida'ama": d_1_8 + dh_1_8})

      d_9_12 = sum(st.session_state.targets[str(i)]["Dhiira"] for i in range(9, 13))
      dh_9_12 = sum(st.session_state.targets[str(i)]["Dhalaa"] for i in range(9, 13))
      t_summary.append({"Kutaa": "Ida'ama (9-12)", "Dhiira": d_9_12, "Dhalaa": dh_9_12, "Ida'ama": d_9_12 + dh_9_12})

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
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
      else:
        st.info("Deetaan galmaa'e hin jiru.")

    with tabC:
      st.markdown("### C. Gabaasa Galmee Guyyaa Tokkoo (Specific Date Report)")
      if not db.empty:
        available_dates = db["Guyyaa Galmee (E.C)"].unique().tolist()
        selected_date = st.selectbox("Guyyaa Filadhu (E.C)", available_dates)
        
        day_df = db[db["Guyyaa Galmee (E.C)"] == selected_date]
        st.write(f"Galmee Guyyaa: {selected_date}")
        
        # Aggregate by grade for this specific date
        d_rows = []
        for k in range(1, 13):
          k_str = str(k)
          sub_d = day_df[(day_df["Kutaa"] == k_str)]
          d_c = len(sub_d[sub_d["Koorniyaa"] == "Dhiira"])
          dh_c = len(sub_d[sub_d["Koorniyaa"] == "Dhalaa"])
          d_rows.append({"Kutaa": f"Kutaa {k}", "Dhiira": d_c, "Dhalaa": dh_c, "Ida'ama": d_c + dh_c})
        st.dataframe(pd.DataFrame(d_rows))
        st.write("Barattoota Guyyaa kana galmaa'an hunda:")
        st.dataframe(day_df)
      else:
        st.info("Deetaan hin jiru.")

    with tabD:
      st.markdown("### D. Gabaasa Galmee Hanga Ammaatti (Waliigalaa Kutaa Kutaan)")
      if not db.empty:
        summary_rows = []
        for k in range(1, 13):
          k_str = str(k)
          d, dh, tot = get_grade_rows(db, [k])
          summary_rows.append({"Kutaa": f"Kutaa {k}", "Dhiira": d, "Dhalaa": dh, "Ida'ama": tot})
        
        # Ranges
        d_16, dh_16, tot_16 = get_grade_rows(db, range(1, 7))
        summary_rows.append({"Kutaa": "Ida'ama (1-6)", "Dhiira": d_16, "Dhalaa": dh_16, "Ida'ama": tot_16})

        d_78, dh_78, tot_78 = get_grade_rows(db, range(7, 9))
        summary_rows.append({"Kutaa": "Ida'ama (7-8)", "Dhiira": d_78, "Dhalaa": dh_78, "Ida'ama": tot_78})

        d_18, dh_18, tot_18 = get_grade_rows(db, range(1, 9))
        summary_rows.append({"Kutaa": "Ida'ama (1-8)", "Dhiira": d_18, "Dhalaa": dh_18, "Ida'ama": tot_18})

        d_912, dh_912, tot_912 = get_grade_rows(db, range(9, 13))
        summary_rows.append({"Kutaa": "Ida'ama (9-12)", "Dhiira": d_912, "Dhalaa": dh_912, "Ida'ama": tot_912})

        st.dataframe(pd.DataFrame(summary_rows))
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown("### E. Gabaasa Barattoota Miidhama Qaamaa / Haala Addaa Qabanii (Maqaan)")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        if not disabled_df.empty:
          st.dataframe(disabled_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Daree (Section)", "Umurii", "Gosa Miidhamaa", "Haala Maatii"]])
        else:
          st.info("Barataan miidhama qaamaa qabu hin galmoofne.")
      else:
        st.info("Deetaan hin jiru.")

    with tabF:
      st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa (Gosaan & Kutaan)")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        if not disabled_df.empty:
          st.write("**Gosa Miidhama Qamaa / Haala Addaa Hanga Ammaatti:**")
          st.dataframe(disabled_df["Gosa Miidhamaa"].value_counts().reset_index(name="Baay'ina"))
          st.write("**Haala Maatii (Lachuu hin qabne dabalatee):**")
          st.dataframe(db["Haala Maatii"].value_counts().reset_index(name="Baay'ina"))
        else:
          st.info("Deetaan miidhama qaamaa hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabG:
      st.markdown("### G. Gabaasa Barattoota Irra Deebi'anii (Maqaa, Kutaa, Saala, Sababa)")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
        if not repeat_df.empty:
          st.dataframe(repeat_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Daree (Section)", "Haala Galmee", "Bara Addaan Kute"]])
        else:
          st.info("Barataan irra deebii hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabH:
      st.markdown("### H. Gabaasa Lakkoofsaa Barattoota Irra Deebi'anii (Kutaa, Dhiira, Dhalaa, Ida'ama)")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
        if not repeat_df.empty:
          rep_summary = repeat_df.groupby(["Kutaa", "Koorniyaa"]).size().unstack(fill_value=0)
          for col in ["Dhiira", "Dhalaa"]:
            if col not in rep_summary.columns:
              rep_summary[col] = 0
          rep_summary["Ida'ama"] = rep_summary["Dhiira"] + rep_summary["Dhalaa"]
          st.dataframe(rep_summary.reset_index())
        else:
          st.info("Deetaan irra deebii hin jiru.")
      else:
        st.info("Deetaan hin jiru.")

    with tabI:
      st.markdown("### I. Gabaasa Galmee Waligalaa 2019 (Karoora vs Raawwii fi Parsantii)")
      perf_data = []
      
      def add_perf_row(label, grade_list):
        # Target sum
        t_d = sum(st.session_state.targets[str(g)]["Dhiira"] for g in grade_list)
        t_dh = sum(st.session_state.targets[str(g)]["Dhalaa"] for g in grade_list)
        t_tot = t_d + t_dh

        # Actual sum
        r_d, r_dh, r_tot = get_grade_rows(db, grade_list)

        p_d = (r_d / t_d * 100) if t_d > 0 else 0
        p_dh = (r_dh / t_dh * 100) if t_dh > 0 else 0
        p_tot = (r_tot / t_tot * 100) if t_tot > 0 else 0

        perf_data.append({
            "Kutaa": label,
            "Karoora Dhiira": t_d,
            "Karoora Dhalaa": t_dh,
            "Karoora Ida'ama": t_tot,
            "Raawwii Dhiira": r_d,
            "Raawwii Dhalaa": r_dh,
            "Raawwii Ida'ama": r_tot,
            "% Dhiira": round(p_d, 1),
            "% Dhalaa": round(p_dh, 1),
            "% Ida'ama": round(p_tot, 1),
        })

      for k in range(1, 13):
        add_perf_row(f"Kutaa {k}", [k])
      
      add_perf_row("Ida'ama (1-6)", range(1, 7))
      add_perf_row("Ida'ama (7-8)", range(7, 9))
      add_perf_row("Ida'ama (1-8)", range(1, 9))
      add_perf_row("Ida'ama (9-12)", range(9, 13))

      st.dataframe(pd.DataFrame(perf_data))

    with tabJ:
      st.markdown("### J. Edit / Delete / Update Data Barattootaa")
      if not db.empty:
        search_query = st.text_input("Maqaa barataa ykn FAN ID barressii barbaadi:")
        filtered_edit = db[db["Maqaa Guutuu"].str.contains(search_query, case=False, na=False) | db["FAN ID"].str.contains(search_query, case=False, na=False)] if search_query else db
        
        if not filtered_edit.empty:
          selected_idx = st.selectbox("Barataa jijjiiruf filadhu (Index)", filtered_edit.index.tolist())
          row_data = db.loc[selected_idx]
          
          st.write("#### Odeeffannoo Ammaa:")
          st.write(row_data)

          with st.form("edit_form"):
            new_maqaa = st.text_input("Maqaa Guutuu", value=row_data["Maqaa Guutuu"])
            new_koorniyaa = st.selectbox("Koorniyaa", ["Dhiira", "Dhalaa"], index=0 if row_data["Koorniyaa"]=="Dhiira" else 1)
            new_kutaa = st.selectbox("Kutaa", [str(i) for i in range(1, 13)], index=int(row_data["Kutaa"])-1)
            new_daree = st.text_input("Daree (Section)", value=row_data["Daree (Section)"])
            new_haala = st.selectbox("Haala Galmee", ["Haaraa", "Kan darbe", "Irra deebii (Kufe)", "Irra deebii (Kute)", "Mana Barumsaa Biroo"])
            new_av = st.number_input("Avireejjii Qabxii", value=float(row_data["Avireejjii Qabxii"]))
            
            col_save_edit, col_del_edit = st.columns(2)
            do_update = col_save_edit.form_submit_button("🔄 Update / Save")
            do_delete = col_del_edit.form_submit_button("🗑️ Delete Barataa")

            if do_update:
              st.session_state.students_db.at[selected_idx, "Maqaa Guutuu"] = new_maqaa
              st.session_state.students_db.at[selected_idx, "Koorniyaa"] = new_koorniyaa
              st.session_state.students_db.at[selected_idx, "Kutaa"] = new_kutaa
              st.session_state.students_db.at[selected_idx, "Daree (Section)"] = new_daree
              st.session_state.students_db.at[selected_idx, "Haala Galmee"] = new_haala
              st.session_state.students_db.at[selected_idx, "Avireejjii Qabxii"] = new_av
              st.success("Odeeffannoon barataa milkaa'inaan *Update* ta'eera!")
              st.rerun()

            if do_delete:
              st.session_state.students_db = db.drop(selected_idx).reset_index(drop=True)
              st.success("Barataan kun haqameera (Deleted)!")
              st.rerun()
        else:
          st.info("Barataan barbaadame hin argamne.")
      else:
        st.info("Deetaan barattootaa hin jiru.")

  elif password != "":
    st.error("Password sirrii miti! Irra deebi'ii yaali.")
