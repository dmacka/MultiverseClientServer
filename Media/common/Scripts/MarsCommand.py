"""This module contains the various methods for dealing with the target."""

import ClientAPI

import MarsTarget

#
# CommandAPI Methods
#

def HandleCommand(message):
    """This is the standard implementation of HandleCommand for handling
       commands entered on the client."""
    global _commandHandlers
    ClientAPI.Log("HandleCommand: %s" % message);
    if len(message) == 0:
        return
    if not message.startswith("/"):
        message = "/say " + message
    # Handle some client side commands
    tokens = message.split()
    if len(tokens) <= 0:
        return
    args = ""
    if len(message) > len(tokens[0]):
        args = message[len(tokens[0])+1:]
    command = tokens[0][1:]
    if _commandHandlers.has_key(command):
        # We have a local handler for this command on the client.
        func = _commandHandlers[command]
        try:
            func(args)
        except Exception, e:
            ClientAPI.LogWarn("Failed to run command handler '%s' for command line: '%s'" % (str(command), message))
            ClientAPI.LogWarn("Exception: %s" % str(e))
            ClientAPI.LogWarn("Backtrace: %s" % e.clsException.StackTrace)
    else:
        # This command is not handled on the client.  Send it to the server.
        target = MarsTarget.GetCurrentTarget()
        if target is None:
            target = ClientAPI.GetPlayerObject()
        ClientAPI.Network.SendTargetedCommand(target.OID, message)

def RegisterCommandHandler(command, method):
    """Register the method with the command handler, so that when the
       command is entered, the associated method will be called."""
    global _commandHandlers
    # Add the command and method to our dispatch table.
    # This will be used for the HandleCommand method, as well as for /help.
    _commandHandlers[command] = method


#
# Variables to keep track of state
#

# this is a dictionary of commands that are registered
_commandHandlers = {}

