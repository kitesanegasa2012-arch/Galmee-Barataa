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
      daree = grade_col2.selectbox("Daree (Section)", [chr(65+i) for i in range(11)])

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
      
      # Sirreeffama: Miidhama Qaamaa yoo "Jira" ta'e qofa filannoowwan gosa miidhamaa ni mul'atu
      gosa_miidhamaa = "Hin qabu"
      if miidhama_qaamaa == "Jira":
          gosa_miidhamaa = st.selectbox(
              "Gosa Miidhama Qaamaa / Haala Addaa",
              [
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

    with col2:
      st.markdown("**8. Bakka Dhalootaa**")
      godina = st.text_input("Godina", value=default_godina)
      aanaa = st.text_input("Aanaa", value=default_aanaa)
      ganda = st.text_input("Ganda", value=default_ganda)

      maqaa_haadhaa = st.text_input("9. Maqaa Guutuu Haadhaa ykn Guddistuu")
      fan_id = st.text_input("10. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID) - Dirqama miti")
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
      guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C - Fkn: 25/11/2018)", value="25/11/2018")

    submitted = st.form_submit_button("💾 Save (Enter)")

    if submitted:
      # Sirreeffama: FAN ID yeroo kana dirqama miti, Maqaa Guutuu qofatu dirqamaadha
      if not maqaa_guutuu:
        st.error("Maaloo Maqaa Guutuu barataa guuti!")
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
        t_summary.append({"Kutaa": f"Kutaa {k}", "Dhiira": td, "Dhalaa": tdh, "Ida'ama": td + tdh})
      
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
          summary_rows.append({"Kutaa": f"Kutaa {k}", "Dhiira": d, "Dhalaa": dh, "Ida'ama": tot})
        st.dataframe(pd.DataFrame(summary_rows))
      else:
        st.info("Deetaan hin jiru.")

    with tabE:
      st.markdown("### E. Gabaasa Barattoota Miidhama Qaamaa Qabanii")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        if not disabled_df.empty:
          st.dataframe(disabled_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Gosa Miidhamaa"]])
        else:
          st.info("Barataan miidhama qaamaa qabu hin galmoofne.")

    with tabF:
      st.markdown("### F. Gabaasa Lakkoofsaa Miidhama Qaamaa")
      if not db.empty:
        disabled_df = db[db["Miidhama Qaamaa"] == "Jira"]
        if not disabled_df.empty:
          st.dataframe(disabled_df["Gosa Miidhamaa"].value_counts().reset_index(name="Baay'ina"))

    with tabG:
      st.markdown("### G. Gabaasa Barattoota Irra Deebi'anii")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
        st.dataframe(repeat_df[["Maqaa Guutuu", "Koorniyaa", "Kutaa", "Haala Galmee"]])

    with tabH:
      st.markdown("### H. Gabaasa Lakkoofsaa Irra Deebii")
      if not db.empty:
        repeat_df = db[db["Haala Galmee"].str.contains("Irra deebii|Kan darbe", na=False)]
        if not repeat_df.empty:
          st.dataframe(repeat_df.groupby(["Kutaa", "Koorniyaa"]).size().unstack(fill_value=0).reset_index())

    with tabI:
      st.markdown("### I. Gabaasa Waligalaa 2019 (Karoora vs Raawwii)")
      perf_data = []
      for k in range(1, 13):
        t_d = st.session_state.targets[str(k)]["Dhiira"]
        t_dh = st.session_state.targets[str(k)]["Dhalaa"]
        r_d, r_dh, r_tot = get_grade_rows(db, [k])
        perf_data.append({"Kutaa": f"Kutaa {k}", "Karoora Dhiira": t_d, "Raawwii Dhiira": r_d, "Karoora Dhalaa": t_dh, "Raawwii Dhalaa": r_dh})
      st.dataframe(pd.DataFrame(perf_data))

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
