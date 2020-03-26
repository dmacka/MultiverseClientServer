import sys
from build_assets import *

if sys.argv[1] == "":
    copy_assets(["Base","FCworld"], "update/")
else:
    copy_assets(["Base","FCworld"], sys.argv[1])
