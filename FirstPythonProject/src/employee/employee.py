class Employee:
    raisePct = 1.05
    
    def __init__(self, fName, lName, pay):
        self.fName = fName
        self.lName = lName
        self.pay = pay
        self.email = fName + "." + lName + "@company.com"
        
    def fullName(self):
        return self.fName + " " + self.lName
    
    def apply_raise(self):
        return (int)(self.pay * Employee.raisePct)
    
    def apply_raise_me(self):
        return (int)(self.pay * self.raisePct)
     
        
emp_1 = Employee("ADFE", "JUH", 100)
print(emp_1.fullName())
print(emp_1.apply_raise())    
emp_1.raisePct = 1.08    
print(emp_1.apply_raise_me()) 

emp_2 = Employee("ABC", "ZZZ", 100)
print(emp_2.fullName())
print(emp_2.apply_raise())    
print(emp_2.apply_raise_me()) 
print(emp_1.__dict__)