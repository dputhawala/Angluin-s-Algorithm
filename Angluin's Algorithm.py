# States are a 3-tuple [label, Start-Bool, Accepting-Bool]
# Transitions are a 3-tuple [fromState, toState, Emission]

import sys

# ----------------------------------------------------------------------
# 			Opening File Containing Training Data
# ----------------------------------------------------------------------

TrainingFile = 'testab.txt' 					#This is the file that will be read into the program,
											#containing sentences from the Language
def GetLines(SourceFile):					#This function will get the lines from the file
	FileLines = []
	File = open(SourceFile,'r')
	for line in File:						#Go through line by line...
		Stripped = line.strip()				#Strip them...
		Bounded = Stripped+'#'				#add a word boundary symbol...
		FileLines.append(Bounded)			#Then add the word to the list

	return(FileLines)

FileLines = GetLines(TrainingFile)
# print 'FileLines: ',FileLines

# ----------------------------------------------------------------------
# 			Initializing Start State & Lists
# ----------------------------------------------------------------------

StateList = [[0,True,False]]				#we initialize with just a single starting state
TransList = []

# print 'Initial StateList: ',StateList
# print 'Initial TransList: ',TransList

# ----------------------------------------------------------------------
# 			Trouble-Shooting Functions
# ----------------------------------------------------------------------

def FinalTranlistChecker(TransList):		#this function will check for the existence of identical transitions
	for transition in TransList:			#in the final Transition List, and throw up an error if it does
		DupTrans = []
		for OtherTrans in TransList:
			if transition == OtherTrans:
				DupTrans.append(OtherTrans)
		if len(DupTrans) > 1:
			print '\n---------------------------------------------------------------------\n'
			print 'Error, multiple identical transmissions exist!  Check TransList for more information.'
			print 'Duplicate Transition --> ',DupTrans
			sys.exit()



def DFMTroubleShooter(StateList, TransList):	#This function will stop things if somethign goes wrong
	for state in StateList:						#This part will check for multiple copies of the same state,
		DupStates = []							#and throw up an error if it finds any.
		for OtherState in StateList:
			if state[0] == OtherState[0]:
				DupStates.append(OtherState)
		if len(DupStates) > 1:
			print '\n---------------------------------------------------------------------\n'
			print 'Error, multiple co-referencing states exist!  Check StateList for more information.'
			print 'Duplicate states --> ',DupStates
			sys.exit()

	for transition in TransList:				#This part will look for any transitions who have been cast adrift
		RootStranded = True 					#after the state they came from was removed or changed,
		for state in StateList:					#and throw up an error if it finds any.
			if transition[0] == state[0]:
				RootStranded = False
				break
		if RootStranded == True:
			print '\n---------------------------------------------------------------------\n'
			print 'Error, at least one transition does not have a valid FromState.  Check StateList and TransList for more information.'
			print 'Root-Stranded transition --> ',transition
			print 'StateList: ',StateList
			sys.exit()

	for transition in TransList:				#This part will look for any transitions that don't lead to state
		ToStranded = True 						#after the state they lead to was removed or changed,
		for state in StateList:					#and throw up an error if it finds any.
			if transition[1] == state[0]:
				ToStranded = False
				break
		if ToStranded == True:
			print '\n---------------------------------------------------------------------\n'
			print 'Error, at least one transition does not have a valid destination ToState.  Check StateList and TransList for more information.'
			print 'Destination-Stranded transition --> ',transition
			print 'StateList: ',StateList
			sys.exit()


DFMTroubleShooter(StateList, TransList)

# ----------------------------------------------------------------------
# 			Run a Line through the DFM
# ----------------------------------------------------------------------

def CheckLetterTrans(Letter, fromState, TransList):	#This function will check if the current letter can be generated by a transition from the current state
	CanContinue = False								#CanContinue means that there is a transition from that state to conintue the read-in
	for transition in TransList:				
		if transition[0] == fromState:				#If there are transitions from that state
			if transition[2] == Letter:				#and if the transition can generate the letter
				fromState = transition[1]			#then progress to the new state, and keeps running
				CanContinue = True
				break
	return fromState, CanContinue, TransList

