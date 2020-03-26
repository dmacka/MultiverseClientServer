"""This module keeps track of the last quest we were offered, as well as some
   information about each of the entries in our quest log."""

import ClientAPI

# I haven't implemented MarsUnit yet, but once I do, I want to link it in so
# I can keep track of what npc the player is interacting with (updated when I
# get a QuestInfo message).
# import MarsUnit

from Multiverse.Network import WorldMessageType
from Multiverse.Network import MessageDispatcher
from Multiverse.Network import ItemEntry

class QuestLogEntry:
    """This class holds information about an entry in the quest log."""
    def __init__(self):
        self.QuestId = 0
        self.Title = ""
        self.Description = ""
        self.Objective = ""
        self.Objectives = []
        self.RewardItems = []

#
# QuestAPI Methods
#

def AbandonQuest():
    pass

def AcceptQuest():
    """Accept the currently offered quest"""
    global _lastObjectId, _lastQuestId
    ClientAPI.Network.SendQuestResponseMessage(_lastObjectId, _lastQuestId, True)
    
def CompleteQuest():
    pass

def DeclineQuest():
    """Decline the currently offered quest"""
    global _lastObjectId, _lastQuestId
    ClientAPI.Network.SendQuestResponseMessage(_lastObjectId, _lastQuestId, False)

def GetNumQuestLeaderBoards(questIndex):
    global _questLogEntries
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return 0
    return len(_questLogEntries[questIndex - 1].Objectives)

def GetNumQuestLogEntries():
    global _questLogEntries
    return [len(_questLogEntries), len(_questLogEntries)]
    
def GetNumQuestLogRewards():
    global _questLogSelectedIndex, _questLogEntries
    questIndex = _questLogSelectedIndex
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return 0
    return len(_questLogEntries[questIndex - 1].RewardItems)
    
def GetNumQuestRewards():
    global _rewardItems
    return len(_rewardItems)
    
def GetObjectiveText():
    global _lastQuestObjectiveText
    return _lastQuestObjectiveText
    
def GetQuestItemInfo(itemType, itemIndex):
    global _rewardItems
    return _GetQuestRewardInfo(_rewardItems, itemIndex)

def GetQuestLogLeaderBoard(objIndex, questIndex):
    global _questLogEntries
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return None
    if (objIndex <= 0 or objIndex > len(_questLogEntries[questIndex - 1].Objectives)):
        return None
    return [_questLogEntries[questIndex - 1].Objectives[objIndex - 1], "monster", False]

def GetQuestLogPushable():
    return False

def GetQuestLogQuestText():
    global _questLogSelectedIndex, _questLogEntries
    questIndex = _questLogSelectedIndex
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return None
    for entry in _questLogEntries:
        ClientAPI.Log("Desc: %s; Obj: %s" % (entry.Description, entry.Objective))
    return [_questLogEntries[questIndex - 1].Description, _questLogEntries[questIndex - 1].Objective]

def GetQuestLogRewardInfo(itemIndex):
    global _questLogSelectedIndex, _questLogEntries
    questIndex = _questLogSelectedIndex
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return None
    entries = _questLogEntries[questIndex - 1].RewardItems
    return _GetQuestRewardInfo(entries, itemIndex)

def GetQuestLogSelection():
    global _questLogSelectedIndex
    return _questLogSelectedIndex

def GetQuestLogTitle(questIndex):
    global _questLogEntries
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        return None
    return _questLogEntries[questIndex - 1].Title

def GetQuestMoneyToGet():
    return 0

def GetQuestText():
    global _lastQuestDescriptionText
    return _lastQuestDescriptionText
    
def GetTitleText():
    global _lastQuestTitleText
    return _lastQuestTitleText
    
def SelectQuestLogEntry(questIndex):
    global _questLogSelectedIndex, _questLogEntries
    if (questIndex <= 0 or questIndex > len(_questLogEntries)):
        _questLogSelectedIndex = 0
    else:
        _questLogSelectedIndex = questIndex


