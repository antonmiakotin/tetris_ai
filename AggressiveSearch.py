# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin


# Method runs the algorithm
@staticmethod
def run(board, state_list, threshold):
    pass
    # for list of pieces
    # first grab the first set of states given the parent state
    # order them by points
    # if under the threshold
    # remove the ones where less than 4 lines have been created
    # else place the ones where a line has been created to the front
    # remove all but the best 3 choices
    # if lines have been created calculate the points
    # expand the results on those 3 choices
    # as we want to remove those first
    # loop back and grab the next piece
    #
    # after all pieces have been played
    # return board with highest score
