from __future__ import division
from numpy import * 
import numpy as np
import matplotlib.animation as animation
import math
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class OutStep():
    #seconds of examination
    endxpoint = 5
    #number of points per second * sdeconds
    numxpoint = 1000*endxpoint


    def __init__(self):
        print("""
              __|Zs|_*___|Zl|____|Zr|_
             |                        |  
            |Es|                     |Er|
            _|_                      _|_

             * (Evaluation point)
        """)
        print("""Es and Er will be saved  using the RMS value and frecuency of these signals.
Please insert RMS value of Es(source voltage):""")
        self.Es_module = input()
        print("Please insert frecuency(w) value of Es(source voltage):")
        self.Es_fre = input()
        print("Please insert RMS value of Er(load side voltage):")
        self.Er_module = input()
        print("Please insert frecuency(w) value of Er(load side voltage):")
        self.Er_fre = input()
        print("""Nice! Lets get the impedance value for the source, line and load side. 
Remember to introduce this value in the following format --> R + Xj
Otherwise, the program will not identify it as a number.
Please insert impedance value for Zs (source side impedance):""")
        self.Zs = input()
        print("Please insert impedance value for Zl (source side impedance):")
        self.Zl = input()
        print("Please insert impedance value for Zr (load side impedance):")
        self.Zr = input()
        print("We have all the information we need to study your out of step power swing and to show it to you!")
        self.calculations()

    def yang(self,num):
        if ((num // 180 ) % 2) == 1:
            return (-180 + (num % 180))
        else:
            return num % 180

    def calculations(self):
        # Get x points values
        self.x_points = np.linspace(0, self.endxpoint, self.numxpoint)

        # Calculations for Es
        self.Es_angle = []
        for i in range(len(self.x_points)):
            self.Es_angle.append(2 * math.pi * self.Es_fre *self.x_points[i])
        self.Es = self.Es_module * np.sqrt(2) * np.sin(self.Es_angle)

        # Calculations for Er
        self.Er_angle = []
        for i in range(len(self.x_points)):
            self.Er_angle.append(2 * math.pi * self.Er_fre *self.x_points[i])
        self.Er = self.Er_module * np.sqrt(2) * np.sin(self.Er_angle)

        #diffference of signals
        self.Er_Es_angle = []
        self.Er_Es = []
        for i in range(len(self.x_points)):
            self.Er_Es_angle.append(self.Er_angle[i] - self.Es_angle[i])
            self.Er_Es.append(self.Er[i] - self.Es[i])

        #Calculate impedance during power sqing, for more importance about this step check out of step theory
        self.k = self.Er_module / self.Es_module
        comp1 = np.sin(self.Er_Es_angle)
        comp2 = np.zeros(len(comp1),dtype=complex)
        comp2.imag = comp1
        comp3 = self.k*(comp2 + np.cos(self.Er_Es_angle))
        comp4 = self.k*(np.cos(self.Er_Es_angle)+comp2)-1
        volt_rat = comp3 / comp4 
        self.result_volt =  volt_rat * (self.Zs + self.Zr+ self.Zl) - self.Zs

        self.menu()

    def menu(self):
        choice = 0
        print(""" Choose your option:
1) See both Es and Er
2) See Er - Es signal
3) See the impedance R-X graph
4) Watch the complete animation for the impedance reading at evaluation point
Your option:""")
        choice = input()

        if choice == 1 :
            self.signal()
            #See both es and er
        elif choice == 2:
            self.diff()
            #del self
            # see impedance map
        #elif choice == 3:
        #    self.diffang()
            #Animation
        elif choice == 3:
            self.imp()
            #Animation
        elif choice == 4:
            self.animationps()
            #Animation
        else:
            print("Try again...")
            self.menu()

    def signal(self):
        plt.style.use('seaborn-pastel')
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 5), ylim=(min([min(self.Es),min(self.Er)])*1.1, max([max(self.Es),max(self.Er)])*1.1))
        line, = ax.plot([], [], lw=3)
        #Es draw
        lbl = str(self.Es_fre) + "Hz"
        plt.plot(self.x_points,self.Es,label=lbl)
        #Er draw
        lbl2 = str(self.Er_fre) + "Hz"
        plt.plot(self.x_points,self.Er,label=lbl2)

        plt.title('Er and Es voltage signals. \n Press ''q'' to close and return to menu ', fontsize=16)
        plt.xlabel('Time(s)')
        plt.ylabel('Voltage(V)')
        plt.legend()
        plt.show()
        self.menu()

    def diff(self):
        plt.style.use('seaborn-pastel')
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 5), ylim=(min(self.Er_Es)*1.1, max(self.Er_Es)*1.1))
        line, = ax.plot([], [], lw=3)
        #Er-Es draw
        lbl3 = "Er - Es"
        plt.plot(self.x_points,self.Er_Es,label=lbl3)

        plt.title('Er - Es voltage signals. \n Press ''q'' to close and return to menu ', fontsize=16)
        plt.xlabel('Time(s)')
        plt.ylabel('Voltage(V)')        
        plt.legend()
        plt.show()
        self.menu()

    def diffang(self):
        plt.style.use('seaborn-pastel')
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 5), ylim=(0, 400))
        line, = ax.plot([], [], lw=3)
        #Er-Es draw
        Er_Es_angle_temp = []
        for i in range(len(self.x_points)):
            Er_Es_angle_temp.append(self.Er_Es_angle[i]%360)
        lbl3 = "ang(Er - Es)"
        plt.plot(self.x_points,Er_Es_angle_temp ,label=lbl3)

        plt.title('Er - Es voltage signals. \n Press ''q'' to close and return to menu ', fontsize=16)
        plt.xlabel('Time(s)')
        plt.ylabel('Voltage(V)')  
        plt.legend()
        plt.show()
        self.menu()

    def fromComplextoModang(self,num):
        return (abs(num),rad2deg(angle(num)))
    
    def fromModangtoComplex(self,mod,ang):
        return  mod * exp(1j*deg2rad(ang))

    def plotfromphasor(self,phasor,origin_x,origin_y,color_name,label_name,ax):
        a,ang_use = self.fromComplextoModang(phasor)
        # find the end point
        endy = a * math.sin(math.radians(ang_use)) + origin_y
        endx = a * math.cos(math.radians(ang_use)) + origin_x
        # plot the points
        plt.annotate(s='', xy=(endx,endy), xytext=(origin_x,origin_y), arrowprops=dict(color=color_name,arrowstyle='->', shrinkA=0, shrinkB=0))
        ax.plot([origin_x, endx], [origin_y, endy], color=color_name, label = label_name)
        plt.plot()
        return (endx,endy)

    def plotfromphasorInv(self,phasor,origin_x,origin_y,color_name,label_name,ax):
        a,ang_use = self.fromComplextoModang(phasor)
        # find the end point
        endy = -a * math.sin(math.radians(ang_use)) + origin_y
        endx = -a * math.cos(math.radians(ang_use)) + origin_x
        # plot the points
        plt.annotate(s='', xy=(endx,endy), xytext=(origin_x,origin_y), arrowprops=dict(color=color_name,arrowstyle='<-', shrinkA=0, shrinkB=0))
        ax.plot([origin_x, endx], [origin_y, endy], color=color_name, label = label_name)
        plt.plot()
        return (endx,endy)

    def getEnd(self,phasor,origin_x,origin_y):
        a,ang_use = self.fromComplextoModang(phasor)
        # find the end point
        endy = a * math.sin(math.radians(ang_use)) + origin_y
        endx = a * math.cos(math.radians(ang_use)) + origin_x
        # plot the points
        return (endx,endy)

    def getEndInv(self,phasor,origin_x,origin_y):
        a,ang_use = self.fromComplextoModang(phasor)
        # find the end point
        endy = -a * math.sin(math.radians(ang_use)) + origin_y
        endx = -a * math.cos(math.radians(ang_use)) + origin_x
        # plot the points
        return (endx,endy)

    def imp(self):
        plt.style.use('seaborn-pastel')
        fig = plt.figure()
        #Get limits for graph
        endxZl, endyZl = self.getEnd(self.Zl,0,0)
        endxZr, endyZr = self.getEnd(self.Zr,endxZl,endyZl)
        endxZs, endyZs = self.getEndInv(self.Zs,0,0)
        
        ax = plt.axes(xlim=(min([endxZl,endxZr,endxZs,0])*1.1, max([endxZl,endxZr,endxZs])*1.1), ylim=(min([endyZl,endyZr,endyZs,0])*1.1, max([endyZl,endyZr,endyZs])*1.1))
        line, = ax.plot([], [], lw=3)
        #here strts new code
        zlend_x,zlend_y = self.plotfromphasor(self.Zl,0,0,'green','Zl',ax)
        zrend_x,zrend_y = self.plotfromphasor(self.Zr,zlend_x,zlend_y,'blue','Zr',ax)
        zsend_x,zsend_y = self.plotfromphasorInv(self.Zs,0,0,'red','Zs',ax)
        #       
        plt.title('Impedance R-X graph. \n Press ''q'' to close and return to menu ', fontsize=16)
        plt.xlabel('R(ohm)')
        plt.ylabel('X(ohm)')  
        plt.legend()
        plt.show()
        self.menu()

    def animationps(self):
        plt.style.use('seaborn-pastel')
        fig = plt.figure()

        #Get limits for graph
        self.endx=[]
        self.endy=[]
        for i in xrange(0,len(self.result_volt)-1):
            a,ang_use = self.fromComplextoModang(self.result_volt[i])
            # find the end point
            self.endy.append(a * math.sin(math.radians(ang_use)))
            self.endx.append(a * math.cos(math.radians(ang_use)))

        ax = plt.axes(xlim=(self.setmin(self.endx)*1.1, self.setmax(self.endx)*1.1), ylim=(self.setmin(self.endy)*1.1, self.setmax(self.endy)*1.1))

        zlend_x,zlend_y = self.plotfromphasor(self.Zl,0,0,'green','Zl',ax)
        zrend_x,zrend_y = self.plotfromphasor(self.Zr,zlend_x,zlend_y,'blue','Zr',ax)
        zsend_x,zsend_y = self.plotfromphasorInv(self.Zs,0,0,'red','Zs',ax)

        self.x, self.y = 0 , 0
        self.line, = ax.plot([self.x, 0], [self.y, 0],label = 'Z at gen terminal')
        realinterval = (self.endxpoint/self.numxpoint)* 1000 # in miliseconds
        intervalx100 = realinterval 
        ani = animation.FuncAnimation(fig, self.update, frames=len(self.endx)-1, interval=intervalx100,repeat = False) #interval is set in miliseconds 
        
        plt.title('Out of Step Power Swing animation \n Press ''q'' to close and return to menu ', fontsize=16)
        plt.xlabel('R(ohm)')
        plt.ylabel('X(ohm)')          
        plt.legend()
        plt.show()
        self.menu()

    def setmin(self,num):
        if min(num[1:(len(num)-1)]) < -500  :
            return -500
        else :
            return min(num)

    def setmax(self,num):
        if max(num[1:(len(num)-1)]) > 500 :
            return 500
        else :
            return max(num)

    def update(self,i):
        new_data = [self.endx[i],self.endy[i]]
        self.line.set_data([self.x,new_data[0]],[self.y,new_data[1]])
        return self.line,      

if __name__=='__main__':
    OutStep()


