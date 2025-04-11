from flask import Flask


app = Flask(__name__)
app.secret_key = "une_clé_très_secrète_et_unique" 