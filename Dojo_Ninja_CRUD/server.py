from flask_app import app 
from flask_app.controllers import Dojos, Ninjas 

if __name__ == "__main__":
    app.run(debug=True)