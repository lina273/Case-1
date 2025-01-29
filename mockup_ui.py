from Modules.reservations import add_reservation, get_reservations_by_device
from Modules.maintenance import add_maintenance, get_maintenance_by_device


import streamlit as st
from tinydb import TinyDB, Query
from Modules.serializer import db
from datetime import datetime
import pandas as pd


##Funktionen in seperate datei auslagern - Soukopf

# Initialize database
Device = Query()
user_db = TinyDB('db/users.json')
User = Query()

def add_device(device_id, name, responsible_person, creation_date, status, image_url, device_type):
    db.insert({
        'id': device_id,
        'name': name,
        'responsible_person': responsible_person,
        'creation_date': creation_date,
        'status': status,
        'image': image_url,
        'type': device_type
    })

def get_devices_by_type(device_type):
    return db.search(Device.type == device_type)

def update_device_status(name, new_status):
    db.update({'status': new_status}, Device.name == name)

def get_all_users():
    return user_db.all()

def add_user(username, name, img_link):
    user_db.insert({
        'username': username,
        'name': name,
        'img_link': img_link
    })

def update_user(username, field, value):
    user_db.update({field: value}, User.username == username)


#State diagramm erstellen - Soukopf

# Session state for login and user functionality
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "guest"
if "selected_type" not in st.session_state:
    st.session_state.selected_type = "3D-Drucker" # Set 3D-Drucker as default
if "selected_device" not in st.session_state:
    st.session_state.selected_device = None
if "adding_device" not in st.session_state:
    st.session_state.adding_device = False
if "managing_users" not in st.session_state:
    st.session_state.managing_users = False

# General Login
if st.sidebar.button("Geräteverwaltung"):
            st.session_state.adding_device = False
            st.session_state.selected_device = None
            st.rerun()
st.sidebar.button("Home")
if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
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
        if st.sidebar.button("Userverwaltung"):
            st.session_state.managing_users = True

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = "guest"

# Main Page Layout
if st.session_state.managing_users:
    st.title("Userverwaltung")

    users = get_all_users()
    user_df = pd.DataFrame(users)

    if not user_df.empty:
        edited_df = st.data_editor(user_df, key="user_editor")
        for index, row in edited_df.iterrows():
            for column in user_df.columns:
                if row[column] != users[index].get(column):
                    update_user(users[index]['username'], column, row[column])

    st.subheader("Neuen Benutzer hinzufügen")
    new_username = st.text_input("Username:")
    new_name = st.text_input("Name:")
    new_img_link = st.text_input("Bild-URL (1:1 Format):")

    if st.button("Benutzer speichern"):
        if new_username and new_name and new_img_link:
            add_user(new_username, new_name, new_img_link)
            st.success("Benutzer erfolgreich hinzugefügt!")
            st.rerun()
        else:
            st.error("Bitte alle Felder ausfüllen.")

    if st.button("Zurück"):
        st.session_state.managing_users = False
        st.rerun()
elif st.session_state.adding_device:
    st.title(f"Neues Gerät hinzufügen: {st.session_state.selected_type}")
    device_id = st.text_input("ID:")
    model = st.text_input("Model:")
    responsible_person = st.selectbox("Verantwortliche Person:", [user['name'] for user in get_all_users()])
    creation_date = st.date_input("Erstellungsdatum:", datetime.now())
    status = st.selectbox("Status:", ["Aktiv", "Wartung", "Reserviert", "Defekt", "Standby"])
    image_url = st.text_input("Bild-URL (1:1 Format):")

    if st.button("Speichern"):
        if not image_url:
            st.error("Bild-URL darf nicht leer sein.")
        else:
            add_device(device_id, model, responsible_person, creation_date.strftime("%Y-%m-%d"), status, image_url, st.session_state.selected_type)
            st.success("Gerät erfolgreich hinzugefügt!")
            st.session_state.adding_device = False
            st.rerun()

    if st.button("Abbrechen"):
        st.session_state.adding_device = False
        st.rerun()
