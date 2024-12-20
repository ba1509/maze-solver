# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:04:23 2024

@author: AB 1509
"""
import heapq

import tkinter as tk
from tkinter import filedialog

# Goal state



Goal_state3 = (1,2,3,
               4,5,6,
               7,8,0)

Goal_state4 = (1,2,3,4,
               5,6,7,8,
               9,10,11,12,
               13,14,15,0)

"""
Function is used to find the neighbouring state of the puzzle.
"""

def neighbouringstate(state, grid_size ):
    #state will be an array
   neighbors = []
   index = state.index(0)  # Find the blank
   row = index // grid_size  # Integer division to get the row number
   col = index % grid_size   # Modulus to get the column number
   
   dictionarynumber = {'Up': -grid_size,'Down': grid_size,'Left': -1, 'Right': 1}
   

   
   possible_moves = []
   # Check if the blank can move Right
   if col < grid_size - 1:
       possible_moves.append('Right')
   # Check if the blank can move Up
   if row > 0:
       possible_moves.append('Up')
   # Check if the blank can move Down
   if row < grid_size - 1:
       possible_moves.append('Down')
   # Check if the blank can move Left
   if col > 0:
       possible_moves.append('Left')
  
   
   #print(moves)
   for move in possible_moves:
       change = dictionarynumber[move]
       new_index = index + change
       # Swap the blank with the adjacent tile
       # convert to list as tuple are immutable
       newstate = list(state)
       temp = newstate[index]              # Store the value at the original index in temp
       newstate[index] = newstate[new_index]  
       newstate[new_index] = temp          
       neighbors.append(tuple(newstate))
   
    
   return neighbors 
    
    
 #need to adapt the code to size need to add an index parameter
"""
Checks if goal state of a puzzle has been reached
""" 

def isgoal (state , index):
    
    #if state == Goal_state3 or state == Goal_state4:
       # return Goal_state3
    if index == 3 and state == Goal_state3:
        return True
    if index == 4 and state == Goal_state4:
         return True
     
    return False
     

#iddfs implementation

def dls( state, depth, path, index):
    if isgoal(state, index):
        return path + [state]
    
    if depth == 0:
        return None
    
    for neighbour in neighbouringstate(state, index):
        
        if neighbour not in path:
           
            result = dls(neighbour,depth-1, [state]+path, index)
            
            if result is not None :
                return result
               
    return None


def iddfs (startstate, index):
    depth = 0
    max_depth = 50  # Adjust as necessary
    while depth <= max_depth:
        result = dls(startstate, depth, [], index)
        if result is not None:
            return result
        depth += 1
    print("Solution not found within maximum depth.")
    return None
    
        
"""
function prints the number of path till solution is found and the change in state
"""    
def printsol(path, size):
    numberofpath = len(path)
    
    if path:
        print("solution found in ")
        print(numberofpath)
        for x in path:
           for i in range(len(x)):
               if x[i] == 0:
                   print('_', end=' ')
               else:
                   print(x[i], end=' ')
    
               if (i + 1) % size == 0:
                   print()
           print("\n")
                
                #for num in x[i:i+size]:
                   # print(num)
                    
    else:
         print("no solution")                           
                
            
        
"""
calculate the manhattan distance between current state and the goal state
"""

def manhattan_distance(state, index):
    dis = 0 # distance for the manhattan
    
    for number in range(1, index -1):
        current = state.index(number)
        if index == 3: # for 3*3 maze
           goalindex = Goal_state3.index(number)
       
        if index == 4: # for 4 * 4 maze
            goalindex = Goal_state4.index(number)
            
        current_row = current // 3
        current_col = current % 3
        
        goalrow = goalindex // 3
        goal_col = goalindex % 3
        
        row_difference = abs(current_row - goalrow)
        col_difference = abs(current_col - goal_col)

# Update the total distance
        dis = dis + row_difference + col_difference
        
    return dis  

# a star implementation with manhattan heuristic

def a_star(state,  index):
    
    openlist = [(manhattan_distance(state, index), 0 , state)] #  priority queue to keep track of states to explore. stores f_score, g_score, state
    heapq.heapify(openlist)
    gscore = {state:0}
    closed_set = set() # keep track of visited states
    
    camefrom = {}
    while openlist:
        currentf, currentg, current = heapq.heappop(openlist)
        #currentf = f score
        #currentg = g score
        #current = current state
        
        if index == 3: # for maze of size 9
            if current == Goal_state3:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
                return path

# Mark the current state as visited
        closed_set.add(current)
        
        if index == 4: # for maze of size 16
            if current == Goal_state4:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
    
                return path

        closed_set.add(current)
        
#
        
        
        
        for neighbour in neighbouringstate(current, index): # generates neigbouring states
            if neighbour in closed_set:
                continue
            tg = gscore[current]+ 1
            
            if neighbour not in gscore or tg < gscore[neighbour]:
                camefrom[neighbour] = current
                gscore[neighbour] = tg
                fscore = tg + manhattan_distance(neighbour,index)
                heapq.heappush(openlist, (fscore, tg, neighbour))
    
    return None 


# second heuristic

"""
@param: state represents the puzzle
@param: goalstate reprsents the target of the puzzle for an index of 3
@param: goalstate2 reprsents the target of the puzzle for an index of 4
@param: index = size of puzzle must be 3 or 4

