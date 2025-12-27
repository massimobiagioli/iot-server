import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.lib.passwords import hash_password
from dotenv import load_dotenv

USERNAME = "admin"
PASSWORD = "admin123"
FIRSTNAME = "Admin"
LASTNAME = "User"
ROLE = "admin"

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

user = User(
    username=USERNAME, 
    password=hash_password(PASSWORD), 
    firstname=FIRSTNAME, 
    lastname=LASTNAME, 
    role=ROLE
)

session.add(user)
session.commit()
session.close()

print(f"Admin user '{USERNAME}' created.")
