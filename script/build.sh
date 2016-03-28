#!/bin/bash

./toolchain.py create --dist_name=xxnet.android --bootstrap=sdl2 --requirements=sdl2,python2,openssl,pyopenssl,cryptography,pyjnius,kivy,android

./toolchain.py apk  --package xxnet.net --name XX-Net --version 3.0.0 --private private \
--permission ACCESS_NETWORK_STATE --permission INTERNET --permission WRITE_EXTERNAL_STORAGE --permission BATTERY_STATS \
--icon default/launcher/web_ui/img/logo.png \
--presplash default/launcher/web_ui/img/logo.png
