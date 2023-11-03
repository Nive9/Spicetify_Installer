import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread
from splash_window import Splash
from manager_window import Manager
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from components.popups import errorDialog,windowsToast
from components.tools import writeConfig,readConfig,initConfig

initConfig()

class SpicetifyPatcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash_window = Splash()
        self.manager_window = Manager()

        self.splash_window.show()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_menu)
        self.timer.start(5000)

    # Check os and redirect to manager
    def show_menu(self):
        if sys.platform == 'win32':
            self.splash_window.hide()
            self.manager_window.show()
        else:
            self.splash_window.hide()
            errorDialog("This script is only compatible with Windows!")
            
    def run(self):
        sys.exit(self.app.exec())

# Spotify WatchWitch on new thread (it's helloween)

@Request.application
def application(request):
    if request.path == '/watchwitch/spotify/startup':
        windowsToast("Spicetify Manager", "Spotify just started!")
        return Response('ok', content_type='text/plain')
    return Response('Not Found', status=404, content_type='text/plain')

class WerkzeugThread(QThread):
    def run(self):
        print("Server started")
        run_simple('localhost', 1738, application)

if readConfig('Manager', 'watchwitch') == "True":
    watchwitch = WerkzeugThread()
    watchwitch.start()
#start the app
if __name__ == "__main__":
    app = SpicetifyPatcher()
    app.run()