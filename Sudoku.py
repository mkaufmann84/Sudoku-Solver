# -*- coding: utf-8 -*-
#https://www.websudoku.com/
#WORKING SUDOKU SOLVER FOR LINK ABOVE
import time 
import copy
import undetected_chromedriver as uc
#Using this instead of selenium, because it is sneakier. Although I havent tried, 
#Selenium could probably be used instead of this 
import random



uc.TARGET_VERSION = 89 #what version is your chrome/ chrome driver

driver = uc.Chrome(executable_path='C:\chromedriver_win32\chromedriver.exe')
# driver.minimize_window() #minimizes the window when launches
#executable path is where the chrome driver is located. 

class ws:
    sq = [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], [(3, 0), (3, 1), (3, 2), (4, 0), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)], [(6, 0), (6, 1), (6, 2), (7, 0), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)], [(0, 3), (0, 4), (0, 5), (1, 3), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], [(3, 6), (3, 7), (3, 8), (4, 6), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)], [(3, 3), (3, 4), (3, 5), (4, 3), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)], [(0, 6), (0, 7), (0, 8), (1, 6), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)], [(6, 3), (6, 4), (6, 5), (7, 3), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)], [(6, 6), (6, 7), (6, 8), (7, 6), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]]
    def __init__(self,diff = None, PuzzleNum = None,user = None,password = None):
        self.user = user
        self.password = password
        if diff not in [None,1,2,3,4]:
            raise Exception('The Number for difficulty is not valid: easy -1, med -2, hard - 3, evil-4 ')
        self.diff = diff
        if PuzzleNum ==None:
            pass
        else:
            if type(PuzzleNum)!=int or PuzzleNum<=0:
                raise Exception(f'Puzzle Num: {PuzzleNum}, is not an acceptable number. Must be a positive integer, and may have a max limit.')
        self.PuzzleNum = PuzzleNum
        self.ftime = True
    def login(self):
        #logs into account
        global driver

        driver.get(f'https://www.websudoku.com/?level={self.diff}&set_id={self.PuzzleNum}')
        frame = driver.find_element_by_xpath('/html/frameset/frame')
        driver.switch_to.frame(frame)
        time.sleep(3)
        #login
        driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/a[2]').click()
        time.sleep(0.5)
        frame = driver.find_element_by_xpath('/html/frameset/frame')
        driver.switch_to.frame(frame)
        driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input').send_keys(self.user)
        time.sleep(0.5)
        driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr/td/form/table/tbody/tr[4]/td[2]/input').send_keys(self.password)
        time.sleep(0.25)
        driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr/td/form/table/tbody/tr[6]/td/input').click()
        time.sleep(3)
        driver.get(f'https://www.websudoku.com/?level={self.diff}&set_id={self.PuzzleNum}')
        time.sleep(3)
        print('Logged in...')
        #now logged in, returns to sudoku page
        
    def get_cv(self):
        if self.ftime:
            driver.get(f'https://www.websudoku.com/?level={self.diff}&set_id={self.PuzzleNum}')
            time.sleep(3)
            self.ftime = False #this is so after first puzzle, it will randomly solve puzzles

        driver.switch_to.default_content()
        frame = driver.find_element_by_xpath('/html/frameset/frame')
        driver.switch_to.frame(frame)
      
              
        time.sleep(1)
        #will proceed to convert puzzle into list

        rows = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/div[2]/table/tbody')
        driver.find_elements_by_tag_name('iframe')
        self.cv = dict()
        for i in range(9):
            for t in range(9):
                self.cv[(i,t)] = None
        for i in range(9):
            for ii in range(9):
                cell = rows.find_element_by_xpath(f'/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/div[2]/table/tbody/tr[{i+1}]/td[{ii+1}]/input')
                value =  cell.get_attribute('value')
                if value =='':
                    self.cv[(i,ii)] = '0'
                else:
                    self.cv[(i,ii)] = value
        self.initial_cv = copy.deepcopy(self.cv)
        print('CV acquired: solving...')
    

    def init_solve(self,cv):
        #initializes solving
        initial_cd = self.domains(cv)
        initial_grid = self.creategrid(cv)
        print('Initial:')
        print(*initial_grid,sep='\n')
        

        self.result = self.solve(cv,initial_cd,initial_grid)
        print('Result:')
        print(*self.result,sep='\n')
              
        
    def creategrid(self,cv): 
        #creates grid based off cv
        grid = []
        for v in range(9):
            tmp = []
            for h in range(9):
                tmp.append(cv[(v,h)])
            grid.append(tmp)
        return grid

                
    def domains(self,cv): 
        #initalizes self.cd
        cd = dict()
        base = {'1','2','3','4','5','6','7','8','9'}
        for i in cv:
            if cv[i]=='0':
                cd[i] = base.copy()
            else:
                cd[i] = set() #there is already a known valuye
        return cd
       
    def solve(self,cv,cd,grid): #v,h
        #this functions uses basic inferences made from the board to speed up the solver. 
        cv = copy.deepcopy(cv)
        cd = copy.deepcopy(cd)
    
        checkcv = copy.copy(cv)
        checkcd = copy.copy(cd)
        checkgrid = copy.copy(grid)
        did_work = self.is_puzzle_solved(grid)
        if did_work==None: #there is a cell with a value that has yet to be solved.
            for i in cv:
                if cv[i] =='0':
                    row = grid[i[0]]
                    
                    for value in row:
                        if len(cd[i]) ==1:
                            p = cd[i].pop()
                            cv[i] = p
                            return self.solve(cv,cd,grid)
                        cd[i].discard(value) 
                    col = [grid[num][i[1]] for num in range(9)]
                    for value in col:
                        if len(cd[i]) ==1:
                            p = cd[i].pop()
                            cv[i] = p
                            return self.solve(cv,cd,grid)
                        cd[i].discard(value)
                    
                    box = [var for var in ws.sq if i in var]
                    boxvalues = [cv[va] for va in box[0]]
                    for value in boxvalues:
                        if len(cd[i]) ==1:
                            p = cd[i].pop()
                            cv[i] = p
                            return self.solve(cv,cd,grid)
                        cd[i].discard(value)

            if checkcv ==cv and checkcd ==cd and checkgrid == grid:
                return self.backtrack(cv,cd,grid) #stuck, need some help
            return self.solve(cv,cd,grid)  #domain values were changed
        elif did_work ==False: #puzzle is filled, but is not a real solution
            return False #backtrack did not work for this solution
        elif did_work==True:#puzzle is a valid solution
            return grid

        
        
    def backtrack(self,cv,cd,grid):
        #backtracking search algorithim. This is used when basic inferences(solve) can not find solution
        cv = copy.deepcopy(cv)
        cd = copy.deepcopy(cd)
        solved = self.unsolveable(cv,cd,self.creategrid(cv))
        if solved == True:
            return self.creategrid(cv)
        elif solved == False:
            return False

        var = self.select_unassigned_variable(cv,cd) #looks at variables that have already been assigned in assingment.:
        for value in cd[var]:
            cvcopy = copy.deepcopy(cv)
            cvcopy[var] = value
            result = self.is_puzzle_solved(self.creategrid(cvcopy))
            if result ==True:
                return self.creategrid(cvcopy)
            elif result ==False:
                cvcopy[var] = cv[var]
            else: #keep going, there is empty (result = none)
                result = self.solve(cvcopy,cd,self.creategrid(cvcopy))
                if result ==False:#grid no work, and flled
                    cvcopy[var] = cv[var]

                else:
                    return result
        return False

    def unsolveable(self,cv,cd,grid):
        #sees if puzzle is completed, and if it can be completed
        p = self.is_puzzle_solved(grid)
        if p== True:
            #puzzle is solved and filled
            return True
        elif p==False:
            #puzz filed but does not follow rules.
            return False
        elif p == None: #puzzle is not filled out
            #checks for:
            #Makes sure ther is still at least one cd for each coord with value 0
            for coordnite in cv:
                if cv[coordnite]=='0':
                    if len(cd[coordnite])==0:
                        return False #this is because a square could have no possible solution, so it is bad puzzle
            return None #as in no problem yet

            
    def is_puzzle_solved(self,board):
        #sees if puzzle is completed
        #checks if filled in
        for i in board: #i is row
            for ii in i: #ii is char
                if ii =='0':
                    return None
        # checks rows
        numset = {'1','2','3','4','5','6','7','8','9'}
        for row in board:
            if set(row) != numset:
                return False
        #checks col
        for col in range(9):
            tmp = []
            for row in range(9):
                tmp.append(board[row][col])

            if set(tmp) != numset:
                return False
        # checks box
        for box in ws.sq:
            tmp = []
            for i in box: #i is a coordnite
                tmp.append(board[i[0]][i[1]])
            if set(tmp) != numset:
                return False
            
        return True
    
    def select_unassigned_variable(self, cv,cd):
        #optimization for speed
        zeros = []
        for i in cv:
            if cv[i]=='0':
                zeros.append(i) #i is a coordnite, where the vlaue is 0
        smallest_domain = {i:100 for i in zeros}#10 cause thats a max value
        for i in smallest_domain:
            smallest_domain[i] = len(cd[i])
            
            
        v=list(smallest_domain.values())
        k=list(smallest_domain.keys())
        return k[v.index(min(v))]   
        
    def send_values(self):
        #sends values into puzzle when completed
        
        ###self.result = grid, self.cv = (tuple(row,column):value)
        # for row in range(9): This method will send the the values left to right, starting from upper left
        #     for column in range(9):
        #         time.sleep(0.01)
        #         xpath = f'/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/div[2]/table/tbody/tr[{row+1}]/td[{column+1}]/input'
        #         driver.find_element_by_xpath(xpath).send_keys(self.result[row][column])
        #this method randomly picks coordnites to enter, which makes it look cooler
        total=[]
        for row in range(9): 
            for column in range(9):
                total.append((row,column))
        
        for block in self.initial_cv:
            if self.initial_cv[block]!='0':
                total.remove(block)
        rand_list = random.sample(range(0, len(total)),len(total))
        for i in rand_list:
            tup = total[i]
            # time.sleep(0.005)
            xpath = f'/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/div[2]/table/tbody/tr[{tup[0]+1}]/td[{tup[1]+1}]/input'
            driver.find_element_by_xpath(xpath).send_keys(self.result[tup[0]][tup[1]])
            
        time.sleep(0.1)
        driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[4]/input[1]').click()


#password = 'yourpassword'
#user = 'youremail'

#first input is difficult, next is the puzzle number
#ws = ws(4,42069,user,password) #easy -1, med -2, hard - 3, evil-4, puzzle number
ws = ws(4,42069)
#ws.login() #Optional, only call if password and user are filled out. 
ws.get_cv() #this goes to a link and gets the cv dictonary
ws.init_solve(ws.cv) #if u have your own sudoku puzzle, you can solve by making the coordnites(A dictonary), where (row, column): str(value). Unknowns are marked by '0'
ws.send_values()#this will send the values of a completed puzzle into the web browser and submit


    
def ksolve(): #if you have an ide with interactive testing, if u call ksolve() it will solve and input the puzzle the
#driver is currently on. 
    ws.get_cv()
    ws.init_solve(ws.cv)
    ws.send_values()
    
#loop to make the puzzle keep solving random puzzle indefiantly
while True: 
    time.sleep(5)
    print('\n')
    print('New Puzzle time')
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[3]/input').click()
    time.sleep(5)
    ksolve()
    
