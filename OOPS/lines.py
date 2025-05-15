class LINES:
    def __init__(self,x,y,c):
        self.x=x
        self.y=y
        self.c=c


    def type(self,other):
        r1=self.x/other.x
        r2=self.y/other.y
        r3=self.c/other.c

        if (r1==r2 and r2==r3):
            print(f'{self.x}X+{self.y}Y+{self.c}=0 ,{other.x}X+{other.y}Y+{other.c}=0 lines are Coinciding to each other')

        elif r1==r2 and r2!=r3:
            dist=abs((self.c-other.c)/((self.x**2+self.y**2)**0.5))
            print(f'{self.x}X+{self.y}Y+{self.c}=0 ,{other.x}X+{other.y}Y+{other.c}=0 lines are Parallel to each other with a distance of {dist}')

        else:
            x_intercept=(((self.y*other.c)-(other.y*self.c))/((other.y*self.x)-(other.x*self.y)))
            y_intercept=(((self.c*other.x)-(self.x*other.c))/((other.y*self.x)-(other.x*self.y)))
            print(f'{self.x}X+{self.y}Y+{self.c}=0 ,{other.x}X+{other.y}Y+{other.c}=0 lines are intersecting each other at ({x_intercept},{y_intercept})')