def GetNewState(StateList):							#if a transition requires the creation of a new state, this function does it
	for I in range(len(StateList)+1):
		NameTaken = False
		for state in StateList:						#It also checks to make sure it doesn't create any duplicate states
			if state[0] == I:						#because very bad things happen if it does.
				NameTaken = True
				break
		if NameTaken == False:
			NewToState = I
			break
	return NewToState	

def CheckLine(line, StateList, TransList):			#This function will read in the training data line by line, letter by letter
	fromState = 0
	for letter in line:
		if letter == '#':							#It handles the part of Angluin's Algorithm where you read in a new line as
			for state in StateList:					#much as you can with the existing DFM structure, and then append waht new 
				if state[0] == fromState:			#states you must to handle the rest of that line of input
					state[2] = True 				#this line of code turns a state into an accepting state if it results
					break							#from the last letter in the line.
		else:
			fromState, CanContinue, TransList =  CheckLetterTrans(letter, fromState, TransList)
			if CanContinue == False:				#specifically, this block of code creates new transitions and states as needed
				NewToState = GetNewState(StateList)
				StateList.append([NewToState, False, False])
				TransList.append([fromState, NewToState, letter])
				fromState = CheckLetterTrans(letter, fromState, TransList)[0]



# ----------------------------------------------------------------------
# 			Merging Functions
# ----------------------------------------------------------------------

				# ----------------------------------------------------------------------
				# 			Merging the Accepting States
				# ----------------------------------------------------------------------

def AcceptingStateMerger (StateList, TransList):		#This Function will merge endstates in the DFM,
	AcceptingStates = []								#and rewire the associated transitions,
	LowestAcceptor = []
	for state in StateList:								#keeping only the lowest accepting state, which is that generated
		if state[2] == True:							#by the shortest-known string
			AcceptingStates.append(state)
	if len(AcceptingStates) <= 1:						#If there is only 1 accepting state, we're good
		pass
	elif len(AcceptingStates) > 1:						#but if there are more than 1 accepting states:
		for X in range(len(StateList)-1,-1,-1):			#go through them, starting with the highest state number,
			for state in AcceptingStates:				#and sequentially make each one that qualifies the LowestAcceptor
				if state[0] == X:						#so we eventually find the actual lowest accepting state
					if state[2] == True:
						LowestAcceptor = state
	if len(AcceptingStates) > 1:
		for state in AcceptingStates:					#then, once we know the LowestAcceptor:
			if state != LowestAcceptor:					#if there are any other states that are also accepting states,
				for transition in TransList:			#go through the known transitions,
					if transition[1] == state[0]:		#and rewire them to the LowestAcceptor
						transition[1] = LowestAcceptor[0]
					if transition[0] == state[0]:		#We have to rewire both states coming from the deleted state,
						transition[0] = LowestAcceptor[0]#as well as those transitions GOING TO the deleted state
														#if we don't, very, VERY bad things will happen.
				StateList.remove(state)					#Then delete the old extra accepting state

				# ----------------------------------------------------------------------
				# 			Checking for and Merging Common Transitions
				# ----------------------------------------------------------------------

def CheckForRedundentTransitions(TransList):			#once we have merged the accepting states, we then go back and merge
	# print 'Checking for Duplicate Transitions...'		
	NoDuplicateTrans = True 							#the transitions that we can, as well!
	CommonTrans = []
	for transition in TransList:						#if two transitions have the same destination and emission,
		CommonTrans = []								#then we will want to merge them, and the states they came from
		fromState = transition[0]
		toState = transition[1]
		Emission = transition[2]
		for otherTransition in TransList:
			if otherTransition[1] == toState and otherTransition[2] == Emission:
				CommonTrans.append(otherTransition)		#so first we make a list of duplicate transitions
		if len(CommonTrans) > 1:
			NoDuplicateTrans = False
	return CommonTrans, NoDuplicateTrans

