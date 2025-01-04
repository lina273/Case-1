import streamlit as st

# Session state for login and user functionality
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "guest"
if "selected_type" not in st.session_state:
    st.session_state.selected_type = "3D-Drucker" #Set 3D-Drucker as default
if "selected_device" not in st.session_state:
    st.session_state.selected_device = None

# General Login
st.sidebar.title("Login")
if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password") #Login logik muss mit Datenbank verknüpft werden wenn wir jeden user login ermöglichen wollen (nicht gefordert soweit verstanden) - Soukopf
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.session_state.user_role = "admin"
        elif username == "user" and password == "user":
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.success(f"Logged in as {st.session_state.user_role.capitalize()}")
    if st.session_state.user_role == "admin":
        if st.sidebar.button("Admin Optionen"):
            st.sidebar.write("Hier können Adminoptionen implementiert werden.")
        if st.sidebar.button("Neuen Maschinentyp hinzufügen"):
            st.sidebar.write("Maschinentyp hinzufügen-Funktionalität hier implementieren.")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = "guest"

# Main Page Layout
if st.session_state.selected_device is None:
    st.title("Geräteverwaltung")

    # Maschinentypen oben links
    st.subheader("Maschinentypen")
    cols = st.columns(len(types := ["3D-Drucker", "Laser-Cutter", "Fräsmaschine"])) # nur testweise muss typen aus datenbank beziehen - Soukopf
    for i, maschinentyp in enumerate(types):
        with cols[i]:
            if st.button(maschinentyp, key=f"type_{i}"):
                st.session_state.selected_type = maschinentyp

    # Maschinenanzeige als Felder
    st.subheader(f"Maschinenübersicht: {st.session_state.selected_type}")

    # Beispielgeräte nach Typ gruppiert
    all_devices = {
        "3D-Drucker": [
            {"name": "3D-Drucker 1", "image": "https://asset.conrad.com/media10/isa/160267/c1/-/de/003200727PI00/image.jpg?x=400&y=400&format=jpg&ex=400&ey=400&align=center", "status": "Aktiv"},
            {"name": "3D-Drucker 2", "image": "https://3dee.at/wp-content/uploads/2022/09/creality-ender-3-tiny.png", "status": "Inaktiv"},
        ],
        "Laser-Cutter": [
            {"name": "Laser-Cutter 1", "image": "https://omtechlaser.uk/cdn/shop/files/3_3485253b-573f-4169-b474-8b4a7d2abe3a.jpg?v=1716430665", "status": "Wartung"},
            {"name": "Laser-Cutter 2", "image": "https://lotus-laser.sirv.com/WP_www.lotuslaser.com/2020/10/Lotus-Laser-Systems-Blu125-100w-laser-cutting-machine-scaled.webp", "status": "Aktiv"},
        ],
        "Fräsmaschine": [
            {"name": "Fräsmaschine 1", "image": "https://www.holzmann-maschinen.at/uploadPim/199/001_bf1000ddro-400v-thumbnail-260-260.jpg", "status": "Aktiv"},
        ],
    } # Hier müssten die Geräte aus der Datenbank geladen werden - Soukopf

    columns = st.columns(4)
    devices = all_devices.get(st.session_state.selected_type, [])

    for idx, device in enumerate(devices):
        with columns[idx % 4]:
            st.write(f"**{device['name']}**")
            st.image(device["image"], use_container_width=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                status_color = "green" if device["status"] == "Aktiv" else ("red" if device["status"] == "Inaktiv" else "orange")
                st.markdown(
                    f"<div style='background-color:{status_color}; color:white; text-align:center; padding:5px;'>{device['status']}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                if st.button("Details", key=f"details_{device['name']}"):
                    st.session_state.selected_device = device

    # Hinzufügen-Funktionalität für Admins
    if st.session_state.user_role == "admin":
        with columns[len(devices) % 4]:
            st.write("Neue Maschine")
            st.image("https://i.otto.de/i/otto/996e0c7d-bc6e-4488-a30d-4863ff34b252/nintendo-nachttischlampe-super-mario-kart-fragezeichen-question-block-leuchte-lampe.jpg?$formatz$", use_container_width=True)
            st.button("+ Hinzufügen", key="add_device")
else:
    # Detailseite einer Maschine (Noch optimierungsbedarf... - Soukopf)
    device = st.session_state.selected_device
    st.title(device["name"])

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Reservierungen")
        st.write("- 01.01.2023 bis 02.01.2023: Projekt A von Benutzer X")
        st.write("- 03.01.2023 bis 04.01.2023: Projekt B von Benutzer Y")
        st.subheader("Wartungen")
        st.write("- 05.01.2023: Austausch von Teilen, Kosten: 100€")
        st.write("- 10.01.2023: Allgemeine Überprüfung, Kosten: 50€")
    with col2:
        st.image(device["image"], use_container_width=True)
        st.subheader("Zuständiger Benutzer")
        st.write("Max Mustermann")
        st.image("https://brings-online.com/demo/wordpress-theme-lexus/wp-content/uploads/2021/11/lexus-max-mustermann.jpg", use_container_width=True)

    if st.session_state.user_role == "admin":
        if st.button("Bearbeiten"):
            st.write("Hier könnte ein Bearbeitungsformular implementiert werden.")

    if st.button("Zurück"):
        st.session_state.selected_device = None
