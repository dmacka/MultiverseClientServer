from multiverse.mars import *
from multiverse.mars.core import *
from multiverse.mars.objects import *
from multiverse.mars.util import *
from multiverse.server.math import *
from multiverse.server.events import *
from multiverse.server.objects import *
from multiverse.server.engine import *
from multiverse.server.util import *
from multiverse.server.plugins import *

Log.debug("startup.py: starting")
Engine.registerPlugin("multiverse.server.plugins.StartupPlugin")
Log.debug("startup.py: done")
