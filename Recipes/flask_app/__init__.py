from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # مهم لأمان الجلسات

# تهيئة الحماية

bcrypt = Bcrypt(app)