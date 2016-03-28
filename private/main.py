#!/usr/bin/kivy

import os, sys
import threading
import zipfile

import kivy                                                                                     
from kivy.app import App                                                                        
from kivy.lang import Builder                                                                   
from kivy.utils import platform                                                                 
from kivy.uix.widget import Widget                                                              
from kivy.clock import Clock                                                                    
from jnius import autoclass                                                                     
from android.runnable import run_on_ui_thread                                                   


current_path = os.path.dirname(os.path.abspath(__file__))

WebView = autoclass('android.webkit.WebView')                                                   
WebViewClient = autoclass('android.webkit.WebViewClient')                                       
activity = autoclass('org.renpy.android.PythonActivity').mActivity                              


class Wv(Widget):                                                                               
    def __init__(self, **kwargs):                                                               
        super(Wv, self).__init__(**kwargs)                                                      
        Clock.schedule_once(self.create_webview, 0)                                             

    @run_on_ui_thread                                                                           
    def create_webview(self, *args):                                                            
        webview = WebView(activity)                                                             
        webview.getSettings().setJavaScriptEnabled(True)                                        
        wvc = WebViewClient();                                                                  
        webview.setWebViewClient(wvc);                                                          
        activity.setContentView(webview)                                                        
        webview.loadUrl('http://127.0.0.1:8085')


class ServiceApp(App):                                                                          
    def build(self):                                                                            
        return Wv()


def get_sdcard_path():
    ext0 = os.getenv('EXTERNAL_STORAGE', "")
    if os.path.isdir(ext0):
        return ext0

    ext1 = os.getenv('SECONDARY_STORAGE', "")
    if os.path.isdir(ext1):
        return ext1

    ext2 = os.getenv('EMULATED_STORAGE_SOURCE', "")
    for i in range(0, 3):
        path2 = os.path.join(ext2, str(i))
        if os.path.isdir(path2):
            return path2

    default_path = "/storage/sdcard0"
    if os.path.isdir(default_path):
        return default_path

    raise Exception("no sdcard path can get!")


def load_xxnet():
    sdcard_path = get_sdcard_path()
    if not os.path.exists(sdcard_path):
        print("sdcard path can't access:%s" % sdcard_path)
        return

    xxnet_path = os.path.join(sdcard_path, "XX-Net")
    print "load_xxnet on:", xxnet_path
    if not os.path.exists(xxnet_path):
        os.mkdir(xxnet_path)

    launcher_path = os.path.join(xxnet_path, "launcher")
    if not os.path.exists(launcher_path):
        default_zip = os.path.join(current_path, "default.zip")
        with zipfile.ZipFile(default_zip, "r") as dz:
            dz.extractall(xxnet_path)

    sys.path.insert(0, launcher_path)
    from start import main as launcher_main
    print "launcher_main"
    launcher_main()



def start_xxnet():
    th = threading.Thread(target=load_xxnet)
    th.start()



def main():
    start_xxnet()
    ServiceApp().run()


if __name__ == '__main__':
    main()