import sys
from build_assets import *

if sys.argv[1] == "":
    copy_assets(["Base","SocialWorld","Rocketbox"], "update/")
else:
    copy_assets(["Base","SocialWorld","Rocketbox"], sys.argv[1])
