from Multiverse.Config import *
from Multiverse.Network import *
from Multiverse.Interface import *

import MarsCommand

def CreateClientParmWiki(args_str):
    subsystemString = ParameterRegistry.GetSubsystems()
    subsystems = subsystemString.split()
    docs = ""
    for sub in subsystems:
        s = str(sub)
        docs += "= Subsystem '''" + s + "''' Parameter Documentation =\n\n"
        linestring = ParameterRegistry.GetParameter(s, "Help")
        lines = linestring.rsplit("\n");
        for line in lines:
            i = len(line)
            if i == 0:
                continue
            ind = line.index(":");
            docs += "* '''" + line[0:ind] + "''': " + line[ind + 1:i] + "\n\n"
        docs += "\n"
    FILE = open("C:/Multiverse/Notes/ClientParmsDocumentation.txt","w")
    FILE.write(docs)
    FILE.close()

MarsCommand.RegisterCommandHandler("genwiki", CreateClientParmWiki)
