import GameBoard
import Util
import Shapes
import copy
import State
import os

max_tree_depth = 8

def run(myBoard, myShapes):
    print 'Running from BFS.py...'
	
    finished = False
    root_state = State.State((0,0), myBoard, 0, None)
    state_queue = [ root_state ]
    shape_queue = copy.deepcopy(myShapes)
    tree_depth = 0
    
    while(len(shape_queue) > 0):
        # Use the same shape to generate child states for all current states in the queue
        for i in range(len(state_queue)):
            child_states = getSortedChildStates( state_queue[0], shape_queue[0] )
            state_queue.remove(state_queue[0])
            # need to prune some child states to reduce the state space
            child_states = prune_states(child_states,2,3)
            # CODE HERE
            state_queue.extend(child_states)
        shape_queue.remove(shape_queue[0])
        tree_depth += 1
        # If the tree gets too deep, we need to start over at the best state so far
        if tree_depth > max_tree_depth:
            print 'Restarting BFS from best state...'
            os.system('pause')
            state_queue = getHighestScoringStates(state_queue)[0]
            tree_depth = 0
	
    # Get the best final states (highest game scores)
    print 'getting best states...'
    best_states = getHighestScoringStates(state_queue)
    print str(best_states[0])
    os.system('pause')
    return best_states[0]

def getSortedChildStates(myCurrentState, shape):
    result_tuples = Util.Util.generate_child_states(myCurrentState, shape)
    child_states = sorted(result_tuples, key=lambda myCurrentState: myCurrentState[0], reverse = True)
    result_states = []
    for tup in child_states:
        result_states.append(tup[1])
    return result_states

# Returns a list of states with the highest game scores
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

# This method will prune the states that kill 1 or more rows but don't kill at least kill_min states
# Also, it will return no more than num_to_return states
def prune_states(state_list, num_to_return, kill_min):
    pruned_list = []
    count = 0
    for st in state_list:
        if st.lines_killed == 0 or st.lines_killed >= kill_min:
            pruned_list.append(st)
            count += 1
        if count >= num_to_return:
            break
    return pruned_list