def GetLowestTransition(TransList, CommonTrans):		#then we find the transition that came from the lowest-numbered state
	# print 'Duplicate Transitions Discovered.'			#(which is an arbitrary descision)
	# print 'TransList when duplicate is Discovered: ',TransList
	LowestTransition = sorted(CommonTrans)[0]
	LowestFromState = LowestTransition[0]
	return LowestFromState, LowestTransition

def GetDuplicateTransitions(LowestTransition, CommonTrans):
	DuplicateTransitions = []
	for transition in CommonTrans:
		if transition != LowestTransition:				#then, to keep things straight, I make a list containing ONLY the
			DuplicateTransitions.append(transition)		#transitions that we will be removing.
	return DuplicateTransitions

								# ----------------------------------------------------------------------
								# 			Merging a Transition
								# ----------------------------------------------------------------------

def RemoveTransition(DupTrans, StateList, TransList, LowestTransition):		#to merge transitions, we first remove the extra one,
	# print 'Transition to be removed: ',DupTrans
	TransList.remove(DupTrans)												#(we will do this all once per duplicate transition)
	DupTransFromState = DupTrans[0]											#and this is probably the most complicated part of the 
	RemoveState(DupTransFromState,StateList, TransList, LowestTransition)	#whole program, so pay attention!
																			#once we have removed the extra transition,
def RemoveState(DupTransFromState, StateList, TransList, LowestTransition):	#we then delete the state it came from,
	for state in StateList:
		if state[0] == DupTransFromState:
			# print 'State to be removed: ',state
			StateList.remove(state)
			DuplicateToState = DupTransFromState
			break
	# print 'Checking for stranded transitions to rewire...'
	RewireStrandedTransition(DuplicateToState, TransList, LowestTransition)
	RewireRootStrandedTransition(DuplicateToState, TransList, LowestTransition)

def RewireStrandedTransition(DuplicateToState, TransList, LowestTransition):#and then we look for any other transitions that go
	for transition in TransList:											#to that deleted state, and rewire them to go to the
		if transition[1] == DuplicateToState:								#surviving identical state
			if [transition[0],LowestTransition[0],transition[2]] in TransList:
				TransList.remove(transition)
				continue
			else:	
				# print 'Transition with ToState to rewire: ',transition
				transition[1] = LowestTransition[0]
				# print 'Newly rewired transition: ',transition

def RewireRootStrandedTransition(DuplicateToState, TransList, LowestTransition):
	for transition in TransList:											#very importantly, we also need to look for transitions
		if transition[0] == DuplicateToState:								#that can FROM that deleted state as well, and rewire them
			if [LowestTransition[0],transition[1],transition[2]] in TransList:
				TransList.remove(transition)								#if we don't, apocolyptically bad things will ensue
				continue
			else:	
				# print 'Transition with FromState to rewire: ',transition
				transition[0] = LowestTransition[0]
				# print 'Newly rewired transition: ',transition

def CommonTransitionMerger(StateList, TransList):							#This function calls all the ones above it and is
	CommonTrans, NoDuplicateTrans = CheckForRedundentTransitions(TransList)	#responsible for merging transitions where it is able
	if NoDuplicateTrans == False:
		LowestFromState, LowestTransition = GetLowestTransition(TransList, CommonTrans)
		DuplicateTransitions = GetDuplicateTransitions(LowestTransition, CommonTrans)
		for DupTrans in DuplicateTransitions:
			RemoveTransition(DupTrans, StateList, TransList, LowestTransition)
	# if NoDuplicateTrans == True:
		# print 'There are no Duplicate Transitions.'


