"""
    This script will launch the view for Star Coordinates on
    http://localhost:5006/starcoordinatesview
"""

# TODO gchicafernandez
#   Define HTML templates
#   Break logic into several flask modules
from os import path
from flask import Flask, redirect, render_template, request, flash, url_for
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from .logger.logger import Logger
from ..frontend.model.general_model import GeneralModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path.join(path.dirname(path.realpath(__file__)), 'resources')
location = "http://localhost:5006/datavisualization"
UPLOAD_SUCCESS = "File successfully uploaded"
UPLOAD_FAILURE = "Error while loading file"
# Initialize logging
Logger.init_logging()

def modify_doc(doc):
    filename = "cereal.csv"
    GeneralModel.star_coordinates_init("SC", filename, doc=doc)

bokeh_app = Application(FunctionHandler(modify_doc))

io_loop = IOLoop.current()

server = Server({'/datavisualization': bokeh_app}, io_loop=io_loop, allow_websocket_origin=["localhost:5000"])
# Might need if we upgrade to 0.12.4
#server.start()


@app.route('/')
def bokeh_server():
    bokeh_embed = autoload_server(model=None,
                                  app_path="/datavisualization",
                                  url="http://localhost:5006")

    file_upload = render_template('uploader.html')
    html = "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"/static/bokeh_style.css\"><body><div>{}</div>{}</body></head>".format(file_upload, bokeh_embed)

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