from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['luxious']

try:
    db.products.insert_many([
    {
        "name": "Iphone 15",
        "description": "This is the new Iphone 15",
        "price": 1999,
        "image_url": "https://www.apple.com/newsroom/images/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/tile/Apple-iPhone-15-Pro-lineup-hero-230912.jpg.news_app_ed.jpg"
    },
    {
        "name": "Nike Air Jordan",
        "description": "This is the new Nike Air Jordan",
        "price": 2999,
        "image_url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.architecturaldigest.com%2Fstory%2Fnikes-senior-designer-explains-what-went-into-new-air-jordan&psig=AOvVaw3AS6fQkP4D6Vr905YgNdVg&ust=1749052474635000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPjy9q3O1Y0DFQAAAAAdAAAAABAE"
    }
    ])

    print("insertion successful")

except Exception as e:
    print("Insertion failed")