elif st.session_state.selected_device is None:
    st.title("Geräteverwaltung")

    # Maschinentypen oben links
    st.subheader("Maschinentypen")
    cols = st.columns(len(types := ["3D-Drucker", "Laser-Cutter", "Fräsmaschine"]))
    for i, maschinentyp in enumerate(types):
        with cols[i]:
            if st.button(maschinentyp, key=f"type_{i}"):
                st.session_state.selected_type = maschinentyp

    # Maschinenanzeige als Felder
    st.subheader(f"Maschinenübersicht: {st.session_state.selected_type}")

    devices = get_devices_by_type(st.session_state.selected_type)

    columns = st.columns(4)
    for idx, device in enumerate(devices):
        with columns[idx % 4]:
            st.write(f"**{device['name']}**")
            if "image" in device and device["image"]:
                st.image(device["image"], use_container_width=True)
            else:
                st.error("Kein Bild verfügbar.")
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
            if st.button("+ Hinzufügen", key="add_device"):
                st.session_state.adding_device = True
else:
   device = st.session_state.selected_device
st.title(device["name"])

# Reservierungen anzeigen
st.subheader("📆 Reservierungen")
reservations = get_reservations_by_device(device["id"])
if reservations:
    for res in reservations:
        st.write(f"📅 {res['start_date']} bis {res['end_date']}: {res['user']}")
else:
    st.write("🔍 Keine Reservierungen für dieses Gerät.")

# Neue Reservierung hinzufügen (nur Admins)
if st.session_state.user_role == "admin":
    st.subheader("➕ Neue Reservierung hinzufügen")
    start_date = st.date_input("Startdatum")
    end_date = st.date_input("Enddatum")
    user = st.text_input("Reserviert von:")

    if st.button("Reservierung speichern"):
        if add_reservation(device["id"], user, str(start_date), str(end_date)):
            st.success("✅ Reservierung erfolgreich gespeichert!")
            st.rerun()
        else:
            st.error("⚠️ Fehler: Gerät ist bereits in diesem Zeitraum reserviert!")

# Wartungen anzeigen
st.subheader("🛠️ Wartungen")
maintenances = get_maintenance_by_device(device["id"])
if maintenances:
    for m in maintenances:
        st.write(f"🛠️ {m['maintenance_date']}: {m['description']}, Kosten: {m['cost']}€")
else:
    st.write("🔍 Keine geplanten Wartungen.")

# Neue Wartung 
if st.session_state.user_role == "admin":
    st.subheader(" Neue Wartung hinzufügen")
    maintenance_date = st.date_input("Wartungsdatum")
    cost = st.number_input("Kosten (€)", min_value=0)
    description = st.text_input("Beschreibung")

    if st.button("Wartung speichern"):
        add_maintenance(device["id"], str(maintenance_date), cost, description)
        st.success("Wartung erfolgreich gespeichert!")
        st.rerun()




    col1, col2 = st.columns([2, 2])
    with col1:
        st.subheader("Maschineninformationen")
        st.write(f"**Typ:** {device.get('type', 'Nicht angegeben')}")
        st.write(f"**Model:** {device.get('name', 'Nicht angegeben')}")
        st.write(f"**Status:** {device.get('status', 'Nicht angegeben')}")
        st.write(f"**Erstellungsdatum:** {device.get('creation_date', 'Nicht angegeben')}")
        st.image(device["image"], use_container_width=True, width=20)

    with col2:
        st.subheader("Zuständiger Benutzer")
        responsible_user = user_db.search(User.name == device['responsible_person'])
        if responsible_user:
            user = responsible_user[0]
            st.image(user['img_link'], use_container_width=True, width=20)
            st.write(f"**Username:** {user.get('username', 'Nicht angegeben')}")
            st.write(f"**Name:** {user.get('name', 'Nicht angegeben')}")
        else:
            st.write("Kein zuständiger Benutzer gefunden.")

    if st.session_state.user_role == "admin":
        if st.button("Bearbeiten"):
            st.write("Hier könnte ein Bearbeitungsformular implementiert werden.")

    if st.button("Zurück"):
        st.session_state.selected_device = None