from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "votre_clé_secrète_très_complexe_ici"

bcrypt = Bcrypt(app)