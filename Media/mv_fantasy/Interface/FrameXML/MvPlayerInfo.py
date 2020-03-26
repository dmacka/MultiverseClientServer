import ClientAPI
import MarsSkill

def MvPlayerInfoFrame_OnLoad(frame):
	frame.SetBackdropColor(0, 0, 0)
	frame.RegisterEvent("SKILL_LIST_UPDATE")
	
def MvPlayerInfoFrame_OnEvent(frame, event):
        if event.eventType == "SKILL_LIST_UPDATE":
                UpdateSkillInfo()
	
def GetUnitProperty(obj, prop, default):
	if obj is None:
		return default
	if not obj.PropertyExists(prop):
		return default
	return obj.GetProperty(prop)	
	
def LoadPlayerValues():
	player = ClientAPI.GetPlayerObject()	

	MvPlayerNameValue.SetText(player.Name)
	MvPlayerProfessionValue.SetText(str(GetUnitProperty(player, "class", 0)))
	MvPlayerLevelValue.SetText(str(GetUnitProperty(player, "level", 0)))
	strength = GetUnitProperty(player, "strength", 0)
	MvPlayerStrengthValue.SetText(str(strength))
	MvPlayerDexterityValue.SetText(str(GetUnitProperty(player, "dexterity", 0)))
	MvPlayerWisdomValue.SetText(str(GetUnitProperty(player, "wisdom", 0)))
	MvPlayerIntelligenceValue.SetText(str(GetUnitProperty(player, "intelligence", 0)))

	UpdateSkillInfo()

def UpdateSkillInfo():
        numSkills = MarsSkill.GetNumSkills()

        if numSkills > 0:
                #Skill.SetText(MarsSkill.GetSkillName(1))
                for i in range(1,numSkills+1):                        
                       frame = getglobal("Skill" + str(i))
                       frame.SetText(MarsSkill.GetSkillName(i))
                       frame = getglobal("SkillRank" + str(i))
                       frame.SetText(str(MarsSkill.GetSkillRank(i)))
