import GameBoard
import Util
import Shapes
from random import choice
import State
import time
from Tkinter import *

class local:

	def __init__(self, board, piece_list):
		self.board = board
		self.parent = board.parent
		self.piece_list = piece_list
		self.id = (0,0)
		self.init_state = State.State(self.id, self.board, 0, None)
		
		self.board.pack_tk()
		self.after_id = self.parent.after( 0, self.run )
		
		#iterator for run function
		self.count = 0

	#run must not take any arguments
	def run(self):
		if self.count < len(self.piece_list):
			piece = self.piece_list[self.count]
		#while True:
			#for i in range(len(self.child_states)):
			#need to remove root nodes from board list
			#state = self.child_states.pop(i)
			#run states function
			result_tuples = Util.Util.generate_child_states(self.init_state, piece)
			
			#sort all boards, highest score first
			result_tuples = sorted(result_tuples, key=lambda state: state[0], reverse = True)
			#pick the top 3
			result_tuples = result_tuples[:1]
			best_state = result_tuples[0][1]

			self.init_state = best_state
			
			#TK drawing
			self.board.canvas.delete(ALL)
			for coord in best_state.board.landed:
				self.board.add_block(coord, "blue")
			
			for block in best_state.board.last_piece.blocks:
				if block.coord() in best_state.board.landed:
					self.board.add_block(block.coord(), "red")
			#re-schedule to run again
			self.count += 1
			self.after_id = self.parent.after( 1, self.run )
		else:
			Toplevel().quit()
			self.board.parent.quit()
			
	if __name__ == "__main__":
		#for now controller doesn't do anything
		#do all work manually
		
		#create game board, fill with some squares to test eval
		board = GameBoard.Board()
		
		#fill in the bottom row
		for x in range (1,10):
			for y in range(5,20):
				board.landed.append((x,y))
		#throw some more random blocks
		#board.landed.append((3,18))
		#board.landed.append((2,18))
		#board.landed.append((7,18))
		#board.landed.append((7,17))
		
		f = open("output.txt", 'w')   

		shape_classes = [Shapes.square_shape, Shapes.t_shape, Shapes.l_shape, Shapes.reverse_l_shape, Shapes.i_shape]
		random_pieces = []
		#pic random pieces
		for i in range(1000):
			cls = choice(shape_classes)
			random_pieces.append(cls)
		id = (0,0)
		init_state = State.State(id, board, 0, None)
		child_states = [init_state]
		random_pieces = [Shapes.i_shape]

		for piece in random_pieces:
		#while True:
			#piece = choice(shape_classes)    
			for i in range(len(child_states)):
				#need to remove root nodes from board list
				state = child_states.pop(i)
				#run states function
				result_tuples = Util.Util.generate_child_states(state, piece)
				
				#sort all boards, highest score first
				#result_tuples = sorted(result_tuples, key=lambda state: state[0], reverse = True)
				#pick the top 3
				#result_tuples = result_tuples[:1]

				#output to file
				#f.write( "BASE STATE\n" )
				#f.write( "#"*30+"\n" )
				#f.write( str(state) )
				#f.write( "CHILD STATES\n" )
				print "CHILD STATES"
				print "#"*30+"\n"
				
				#f.write ( "#"*30+"\n" )
				for tup in result_tuples:
					#f.write( str(tup[1].board.last_piece) + "\n")
					#f.write( str(tup[1]) )
					print "Score: ", str(tup[1].game_score)
					print str(tup[1])
					child_states.append(tup[1])
					#time.sleep(.5)
				#f.write( "\n\n")
