from multiverse.server.engine import *
from multiverse.server.util import *
from multiverse.server.plugins import *

# Uncomment if you want to set a log level for this process
# that is different from the server's default log level
Log.setLogLevel(3)

# Engine.MAX_NETWORK_BUF_SIZE = 1000

ProxyPlugin.MaxConcurrentUsers = 5

