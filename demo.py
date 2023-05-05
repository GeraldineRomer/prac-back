from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def greetings():
    return "Hello Backend developers!"

@app.route('/config')
def get_config():
    config = {
        'environment': app.config['ENVIRONMENT'],
        'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
        'secret_key': app.config['SECRET_KEY']
    }
    return jsonify(config)
    
if __name__ == "__main__":
    app.run()


