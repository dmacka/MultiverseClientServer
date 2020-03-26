#!/bin/sh

MAIN_CLASS=multiverse.server.util.SecureTokenUtil

if [ "X$MV_HOME" = "X" ]; then
    export MV_HOME=`dirname $0`/..
fi
MV_COMMON="$MV_HOME/config/common"

MVJAR="$MV_HOME/dist/lib/multiverse.jar"
MARSJAR="$MV_HOME/dist/lib/mars.jar"
GETOPT="$MV_HOME/other/java-getopt-1.0.11.jar"
LOG4J="$MV_HOME/other/log4j-1.2.14.jar"
BCEL="$MV_HOME/other/bcel-5.2.jar"
INJECTED_JAR=${INJECTED_JAR:-"${MV_HOME}/dist/lib/injected.jar"}

    MV_CLASSPATH="$INJECTED_JAR:$MVJAR:$MARSJAR:$BCEL:$GETOPT:$LOG4J:$JAVA_HOME/lib/tools.jar"

DISABLE_LOG="-Dmultiverse.disable_logs=true"

JAVA_FLAGS=-$JVM_TYPE $JVM_HEAP_FLAGS -cp "$MV_CLASSPATH" -Dmultiverse.propertyfile=$PROPFILE
JAVA_FLAGS=$JAVA_FLAGS -Dmultiverse.logs=$MV_LOGS


java $JAVA_FLAGS multiverse.server.util.SecureTokenManager > masterserverkeys.txt