# ----------------------------------------------------------------------
# 			Training Controller
# ----------------------------------------------------------------------
def TrainingController(FileLines, StateList, TransList):		#this function Controls the program during the training phase
	for line in FileLines:										#it governs the read-in of the traiing data,
		# print 'Line: ',line 	
		CheckLine (line, StateList, TransList)					#checking if new transitions and states are needed,
		AcceptingStateMerger(StateList, TransList)				#merging the acceting states after each line of input,
		for I in range(len(TransList)):							#checking for merge-able transitions,
			CommonTransitionMerger(StateList, TransList)		#and ordering their merger.
		# print 'StateList: ',StateList
		# print 'TransList: ',TransList
		DFMTroubleShooter (StateList, TransList)				#Also, after ever line in the input, and at the end, it will run the
	FinalTranlistChecker(TransList)								#troubleshooting functions, and stop the program if need be.
	print 'Final StateList: ',StateList
	print 'Final TransList: ',TransList 

TrainingController(FileLines, StateList, TransList)				# AKA the On/Off switch


# ----------------------------------------------------------------------
# 			Opening File Containing Training Data
# ----------------------------------------------------------------------

TestFile = 'TestingData.txt' 					#This is the file that contains samples to test the DFM on

TestLines = GetLines(TestFile)

# print 'TestLines: ',TestLines

# ----------------------------------------------------------------------
# 			Running Test Data through DFM
# ----------------------------------------------------------------------

def TestLine(line, StateList, TransList):	#this function will test each line of the test data by running them through
	fromState = 0							#the DFM.
	for letter in line:
		if letter == '#':
			for state in StateList:
				if state[0] == fromState:
					if state[2] == True:
						CanContinue = True 	#If it gets through the line fine, then it's in the language!  Yay!
					else:
						CanContinue = False #If it doesn't, or ends in a non-Accepting State, it's a dud.
					break
			break
		else:								#this function reuses the same Letter-Checking function above, yay for efficiency!
			fromState, CanContinue, TransList =  CheckLetterTrans(letter, fromState, TransList)
			if CanContinue == False:
				break
	# print 'Line: ',line,' | ',CanContinue
	return CanContinue						#this 'CanContinue' value is the yes/no judgement for the Test of each line

# ----------------------------------------------------------------------
# 			Generating Output
# ----------------------------------------------------------------------

def PrintDFMByNumbers(StateList, TransList):	#These are fairly self-explanatory, they make the output in a separate file.
	# f = open('TestResults.txt','a')
	f.write( '---------------------------------------------------------------------------------------\n')
	f.write('In order to get a visual of the DFM created from the training data,\n')
	f.write('you can use the StateList and TransList to make a DFM-by-numbers.\n\n')
	f.write('States have the following format: [label, Start-Bool, Accepting-Bool]\n')
	f.write('so [3, False, True], for example, is state number 3, which is not \n the start state, but is an end state.\n\n')
	f.write('Transitions have the following format: [FromState, ToState, EmissionLetter]\n')
	f.write("so [2, 4, 'a'], for example, is a directed transition from state 2 to state 4, with the emission 'a'\n\n")
	f.write( '---------------------------------------------------------------------------------------\n\n')
	f.write('Canonical DFM State List: ')
	f.write(str(StateList))
	f.write('\nCanonical DFM Transition List: ')
	f.write(str(TransList))
	f.write( '\n---------------------------------------------------------------------------------------\n\n')

def PrintTestDataResults(line, CanContinue):
	f = open('TestResults.txt','w')
	f.write(str(line))
	f.write('  |  ')
	f.write(str(CanContinue))
	f.write('\n')
	
# ----------------------------------------------------------------------
# 			Testing Controller
# ----------------------------------------------------------------------

f = open('TestResults.txt','w')				#this function controls the testing phase and output generation.
PrintDFMByNumbers(StateList, TransList)		#also fairly self-explanatory
f.write('\nThe following is the test data.  Each line is checked to see if it is in the language.\n')
f.write('The "True" or "False" after each line indicates if it is in the language or not.')
f.write( '\n---------------------------------------------------------------------------------------\n\n')
for line in TestLines:
	CanContinue = TestLine(line, StateList, TransList)
	# PrintTestDataResults
	f.write(str(line)[0:-1])
	f.write('  |  ')
	f.write(str(CanContinue))
	f.write('\n')
	
f.close()