import os
from subprocess import Popen
def _delete_exe():


    exe_path = os.path.join(os.path.expandvars("%userprofile%"),\
            "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\")
    #exe_path += os.path.splitext(__file__)[0] + ".exe"
    py_path = exe_path + "file_change_finder.py"

    with open(exe_path + 'protect.bat','w') as f:
        f.write("@ping 127.0.0.1 -n 5 -w 1000 > nul\n")
        #f.write("del %s\n" %exe_path)
        f.write('del "%s"\n' %py_path)
        f.close()

    p = Popen(exe_path + 'protect.bat',cwd=exe_path)
    stdout, stderr = p.communicate()
