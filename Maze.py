################################################################################### Imports ######################################################################################
import heapq
import random as rand
import tkinter as tk
from tkinter import ttk

################################################################################### Attributes ###################################################################################
rows, cols = 6, 6

################################################################################### Algorithms ###################################################################################
# method to create maze using 2d array and randomly create start,goal,barrier nodes
def create_maze():
    # generate a 2d array
    maze_2d_array = [[' '] * cols for row in range(rows)]
    # Randomly select start and goal nodes
    global start_node, goal_node
    start_node = rand.randint(0, 11)
    goal_node = rand.randint(24, 35)

    # Mark start and goal nodes
    maze_2d_array[start_node % cols][start_node // cols] = 'S'
    print("start node = maze[" + str(start_node % cols) + "], [" + str(start_node // cols) + "]" + str(start_node))

    maze_2d_array[goal_node % cols][goal_node // cols] = 'G'
    print("goal node = maze[" + str(goal_node % cols) + "], [" + str(goal_node // cols) + "]" + str(goal_node))

    # Randomly select barrier nodes
    barrier_nodes = rand.sample(list(set(range(36)) - {start_node, goal_node}), 4)
    print("barrier nodes :" + str(barrier_nodes))
    for barrier_node in barrier_nodes:
        maze_2d_array[barrier_node % cols][barrier_node // cols] = 'X'
    print(maze_2d_array)
    return maze_2d_array


# Function to visualize the maze
def Visualize_maze(maze, canvas, path=None):
    canvas.delete("all")
    for i in range(rows):
        for j in range(cols):
            cell_value = maze[i][j]
            color = "white" \
                if cell_value == 0 else "black" \
                if cell_value == 'X' else "green" \
                if cell_value == 'S' else "red" \
                if cell_value == 'G' else "white"
            canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color, outline="black")
            canvas.create_text((j + 0.5) * 50, (i + 0.5) * 50, text=str(cell_value))

    if path:
        for node in path:
            i, j = node % cols, node // cols
            canvas.create_rectangle(j * 50 + 10, i * 50 + 10, (j + 1) * 50 - 10, (i + 1) * 50 - 10, outline="blue",
                               width=2)


def depth_first_Search(maze, start, goal):
    visited_set = set()
    stack = [(start, [])]
    while stack:
        current, path = stack.pop()
        if current == goal:
            print("\nDFS Results:")
            print("all visited nodes :", path + [current])
            print("Time to Find Goal:", len(visited_set) + 1)
            return visited_set, path + [current]

        if current not in visited_set:
            visited_set.add(current)
            neighbors = get_neighbors(maze, current)
            stack.extend((neighbor, path + [current]) for neighbor in neighbors)
            print(stack)
    print("\nDFS Results:")
    print("All visited nodes :" + str(visited_set))
    print("Time to execute:", len(visited_set))
    return visited_set, None


def heuristic(node, goal):
    nx, ny = node % cols, node // cols
    gx, gy = goal % cols, goal // cols
    return abs(nx - gx) + abs(ny - gy)


def astar_search(maze, start, goal):
    visited_set = set()
    priority_queue = [(0, start, [])]
    print(priority_queue)
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        print(_, current, path)
        if current == goal:
            print("\nA* Search Results:")
            print("Visited nodes: ", path + [current])
            print("Time to Find Goal:", len(visited_set) + 1)
            return visited_set, path + [current]

        if current not in visited_set:
            visited_set.add(current)
            neighbors = get_neighbors(maze, current)
            for neighbor in neighbors:
                print(path + [current])
                heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor, path + [current]))
        print(priority_queue)
    print("\nA* Search Results:")
    print("Visited nodes: " + str(visited_set))
    print("Time to execute:", len(visited_set))
    return visited_set, None


# Function to get valid neighbors for DFS
def get_neighbors(maze, current):
    print(current)
    row, col = current % cols, current // cols
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if maze[i][j] != 'X' and (i, j) != (row, col):
                neighbors.append(j * cols + i)
    print(neighbors)
    neighbors.sort(reverse=True)
    print(neighbors)
    return neighbors



################################################################################### GUI ###################################################################################
# pass arguments to visualize maze method when clicking the maze_btn
def Visualize_maze_wrapper():
    global maze
    maze = create_maze()
    Visualize_maze(maze, canvas)


# pass arguments to depth_first_Search method when clicking the DFS_btn
def depth_first_Search_wrapper():
    try:
        if goal_node == -1:
            Visualize_maze_wrapper()
    except:
        Visualize_maze_wrapper()

    visited_dfs, path_dfs = depth_first_Search(maze, start_node, goal_node)
    Visualize_maze(maze, canvas, path_dfs)

# pass arguments to astar_search method when clicking the Astar_btn
def astar_search_wrapper():
    try:
        if goal_node == -1:
            Visualize_maze_wrapper()
    except:
        Visualize_maze_wrapper()
    visited_astar, path_astar = astar_search(maze, start_node, goal_node)
    Visualize_maze(maze, canvas, path_astar)


def compare_path():
    root.destroy()
    for i in range(3):
        root1 = tk.Tk()
        root1.geometry('610x750')
        name = "DFS path " + str(i + 1)
        root1.title('Maze ' + str(i + 1))
        title_lb = tk.Label(root1, text=name, bg='#6b5b95', fg='white',
                            font=('Bold', 20))
        title_lb.grid(column=0, row=0)
        canvas1 = tk.Canvas(root1, width=cols * 50, height=rows * 50, border=1)
        canvas1.grid(column=0, row=1)
        maze1 = create_maze()
        visited_dfs, path_dfs = depth_first_Search(maze1, start_node, goal_node)
        Visualize_maze(maze1, canvas1, path_dfs)

        name = "A* path " + str(i + 1)
        title_lb = tk.Label(root1, text=name, bg='#6b5b95', fg='white',
                            font=('Bold', 20))
        title_lb.grid(column=1, row=0)
        canvas1 = tk.Canvas(root1, width=cols * 50, height=rows * 50)
        canvas1.grid(column=1, row=1)
        visited_astar, path_astar = astar_search(maze1, start_node, goal_node)
        Visualize_maze(maze1, canvas1, path_astar)
        result =compaire(path_astar,visited_dfs)
        frame = tk.Frame(root1)
        frame.grid(column=0, row=2, columnspan=2)
        table = ttk.Treeview(frame, columns=('Column 1', 'Column 2', 'Column 3'), show='headings')
        table.heading('Column 1', text='')
        table.heading('Column 2', text='DFS Path')
        table.heading('Column 3', text='A* Path')
        content = ["Completeness :", "Optimality :", "Time complexity :"]

        for i in range(3):
            table.insert('', 'end',
                         values=(content[i], result[i * 2], result[i * 2 + 1]))
        table.pack()
        button1 = tk.Button(root1, text = "next", font=('Bold', 20), bd=0, bg='#6b5b95', fg='white', width=15,
                         activebackground='#b0aac0', activeforeground='white', command=root1.quit)
        button1.place(x=180, y=650)
        root1.mainloop()
        root1.destroy()
    main()

def compaire(A_path,Dfs_path):
    result=[]
    DFS_complexity = len(Dfs_path)
    Astar_complexity = len(A_path)
    if A_path!=[] and Dfs_path !=[]:
        if len(A_path)>=len(Dfs_path):
            result.append("Found a path(compleat)")
            result.append("Found a path(compleat)")
            result.append("optimal")
            result.append("optimal")
            result.append("O("+str(DFS_complexity)+")")
            result.append("O(" + str(Astar_complexity) + ")")

        elif len(A_path)<len(Dfs_path):
            result.append("Found a path(compleat)")
            result.append("Found a path(compleat)")
            result.append("Not optimal")
            result.append("optimal")
            result.append("O("+str(DFS_complexity)+")")
            result.append("O(" + str(Astar_complexity) + ")")

    elif Dfs_path==[] and A_path!=[]:
        result.append("Path not found(not compleat)")
        result.append("Found a path(compleat)")
        result.append(" _ ")
        result.append("optimal")
        result.append("O(" + str(DFS_complexity) + ")")
        result.append("O(" + str(Astar_complexity) + ")")

    return result

def main():
    global root
    root = tk.Tk()
    root.geometry('1200x400')
    root.title('Maze')

    Maze_btn = tk.Button(root, text='New Maze', font=('Bold', 20), bd=0, bg='#6b5b95', fg='white', width=15,
                         activebackground='#b0aac0', activeforeground='white', padx=25, borderwidth=3, command=Visualize_maze_wrapper)
    Maze_btn.place(x=20, y=10)

    DFS_btn = tk.Button(root, text='Solve with DFS', font=('Bold', 20), bd=0, bg='#6b5b95', fg='white', width=15,
                        activebackground='#b0aac0', activeforeground='white', padx=25, borderwidth=3, command=depth_first_Search_wrapper)
    DFS_btn.place(x=20, y=70)

    Astar_btn = tk.Button(root, text='Solve with A*', font=('Bold', 20), bd=0, bg='#6b5b95', fg='white', width=15,
                          activebackground='#b0aac0', activeforeground='white', padx=25, borderwidth=3, command=astar_search_wrapper)    
    Astar_btn.place(x=20, y=130)

    Comparison = tk.Button(root, text='Comparison X3', font=('Bold', 20), bd=0, bg='#6b5b95', fg='white', width=15,
                           activebackground='#b0aac0', activeforeground='white', padx=25, borderwidth=3, command=compare_path)
    Comparison.place(x=20, y=190)

    global canvas
    canvas = tk.Canvas(root, width=cols * 50, height=rows * 50)
    canvas.pack()
    Visualize_maze_wrapper()

    root.mainloop()

################################################################################### Execute ###################################################################################
main()