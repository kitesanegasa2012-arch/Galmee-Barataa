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
