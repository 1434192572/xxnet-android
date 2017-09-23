#!/bin/bash

# This script should run under xxnet-anroid path

# install system package:
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y build-essential ccache git zlib1g-dev python2.7 python2.7-dev libncurses5:i386 libstdc++6:i386 zlib1g:i386 openjdk-7-jdk unzip ant
sudo apt-get install python-sh python-appdirs virtualenv cython python-jinja2 pkg-config autoconf automake libtool zip

git clone https://github.com/xx-net/XX-Net.git


export ANDROIDSDK=~/android-sdk-linux
export ANDROIDNDK=~/android-ndk-r11b
export ANDROIDAPI=14
export ANDROIDNDKVER=r11b
export PATH=/usr/local/bin:/usr/bin:/bin


# prepair the python-for-android env
python ../python-for-android/pythonforandroid/toolchain.py create \
--dist_name=webview.xxnet.android --bootstrap=webview \
--requirements=python2,openssl,pyopenssl,cryptography,pyjnius,cffi
# patch for Android 7
cp ~/.local/share/python-for-android/dists/webview.xxnet.android/libs/armeabi/libssl1.0.2h.so \
 ~/.local/share/python-for-android/dists/webview.xxnet.android/libs/armeabi/libssl.so
cp ~/.local/share/python-for-android/dists/webview.xxnet.android/libs/armeabi/libcrypto1.0.2h.so\
 ~/.local/share/python-for-android/dists/webview.xxnet.android/libs/armeabi/libcrypto.so



# pack default xx-net python code to private path
rm -rf default_code
mkdir -p default_code/code/default
cp -r XX-Net/code/default/gae_proxy XX-Net/code/default/launcher \
 XX-Net/code/default/x_tunnel XX-Net/code/default/version.txt\
 default_code/code/default/.

rm -rf default_code/code/default/gae_proxy/server
mkdir -p default_code/code/default/python27/1.0/lib
cp -r XX-Net/code/default/python27/1.0/lib/noarch \
 default_code/code/default/python27/1.0/lib/.
rm -rf default_code/code/default/python27/1.0/lib/noarch/OpenSSL/
find default_code |grep "\.pyc" |xargs rm
rm private/default.zip

cd default_code
zip -r ../private/default.zip *
cd ..


# build apk
python ../python-for-android/pythonforandroid/toolchain.py apk \
--dist_name=webview.xxnet.android \
 --package xxnet.net --name XX-Net --version 3.6.2 \
--private private \
 --permission ACCESS_NETWORK_STATE \
 --permission INTERNET \
 --permission WRITE_EXTERNAL_STORAGE \
 --permission BATTERY_STATS \
--icon default_code/code/default/launcher/web_ui/img/logo.png \
--presplash default_code/code/default/launcher/web_ui/img/logo.png \
 --port=8085

# install apk to device
/media/dev/android-xxnet/android_sdk/android-sdk-linux/platform-tools/adb install -r XX-Net-3.6.2-debug.apk

# run apk
/media/dev/android-xxnet/android_sdk/android-sdk-linux/platform-tools/adb shell \
am start -n xxnet.net/org.kivy.android.PythonActivity

# show android log
/media/dev/android-xxnet/android_sdk/android-sdk-linux/platform-tools/adb logcat | grep python
