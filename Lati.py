import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Gabaasa Galmee Barattootaa", layout="wide")

# Session State Initialization for Targets
if "targets" not in st.session_state:
    st.session_state.targets = {
        str(k): {"Dhiira": 50, "Dhalaa": 50} for k in range(1, 13)
    }

st.title("📊 Sirna Qindeessa Galmee fi Gabaasa Barattootaa")

# Sample Dataframe Initialization for demonstration if not present
if "db" not in st.session_state:
    # Dummy data generation for testing the layout
    data = []
    for k in range(1, 13):
        for i in range(25):
            data.append({
                "Kutaa": str(k),
                "Koorniyaa": "Dhiira" if i % 2 == 0 else "Dhalaa",
                "Maqaa": f"Barataa {k}_{i}"
            })
    st.session_state.db = pd.DataFrame(data)

db = st.session_state.db

tabI, tabII = st.tabs(["I. Karoora vs Raawwii", "II. Qindoomina Karooraa"])

with tabII:
    st.markdown("### II. Karoora Barattoota Galchuuf")
    st.write("Kutaa hundaaf karoora dhiiraa fi dhalaatiif qopheessi.")
    
    with st.form("target_form"):
        new_targets = {}
        for k in range(1, 13):
            k_str = str(k)
            st.markdown(f"**Kutaa {k}**")
            c1, c2 = st.columns(2)
            with c1:
                t_d = st.number_input(f"Kutaa {k} - Dhiira", min_value=0, value=st.session_state.targets[k_str]["Dhiira"], key=f"t_d_{k}")
            with c2:
                t_dh = st.number_input(f"Kutaa {k} - Dhalaa", min_value=0, value=st.session_state.targets[k_str]["Dhalaa"], key=f"t_dh_{k}")
            new_targets[k_str] = {"Dhiira": t_d, "Dhalaa": t_dh}
        
        submitted = st.form_submit_button("Karoora Olkaa'i")
        if submitted:
            st.session_state.targets = new_targets
            st.success("Karooraanmilkaa'inaan galchaameera!")

