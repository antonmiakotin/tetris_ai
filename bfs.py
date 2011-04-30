import GameBoard
import Util
import Shapes
import copy
import State
import os

panic_factor = 90
gap_killing = True

def run(myBoard, myShapes, max_tree_depth=5, branching_factor=2):
	
    total_shapes = len(myShapes)
    root_state = State.State((0,0), myBoard, 0, None)
    state_queue = [ root_state ]
    shape_queue = copy.deepcopy(myShapes)
    tree_depth = 0
    lost = False # this becomes true if we lose the game, duh
    # this is used to trace back to best state if we lose
    best_states_at_old_depth = State.State((0,0), myBoard, 0, None)
    
    while(len(shape_queue) > 0):
        best_states_at_old_depth = getHighestScoringStates(state_queue)
        # Use the same shape to generate child states for all current states in the queue
        for i in range(len(state_queue)):
            child_states = getSortedChildStates( state_queue[0], shape_queue[0] )
            current_board = state_queue[0].board
            state_queue.remove(state_queue[0])
            
            # we need to prune some child states to reduce the state space.
            # get_min_kill() will tell us the minimum number of lines we are allowed to kill
            min_kill = get_min_kill(current_board, len(shape_queue))
            # prune so only branching_factor states remain
            child_states = prune_states(child_states, branching_factor, min_kill)
            # CODE HERE
            state_queue.extend(child_states)
            print '.',
        shape_queue.remove(shape_queue[0])
        # If we lost the game
        if len(state_queue) == 0:
            lost = True
            break
        tree_depth += 1
        # print 'DEPTH =', str(tree_depth)
        # If the tree gets too deep, we need to start over at the best state so far
        if tree_depth >= max_tree_depth:
            print '.'
            print 'Restarting BFS from best state...'
            #os.system('pause')
            state_queue = [getHighestScoringStates(state_queue)[0]]
            print str(state_queue[0])
            print 'Shape', str(total_shapes - len(shape_queue)), '/', str(total_shapes)
            print 'Num blocks on board:', str(len(state_queue[0].board.landed))
            tree_depth = 0
	
    if lost == False:
        # Get the best final states (highest game scores)
        best_states = getHighestScoringStates(state_queue)
        print str(best_states[0])
        print 'We won! :)'
        print 'Final game score:', best_states[0].game_score
        os.system('pause')
        return best_states[0]
    else: # We lost the game
        print str(best_states_at_old_depth[0])
        print 'We lost! :('
        print 'Final game score:', best_states_at_old_depth[0].game_score
        os.system('pause')
        return best_states_at_old_depth[0]

def get_min_kill(board, num_of_shapes_remaining):
##    if (board.last_piece):
##        gaps = get_gaps(board)
##        last_part_coordinates = board.last_piece.get_coords()
##
##        highest_gap = get_y_min_and_max(gaps)[0]
##        lowest_spot_of_shape = get_y_min_and_max(last_part_coordinates)[1]
##
##        # If there is a gap below the shape somewhere, don't even try to kill more than 1 line
##        if lowest_spot_of_shape > highest_gap:
##            return 0

    num_blocks_on_board = len(board.landed)
    min_lines_to_kill = 0
    # num_blocks_avail is just the total number of blocks on the board plus the blocks yet to drop.
    num_blocks_avail = (num_of_shapes_remaining*4) + num_blocks_on_board
    if num_blocks_on_board >= panic_factor: # if the board starts to get filled up, it's time to panic
        min_lines_to_kill = 0
    elif num_blocks_avail >= 80: # 20 shapes should be able to kill 4 lines
        min_lines_to_kill = 4
    elif num_blocks_avail >= 60:
        min_lines_to_kill = 3
    elif num_blocks_avail >= 40:
        min_lines_to_kill = 2
    elif num_blocks_avail >= 20:
        min_lines_to_kill = 1
    return min_lines_to_kill
    
def getSortedChildStates(myCurrentState, shape):
    result_tuples = Util.Util.generate_child_states(myCurrentState, shape)
    child_states = sorted(result_tuples, key=lambda myCurrentState: myCurrentState[0], reverse = True)
    result_states = []
    for tup in child_states:
        result_states.append(tup[1])
    return result_states

# Returns a list of states with the highest game scores
def getHighestScoringStates(list_of_states):
    assert (len(list_of_states) > 0)
    return_list = []
    highest_score = -1
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
        if st.lines_killed == 0 or st.lines_killed >= kill_min or (gap_killing and is_killer_with_gap(st)):
            pruned_list.append(st)
            count += 1
        if count >= num_to_return:
            break
    return pruned_list

# This method returns a list of all the gap tuples in the board
def get_gaps(board):
    gaps = []
    found_top = False
    for x in range(board.max_x):
        for y in range(board.max_y):
            if found_top == False:
                if (x,y) in board.landed:
                    found_top = True
            else:
                if (x,y) not in board.landed:
                    gaps.append((x,y))
        found_top = False
    return gaps

def get_y_min_and_max(list_of_coords):
    if len(list_of_coords) == 0:
           return (0,0)
    y_max = list_of_coords[0][1]
    y_min = list_of_coords[0][1]
    for coord in list_of_coords:
        if coord[1] > y_max:
            y_max = coord[1]
        elif coord[1] < y_min:
            y_min = coord[1]
    return (y_min, y_max)

def is_killer_with_gap(state):
    board = state.board
    lines_killed = state.lines_killed
    if lines_killed == 0:
        return False
    last_piece = board.last_piece
    if (last_piece):
        piece_min_and_max = get_y_min_and_max(last_piece.get_coords())
        gaps = get_gaps(board)
        for gap in gaps:
            if gap[1] >= piece_min_and_max[0] and gap[1] <= piece_min_and_max[1]:
                return True
    return False
        
    
    
    
    
