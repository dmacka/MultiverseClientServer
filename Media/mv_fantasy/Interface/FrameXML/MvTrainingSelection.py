import ClientAPI
import MarsTraining

def MvTrainingSelectionFrame_OnLoad(frame):
	frame.RegisterEvent("TRAINING_INFO")
	frame.RegisterEvent("TRAINING_FAILED")
	frame.RegisterEvent("ABILITY_UPDATE")
	global sentSkillTrainingRequest
	return

def MvTrainingSelectionFrame_OnEvent(frame, args):
	if args.eventType == "TRAINING_INFO":
		global trainingInfoEvent
		trainingInfoEvent = args
		frame.Show()
	if args.eventType == "TRAINING_FAILED":
		MvAbilityUpdateMsg.SetText(args.eventArgs[0])
	if args.eventType == "ABILITY_UPDATE":
		showTrainingUpdateInfo(args)

def MvTrainingSelectionFrame_OnShow(frame):
	MvTrainingSelectionFrame.SetBackdropColor(0.0,0.0,0.0)
	MvTrainingOptionsFrame.SetBackdropColor(0.3,0.3,0.3)
	LoadTrainingInformation()

def MvTrainingOption_OnClick(frame):	
	if not frame.IsEnabled():
		return
	
	if frame.GetChecked():
		frame.SetChecked(0)
		frame.SetTextColor(1.0,1.0,1.0)
	else:
		for i in range(0, 5):
			skillButton = getglobal("TrainingOption%d" % i)
			if skillButton.IsEnabled():				
				skillButton.SetChecked(0)	
				skillButton.SetTextColor(1.0,1.0,1.0)
		frame.SetChecked(1)
		frame.SetTextColor(1.0,0.0,0.0)
		ClientAPI.Log(frame.Name)

	return	

def MvTrainingSelectionFrameCloseButton_OnClick(frame):
	MvTrainingSelectionScrollFrame.Hide()
	
def MvTrainSkillButton_OnClick(frame):
	skill = ""
	skillButton = None
	for i in range(0, 5):
		skillButton = getglobal("TrainingOption%d" % i)
		if skillButton.GetChecked():
			skill = skillButton.GetText()
			break
			
	if len(skill) == 0:
		MvAbilityUpdateMsg.SetText("You must select a skill to train!")		
	else:
		MarsTraining.SendSkillTrainingRequest(skill)
		ClientAPI.Log("Skill button text = "+skillButton.GetText())
		skillButton.SetChecked(0)
		skillButton.SetTextColor(0.1,0.1,0.1)
		skillButton.Disable()		

	return
	
def MvTrainSkillButton_OnEnter(frame):
	return
	
def MvTrainSkillButton_OnLeave(frame):
	return		
				
def LoadTrainingInformation():
	playerObj = ClientAPI.GetPlayerObject()
	playerName = playerObj.Name
	greetingText = "Greetings "+playerName+"! Select one of the skills below and click the Train button if you would like to receive training in that skill set. Once you learn a skill, you will be granted a default ability. As abilities are used, you will level up the associated akill set and be granted more powerful abilities!"
	GreetingMessage.SetText(greetingText)
	
	skills = str(trainingInfoEvent.eventArgs[0])
	availableSkills = skills.split(';')
	numSkills = len(availableSkills)

	for i in range(0, numSkills):
		eval("TrainingOption"+str(i)+".SetText('"+availableSkills[i]+"')")
		eval("TrainingOption"+str(i)+".Show()")
	
	return	
	
def showTrainingUpdateInfo(args):
	if MvTrainingSelectionFrame.IsVisible():		
		abilityName = MarsAbility.GetAbilityName(MarsAbility.GetNumAbilities())
		abilityUpdate = "Congradulations! You have learn the " + abilityName + " ability."
		MvAbilityUpdateMsg.SetText(abilityUpdate)
	return	
