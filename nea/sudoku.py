import copy
import random
import time
dim = 3 #the dimensions of a single 'square'
full = ['x'*10]*9 #the value of a full square/row/column

class poss_vals:
    def __init__(self):
        #initial possible values for each cell
        self.rows = [['123456789' for i in range(dim**2)]for j in range(dim**2)]
        self.cols = [['123456789' for i in range(dim**2)]for j in range(dim**2)]
        self.squares = [[['123456789' for i in range(dim**2)]for j in range(dim)]for j in range(dim)]
    
    def update(self):
        #used to update values in other cells to reflect a change to the rows
        self.update_cols()
        self.update_squares()

    def update_cols(self):
        #updates rows to columns
        for row in range(dim**2):
            for i in range(dim**2):
                self.cols[i][row] = self.rows[row][i]

    def update_squares(self):
        #updates rows to squares
        for i in range(dim**2):
            for j in range(dim**2):
                row_index = i//dim
                col_index = j//dim
                k = dim*(i%dim)+(j%dim)
                self.squares[row_index][col_index][k] = self.rows[i][j]

    def rev_update_squares(self):
        #updates squares to rows
        for i in range(dim**2):
            for j in range(dim**2):
                row_index = i//dim
                col_index = j//dim
                k = dim*(i%dim)+(j%dim)
                self.rows[i][j] = self.squares[row_index][col_index][k]
        self.update_cols()

class notes(): #class for notes
    def __init__(self):
        self.rows = [[[' ' for i in range(dim**2)]for j in range(dim**2)]for k in range(dim**3)]
    def add_val(self,row,col,v,index):
        self.rows[row][col][index] = v

class grid(poss_vals):
    def __init__(self):
        #initial values in actual solution grid
        self.rows = [[' ' for i in range(dim**2)]for j in range(dim**2)]
        self.cols = [[' ' for i in range(dim**2)]for j in range(dim**2)]
        self.squares = [[[' ' for i in range(dim**2)]for j in range(dim)]for j in range(dim)]
        self.poss = poss_vals() #possible values for generation of grid

    def _generate_grid(self):
        #generates solution
        for s in range(dim):
            self.fill_square(s,s)
        self.fill_square(0,2)
        self.fill_square(2,0)
        self.fill_square(0,1)
        self.fill_square(1,0)
            
    def fill_square(self,sr,sc):
        #used to fill a specified square
        while self.poss.squares[sr][sc] != full:
            cell = self.poss.squares[sr][sc].index(min(self.poss.squares[sr][sc],key=len))
            row =(cell//dim)+dim*sr
            col =(cell%dim)+dim*sc
            val = random.choice(self.poss.squares[sr][sc][cell])
            self.add_val(row,col,val)
            comp = copy.deepcopy(self.poss.rows)
            self.solve()
            while self.poss.rows != comp:
                comp = copy.deepcopy(self.poss.rows)
                self.solve()

    def solve(self):
        #used to solve obvious values in grid
        self.solve_part(self.rows,self.poss.rows)
        self.solve_part(self.cols,self.poss.cols)
        self.solve_squares()                

    def solve_part(self,part,poss_part):
        #used to solve values in rows or columns
        for i in range(dim**2):
            for j in range(dim**2):
                if part == self.rows:
                    row = i
                    col = j
                else:
                    row = j
                    col = i
                val = poss_part[i][j]
                if len(val) == 1:
                    self.add_val(row,col,val)
                if len(val) > 1 and val != 'x'*10:
                    for n in val:
                        ctr = 0
                        for b in poss_part[i]:
                            if n in b:
                                ctr += 1
                        if ctr == 1:
                            self.add_val(row,col,n)
                            break

    def solve_squares(self):
        #used to solve values in squares
        for sr in range(dim): #square row
            for sc in range(dim): #square column
                for cell in range(dim**2):
                    
                    row =(cell//dim)+dim*sr
                    col =(cell%dim)+dim*sc
                    val = self.poss.rows[row][col]
                    #print(val)
                    if len(val) == 1:
                        self.add_val(row,col,val)
                    if len(val) > 1 and val != 'x'*10:
                        for n in val:
                            ctr = 0
                            for b in self.squares[sr][sc]:
                                if n in b:
                                    ctr += 1
                            if ctr == 1:
                                self.add_val(row,col,n)
                                break

    def add_val(self,row,col,v):
        #adds a value to the actual grid
        self.rows[row][col] = v
        self.update()
        #and then changes the possible values of the grid to reflect this
        self.change_poss(row,col,v) 

    def change_poss(self,row,col,v):
        #updates the possible values of cells
        self.poss.rows[row][col] = 'x' * 10
        square_row = row // dim
        square_col = col // dim
        for i in range(dim**2):
            self.poss.rows[row][i] = self.poss.rows[row][i].replace(v,'')
            self.poss.rows[i][col] = self.poss.rows[i][col].replace(v,'')
            self.poss.update()
            self.poss.squares[square_row][square_col][i] = self.poss.squares[square_row][square_col][i].replace(v,'')
            self.poss.rev_update_squares()

    
                            
    def __str__(self):
        sudoku_grid = ''
        for row in self.rows: 
            for num in row: 
                sudoku_grid += str(num) + ' '
            sudoku_grid += '\n'
        return sudoku_grid

class solvable(grid):
    def __init__(self,orig):
        o = copy.deepcopy(orig)
        self.orig = orig
        self.rows = o.rows
        self.cols = o.cols
        self.squares = o.squares
        self.poss = poss_vals()
        self.blank()

    def generate_grid(self):
        for row in range(dim**2):
            for col in range(dim**2):
                val = self.rows[row][col]
                if val != ' ':
                    self.change_poss(row,col,val)

    def blank(self):
        for row in range(dim**2):
            for col in range(dim**2):
                if random.randint(1,20) < difficulty:
                    self.rows[row][col] = " "    
        self.generate_grid()
        return self
 
    def check(self):
        comp = copy.deepcopy(self.poss.rows)
        self.solve()
        while self.poss.rows != comp:
            comp = copy.deepcopy(self.poss.rows)
            self.solve()
        if self.rows == self.orig.rows:
            return True
        return False


def create_grid():
    while True:
        try:
            poss = grid()
            poss._generate_grid()
            print('attempt:')
            print(poss)
            assert poss.poss.rows == [full]*9
            break
        except:
            continue
    blanked = solvable(poss)
    bcopy = copy.deepcopy(blanked)
    print('final:')
    print(poss)
    return poss,blanked,bcopy





notes = notes()
    

