import ClientAPI

_skills = {}

def GetNumSkills():
    global _skills
    return len(_skills)

def GetSkillName(slotId):
    global _skills
    if not _skills.has_key(slotId):
        return None
    return _skills[slotId].name
    
def GetSkillRank(slotId):
    global _skills
    if not _skills.has_key(slotId):
        return None
    return _skills[slotId].rank

class SkillEntry:
    """This class holds information about a skill."""
    def __init__(self):
        self.name = ""
        self.rank = 0

    def __str__(self):
        return "<MarsSkill.SkillEntry '%s' '%s'>" % (self.name, self.rank)

def _HandleSkillUpdate(props):
    global _skills

    _skills.clear()
    keys = props.keys()

    for key in keys:        
        skillInfo = props[key]
        if isinstance(skillInfo,dict):
            ClientAPI.Log("Received Skill : " + skillInfo["name"])
            skill = SkillEntry()
            skill.name = skillInfo["name"]
            if skillInfo["rank"] != None:
                skill.rank = int(skillInfo["rank"])
            # I want these to start at 1, so add 1 to the length
            _skills[len(_skills) + 1] = skill
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("SKILL_LIST_UPDATE",[])
    
ClientAPI.Network.RegisterExtensionMessageHandler("mv.SKILL_UPDATE", _HandleSkillUpdate)
