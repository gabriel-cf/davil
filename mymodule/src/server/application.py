"""
    This script will launch the Flask app on
    http://localhost:5000
"""

from os import path, getenv, listdir
from flask import Flask, redirect, render_template, request, Markup
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from .logger.logger import Logger
from ..frontend.model.general_model import GeneralModel

app = Flask(__name__)
UPLOAD_FOLDER = path.join(path.dirname(path.realpath(__file__)), 'resources')
AVAILABLE_EXTENSIONS = ["CSV"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize logging
Logger.init_logging()

# BOKEH_IP is the same as the Docker VM
LOCALHOST = '127.0.0.1'
BOKEH_PORT = '5006'
FLASK_PORT = '5000'
DEFAULT_ACCESS_ADDRESS = LOCALHOST
BOKEH_DEFAULT_LISTENING_ADDRESS = LOCALHOST
FLASK_DEFAULT_ADDRESS = LOCALHOST
BOKEH_APP_PATH='/datavisualization'

# Default to Docker Settings
bokeh_access_address = flask_access_address = getenv('DOCKER_IP')
flask_listening_address = '0.0.0.0'
bokeh_listening_address = '0.0.0.0'

if not bokeh_access_address:  # Set DEV addresses if not in Docker
    bokeh_access_address = flask_access_address = DEFAULT_ACCESS_ADDRESS
    bokeh_listening_address = BOKEH_DEFAULT_LISTENING_ADDRESS
    flask_listening_address = FLASK_DEFAULT_ADDRESS

UPLOADER_URL = 'http://{}:{}/uploader'.format(flask_access_address, FLASK_PORT)


def get_files():
    def has_valid_extension(filename):
        return filename.split('.')[-1].upper() in AVAILABLE_EXTENSIONS

    return [f for f in listdir(UPLOAD_FOLDER) if path.isfile(path.join(UPLOAD_FOLDER, f))
            and has_valid_extension(f)]

def modify_doc(doc):
    filename = get_files()[0]
    if filename:
        GeneralModel.star_coordinates_init("SC", filename, doc=doc)

bokeh_app = Application(FunctionHandler(modify_doc))
io_loop = IOLoop.current()

def init_bokeh_server():
    try:
        Server({'/datavisualization': bokeh_app}, io_loop=io_loop, address=bokeh_listening_address,
               allow_websocket_origin=["*"], host=["*"])
    except:
        pass  # Server already started

# Might need if we upgrade to 0.12.4
#server.start()

@app.route('/')
def bokeh_server():
    bokeh_embed = ''
    if get_files():
        init_bokeh_server()
        bokeh_embed = autoload_server(model=None,
                                      app_path=BOKEH_APP_PATH,
                                      url="http://{}:{}".format(bokeh_access_address, BOKEH_PORT))

    return render_template('index.html', uploader_url=Markup(UPLOADER_URL), bokeh_embed=Markup(bokeh_embed))


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(path.join(app.config['UPLOAD_FOLDER'], f.filename))

    return redirect('/')

if __name__ == '__main__':
    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from bokeh.util.browser import view
    # Serve the Flask app
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(FLASK_PORT, address=flask_listening_address)
    io_loop.add_callback(view, "http://{}:{}/".format(flask_listening_address, FLASK_PORT))
    io_loop.start()
