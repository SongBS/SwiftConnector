#-*-coding:utf-8
#setup.py
from distutils.core import setup
import py2exe, sys

sys.argv.append("py2exe")

setup(windows=["SwiftManager.py"],\
options={\
"py2exe":{\
"packages" : ["wx", "pycurl", "encodings"], \
"bundle_files":1,\
"optimize":2, \
"compressed":1, \
"dll_excludes":["MSVCP90.dll"],
}
},
zipfile = None
)


