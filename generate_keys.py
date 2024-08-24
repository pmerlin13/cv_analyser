import pickle
from pathlib import Path
import streamlit_authenticator as stauth 


#Users
names = ["Merlin Pineda", "Maurelys Jaquez"]
usernames = ["Pineda","Mau"]
passwords = ["abc123", "def456"]

#Hashed

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)