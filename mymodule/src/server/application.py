"""
    This script will launch the Flask app on
    http://localhost:5000
"""

from os import path
from os import getenv
from flask import Flask, redirect, render_template, request, Markup
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from .logger.logger import Logger
from ..frontend.model.general_model import GeneralModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path.join(path.dirname(path.realpath(__file__)), 'resources')
# Initialize logging
Logger.init_logging()

# BOKEH_IP is the same as the Docker VM
LOCALHOST = '127.0.0.1'
BOKEH_DEFAULT_ACCESS_ADDRESS = LOCALHOST
BOKEH_DEFAULT_LISTENING_ADDRESS = LOCALHOST
FLASK_DEFAULT_ADDRESS = LOCALHOST

# Default to Docker Settings
bokeh_access_address = getenv('BOKEH_IP')
flask_listening_address = '0.0.0.0'
bokeh_listening_address = '0.0.0.0'

if not bokeh_access_address: # DEV (localhost)
    bokeh_access_address = BOKEH_DEFAULT_ACCESS_ADDRESS
    bokeh_listening_address = BOKEH_DEFAULT_LISTENING_ADDRESS
    flask_listening_address = FLASK_DEFAULT_ADDRESS

def modify_doc(doc):
    filename = "cereal.csv"
    GeneralModel.star_coordinates_init("SC", filename, doc=doc)

bokeh_app = Application(FunctionHandler(modify_doc))

io_loop = IOLoop.current()

server = Server({'/datavisualization': bokeh_app}, io_loop=io_loop, address=bokeh_listening_address,
                allow_websocket_origin=["*"], host=["*"])
# Might need if we upgrade to 0.12.4
#server.start()

@app.route('/')
def bokeh_server():
    bokeh_embed = autoload_server(model=None,
                                  app_path="/datavisualization",
                                  url="http://{}:5006".format(bokeh_access_address))

    html = render_template('index.html', bokeh_embed=Markup(bokeh_embed))

    return html

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(path.join(app.config['UPLOAD_FOLDER'], 'main.csv'))
    return redirect('/')

if __name__ == '__main__':
    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from bokeh.util.browser import view
    # Serve the Flask app
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000, address=flask_listening_address)
    io_loop.add_callback(view, "http://{}:5000/".format(flask_listening_address))
    io_loop.start()
    print "Server started"
    app.run(debug=True)
