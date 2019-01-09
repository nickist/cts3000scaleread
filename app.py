#!/usr/bin/python
from flask import Flask, render_template, request
from readScale import scaleRead
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates', methods=['GET', 'POST'])
def runScript():
    #sku = request.form['sku']
    #lotNumber = request.form['lotNumber']
    #PONumber = request.form['PONumber']
    #boxQty = request.form['boxQty']
    ReadScale = request.form['readscale']
    r = "Nothing"
    while (ReadScale):
        r = scaleRead()
        ReadScale = request.form['readscale']
        return "<h1> %s </h1>" % (r)
if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.93')
