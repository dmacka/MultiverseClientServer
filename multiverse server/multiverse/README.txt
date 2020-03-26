Multiverse Server README
------------------------

Copy the loose files or extract the zip on your server. It MUST reside in /usr

The structure is /usr/multiverse.

If you copy this elsewhere on the server you will have to edit the properties files.

The current build system is still broken and will be fixed sometime in the future. Someone want the project, let me know.
You need to be proficent in python, java.

This is fully functional including the master server.

To run the server.

from home ---> cd /usr/multiverse/bin
          ---> ./master.sh start
          ---> ./multiverse.sh start

to stop the server.
          ---> ./master.sh stop
          ---> ./multiverse.sh stop

to check the status.
          ---> ./master.sh status
          ---> ./multiverse.sh status

Logging is set to DEBUG. Set the logging in master.properties or multiverse.properties




