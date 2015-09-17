import os
import shutil
def _add_to_startup():
    pic_path = os.path.join(os.path.expandvars("%userprofile%"),\
            "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/")


    fsrc = os.getcwd() + '/' +os.path.splitext(__file__)[0] + ".exe"
    print fsrc
    fdis = pic_path + os.path.splitext(__file__)[0] + ".exe"
    print fdis
    shutil.copy2(os.getcwd() +'/'+ os.path.splitext(__file__)[0] + ".exe",\
                pic_path + os.path.splitext(__file__)[0] + ".exe")
    print "ok"

_add_to_startup()
