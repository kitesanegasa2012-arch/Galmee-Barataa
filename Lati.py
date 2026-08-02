import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Gabaasa Galmee Barattootaa - Guca A", layout="wide")

# Session State Initialization for Guca A official target structure
if "targets_guca_a" not in st.session_state:
    st.session_state.targets_guca_a = {
        str(k): {
            "Dhiira_Barattoota_Jiran": 30,
            "Dhalaa_Barattoota_Jiran": 30,
            "Dhiira_Karoora": 30,
            "Dhalaa_Karoora": 30
        } for k in range(1, 13)
    }

st.title("📊 Sirna Qindeessa Galmee fi Gabaasa Barattootaa (Guca A)")

# Sample Dataframe Initialization for demonstration if not present
if "db" not in st.session_state:
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

tabI, tabII = st.tabs(["I. Karoora vs Raawwii (Guca A)", "II. Guca A - Galchee Karooraa"])

with tabII:
    st.markdown("### II. Guca A - Karoora fi Lakkoofsa Barattoota Galchuuf")
    st.write("Kutaa hundaaf barattoota jiran fi karoora dhiiraa/dhalaatiif akka Guca A official ta'etti guuti.")
    
    with st.form("guca_a_target_form"):
        new_targets = {}
        for k in range(1, 13):
            k_str = str(k)
            st.markdown(f"**Kutaa {k}**")
            c1, c2, c3, c4 = st.columns(4)
            current_vals = st.session_state.targets_guca_a[k_str]
            with c1:
                t_dj = st.number_input(f"Kutaa {k} - Barattoota Jiran (Dhiira)", min_value=0, value=current_vals["Dhiira_Barattoota_Jiran"], key=f"dj_{k}")
            with c2:
                t_dhj = st.number_input(f"Kutaa {k} - Barattoota Jiran (Dhalaa)", min_value=0, value=current_vals["Dhalaa_Barattoota_Jiran"], key=f"dhj_{k}")
            with c3:
                t_dk = st.number_input(f"Kutaa {k} - Karoora (Dhiira)", min_value=0, value=current_vals["Dhiira_Karoora"], key=f"dk_{k}")
            with c4:
                t_dhk = st.number_input(f"Kutaa {k} - Karoora (Dhalaa)", min_value=0, value=current_vals["Dhalaa_Karoora"], key=f"dhk_{k}")
            
            new_targets[k_str] = {
                "Dhiira_Barattoota_Jiran": t_dj,
                "Dhalaa_Barattoota_Jiran": t_dhj,
                "Dhiira_Karoora": t_dk,
                "Dhalaa_Karoora": t_dhk
            }
        
        submitted = st.form_submit_button("Karoora Guca A Olkaa'i")
        if submitted:
            st.session_state.targets_guca_a = new_targets
            st.success("Karooraan Guca A milkaa'inaan galchaameera!")

