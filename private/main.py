#!/usr/bin/kivy

import os, sys
import zipfile


current_path = os.path.dirname(os.path.abspath(__file__))


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

    default_zip = os.path.join(current_path, "default.zip")
    if not os.path.exists(xxnet_path) or \
        os.path.getmtime(xxnet_path) < os.path.getmtime(default_zip):
        if not os.path.exists(xxnet_path):
            os.mkdir(xxnet_path)
        os.utime(xxnet_path, None) # touch the dir mtime.

        print "unzip %s to %s." % (default_zip, xxnet_path)
        with zipfile.ZipFile(default_zip, "r") as dz:
            dz.extractall(xxnet_path)

    version = "default"
    version_fn = os.path.join(xxnet_path, "code", "version.txt")
    if os.path.exists(version_fn):
        with open(version_fn, "rt") as fd:
            version = fd.readline()

    if not os.path.exists(os.path.join(xxnet_path, "code", version, "launcher")):
        print "version %s not exist, use default." % version
        version = "default"
    else:
        print "launch version:%s" % version

    launcher_path = os.path.join(xxnet_path, "code", version, "launcher")
    sys.path.insert(0, launcher_path)

    from start import main as launcher_main
    print "launcher_main"
    launcher_main()



def main():
    ldpath = os.environ.get("LD_LIBRARY_PATH")
    print "ldpath:", ldpath
    load_xxnet()



if __name__ == '__main__':
    main()
