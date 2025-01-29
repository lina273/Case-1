from tinydb import TinyDB, Query

# Verbindung zur Datenbank
reservations_db = TinyDB("db/reservations.json")
Reservation = Query()

def add_reservation(device_id, user, start_date, end_date):
    """
    Fügt eine neue Reservierung hinzu, falls keine Überschneidung existiert.
    """
    # Prüfen Überschneidung 
    existing = reservations_db.search(
        (Reservation.device_id == device_id) &
        (Reservation.start_date <= end_date) &
        (Reservation.end_date >= start_date)
    )
    if existing:
        return False  # Kollision mit bestehender Reservierung!

    # Neue Reservierung speichern
    reservations_db.insert({
        "device_id": device_id,
        "user": user,
        "start_date": start_date,
        "end_date": end_date
    })
    return True

def get_reservations_by_device(device_id):
    """
    Holt alle Reservierungen für ein bestimmtes Gerät.
    """
    return reservations_db.search(Reservation.device_id == device_id)
