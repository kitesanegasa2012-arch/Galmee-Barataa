with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
        maqaa_guutuu = st.text_input("1. Maqaa Guutuu Barataa", value=st.session_state.form_maqaa)
        koorniyaa = st.selectbox("2. Koorniyaa", ["Filadhu", "Dhiira", "Dhalaa"])

        grade_col1, grade_col2 = st.columns(2)
        kutaa = grade_col1.selectbox("3. Kutaa", [str(i) for i in range(1, 13)])
        daree = grade_col2.selectbox("Daree (Section)", [chr(65 + i) for i in range(11)])

        st.markdown("**4. Bara Dhalootaa (Akka Lakkoofsa Itoophiyaatti)**")
        b_col1, b_col2, b_col3 = st.columns(3)
        b_guyyaa = b_col1.selectbox("Guyyaa", [str(i) for i in range(1, 32)])
        b_jiia = b_col2.selectbox(
            "Ji'a",
            [
                "Fulbaana", "Onkololeessa", "Sadaasa", "Muddee",
                "Amajjii", "Guraandhala", "Bitootessa", "Ebla", "Caamsaa",
                "Waxabajjii", "Adoolessa", "Hagayya", "Pagumee",
            ],
        )
        b_bara = b_col3.number_input(
            "Bara Dhalootaa (Fkn: 2011)", min_value=1990, max_value=2025, value=2011
        )
        current_et_year = 2018
        umurii = current_et_year - b_bara

        st.text_input("5. Haala Galmee (Filatame)", value=haala_galmee, disabled=True)

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
        st.markdown("**9. Bakka Dhalootaa** _(galmee dabre irraa ofumaan bahe)_")
        godina = st.text_input("Godina", value=default_godina)
        aanaa = st.text_input("Aanaa", value=default_aanaa)
        ganda = st.text_input("Ganda", value=default_ganda)

        maqaa_haadhaa = st.text_input(
            "10. Maqaa Guutuu Haadhaa ykn Guddistuu",
            value=st.session_state.form_haadhaa,
        )
        fan_id = st.text_input(
            "11. Lakkoofsa Waraqaa Eenyummaa Dijitaalaa (FAN ID - Digiti 16)",
            value=st.session_state.form_fan,
        )
        lakk_bilbila_barataa = st.text_input(
            "12. Lakkoofsa Bilbila Barataa (+251...)",
            value=st.session_state.form_p_barataa,
        )
        lakk_bilbila_maatii = st.text_input(
            "13. Lakkoofsa Bilbila Maatii (+251...)",
            value=st.session_state.form_p_maatii,
        )
        st.markdown("---")
        st.markdown("**14. Mana Barumsaa Duraan Itti Barachaa Ture / Biroo**")

        # --- SIRREEFFAMA (item 2) ---
        # Haala galmee "Mana Barumsaa Biroo" ykn "Irra deebii Mana Barumsaa Biroo"
        # yoo TA'E QOFA barataan maqaa mana barumsaa haaraa akka barreessu gaafatama.
        # Haalota kaan hunda keessatti (haaraa, darbe, irra deebii kufe, irra deebii,
        # kute) maqaan mana barumsaa kan jalqaba save ta'e ofumaan ni bahaaf.
        if haala_galmee not in [
            "Mana Barumsaa Biroo",
            "Irra deebii Mana Barumsaa Biroo",
        ]:
            saved_name = st.session_state.get("saved_school_name", "")
            if saved_name:
                st.info(f"Maqaan Mana Barumsaa Ofumaan Guutame: **{saved_name}**")
                mb_duraan = saved_name
            else:
                # Yeroo jalqabaaf (saved_school_name kan hin jirre) barataan mataan isaa haa galchu
                mb_duraan = st.text_input(
                    "Maqaa Mana Barumsaa (Dursee kan barachaa ture)",
                    value=st.session_state.get("form_mb_biroo", ""),
                )
        else:
            mb_duraan = st.text_input(
                "Maqaa Mana Barumsaa Biroo (Mana barumsaa barataan irraa dhufe)",
                value=st.session_state.get("form_mb_biroo", ""),
            )

        avireejjii = st.number_input(
            "15. Avireejjii Qabxii Bara Darbee (0 - 100)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
        )
        barsiisaa = st.text_input("16. Barsiisaa Galmeessee", value=default_barsiisaa)
        guyyaa_galmee_ec = st.text_input("Guyyaa Galmee (E.C)", value=default_guyyaa)

    submitted = st.form_submit_button("💾 Save (Enter)")

