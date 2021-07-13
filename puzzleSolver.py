'''
This program should be able to take as input an 8 or a 15 puzzle and output the set of moves required to solve the problem.

python puzzleSolver.py <A> <N> <H> <INPUT FILE> <OUTPUT FILE> 
A -> Algorithm (1 = A*, 2 = RBFS) 
N -> Size of puzzle (3 = 8-puzzle, 4 = 16-puzzle) 
H -> Heuristic (1 = h1, 2 = h2) 


h1(n) > h2(n) for all n ** 
'''
import sys 
from TileProblem import TileProblem 
from queue import PriorityQueue

############# Heuristics ###############
class Heuristic: 
    # Manhatten Distance 
    def h1(self, state, goal):
        goalLocations = dict() 
        
        for i in range(len(goal)): 
            for j in range(len(goal[i])): 
                goalLocations[goal[i][j]] = [i,j]

        sum = 0 
        for i in range(len(state)): 
            for j in range(len(state[i])): 
                if state[i][j] != 0: 
                    g = goalLocations[state[i][j]]  
                    sum += abs(g[0] - i) + abs(g[1] - j)

        return sum 
    
    # Hamming Distance 
    def h2(self, state, goal):
        misplaced = 0 
        for i in range(len(state)): 
            for j in range(len(state[i])): 
                if state[i][j] != goal[i][j] and state[i][j] != 0: 
                    misplaced += 1 
        return misplaced 
        

############### RBFS ##################
def rbfs(problem, f_limit, goal, heuristic): 
    if problem.goalState(): 
        return problem, f_limit
        
    successors = [] 
    for action in problem.actions(): 
        new = problem.transition(action) 
        newNode = TileProblem(new, problem, action) 
        newNode.h = heuristic(newNode.state, goal)
        newNode.g = problem.g+1 
        successors.append(newNode) 
    
    
    if len(successors) == 0: 
        return None, float('inf')
    
    for s in successors: 
        s.f = max(s.g + s.h, problem.f)

    while True: 
        best = successors[0] 
        index = 0 
        for i in range(len(successors)): 
            if best.f > successors[i].f: 
                best = successors[i] 
                index = i 
                
        
        temp = successors.pop(index) 

        if best.f > f_limit: 
            return None, best.f 

        alternative = successors[0]
        for i in range(len(successors)): 
            if alternative.f > successors[i].f and successors[i].f > best.f: 
                alternative = successors[i]

        successors.insert(index, temp)
        
        result, best.f = rbfs(best, min(f_limit, alternative.f), goal, heuristic)
        if result is not None: 
            return result, best.f



############## A* #################    
def a(start, goal, heuristic): 
    frontier = PriorityQueue()
    explored = [] 
    frontier.put(start)

    while not frontier.empty(): 
        
        current = frontier.get() 
     
        if current.goalState(): 
            return current 
        if current.state not in explored: 
            
            explored.append(current.state) 

            for action in current.actions(): 
                new = current.transition(action)
                newNode = TileProblem(new, current, action) 
                newNode.h = heuristic(newNode.state, goal)
                newNode.g = current.g+1 
                frontier.put(newNode)
           
    return None 


######## Proccess Results and output to text file ########    
def processResult(state, outputFile): 
    if not state: 
        return 
        
    if state.prevState.prevAction != "": 
        processResult(state.prevState, outputFile)

    if state.goalState(): 
        with open(outputFile, 'a') as f:
            f.write(state.prevAction)
    else: 
        with open(outputFile, 'a') as f:
            f.write(state.prevAction + ",")


####### Main Function ########
def main(): 
    args = sys.argv 
    if len(args) != 6: 
        print("Incorrect number of arguments") 
        exit() 
        
    A = int(args[1])
    N = int(args[2])
    H = int(args[3])
    inputFile = args[4] 
    outputFile = args[5] 

    if A != 1 and A != 2: 
        print("Invalid Algorithm") 
        exit()
    if N != 3 and N != 4: 
        print("Invalid Size")
        exit() 
    if H != 1 and H != 2: 
        print("Invalid Heuristic")
        exit() 

    puzzle = [] 
    goal = [] 
    with open(inputFile, 'r') as f: 
        i = 1 
        for line in f.read().split(): 
            row = [] 
            goalRow = [] 
            for number in line.split(','): 
                if number == "": 
                    row.append(0) 
                else: 
                    row.append(int(number))
                goalRow.append(i) 
                i += 1 
            puzzle.append(row) 
            goal.append(goalRow) 
            
        goal[-1][-1] = 0
    
    problem = TileProblem(puzzle)
    heuristic = Heuristic() 
    
    if len(goal) != N: 
        print("N Mismatch")
        exit() 
        
    f = open(outputFile, 'w+')
    f.close()
    
    # Perform A* 
    if A == 1: 
        if H == 1: 
            result = a(problem, goal, heuristic.h1)
        else:
            result = a(problem, goal, heuristic.h2)
        processResult(result, outputFile)


    # Perform RBFS 
    else: 
        if H == 1: 
            result, bestf = rbfs(problem, float('inf'), goal, heuristic.h1)
        else: 
            result, bestf = rbfs(problem, float('inf'), goal, heuristic.h2)
            
        processResult(result, outputFile)

if __name__ == "__main__":
    main()      

    