#
# Variables to track state
#

# info about the last quest we were offered
_lastQuestId = 0
_lastObjectId = 0
_lastQuestTitleText = ""
_lastQuestObjectiveText = ""
_lastQuestDescriptionText = ""
_rewardItems = []

# quest log info
_questLogSelectedIndex = 0
_questLogEntries = []


#
# Helper Methods
#

def _GetQuestRewardInfo(entries, itemIndex):
    if (itemIndex <= 0 or itemIndex > len(entries)):
        return None
    entry = entries[itemIndex - 1]
    return [entry.name, entry.icon, entry.count, 1, True]

def _HandleQuestInfoResponse(props):
    global _lastQuestTitleText, _lastQuestObjectiveText, _lastQuestDescriptionText, _lastObjectId, _lastQuestId, _rewardItems
    #
    # update our idea of the state
    #
    _lastQuestTitleText = props["title"]
    _lastQuestObjectiveText = props["objective"]
    _lastQuestDescriptionText = props["description"]
    _lastObjectId = props["ext_msg_subject_oid"]
    _lastQuestId = props["questOid"]
    _rewardItems = []
    for item in props["rewards"]:
        name, icon, count = item
        entry = ItemEntry()
        entry.name = name
        entry.icon = icon
        entry.count = count
        _rewardItems.append(entry)
    ClientAPI.DebugWrite("quest npc=" + str(_lastObjectId) + " quest=" + str(_lastQuestId))
    # TODO: Set the "npc" unit oid to lastObjectId in the MarsUnit module
    # MarsUnit._SetUnitOid("npc", props["ext_msg_target_oid"])
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("QUEST_DETAIL", [])

def _HandleQuestLogInfo(props):
    global _questLogEntries
    #
    # update our idea of the state
    #
    logEntry = None
    for entry in _questLogEntries:
        if (entry.QuestId == props["ext_msg_subject_oid"]):
            logEntry = entry
            break
    if logEntry is None:
        logEntry = QuestLogEntry()
        _questLogEntries.Add(logEntry)
    logEntry.QuestId = props["ext_msg_subject_oid"]
    logEntry.Title = props["title"]
    logEntry.Description = props["description"]
    logEntry.Objective = props["objective"]
    logEntry.RewardItems = []
    for item in props["rewards"]:
        name, icon, count = item
        entry = ItemEntry()
        entry.name = name
        entry.icon = icon
        entry.count = count
        logEntry.RewardItems.append(entry)
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("QUEST_LOG_UPDATE", [])

def _HandleQuestStateInfo(props):
    global _questLogEntries
    #
    # update our idea of the state
    #
    for entry in _questLogEntries:
        if (entry.QuestId != props["ext_msg_subject_oid"]):
            continue
        entry.Objectives.Clear()
        for objective in props["objectives"]:
            entry.Objectives.Add(objective)
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("QUEST_LOG_UPDATE", [])

def _HandleRemoveQuestResponse(props):
    global _questLogSelectedIndex, _questLogEntries
    index = 1 # questLogSelectedIndex is 1 based.
    for entry in _questLogEntries:
        if (entry.QuestId == props["ext_msg_subject_oid"]):
            _questLogEntries.Remove(entry)
            break
        index = index + 1
    if (index == _questLogSelectedIndex):
        # we removed the selected entry. reset selection
        _questLogSelectedIndex = 0
    elif (index < _questLogSelectedIndex):
        # removed an entry before our selection - decrement our selection
        _questLogSelectedIndex = _questLogSelectedIndex - 1
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("QUEST_LOG_UPDATE", [])

# Register callbacks for some quest messages
ClientAPI.Network.RegisterExtensionMessageHandler("mv.QUEST_INFO", _HandleQuestInfoResponse)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.QUEST_LOG_INFO", _HandleQuestLogInfo)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.QUEST_STATE_INFO", _HandleQuestStateInfo)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.REMOVE_QUEST_RESP", _HandleRemoveQuestResponse)
