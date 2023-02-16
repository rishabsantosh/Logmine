from flask import Flask, render_template
import os

# The below statement creates a WSGI application, it's required because it's a standard to communicate between web server and the web application
app = Flask(__name__)

@app.route('/') # Decorator
def welcome():
    return render_template("index.html")

@app.route('/cluster', methods = ['GET']) # Default value also is 'GET'
def logs():
    os.system("./logmine Apache/Apache_2k.log -m0.5 > cout.txt")
    txt_file = open("cout.txt")
    out = txt_file.read()
    txt_file.close()

    return render_template('lghtml.html', dataToRender = out)


if __name__ == '__main__':
    app.run(debug = True)