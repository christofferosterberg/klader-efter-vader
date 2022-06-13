from flask import Flask

app = Flask(__name__, static_folder='client', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'

# db.init_app(app)

host = "http://localhost:3000"

@app.route("/")
def client():
    # return "<p>Hello, World!</p>"
    return app.send_static_file("client.html")

app.run(debug=True, port=3000)