from flask import Flask, render_template
import report as rp


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/data')
def get_data():
    return rp.report()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)