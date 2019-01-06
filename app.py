#!/usr/bin/python
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates', methods=['POST'])
def runScript():
    sku = request.form['sku']
    lotNumber = request.form['lotNumber']
    PONumber = request.form['PONumber']
    boxQty = request.form['boxQty']

    return "<h1> it worked </h1>"
if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.93')
