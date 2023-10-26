import pandas as pd

# df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


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
        database.update_available(self.hotel_id, "no")
        # df.loc[df["id"] == self.hotel_id, "available"] = "no"
        # df.to_csv("hotels.csv", index=False)

    def availability(self):
        """Check if the hotel is available"""
        # availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
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


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        credit_card = {'number': self.number, 'expiration': expiration,
                       'holder': holder, 'cvc': cvc}
        if credit_card in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_pass):
        password = df_card_security.loc[
            df_card_security['number'] == self.number, 'password'].squeeze()
        return password == given_pass


print(df)
hotel_ID = input("Enter Hotel id:")

if database.hotel_exist(df, hotel_ID):
    hotel = Hotel(hotel_ID)

    if hotel.availability():
        credit_card = SecureCreditCard("1234567890123456")

        if credit_card.validate("12/26", "JOHN SMITH", "123"):
            ccn = credit_card.number
            ccn = ccn[:3] + '*' * (len(ccn) - 6) + ccn[-3:]
            print(f"Credit Card Nr. {ccn} was validated...")

            if credit_card.authenticate(given_pass="mypass"):
                print(f"Credit Card Nr. {ccn} "
                      f"was authenticated...")
                hotel.book()
                customer_name = input("Reservation under (name): ")
                reservation_ticket = ReservationTicket(customer_name, hotel)
                print(reservation_ticket.generate())
            else:
                print("Credit Card Authentication Error...")
        else:
            input("There was a problem with your payment...")
    else:
        msg = f'The Hotel "{hotel.name}" in "{hotel.city}" is NOT Free'
        print(msg)
else:
    print(f"Hotel id: {hotel_ID} is not registered. Try again...")
