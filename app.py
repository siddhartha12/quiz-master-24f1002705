from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_details():
    return render_template('registered.html')

if __name__ == '__main__':
    app.run(debug=True)