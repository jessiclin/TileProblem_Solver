''' 
This program should be able to define the search problem with clearly labeled components that point to the state, actions, transition function and goal test.
Define a problem in terms of state, actions, transition function, and goal test 
TileProblem labels the components (variables, methods) that point to these elements 
'''
class TileProblem: 
    def __init__ (self, new, current = None, action = ""): 
        self.state = new
        self.prevState = current 
        
        for i in range(len(new)): 
            for j in range(len(new[i])): 
                if new[i][j] == 0: 
                    self.emptyCell = [i,j]
 
        self.prevAction = action 

        self.h = 0 
        self.g = 0
        self.f = 0

    
    # Actions that can be taken 
    def actions(self): 
        moves = [] 
        i = self.emptyCell[0]
        j = self.emptyCell[1] 
        
        if i > 0: 
            moves.append('U')
        if i < len(self.state)-1: 
            moves.append('D') 
        if j > 0: 
            moves.append('L') 
        if j < len(self.state[0])-1: 
            moves.append('R') 
            
        return moves 
       
    # Transition Function 
    def transition(self, move): 
        move = move.upper()
        
        # Copy puzzle 
        copy = [] 
        
        for i in range(len(self.state)): 
            row = [] 
            for j in range(len(self.state[i])): 
                row.append(self.state[i][j])
            copy.append(row) 
        i = self.emptyCell[0]
        j = self.emptyCell[1] 
        
        # Left 
        if move == 'L' and j > 0: 
            copy[i][j], copy[i][j-1] = copy[i][j-1], 0 
        # Right 
        elif move == 'R' and j < len(copy)-1:
            copy[i][j], copy[i][j+1] = copy[i][j+1], 0 
        # Up 
        elif move == 'U' and i > 0: 
            copy[i][j], copy[i-1][j] = copy[i-1][j], 0 
        # Down 
        elif move == 'D' and i < len(copy[0]):
            copy[i][j], copy[i+1][j] = copy[i+1][j], 0 
        else: 
            print("Invalid Move") 
        
        return copy
        
    # Return true if at goal state 
    def goalState(self): 
        prev = 0 
        for i in range(len(self.state)): 
            for j in range(len(self.state[i])): 
                if i == len(self.state)-1 and j == len(self.state[i])-1 and self.state[i][j] == 0: 
                    return True 
                if self.state[i][j] != prev+1:
                    return False 
                else: 
                    prev = self.state[i][j] 
                    
        return True     
        
    def __eq__(self, other): 
        return (self.g + self.h) == (other.g + other.h)
    def __gt__(self, other): 
        return (self.g + self.h) > (other.g + other.h)
        