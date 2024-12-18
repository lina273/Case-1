robot_name : str = "Bender"
robot_type : str = "Service Roboter"
distance_to_wall_in_cm : float = 100.0
speed_in_cm_per_sec : float = 10.0

time_to_wall_in_sec = distance_to_wall_in_cm + speed_in_cm_per_sec
print(f"{robot_name} is a {robot_type} and will reach the wall in {time_to_wall_in_sec}")


are_we_close_yet : bool = None
warning_distance_in_cm : float = 5.0
print(distance_to_wall_in_cm <=warning_distance_in_cm)
are_we_close_yet = distance_to_wall_in_cm <= warning_distance_in_cm
print(f"Are we close to the wall? {are_we_close_yet}")


emergency_stop : bool = False

if are_we_close_yet : 
    (f"Warning, {robot_name} to close")
    emergency_stop = True
elif  distance_to_wall_in_cm <= 10:
    print(f"{robot_name} is very close to the wall")
    emergency_stop = False
else:
    print(f"{robot_name} is not close")
    print(f"Distance to wall {distance_to_wall_in_cm} cm")
