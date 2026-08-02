with tabI:
            st.markdown("### I. Karoora vs Raawwii (Comparison - Tab A waliin wal fakkaatu)")
            if not db.empty:
                raw_comparison = []
                for k in range(1, 13):
                    k_str = str(k)
                    t_d = st.session_state.targets[k_str]["Dhiira"]
                    t_dh = st.session_state.targets[k_str]["Dhalaa"]
                    
                    sub_k = db[db["Kutaa"] == k_str]
                    a_d = len(sub_k[sub_k["Koorniyaa"] == "Dhiira"])
                    a_dh = len(sub_k[sub_k["Koorniyaa"] == "Dhalaa"])
                    
                    raw_comparison.append({
                        "Kutaa_Num": k_str,
                        "Kutaa": f"Kutaa {k}",
                        "Dhiira": f"Kar: {t_d} | Raw: {a_d}",
                        "Dhalaa": f"Kar: {t_dh} | Raw: {a_dh}",
                        "Ida'ama": f"Kar: {t_d+t_dh} | Raw: {a_d+a_dh}",
                        # Values for grouping calculation (Karoora fi Raawwii walitti dabaluudhaaf)
                        "Target_Dhiira": t_d,
                        "Target_Dhalaa": t_dh,
                        "Actual_Dhiira": a_d,
                        "Actual_Dhalaa": a_dh
                    })
                
                # Helper function to format Target vs Actual display strings
                def fmt_val(t_val, a_val):
                    return f"Kar: {t_val} | Raw: {a_val}"

                # Calculation for Group 1-6
                t_1_6_d = sum(r["Target_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                t_1_6_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                a_1_6_d = sum(r["Actual_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                a_1_6_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) <= 6)
                
                # Calculation for Group 7-8
                t_7_8_d = sum(r["Target_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                t_7_8_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                a_7_8_d = sum(r["Actual_Dhiira"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                a_7_8_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if 7 <= int(r["Kutaa_Num"]) <= 8)
                
                # Calculation for Group 9-12
                t_9_12_d = sum(r["Target_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                t_9_12_dh = sum(r["Target_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                a_9_12_d = sum(r["Actual_Dhiira"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)
                a_9_12_dh = sum(r["Actual_Dhalaa"] for r in raw_comparison if int(r["Kutaa_Num"]) >= 9)

                comp_final_table = []
                
                # 1. Kutaa 1 hanga 6 dhuunfaadhaan dabaluu
                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) <= 6:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                
                # Ida'ama Kutaa 1 - 6
                comp_final_table.append({
                    "Kutaa": "Ida'ama Kutaa 1 - 6", 
                    "Dhiira": fmt_val(t_1_6_d, a_1_6_d), 
                    "Dhalaa": fmt_val(t_1_6_dh, a_1_6_dh), 
                    "Ida'ama": fmt_val(t_1_6_d + t_1_6_dh, a_1_6_d + a_1_6_dh)
                })
                
                # 2. Kutaa 7 hanga 8 dhuunfaadhaan dabaluu
                for r in raw_comparison:
                    if 7 <= int(r["Kutaa_Num"]) <= 8:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                
                # Ida'ama Kutaa 7 - 8
                comp_final_table.append({
                    "Kutaa": "Ida'ama Kutaa 7 - 8", 
                    "Dhiira": fmt_val(t_7_8_d, a_7_8_d), 
                    "Dhalaa": fmt_val(t_7_8_dh, a_7_8_dh), 
                    "Ida'ama": fmt_val(t_7_8_d + t_7_8_dh, a_7_8_d + a_7_8_dh)
                })
                
                # Ida'ama Waliigalaa (1 - 8)
                comp_final_table.append({
                    "Kutaa": "Ida'ama Waliigalaa (1 - 8)", 
                    "Dhiira": fmt_val(t_1_6_d + t_7_8_d, a_1_6_d + a_7_8_d), 
                    "Dhalaa": fmt_val(t_1_6_dh + t_7_8_dh, a_1_6_dh + a_7_8_dh), 
                    "Ida'ama": fmt_val((t_1_6_d + t_7_8_d) + (t_1_6_dh + t_7_8_dh), (a_1_6_d + a_7_8_d) + (a_1_6_dh + a_7_8_dh))
                })

                # 3. Kutaa 9 hanga 12 dhuunfaadhaan dabaluu
                for r in raw_comparison:
                    if int(r["Kutaa_Num"]) >= 9:
                        comp_final_table.append({"Kutaa": r["Kutaa"], "Dhiira": r["Dhiira"], "Dhalaa": r["Dhalaa"], "Ida'ama": r["Ida'ama"]})
                
                # Ida'ama Kutaa 9 - 12
                comp_final_table.append({
                    "Kutaa": "Ida'ama Kutaa 9 - 12", 
                    "Dhiira": fmt_val(t_9_12_d, a_9_12_d), 
                    "Dhalaa": fmt_val(t_9_12_dh, a_9_12_dh), 
                    "Ida'ama": fmt_val(t_9_12_d + t_9_12_dh, a_9_12_d + a_9_12_dh)
                })

                # Waliigalaa (1 - 12)
                tot_t_d = t_1_6_d + t_7_8_d + t_9_12_d
                tot_t_dh = t_1_6_dh + t_7_8_dh + t_9_12_dh
                tot_a_d = a_1_6_d + a_7_8_d + a_9_12_d
                tot_a_dh = a_1_6_dh + a_7_8_dh + a_9_12_dh
                
                comp_final_table.append({
                    "Kutaa": "Waliigalaa (1 - 12)", 
                    "Dhiira": fmt_val(tot_t_d, tot_a_d), 
                    "Dhalaa": fmt_val(tot_t_dh, tot_a_dh), 
                    "Ida'ama": fmt_val(tot_t_d + tot_t_dh, tot_a_d + tot_a_dh)
                })

                comp_df = pd.DataFrame(comp_final_table)
                st.dataframe(comp_df, use_container_width=True)
            else:
                st.info("Deetaan galmaa'e hin jiru.")
