class User:

    def __init__ (self,user_id,user_name):
        self.user_id=user_id
        self.user_name=user_name

    def __str__(self):
        return f"{self.name} ({self.user_id})"
    
    ##def


class Device:
    def __init__(self, device_id: int, device_name: str, responsible_person: User, maintenance_interval: int, maintenance_cost: float):
        self.device_id = device_id
        self.device_name = device_name
        self.responsible_person = responsible_person
        ## self.__last_update = 
        ## self.__creation_date = 
        ##self.end_of_life = 
        ##self.first_maintenance = 
        ##self.next_maintenance = 
        ##self.__maintenance_interval = 
        ##self.__maintenance_cost = 


    def __str__(self):
        return f"Device {self.device_name} (Responsible: {self.responsible_person.name})"


class Reservation:
    def __init__(self, device_name, user_name, start_time, end_time):
        self.device_name = device_name
        self.user_name = user_name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return



        
