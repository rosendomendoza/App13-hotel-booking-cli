import pandas as pd

#df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotel():
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        # Load the rest of the hotel information
        info_hotel = df.loc[df["id"] == self.hotel_id]
        self.name = info_hotel["name"].squeeze()
        self.city = info_hotel["city"].squeeze()
        self.capacity = info_hotel["capacity"].squeeze()
        self.available = info_hotel["available"].squeeze()


    def book(self):
        """Book a hotel by changing  its availability to 'no' """
        self.available = "no"
        database.update_available(self.hotel_id,"no")
        #df.loc[df["id"] == self.hotel_id, "available"] = "no"
        #df.to_csv("hotels.csv", index=False)

    def availability(self):
        """Check if the hotel is available"""
        #availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return self.available == "yes"


class ReservationTicket():
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        ticket = f"""
         *** RESERVATION HOTEL ***
         Hotel: {self.hotel.name}
         City: {self.hotel.city}
         Customer: {self.customer_name}
        """
        return ticket

class Database():
    def __init__(self, pathfile):
        self.pathfile = pathfile

    def open(self):
        return pd.read_csv(self.pathfile, dtype={"id": str})

    def hotel_exist(self, df, hotel_id):
        return len(df.loc[df["id"] == hotel_id]) != 0
    def update_available(self, hotel_id, new_value):
        df.loc[df["id"] == hotel_id, "available"] = new_value
        df.to_csv(self.pathfile, index=False)


database = Database("hotels.csv")
df = database.open()

print(df)
hotel_ID = input("Enter Hotel id:")

if database.hotel_exist(df, hotel_ID):
    hotel = Hotel(hotel_ID)

    if hotel.availability():
        hotel.book()
        customer_name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(customer_name, hotel)
        print(reservation_ticket.generate())
    else:
        msg = f'The Hotel "{hotel.name}" in "{hotel.city}" is NOT Free'
        print(msg)
else:
    print(f"Hotel id: {hotel_ID} is not registered. Try again...")
