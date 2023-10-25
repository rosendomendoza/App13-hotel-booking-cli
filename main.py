import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotel():
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id

    def book(self):
        """Book a hotel by changing  its availability to 'no' """
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()

        if availability == "yes":
            return True
        else:
            return False

class ReservationTicket():
    def __init__(self, customer_name, hotel_object):
        pass

    def generate(self):
        pass



print(df)
hotel_ID = input("Enter Hotel id:")
hotel = Hotel(hotel_ID)

if hotel.available():
    hotel.book()
    customer_name = input("Enter your name: ")
    reservation_ticket = ReservationTicket(customer_name, hotel)
    print(reservation_ticket.generate())
else:
    print("Hotel is not available...")

