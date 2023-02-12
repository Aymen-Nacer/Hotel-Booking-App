import pandas
df = pandas.read_csv("hotels.csv", dtype={"id" : str})
df_cards = pandas.read_csv("cards.csv", dtype = str).to_dict(orient= "records")
df_cards_security = pandas.read_csv("card-security.csv", dtype=str)


class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()



    def book(self):
        """"book an hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = 'no'
        df.to_csv("hotels.csv" , index=False)


    def available(self):
        """ check if the hotel is available"""
        available = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if available == 'yes':
            return True
        else:
            return False



class ReservationTicket:
    def __init__(self, customer_name, hotel):
        self.customer_name = customer_name
        self.hotel = hotel


    def generate(self):
        content = f"""
                Thank your for reservation! 
                Your booking data:
                Name: {self.customer_name}
                Hotel Name : {self.hotel.hotel_name}
                """

        return content


class CreditCard:
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self, expiration_date, holder, cvc ):
        card_data = {"number": self.card_number, "expiration": expiration_date,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.card_number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False



print(df)
hotel_id = input("Enter the id of the hotel:")
hotel = Hotel(hotel_id)
if hotel.available():
    credit_card = SecureCreditCard(card_number="1234567890123456")
    if credit_card.validate(expiration_date="12/26", holder="Aymen Nacer", cvc = "123" ):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            customer_name = input("Please Enter your name: ")
            reservationTicket = ReservationTicket(customer_name, hotel)
            print(reservationTicket.generate())
        else:
            print("Authentication has failed")
    else:
        print("There was a problem with your payment")
else:
    print("hotel is not available")