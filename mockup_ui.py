import streamlit as st

st.title("Geräteverwaltung")

# Geräteliste (Platzhalterdaten)
devices = ["3D-Drucker", "Laser-Cutter", "Fräsmaschine"]

# Auswahl eines Geräts
selected_device = st.selectbox("Gerät auswählen", devices)

# Geräteinformationen anzeigen
if selected_device:
    st.write(f"Informationen zu: {selected_device}")
    st.text_input("Verantwortlicher", placeholder="Name der verantwortlichen Person")
    st.date_input("Nächste Wartung")
    st.button("Speichern")

st.write("ToDo: Authentifizierung, Datenbankanbindung, ...")