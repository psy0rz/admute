import pickle

from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl, MediaControl, InputControl


class ControlWebos:

    def __init__(self):

        webos_store={'auth': {}}
        try:
            webos_store=pickle.load(open("webos.auth", "rb"))
        except:
            print("Cant load webos auth, registering new one.")
            pass

        if not 'host' in webos_store:
            print("Searching tv...")
            webos_client = WebOSClient.discover()[0]
        else:
            print("Connecting to tv at {}".format(webos_store['host']))
            webos_client = WebOSClient(webos_store['host'])

        webos_client.connect()
        for status in webos_client.register(webos_store['auth']):
            if status == WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == WebOSClient.REGISTERED:
                print("Webos connection successful!")
                webos_store['host']=webos_client.host
                pickle.dump(webos_store, open("webos.auth", "wb"))

        self.webos_system= SystemControl(webos_client)

        self.webos_media = MediaControl(webos_client)

        self.webos_inp = InputControl(webos_client)
        self.webos_inp.connect_input()

        self.notify("Skipper connected")

    def notify(self, txt):
        self.webos_system.notify(txt)

    def mute(self):
        self.notify("Muted ad")
        self.webos_media.mute(True)

    def unmute(self):
        self.notify("Unmuted ad")
        self.webos_media.mute(False)

    def skip(self):
        self.notify("Skipped ad")
        self.webos_inp.ok()