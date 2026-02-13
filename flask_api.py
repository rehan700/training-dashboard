from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return 'hello'
@app.route('/tools')
def tools():
    return {'frontend': 'react', 'backend': 'flask'}
def get_data():
    return {'name': 'rehan', 'age': 24}
if __name__ == '__main__':
    app.run(debug=True)