from multiverse.mars import *
from multiverse.server.worldmgr import *
from multiverse.mars.objects import *
from multiverse.mars.util import *
from multiverse.server.math import *
from multiverse.server.events import *
from multiverse.server.objects import *
from multiverse.server.engine import *
from multiverse.server.util import *
from multiverse.msgsys import *

# Uncomment if you want to set a log level for this process
# that is different from the server's default log level
#Log.setLogLevel(1)

#
# set us up as a mob server
#
#Engine.setServerID(10)
#Engine.isEntityManager(true)
#Engine.setWorldID(1)
#Engine.setPort(5200)

Engine.msgSvrHostname = "localhost"
Engine.msgSvrPort = 20374

Engine.setBasicInterpolatorInterval(5000)

World.setGeometry(Geometry.maxGeometry())

#
# add world servers to the world server manager
#
# Log.debug("Connnecting to world servers")
# wsMgr = Engine.getWSManager()
# wsMgr.addWorldServer(WorldServer("localhost", 5090, 0))
# wsMgr.addWorldServer(WorldServer("localhost", 5091, 1))

# Log.setLogFilename("fantasy.log")
Log.debug("mobserver_local: done with local config")
