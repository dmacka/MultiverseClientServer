import sys
from build_assets import *

if sys.argv[1] == "":
    copy_assets(["Base","Particles","Mars","HumanFemale","SampleWorld"], "update/")
else:
    copy_assets(["Base","Particles","Mars","HumanFemale","SampleWorld"], sys.argv[1])
