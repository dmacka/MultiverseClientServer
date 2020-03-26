import ClientAPI

def SendTrainingInfoRequestMessage(npcId):
	playerOid = ClientAPI.GetPlayerObject().OID
	props = { "playerOid" : playerOid, "npcOid" : npcId }
	ClientAPI.Log("************** Sending Trainer Info Request ******************")
	ClientAPI.Network.SendExtensionMessage(0, False, "mv.REQ_TRAINER_INFO", props)

def SendSkillTrainingRequest(skill):
	playerOid = ClientAPI.GetPlayerObject().OID
	props = { "playerOid" : playerOid, "skill" : skill }
	ClientAPI.Network.SendExtensionMessage(0, False, "mv.REQ_SKILL_TRAINING", props)		

def _HandleTrainingInfo(props):
	ClientAPI.Log("************** Received Trainer Info Response ******************")
	ClientAPI.Interface.DispatchEvent("TRAINING_INFO", [str(props["skills"])])	

def _HandleTrainingFailed(props):
	ClientAPI.Interface.DispatchEvent("TRAINING_FAILED", [str(props["reason"])])

ClientAPI.Network.RegisterExtensionMessageHandler("mv.TRAINING_INFO", _HandleTrainingInfo)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.TRAINING_FAILED", _HandleTrainingFailed)