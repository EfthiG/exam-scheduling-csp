import time
import csp
import pandas as pd
from utils import F 

#converts the data from the csv file into a dict {Course : [list of its row]}
def coursesDict(courses):

    courDict = {row['Μάθημα']: [row['Εξάμηνο'], row['Μάθημα'], row['Καθηγητής'], row['Δύσκολο (TRUE/FALSE)'], row['Εργαστήριο (TRUE/FALSE)']]  
                for _, row in courses.iterrows()}

    return courDict

#returns the teacher of the course cour
def courseProfessor(courses, cour):
    return courses[cour][2]

#returns if the course cour is hard
def course_ishard(courses, cour):
    return courses[cour][3]  

#returns the semester of the course cour
def courseSemester(courses, cour):
    return courses[cour][0]   

#returns if the course cour has lab
def course_hasLab(courses, cour):
    return courses[cour][4]


class Timetable(csp.CSP):
    
    def __init__(self, courses):
        # All the courses data in a dict of {Course : [list of its characteristics]}
        self.coursesData = coursesDict(courses)
        
        # The variables of the problem is a list of the courses names
        self.variables = [key for key in self.coursesData]

        # The domain is a dict of {var : [list of tuples (period, day)]}
        values = []
        for period in range(1,4):    
            for day in range(1,22):
                values.append((period, day))
        self.domains = {var: values for var in self.variables}

        # The neighbors of each variable are all the other variables since only one exam can take place at a time
        self.neighbors = dict()
        for var in self.variables:
            self.neighbors[var]=[neighbor for neighbor in self.variables if neighbor!=var]
        
        
        self.weight = {(var, neighbor): 1 for var in self.neighbors for neighbor in self.neighbors[var]}

        #variable to keep track of how many times constraints the function has been called
        self.constraintsChecks = 0  
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints)

    def constraints(self, A, a, B, b):

        self.constraintsChecks+=1
        data = self.coursesData
        #two exams can't be at the same time
        if (a==b):
            return False
        #two courses of the same semester can't be scheduled at the same day
        if (courseSemester(data, A) == courseSemester(data, B) and a[1] == b[1]) :
            return False
        #two HARD courses can;t be scheduled less than 2 days apart
        if (course_ishard(data, A) and course_ishard(data, B) and abs(a[1]-b[1]) < 2):
            return False        
        #two courses with the same teacher can't be scheduled at the same day
        if (courseProfessor(data, A) == courseProfessor(data, B) and a[1] == b[1] ):
            return False
        #two courses with labs can't fit in one day of 3 periods
        if (course_hasLab(data, A) and course_hasLab(data, B) and a[1] == b[1] ):
            return False
    
        if (course_hasLab(data, A)):
            #if A has lab it can't be scheduled for the last period (since lab exams are after)
            if (a[0]==3):
                return False
            #if A has lab, B can't be scheduled right after A's exams (A's lab's exams are supposed to be at that period)    
            if (a[1]==b[1] and b[0]==a[0]+1):
                return False

        #same for B
        if (course_hasLab(data, B)):
            if (b[1]==3):
                return False
            if (a[1]==b[1] and a[0]==b[0]+1):
                return False


        return True 
        
        

    def printAssignment(self, assignment):
        sortedAssignment = sorted(assignment.items(), key=lambda item: (item[1][1], item[1][0]))
        prevDay = 0
        for var, value in sortedAssignment:
            if value[1]!=prevDay:
                print('____________________________________________________________________________________________________________________________')
                print('ΗΜΕΡΑ', value[1])

            if self.coursesData[var][4]:             #if course has lab print the lab's exam in the next period
                print(var, '|Περίοδος', value[0])
                print(var, 'LAB', '|Περίοδος', value[0]+1)
            else:
                print(var, '|Περίοδος', value[0])

            prevDay = value[1]  



def dom_wdeg(assignment, csp):
    result = dict()

    for var in csp.variables:
        result[var] = 1
    
    for var in csp.variables:
        if var not in assignment:
            sum = 0
            for neighbor in csp.neighbors[var]:
                if (neighbor not in assignment):
                    sum += csp.weight[(var, neighbor)]
            result[var] = sum / len(csp.domains[var]) if len(csp.domains[var]) > 0 else float('inf')

    return min(result, key=result.get)



#_________________________________________main________________________________________________________________________________________________

if __name__ == '__main__':
    data = pd.read_csv('h3-data.csv')  

    #FC + MRV

    timetable = Timetable(data)
    start = time.time()
    result=csp.backtracking_search(timetable, csp.mrv, csp.lcv, csp.forward_checking)
    finish = time.time()
    print('FC with MRV')
    print('Elapsed time: ', finish-start)
    print('Constraints checks: ', timetable.constraintsChecks)
    print('Number of assignments: ', timetable.nassigns)
    print()


    #MAC + MRV

    timetable = Timetable(data)
    start = time.time()
    result = csp.backtracking_search(timetable, csp.mrv, csp.lcv, csp.mac)
    finish = time.time()
    print('MAC with MRV')
    print('Elapsed time: ', finish-start)
    print('Constraints checks: ', timetable.constraintsChecks)
    print('Number of assignments: ', timetable.nassigns)
    print()


    #FC + dom/wdeg

    timetable = Timetable(data)
    start = time.time()
    result=csp.backtracking_search(timetable, dom_wdeg, csp.lcv, csp.forward_checking)
    finish = time.time()
    print('FC with dom/wdeg')
    print('Elapsed time: ', finish-start)
    print('Constraints checks: ', timetable.constraintsChecks)
    print('Number of assignments: ', timetable.nassigns)
    print()

    #MAC + dom/wdeg

    timetable = Timetable(data)
    start = time.time()
    result= csp.backtracking_search(timetable, dom_wdeg, csp.lcv, csp.mac)
    finish = time.time()
    print('MAC with dom/wdeg')
    print('Elapsed time: ', finish-start)
    print('Constraints checks: ', timetable.constraintsChecks)
    print('Number of assignments: ', timetable.nassigns)
    print()

    #MINCONFLICTS

    timetable = Timetable(data)
    start = time.time()
    result=csp.min_conflicts(timetable)
    finish = time.time()
    print(' MinConflicts')
    print('Elapsed time: ', finish-start)
    print('Constraints checks: ', timetable.constraintsChecks)
    print('Number of assignments: ', timetable.nassigns)
    print()


    timetable.printAssignment(result)

