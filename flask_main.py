"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""
from flask import Flask, redirect, render_template, request, flash
import numpy as np
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from mymodule.view.star_coordinates_view import StarCoordinatesView
from mymodule.frontend.model.general_model import GeneralModel
from os import path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path.join(path.dirname(path.realpath(__file__)), 'mymodule', 'resources')
print app.config['UPLOAD_FOLDER']

location = "http://localhost:5006/datavisualization"
file_upload_success = None
UPLOAD_SUCCESS = "File successfully uploaded"
UPLOAD_FAILURE = "Error while loading file"

def modify_doc(doc):
    file_path = "mymodule/resources/main.csv"
    model = GeneralModel(doc=doc)
    model.add_star_coordinates_view("SC", file_path)
    model.add_general_menu("SC")

bokeh_app = Application(FunctionHandler(modify_doc))

io_loop = IOLoop.current()

server = Server({'/datavisualization': bokeh_app}, io_loop=io_loop, allow_websocket_origin=["localhost:5000"])
#server.start()


@app.route('/')
def bokeh_server():
    bokeh_embed = autoload_server(model=None,
                             app_path="/datavisualization",
                             url="http://localhost:5006")

    file_upload = "<html> <body> <form action=\"http://localhost:5000/uploader\" method=\"POST\" enctype=\"multipart/form-data\"> <input type=\"file\" name=\"file\"/> <input type=\"submit\"/> </form> </body></html>"

    html = ""
    if file_upload_success:
        html = "<head><body><div>{}{}</div>{}</body></head>".format(file_upload, UPLOAD_SUCCESS, bokeh_embed)
    else:
        html = "<head><body><div>{}</div>{}</body></head>".format(file_upload, bokeh_embed)

    return html

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(path.join(app.config['UPLOAD_FOLDER'], 'main.csv'))
        file_upload_success = True
    return redirect('/')

if __name__ == '__main__':
    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from bokeh.util.browser import view
    # Serve the Flask app
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    io_loop.add_callback(view, "http://localhost:5000/")
    io_loop.start()
    print "Server started"
    app.run(debug=True)