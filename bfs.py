import GameBoard
import Util
import Shapes
from random import choice
import State

@staticmethod
def run(myBoard, myShapes):
	print 'Running from BFS.py...'
	
	finished = False
	root_state = State((0,0), myBoard, 0, None)
	state_queue = [ root_state ]
	shape_queue = copy.deepcopy(myShapes)
		
	while(len(shape_queue) > 0):
		# Use the same shape to generate child states for all current states in the queue
		for i in range(len(state_queue)):
			child_states = getSortedChildStates( state_queue[0], shape_queue[0] )
			state_queue.remove(state_queue[0])
			# need to prune some child states tp reduce the state space
			# CODE HERE
			state_queue.extend(child_states)
		shape_queue.remove(shape_queue[0])
	
	# Get the best final states (highest game scores)
	best_states = getHighestScoringStates(state_queue)
		
	return best_states[0]

@staticmethod
def getSortedChildStates(myCurrentState, shape):
	result_tuples = Util.Util.generate_child_states(myCurrentState, shape)
	child_states = sorted(result_tuples, key=lambda myCurrentState: myCurrentState[0], reverse = True)
	return child_states

# Returns a list of states with the highest game scores
@staticmethod
def getHighestScoringStates(list_of_states):
	return_list = []
	highest_score = 0
	for temp_state in list_of_states:
		if temp_state.game_score > highest_score:
			highest_score = temp_state.game_score
	for temp_state in list_of_states:
		if temp_state.game_score == highest_score:
			return_list.append(temp_state)
	return return_list