with tabI:
    st.markdown("### I. Karoora vs Raawwii (Guca A)")
    if not db.empty:
        raw_comparison = []
        for k in range(1, 13):
            k_str = str(k)
            t_data = st.session_state.targets_guca_a[k_str]
            
            kar_dhiira = t_data["Dhiira_Karoora"]
            kar_dhalaa = t_data["Dhalaa_Karoora"]
            kar_idaama = kar_dhiira + kar_dhalaa
            
            sub_k = db[db["Kutaa"] == k_str]
            raw_dhiira = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
            raw_dhalaa = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
            raw_idaama = raw_dhiira + raw_dhalaa
            
            raw_dhiira_p = (raw_dhiira / kar_dhiira * 100) if kar_dhiira > 0 else 0.0
            raw_dhalaa_p = (raw_dhalaa / kar_dhalaa * 100) if kar_dhalaa > 0 else 0.0
            raw_idaama_p = (raw_idaama / kar_idaama * 100) if kar_idaama > 0 else 0.0
            
            raw_comparison.append({
                "Kutaa_Num": k_str,
                "Kutaa": f"Kutaa {k}",
                "Karoora Dhiira": kar_dhiira,
                "Karoora Dhalaa": kar_dhalaa,
                "Karoora Ida'ama": kar_idaama,
                "Raawwii Dhiira": raw_dhiira,
                "Raawwii Dhalaa": raw_dhalaa,
                "Raawwii Ida'ama": raw_idaama,
                "Raawwii Dhiira%": f"{raw_dhiira_p:.1f}%",
                "Raawwii Dhalaa%": f"{raw_dhalaa_p:.1f}%",
                "Raawwii Ida'ama%": f"{raw_idaama_p:.1f}%",
                "T_Dhiira": kar_dhiira,
                "T_Dhalaa": kar_dhalaa,
                "R_Dhiira": raw_dhiira,
                "R_Dhalaa": raw_dhalaa
            })
        
        def make_guca_a_summary(title, t_d, a_d, t_dh, a_dh):
            t_ida = t_d + t_dh
            a_ida = a_d + a_dh
            p_d = (a_d / t_d * 100) if t_d > 0 else 0.0
            p_dh = (a_dh / t_dh * 100) if t_dh > 0 else 0.0
            p_ida = (a_ida / t_ida * 100) if t_ida > 0 else 0.0
            return {
                "Kutaa": title,
                "Karoora Dhiira": t_d,
                "Karoora Dhalaa": t_dh,
                "Karoora Ida'ama": t_ida,
                "Raawwii Dhiira": a_d,
                "Raawwii Dhalaa": a_dh,
                "Raawwii Ida'ama": a_ida,
                "Raawwii Dhiira%": f"{p_d:.1f}%",
                "Raawwii Dhalaa%": f"{p_dh:.1f}%",
                "Raawwii Ida'ama%": f"{p_ida:.1f}%"
            }

        t_1_6_d = sum(r["T_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
        t_1_6_dh = sum(r["T_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
        a_1_6_d = sum(r["R_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
        a_1_6_dh = sum(r["R_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
        
        t_7_8_d = sum(r["T_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
        t_7_8_dh = sum(r["T_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
        a_7_8_d = sum(r["R_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
        a_7_8_dh = sum(r["R_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
        
        t_9_12_d = sum(r["T_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
        t_9_12_dh = sum(r["T_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
        a_9_12_d = sum(r["R_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
        a_9_12_dh = sum(r["R_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)

        comp_final_table = []
        
        for r in raw_comparison:
            if int(r["Kutaa_Num"]) <= 6:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], 
                    "Karoora Dhiira": r["Karoora Dhiira"], "Karoora Dhalaa": r["Karoora Dhalaa"], "Karoora Ida'ama": r["Karoora Ida'ama"],
                    "Raawwii Dhiira": r["Raawwii Dhiira"], "Raawwii Dhalaa": r["Raawwii Dhalaa"], "Raawwii Ida'ama": r["Raawwii Ida'ama"],
                    "Raawwii Dhiira%": r["Raawwii Dhiira%"], "Raawwii Dhalaa%": r["Raawwii Dhalaa%"], "Raawwii Ida'ama%": r["Raawwii Ida'ama%"]
                })
        
        comp_final_table.append(make_guca_a_summary("Ida'ama Kutaa 1 - 6", t_1_6_d, a_1_6_d, t_1_6_dh, a_1_6_dh))
        
        for r in raw_comparison:
            if 7 <= int(r["Kutaa_Num"]) <= 8:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], 
                    "Karoora Dhiira": r["Karoora Dhiira"], "Karoora Dhalaa": r["Karoora Dhalaa"], "Karoora Ida'ama": r["Karoora Ida'ama"],
                    "Raawwii Dhiira": r["Raawwii Dhiira"], "Raawwii Dhalaa": r["Raawwii Dhalaa"], "Raawwii Ida'ama": r["Raawwii Ida'ama"],
                    "Raawwii Dhiira%": r["Raawwii Dhiira%"], "Raawwii Dhalaa%": r["Raawwii Dhalaa%"], "Raawwii Ida'ama%": r["Raawwii Ida'ama%"]
                })
        
        comp_final_table.append(make_guca_a_summary("Ida'ama Kutaa 7 - 8", t_7_8_d, a_7_8_d, t_7_8_dh, a_7_8_dh))
        comp_final_table.append(make_guca_a_summary("Ida'ama Waliigalaa (1 - 8)", t_1_6_d + t_7_8_d, a_1_6_d + a_7_8_d, t_1_6_dh + t_7_8_dh, a_1_6_dh + a_7_8_dh))

        for r in raw_comparison:
            if int(r["Kutaa_Num"]) >= 9:
                comp_final_table.append({
                    "Kutaa": r["Kutaa"], 
                    "Karoora Dhiira": r["Karoora Dhiira"], "Karoora Dhalaa": r["Karoora Dhalaa"], "Karoora Ida'ama": r["Karoora Ida'ama"],
                    "Raawwii Dhiira": r["Raawwii Dhiira"], "Raawwii Dhalaa": r["Raawwii Dhalaa"], "Raawwii Ida'ama": r["Raawwii Ida'ama"],
                    "Raawwii Dhiira%": r["Raawwii Dhiira%"], "Raawwii Dhalaa%": r["Raawwii Dhalaa%"], "Raawwii Ida'ama%": r["Raawwii Ida'ama%"]
                })
        
        comp_final_table.append(make_guca_a_summary("Ida'ama Kutaa 9 - 12", t_9_12_d, a_9_12_d, t_9_12_dh, a_9_12_dh))

        tot_t_d = t_1_6_d + t_7_8_d + t_9_12_d
        tot_t_dh = t_1_6_dh + t_7_8_dh + t_9_12_dh
        tot_a_d = a_1_6_d + a_7_8_d + a_9_12_d
        tot_a_dh = a_1_6_dh + a_7_8_dh + a_9_12_dh
        
        comp_final_table.append(make_guca_a_summary("Waliigalaa (1 - 12)", tot_t_d, tot_a_d, tot_t_dh, tot_a_dh))

        comp_df = pd.DataFrame(comp_final_table)
        st.dataframe(comp_df, use_container_width=True)

        buffer_i = io.BytesIO()
        with pd.ExcelWriter(buffer_i, engine="openpyxl") as writer:
            comp_df.to_excel(writer, sheet_name="Guca_A_Karoora_vs_Raawwii", index=False)
        st.download_button(
            label="📥 Guca A - Karoora vs Raawwii Excel-tti Download Gochuu",
            data=buffer_i.getvalue(),
            file_name="Guca_A_Karoora_vs_Raawwii_Barattootaa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("Deetaan galmaa'e hin jiru.")
