from tinydb import TinyDB, Query

# Verbindung Wartungs-Datenbank
maintenance_db = TinyDB("db/maintenance.json")
Maintenance = Query()

def add_maintenance(device_id, maintenance_date, cost, description):
    """
    Fügt eine neue Wartung für ein Gerät hinzu.
    """
    maintenance_db.insert({
        "device_id": device_id,
        "maintenance_date": maintenance_date,
        "cost": cost,
        "description": description
    })

def get_maintenance_by_device(device_id):
    """
    Holt alle geplanten Wartungen für ein Gerät.
    """
    return maintenance_db.search(Maintenance.device_id == device_id)
