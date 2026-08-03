# ============================================================================
# 7. EMIS DATA UPLOAD | RAGAA EMIS FE'UU
# ============================================================================
elif menu == "7. EMIS Data Upload | Ragaa EMIS Fe'uu":
    st.subheader("📤 EMIS Data Upload & Validation | Ragaa EMIS Fe'uu fi Mirkaneessuu")
    st.caption("""
    Upload EMIS data to compare with your app data and find mismatches.
    Ragaa EMIS fe'uu fi ragaa app keessanii wajjin walmadaaluu.
    """)
    
    st.info("""
    **📋 EMIS Data Requirements | Qabxii Ragaa EMIS:**
    - **Student Basic Data**: 
      - Column A: National ID (FAN ID)
      - Column C: Full Name (Maqaa Guutuu)
      - Column D: Father Name (Maqaa Abbaa)
      - Column E: Grandfather Name (Maqaa Akaakayyu)
      - Column G: Gender (Koorniyaa)
      - Column J: Date of Birth (Bara Dhalootaa)
      - Column K: Age (Umurii)
      - Column M: FAN ID (Alternative)
    - **Student Result Data**:
      - Column A: National ID (Student ID)
      - Column C: Grade (Kutaa)
      - Column D: Average Score (Avireejjii Qabxii)
    """)
    
    # File upload section
    st.markdown("### 📂 Upload EMIS Data | Ragaa EMIS Fe'uu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        basic_file = st.file_uploader(
            "📄 Student Basic Data | Ragaa Bu'uuraa (Column A = National ID)",
            type=['xlsx', 'xls'],
            key="emis_basic"
        )
    
    with col2:
        result_file = st.file_uploader(
            "📄 Student Result Data | Ragaa Qabxii (Column A = National ID)",
            type=['xlsx', 'xls'],
            key="emis_result"
        )
    
    if basic_file and result_file:
        st.markdown("---")
        st.markdown("### 🔍 Processing & Validation | Qindeessuu fi Mirkaneessuu")
        
        with st.spinner("Processing EMIS data... | Ragaa EMIS qindeessaa..."):
            # Load both files
            basic_df = load_emis_data(basic_file, "basic")
            result_df = load_emis_data(result_file, "result")
            
            if basic_df is not None and result_df is not None:
                # Parse data
                parsed_basic = parse_student_basic_data(basic_df)
                parsed_result = parse_student_result_data(result_df)
                
                if parsed_basic is not None and parsed_result is not None:
                    # Merge data using National ID
                    emis_data = pd.merge(parsed_basic, parsed_result, on=['National ID'], how='left')
                    
                    # Display EMIS data preview
                    st.markdown("#### 📊 EMIS Data Preview | Raawwii Ragaa EMIS")
                    st.dataframe(emis_data.head(10), use_container_width=True)
                    
                    # Show National ID statistics
                    national_id_count = emis_data['National ID'].notna().sum()
                    total_count = len(emis_data)
                    st.metric("Students with National ID | Barattoota National ID Qaban", 
                             f"{national_id_count}/{total_count}")
                    
                    # Load current app data
                    app_db = load_students()
                    
                    if not app_db.empty:
                        # Compare data
                        comparison_result = compare_with_emis(emis_data, app_db)
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### 📊 Comparison Results | Bu'aa Walmadaaluu")
                        
                        # Summary metrics
                        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                        with col_m1:
                            st.metric("✅ Matches | Walfakkaataa", len(comparison_result['matches']))
                        with col_m2:
                            st.metric("⚠️ Mismatches | Walgaraa", len(comparison_result['mismatches']))
                        with col_m3:
                            st.metric("📤 EMIS Only | EMIS Qofa", len(comparison_result['emis_not_in_app']))
                        with col_m4:
                            st.metric("📥 App Only | App Qofa", len(comparison_result['app_not_in_emis']))
                        
                        # Display mismatches
                        if comparison_result['mismatches']:
                            st.markdown("---")
                            st.markdown("### ⚠️ Data Mismatches Found | Walgaraa Argame")
                            st.warning("""
                            The following students have data that doesn't match EMIS.
                            Barattoota armaan gadii EMIS wajjin wal hin simne.
                            """)
                            
                            mismatch_data = []
                            for item in comparison_result['mismatches']:
                                mismatch_fields = ', '.join(item['mismatch_fields'].keys())
                                mismatch_data.append({
                                    'National ID': item.get('national_id', ''),
                                    'Maqaa Guutuu': item['emis_data'].get('Maqaa Guutuu', ''),
                                    'Kutaa': item['emis_data'].get('Kutaa', ''),
                                    'Koorniyaa': item['emis_data'].get('Koorniyaa', ''),
                                    'EMIS Avireejjii': item['emis_data'].get('Avireejjii Qabxii', ''),
                                    'App Avireejjii': item['app_data'].get('Avireejjii Qabxii', ''),
                                    'Mismatch Fields | Walgaraa': mismatch_fields
                                })
                            
                            mismatch_df = pd.DataFrame(mismatch_data)
                            st.dataframe(mismatch_df, use_container_width=True)
                            
                            # Allow user to update mismatched data
                            st.markdown("---")
                            st.markdown("### ✏️ Fix Mismatches | Walgaraa Fooyyeessuu")
                            st.info("""
                            Select a student below to update their data with EMIS values.
                            Barataa armaan gadii filadhuun odeeffannoo EMIS wajjin fooyyeessuu.
                            """)
                            
                            mismatch_options = []
                            for item in comparison_result['mismatches']:
                                name = item['emis_data'].get('Maqaa Guutuu', 'Unknown')
                                national_id = item.get('national_id', 'No ID')
                                mismatch_options.append(f"{name} ({national_id})")
                            
                            if mismatch_options:
                                selected_mismatch = st.selectbox(
                                    "Select student to fix | Barataa fooyyeessuuf filadhu:",
                                    mismatch_options
                                )
                                
                                if selected_mismatch:
                                    selected_name = selected_mismatch.split(' (')[0]
                                    for item in comparison_result['mismatches']:
                                        if item['emis_data'].get('Maqaa Guutuu', '') == selected_name:
                                            emis_row = item['emis_data']
                                            app_row = item['app_data']
                                            
                                            st.markdown(f"#### 📝 Update: {selected_name}")
                                            
                                            with st.form("update_emis_mismatch"):
                                                col_u1, col_u2 = st.columns(2)
                                                
                                                with col_u1:
                                                    new_name = st.text_input("Full Name | Maqaa Guutuu", value=emis_row.get('Maqaa Guutuu', ''))
                                                    new_gender = st.selectbox("Gender | Koorniyaa", ["Dhiira", "Dhalaa"], 
                                                                             index=0 if emis_row.get('Koorniyaa', '') == "Dhiira" else 1)
                                                    new_dob = st.text_input("Date of Birth | Bara Dhalootaa", value=emis_row.get('Bara Dhalootaa', ''))
                                                
                                                with col_u2:
                                                    new_age = st.number_input("Age | Umurii", 
                                                                             value=int(emis_row.get('Umurii', 0)) if str(emis_row.get('Umurii', '')).isdigit() else 0)
                                                    new_score = st.number_input("Average Score | Avireejjii Qabxii", 
                                                                               value=float(emis_row.get('Avireejjii Qabxii', 0)) if str(emis_row.get('Avireejjii Qabxii', '')).replace('.', '').isdigit() else 0.0)
                                                    new_fan = st.text_input("FAN ID", value=emis_row.get('FAN ID', ''))
                                                
                                                submit_update = st.form_submit_button("💾 Update with EMIS Data | Odeeffannoo EMIS Fooyyeessi")
                                                
                                                if submit_update:
                                                    # Find student ID in app
                                                    app_row_id = app_row.get('id')
                                                    if app_row_id:
                                                        update_student_from_emis(app_row_id, {
                                                            'Maqaa Guutuu': new_name,
                                                            'Koorniyaa': new_gender,
                                                            'Bara Dhalootaa': new_dob,
                                                            'Umurii': new_age,
                                                            'Avireejjii Qabxii': new_score,
                                                            'FAN ID': new_fan
                                                        })
                                                        st.success(f"✅ Student {new_name} updated successfully! | Barataan {new_name} fooyya'eera!")
                                                        st.rerun()
                                                    else:
                                                        st.error("Student not found in database. Barataan database keessa hin jiru.")
                        
                        # Show EMIS only students
                        if comparison_result['emis_not_in_app']:
                            st.markdown("---")
                            st.markdown("### 📤 Students in EMIS but not in App | Barattoota EMIS keessa jiran garuu App keessa hin jiranne")
                            st.info("""
                            These students are in EMIS but not in your app. You can register them directly.
                            Barattoonni kun EMIS keessa jiru garuu App keessa hin jiran. Isaan galmeessuu dandeessu.
                            """)
                            
                            emis_only_df = pd.DataFrame([{
                                'National ID': item.get('national_id', ''),
                                'Maqaa Guutuu': item['data'].get('Maqaa Guutuu', ''),
                                'Kutaa': item['data'].get('Kutaa', ''),
                                'Koorniyaa': item['data'].get('Koorniyaa', ''),
                                'FAN ID': item['data'].get('FAN ID', '')
                            } for item in comparison_result['emis_not_in_app']])
                            
                            st.dataframe(emis_only_df, use_container_width=True)
                            
                            # Option to add EMIS only students to app
                            if st.button("📥 Add EMIS Only Students to App | Barattoota EMIS Qofaa Appitti Galchi"):
                                st.warning("This feature is under development. Please use the registration form.")
                        
                        # Show App only students
                        if comparison_result['app_not_in_emis']:
                            st.markdown("---")
                            st.markdown("### 📥 Students in App but not in EMIS | Barattoota App keessa jiran garuu EMIS keessa hin jiranne")
                            st.warning("""
                            These students are in your app but not in EMIS. They may need to be uploaded to EMIS.
                            Barattoonni kun App keessa jiru garuu EMIS keessa hin jiran. EMIS keessatti galmeessuu qabdu.
                            """)
                            
                            app_only_df = pd.DataFrame([{
                                'Maqaa Guutuu': item['data'].get('Maqaa Guutuu', ''),
                                'Kutaa': item['data'].get('Kutaa', ''),
                                'Koorniyaa': item['data'].get('Koorniyaa', ''),
                                'FAN ID': item['data'].get('FAN ID', '')
                            } for item in comparison_result['app_not_in_emis']])
                            
                            st.dataframe(app_only_df, use_container_width=True)
                        
                        # Export results
                        st.markdown("---")
                        st.markdown("### 📥 Export Results | Bu'aa Baasuu")
                        
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            if comparison_result['mismatches']:
                                pd.DataFrame(mismatch_data).to_excel(writer, sheet_name='Mismatches', index=False)
                            if comparison_result['emis_not_in_app']:
                                emis_only_df.to_excel(writer, sheet_name='EMIS Only', index=False)
                            if comparison_result['app_not_in_emis']:
                                app_only_df.to_excel(writer, sheet_name='App Only', index=False)
                            if comparison_result['matches']:
                                pd.DataFrame([item['data'] for item in comparison_result['matches']]).to_excel(writer, sheet_name='Matches', index=False)
                        
                        st.download_button(
                            label="📥 Download Complete Comparison Report | Gabaasa Walmadaaluu Guutuu Buqqisaa",
                            data=output.getvalue(),
                            file_name=f"EMIS_Comparison_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                    else:
                        st.warning("No data found in the app database. Please register some students first.")
            else:
                st.error("Failed to parse EMIS data. Please check the file format.")
    else:
        st.info("Please upload both Basic Data and Result Data files.")