"""

def misplacedtiles(state, goalstate,goalstate2, index):
    
    count = 0
    if index == 3:
        for i in range(len(state)):
           tile = state[i]  # Get the tile at position i
           if tile != 0 and tile != goalstate[i]:
               count += 1  # Increment the counter
        return count  # Return the total number
    
    count = 0
    if index == 4:
        for i in range(len(state)):
           tile = state[i]  # Get the tile at position i
           if tile != 0 and tile != goalstate2[i]:
               count += 1  # Increment the counter
        return count  # R
        
    
"""
Algorithm for a star with misplaced tiles as heuristics
 
"""   

def a_star2state(state,  index):
    
    openlist = [(manhattan_distance(state, index), 0 , state)] #  priority queue to keep track of states to explore. stores f_score, g_score, state
    heapq.heapify(openlist)
    gscore = {state:0}
    closed_set = set() # keep track of visited states
    
    camefrom = {}
    while openlist:
        currentf, currentg, current = heapq.heappop(openlist)
        #currentf = f score
        #currentg = g score
        #current = current state
        
        if index == 3: # for maze of size 9
            if current == Goal_state3:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
                return path

# Mark the current state as visited
        closed_set.add(current)
        
        if index == 4: # for maze of size 16
            if current == Goal_state4:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
    
                return path

        closed_set.add(current)
        
#
        
        
        
        for neighbour in neighbouringstate(current, index): # generates neigbouring states
            if neighbour in closed_set:
                continue
            tg = gscore[current]+ 1
            
            if neighbour not in gscore or tg < gscore[neighbour]:
                camefrom[neighbour] = current
                gscore[neighbour] = tg
                fscore = tg + misplacedtiles(neighbour,Goal_state3, Goal_state4,index)
                heapq.heappush(openlist, (fscore, tg, neighbour))
    
    return None  


"""
The next 2 function tests whether the puzzle is solvable or not
"""


def inversion (state):
    count = 0
    puzzle = []
    for num in state:
        if num != 0:
            puzzle.append(num)
            
  
    lenghtpuzzle = len(puzzle)
    for i in range(lenghtpuzzle):
        for j in range (i+1,lenghtpuzzle):
            if puzzle[i] > puzzle[j]:
                      count += 1
    return count
                
 # to be redone               
def is_solvable(puzzle, gridsize):
    
    inversions = inversion(puzzle)
    # Find row of the blank
    location0 = (puzzle.index(0))
    
    blanktop = location0 // gridsize + 1
    blankrow = gridsize - blanktop + 1
    
    gridwidth = gridsize % 2 
    
    
    
    if gridwidth != 0:
        # if Grid width = odd, puzzle is solvable
        return inversions % 2 == 0
    else:
        # Grid width is even 
        
        return (blankrow % 2 == 0) == (inversions % 2 !=0)
      
    
    
    
def gascbnig_heuristic(state, goalstate, goalstate2, index):
    countswap = 0
    goalindex3 = list(goalstate)
    goalindex4 = list(goalstate2)
    current = list(state)
    
    
    goal_pos = {}
    
    currentpos = {}
    for u in range(0, len(current)):
        title = current[u]
        currentpos[title] = u
    
    if index == 3:
        for u in range(0, len(goalindex3)):
            title = goalindex3[u]
            goal_pos[title] = u
            
        while current != goalindex3:
             blanktile = currentpos[0]
             
             if current[blanktile] != goalindex3[blanktile]:
           
                    correct_tile = goalindex3[blanktile]  # stores the position of the blank tile
                    correct_tile_idx = currentpos[correct_tile] # stores the content of the current tile
        
                    # Swap the blank tile with the correct tile
                    
                    temp = current[blanktile]
                    current[blanktile] = current[correct_tile_idx]
                    current[correct_tile_idx] = temp
        
                    # Update the positions in the current_pos dictionary
                    currentpos[0] = correct_tile_idx
                    currentpos[correct_tile] = blanktile
             else:
                # Find any tile that is out of place (excluding the blank tile)
                for idx in range(len(current)):
                    if current[idx] != goalindex3[idx] and current[idx] != 0:
                        # Swap the blank tile with this misplaced tile
                        temp = current[blanktile]
                        current[blanktile] = current[idx]
                        current[idx] = temp
    
                        # Update the positions in the current_pos dictionary
                        currentpos[current[blanktile]] = blanktile
                        currentpos[current[idx]] = idx
                        break
    
            # Increment the swap count after each swap
             countswap += 1
    
        # Return the total number of swaps as the heuristic value
        return countswap
                 
             
            
    if index == 4:
         for u in range(0, len(goalindex4)):
             title = goalindex4[u]
             goal_pos[title] = u
             
         while current != goalindex4:
               blanktile = currentpos[0]
               
               if current[blanktile] != goalindex4[blanktile]:
             
                      correct_tile = goalindex4[blanktile]  # stores the position of the blank tile
                      correct_tile_idx = currentpos[correct_tile] # stores the content of the current tile
          
                      
                      
                      temp = current[blanktile]
                      current[blanktile] = current[correct_tile_idx]
                      current[correct_tile_idx] = temp
          
                      # Update the positions in the current_pos dictionary
                      currentpos[0] = correct_tile_idx
                      currentpos[correct_tile] = blanktile
               else:
                  # Find any tile that is out of place (excluding the blank tile)
                  for idx in range(len(current)):
                      if current[idx] != goalindex4[idx] and current[idx] != 0:
                          # Swap the blank tile with this misplaced tile
                          temp = current[blanktile]
                          current[blanktile] = current[idx]
                          current[idx] = temp
    
                          # Update the positions in the current_pos dictionary
                          currentpos[current[blanktile]] = blanktile
                          currentpos[current[idx]] = idx
                          break

          
               countswap += 1

      # Return the total number of swaps as the heuristic value
               return countswap
    
    
    
        
   
"""
a star algorithm for gascbnig_heuristic
""" 
def a_starga(state,  index):
    
    openlist = [(manhattan_distance(state, index), 0 , state)] #  priority queue to keep track of states to explore. stores f_score, g_score, state
    heapq.heapify(openlist)
    gscore = {state:0}
    closed_set = set() # keep track of visited states
    
    camefrom = {}
    while openlist:
        currentf, currentg, current = heapq.heappop(openlist)
        #currentf = f score
        #currentg = g score
        #current = current state
        
        if index == 3: # for maze of size 9
            if current == Goal_state3:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
                return path

# Mark the current state as visited
        closed_set.add(current)
        
        if index == 4: # for maze of size 16
            if current == Goal_state4:
                
                path = []
                node = current
                while node in camefrom:
                    path.insert(0,node)
                    node = camefrom[node]
                path.insert(0, state)  # Add the start state at the beginning
    
                return path

        closed_set.add(current)
        
#
        
        
        
        for neighbour in neighbouringstate(current, index): # generates neigbouring states
            if neighbour in closed_set:
                continue
            tg = gscore[current]+ 1
            
            if neighbour not in gscore or tg < gscore[neighbour]:
                camefrom[neighbour] = current
                gscore[neighbour] = tg
                fscore = tg + gascbnig_heuristic(neighbour,Goal_state3, Goal_state4,index)
                heapq.heappush(openlist, (fscore, tg, neighbour))
    
    return None            
            
            
    
    # TO WRITE PROGRAM TOR READ FILE
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.withdraw() 
    file = filedialog.askopenfile()
    
    if file :
        
        
        #content = file.read()
        lines = file.readline()  # stores the first line
        
        size1 = int( lines)
        # Initialize a variable to store the rest of the lines
        temp = ""
        while lines:
            
            lines = file.readline()
            temp += lines 
            
                
            
        result = temp.split()
        length = len(result)
        for x in range(0, length):
            if result[x] == 'X':
                result[x] = '0'
            
                
        integer_list = list(map(int, result))
        tupleread = tuple(integer_list)
        size = len(tupleread)
        print(tupleread) # Print the file contents
        
        # Check if the puzzle is solvable
        print(is_solvable(tupleread, size))
        print(is_solvable(tupleread,size1))
        
        if is_solvable(tupleread, size1):
               
               print("Solving using IDDFS:")
               solution_iddfs = iddfs(tupleread, size1)
               printsol(solution_iddfs, size1)
               
              # printsol(solution_iddfs, size1)
              # print(neighbouringstate(tupleread, size1) )
               solution = a_star(tupleread,size1)
               print("Solving using A* star  manhattan")
               printsol(solution, size1)
               
               print("Solving using A* star  2 state")
               
               solution1 = a_star2state(tupleread, size1)
               printsol(solution1, size1)
               print("Solving using A* star using the Gaschnig Heurostics  ")
               
               solution4 = a_starga(tupleread, size1)
               printsol(solution4, size1)
               

        else:
            # Solve using IDDFS
            print("The puzzle is not solvable.")
            
    else:
        print("No selection ")
    
    
            
    

        
        
        
        