if submitted:
    st.session_state.form_maqaa = maqaa_guutuu
    st.session_state.form_fan = fan_id
    st.session_state.form_p_barataa = lakk_bilbila_barataa
    st.session_state.form_p_maatii = lakk_bilbila_maatii
    st.session_state.form_haadhaa = maqaa_haadhaa
    st.session_state.form_mb_biroo = mb_duraan
    error_msgs = []

    if not maqaa_guutuu:
        error_msgs.append("Maqaa Guutuu barataa guuti!")
    if koorniyaa == "Filadhu":
        error_msgs.append("Maaloo Koorniyaa barataa filadhu!")

    if avireejjii < 50 and haala_galmee != "Irra deebii (Kufe)":
        error_msgs.append(
            'Barataan avireejjii 50 gadi fide, haala galmeen "Irra deebii (Kufe)" jedhu wajjin walsimuu qaba!'
        )

    clean_fan = fan_id.strip()
    if clean_fan and (not clean_fan.isdigit() or len(clean_fan) != 16):
        error_msgs.append("FAN ID dijiitii 16 qofa ta'uu qaba!")

    def validate_phone(phone_str, field_label):
        p = phone_str.strip()
        if not p.startswith("+251"):
            return f"{field_label}: Lakkoofsi bilbilaa '+251' tiin jalqabuu qaba!"
        subscriber_part = p[4:]
        if len(subscriber_part) != 9 or not subscriber_part.isdigit():
            return f"{field_label}: Koodii biyyaa itti aansuun lakkoofsi jiru dijiitii 9 qofa ta'uu qaba."
        return None

    if lakk_bilbila_barataa.strip():
        err_p1 = validate_phone(lakk_bilbila_barataa, "Bilbila Barataa")
        if err_p1:
            error_msgs.append(err_p1)

    if lakk_bilbila_maatii.strip():
        err_p2 = validate_phone(lakk_bilbila_maatii, "Bilbila Maatii")
        if err_p2:
            error_msgs.append(err_p2)

    if error_msgs:
        for err in error_msgs:
            st.markdown(
                f'<p style="color:red; font-weight:bold;">⚠️ {err}</p>',
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

        insert_student(new_data)

        # --- SIRREEFFAMA (item 1) ---
        # Maqaan mana barumsaa kun amma dhugumatti "save" ta'ee session_state keessatti
        # kaa'ama -- kanaafuu galmee itti aanutti (barataa/waggaa itti aanutti) ofumaan bahaaf.
        # - Yoo haala galmeen "Mana Barumsaa Biroo" ykn "Irra deebii Mana Barumsaa Biroo" ta'e,
        #   maqaan haaraa kun kan ittiin fuula duraatti fayyadamnu ta'a.
        # - Yoo haalonni kaan (haaraa, darbe, kufe, irra deebii, kute) ta'anii fi duraan
        #   maqaan hin save hin taane ta'e, amma kan barataan galchee sana save godha.
        if haala_galmee in ["Mana Barumsaa Biroo", "Irra deebii Mana Barumsaa Biroo"]:
            st.session_state.saved_school_name = mb_duraan
        elif not st.session_state.get("saved_school_name", ""):
            st.session_state.saved_school_name = mb_duraan

        st.session_state.form_maqaa = ""
        st.session_state.form_fan = ""
        st.session_state.form_p_barataa = ""
        st.session_state.form_p_maatii = ""
        st.session_state.form_haadhaa = ""
        st.session_state.form_mb_biroo = ""

        st.success(f"Galmeen barataa {maqaa_guutuu} milkaa'inaan *Save* ta'eera!")
