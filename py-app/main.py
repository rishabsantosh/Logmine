from flask import Flask, render_template
import os
import sys
from logmine_pkg.run import run

# The below statement creates a WSGI application, it's required because it's a standard to communicate between web server and the web application
app = Flask(__name__)

@app.route('/') # Decorator
def welcome():
    return render_template("index.html")

@app.route('/cluster', methods = ['GET']) # Default value also is 'GET'
def logs():
    os.system("./logmine Apache/Apache_2k.log -m0.5 > cout.txt")
    txt_file = open("cout.txt")
    lines = txt_file.readlines()
    out = ""

    for line in lines:
        out = out + "hello"
        out = out + line + '\n'
        # Try <br>, search how to add next line from python to html
    out = out + "world" + "\n" + len(txt_file)

    txt_file.close()

    return render_template('lghtml.html', dataToRender = out)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8080)
