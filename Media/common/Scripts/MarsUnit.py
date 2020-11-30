"""This module contains the various methods for dealing with actions."""

import ClientAPI

import MarsTarget

#
# UnitAPI Methods
#

def UnitAffectingCombat(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "combatstate", None)
    
def UnitExists(unit):
    return _GetUnit(unit) is not None

def UnitHealth(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "health", 0)

def UnitHealthMax(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "health-max", 0)

def UnitInParty(unit):
    # this is just a stub in case it is called
    return False

def UnitIsPartyLeader(unit):
    # this is just a stub in case it is called
    return False

def UnitIsPVP(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "pvpstate", None)

def UnitIsDead(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "deadstate", None)

def UnitLevel(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "level", 0)

def UnitMana(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "mana", 0)

def UnitManaMax(unit):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, "mana-max", 0)

def UnitName(unit):
    obj = _GetUnit(unit)
    if obj is None:
        return ""
    return obj.Name

def UnitStat(unit, statname):
    obj = _GetUnit(unit)
    return _GetUnitProperty(obj, statname, 0)


# This method doesn't actually do the right thing.  It will only return true
# if the unit is this player, rather than if the unit is any player.
def UnitPlayerControlled(unit):
    return _GetUnit(unit) is _GetUnit("player")

#
# Helper Methods
#

def _GetUnit(unit):
    if unit == "player":
        return ClientAPI.GetPlayerObject()
    elif unit == "party1":
        return None
    elif unit == "party2":
        return None
    elif unit == "party3":
        return None
    elif unit == "party4":
        return None
    elif unit == "target":
        return MarsTarget.GetCurrentTarget()
    elif unit == "mouseover":
        return MarsTarget._mouseoverTarget
    elif unit == "npc":
        # fixme -- this should return the oid of the quest mob
        return None
    return None

def _GetUnitProperty(obj, prop, default):
    if obj is None:
        return default
    if not obj.PropertyExists(prop):
        return default
    return obj.GetProperty(prop)

