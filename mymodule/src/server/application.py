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
import logging
from ..frontend.model.general_model import GeneralModel

app = Flask(__name__)
UPLOAD_FOLDER = path.join(path.dirname(path.realpath(__file__)), 'resources')
AVAILABLE_EXTENSIONS = ["CSV"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize logging
Logger.init_logging()
LOGGER = logging.getLogger(__name__)

LOCALHOST = '127.0.0.1'
DEFAULT_LISTENING_ADDRESS = '0.0.0.0'
# SERVICE_HOST = hostname of the service running the application (it should be 'localhost' in local machines)
DEFAULT_ACCESS_ADDRESS = getenv('SERVICE_HOST')

if not DEFAULT_ACCESS_ADDRESS:
    DEFAULT_ACCESS_ADDRESS = LOCALHOST

BOKEH_PORT = '5006'
FLASK_PORT = '5000'
BOKEH_APP_PATH='/datavisualization'

# Default to Docker Settings
bokeh_access_address = flask_access_address_local = DEFAULT_ACCESS_ADDRESS
flask_listening_address = DEFAULT_LISTENING_ADDRESS
bokeh_listening_address = DEFAULT_LISTENING_ADDRESS

UPLOADER_URL = 'http://{}:{}/uploader'.format(flask_access_address_local, FLASK_PORT)


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
    LOGGER.info("bokeh_server::START")
    bokeh_embed = ''
    if get_files():
        LOGGER.info("Rendering Bokeh with sample files from %s", UPLOAD_FOLDER)
        init_bokeh_server()
        bokeh_embed = autoload_server(model=None,
                                      app_path=BOKEH_APP_PATH,
                                      url="http://{}:{}".format(bokeh_access_address, BOKEH_PORT))

    LOGGER.info("bokeh_server::END")
    return render_template('index.html', uploader_url=Markup(UPLOADER_URL), bokeh_embed=Markup(bokeh_embed))


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    LOGGER.info("upload_file::START")
    if request.method == 'POST':
        f = request.files['file']
        f.save(path.join(app.config['UPLOAD_FOLDER'], f.filename))

    LOGGER.info("upload_file::END")
    return redirect('/')

if __name__ == '__main__':
    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from bokeh.util.browser import view
    # Serve the Flask app
    LOGGER.info("Initializing WSGI Container")
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(FLASK_PORT, address=flask_listening_address)
    access_url = "http://{}:{}/".format(flask_listening_address, FLASK_PORT)
    LOGGER.info("Initializing IO Loop")
    io_loop.add_callback(view, access_url)
    LOGGER.info("Flask ready on address {}".format(access_url))
    io_loop.start()