with tabI:
    st.markdown("### I. Karoora vs Raawwii (Column Dhuunfaa Dhuunfaan)")
    if not db.empty:
        raw_comparison = []
        for k in range(1, 13):
            k_str = str(k)
            t_d = st.session_state.targets[k_str]["Dhiira"]
            t_dh = st.session_state.targets[k_str]["Dhalaa"]
            t_ida = t_d + t_dh
            
            sub_k = db[db["Kutaa"] == k_str]
            a_d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
            a_dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
            a_ida = a_d + a_dh
            
            p_d = (a_d / t_d * 100) if t_d > 0 else 0.0
            p_dh = (a_dh / t_dh * 100) if t_dh > 0 else 0.0
            p_ida = (a_ida / t_ida * 100) if t_ida > 0 else 0.0
            
            raw_comparison.append({
                "Kutaa_Num": k_str,
                "Kutaa": f"Kutaa {k}",
                "Kar. Dhiira": t_d,
                "Raw. Dhiira": a_d,
                "% Dhiira": f"{p_d:.1f}%",
                "Kar. Dhalaa": t_dh,
                "Raw. Dhalaa": a_dh,
                "% Dhalaa": f"{p_dh:.1f}%",
                "Kar. Ida'ama": t_ida,
                "Raw. Ida'ama": a_ida,
                "% Ida'ama": f"{p_ida:.1f}%",
                "Target_Dhiira": t_d,
                "Target_Dhalaa": t_dh,
                "Actual_Dhiira": a_d,
                "Actual_Dhalaa": a_dh
            })
        
        def make_summary_row(title, t_d, a_d, t_dh, a_dh):
            t_ida = t_d + t_dh
            a_ida = a_d + a_dh
            p_d = (a_d / t_d * 100) if t_d > 0 else 0.0
            p_dh = (a_dh / t_dh * 100) if t_dh > 0 else 0.0
            p_ida = (a_ida / t_ida * 100) if t_ida > 0 else 0.0
            return {
                "Kutaa": title,
                "Kar. Dhiira": t_d,
                "Raw. Dhiira": a_d,
                "% Dhiira": f"{p_d:.1f}%",
                "Kar. Dhalaa": t_dh,
                "Raw. Dhalaa": a_dh,
                "% Dhalaa": f"{p_dh:.1f}%",
                "Kar. Ida'ama": t_ida,
                "Raw. Ida'ama": a_ida,
                "% Ida'ama": f"{p_ida:.1f}%"
            }

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
        
        for r in raw_comparison:
            if int(r["Kutaa_Num"]) <= 6:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], "Kar. Dhiira": r["Target_Dhiira"], "Raw. Dhiira": r["Actual_Dhiira"], "% Dhiira": r["% Dhiira"],
                    "Kar. Dhalaa": r["Target_Dhalaa"], "Raw. Dhalaa": r["Actual_Dhalaa"], "% Dhalaa": r["% Dhalaa"],
                    "Kar. Ida'ama": r["Target_Dhiira"]+r["Target_Dhalaa"], "Raw. Ida'ama": r["Actual_Dhiira"]+r["Actual_Dhalaa"], "% Ida'ama": r["% Ida'ama"]
                })
        
        comp_final_table.append(make_summary_row("Ida'ama Kutaa 1 - 6", t_1_6_d, a_1_6_d, t_1_6_dh, a_1_6_dh))
        
        for r in raw_comparison:
            if 7 <= int(r["Kutaa_Num"]) <= 8:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], "Kar. Dhiira": r["Target_Dhiira"], "Raw. Dhiira": r["Actual_Dhiira"], "% Dhiira": r["% Dhiira"],
                    "Kar. Dhalaa": r["Target_Dhalaa"], "Raw. Dhalaa": r["Actual_Dhalaa"], "% Dhalaa": r["% Dhalaa"],
                    "Kar. Ida'ama": r["Target_Dhiira"]+r["Target_Dhalaa"], "Raw. Ida'ama": r["Actual_Dhiira"]+r["Actual_Dhalaa"], "% Ida'ama": r["% Ida'ama"]
                })
        
        comp_final_table.append(make_summary_row("Ida'ama Kutaa 7 - 8", t_7_8_d, a_7_8_d, t_7_8_dh, a_7_8_dh))
        comp_final_table.append(make_summary_row("Ida'ama Waliigalaa (1 - 8)", t_1_6_d + t_7_8_d, a_1_6_d + a_7_8_d, t_1_6_dh + t_7_8_dh, a_1_6_dh + a_7_8_dh))

        for r in raw_comparison:
            if int(r["Kutaa_Num"]) >= 9:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], "Kar. Dhiira": r["Target_Dhiira"], "Raw. Dhiira": r["Actual_Dhiira"], "% Dhiira": r["% Dhiira"],
                    "Kar. Dhalaa": r["Target_Dhalaa"], "Raw. Dhalaa": r["Actual_Dhalaa"], "% Dhalaa": r["% Dhalaa"],
                    "Kar. Ida'ama": r["Target_Dhiira"]+r["Target_Dhalaa"], "Raw. Ida'ama": r["Actual_Dhiira"]+r["Actual_Dhalaa"], "% Ida'ama": r["% Ida'ama"]
                })
        
        comp_final_table.append(make_summary_row("Ida'ama Kutaa 9 - 12", t_9_12_d, a_9_12_d, t_9_12_dh, a_9_12_dh))

        tot_t_d = t_1_6_d + t_7_8_d + t_9_12_d
        tot_t_dh = t_1_6_dh + t_7_8_dh + t_9_12_dh
        tot_a_d = a_1_6_d + a_7_8_d + a_9_12_d
        tot_a_dh = a_1_6_dh + a_7_8_dh + a_9_12_dh
        
        comp_final_table.append(make_summary_row("Waliigalaa (1 - 12)", tot_t_d, tot_a_d, tot_t_dh, tot_a_dh))

        comp_df = pd.DataFrame(comp_final_table)
        st.dataframe(comp_df, use_container_width=True)

        buffer_i = io.BytesIO()
        with pd.ExcelWriter(buffer_i, engine="openpyxl") as writer:
            comp_df.to_excel(writer, sheet_name="Karoora_vs_Raawwii", index=False)
        st.download_button(
            label="📥 Karoora vs Raawwii Print / Excel-tti Download Gochuu",
            data=buffer_i.getvalue(),
            file_name="Karoora_vs_Raawwii_Barattootaa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("Deetaan galmaa'e hin jiru.")
