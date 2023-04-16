import random
import math
from bokeh.plotting import figure, show
 
time_history = []
temp_history = []
setpoint_history = []
cooling_history = []
zaburzenia_history = []
pid_history = [] 
voltage_history = []
 
temp_surr = 20
k_c = 0.25  # stal stygniecia

#INPUT DO UKLADU
start_temp = 20
setpoint_temp = 100

kp = 0.01
kd = 0.1
ki = 0.1

uMax = 10
uMin = 0
pMax = 40
pMin = 0

mode = 0
 
SIMULATION_TIME = 400
 
 # cooling simulation
def newtons_cooling(T0, Tambient, k, t):
    return -(T0 + (Tambient - T0) * math.e ** (-k * t))
 

# heater device 

class HeatingDevice:
    def __init__(self,uMax,uMin,pMax,pMin):
        self.uMax = uMax
        self.uMin = uMin
        self.pMax = pMax
        self.pMin = pMin
        self.voltage = 0

    def heat_output(self,voltage):
        return (((self.pMax - self.pMin)/(self.uMax - self.uMin))*voltage - self.uMin )+ pMin

    
# PID controller class
 
 
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0
        self.integral = 0
 
    def update(self, current_value, setpoint):
        error = setpoint - current_value
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error
        return self.Kp*error + self.Ki*self.integral + self.Kd*derivative
 
# Industrial furnace simulation
 
 
class Furnace:
    def __init__(self, initial_temp, setpoint ,Kp_ ,Kd_, Ki_,uMax_,uMin_,pMax_,pMin_,mode_):
        self.temp = initial_temp
        self.setpoint = setpoint
        self.pid = PID(Kp_ ,Kd_, Ki_)
        self.heater = HeatingDevice(uMax_,uMin_,pMax_,pMin_)
        self.timestamp = 0
        self.mode = mode_

 
    def update_temp(self, extra_heat, mode):
        # Simulating the industrial furnace process
        cooling = newtons_cooling(self.temp, temp_surr, k_c, 1)
    
        
        random_wzburzenie = 0
            
        if mode == 1:
            if random.randint(0, 100) < 10 and self.timestamp < 200:
                random_wzburzenie = random.randint(0, 20) - 10
            
        if mode == 2:
            if self.timestamp == 100 or self.timestamp == 200 or self.timestamp == 300:
                random_wzburzenie = -30
            
 
        self.temp += extra_heat + cooling + random_wzburzenie
        zaburzenia_history.append(random_wzburzenie)
        cooling_history.append(cooling)
 
    def run(self):
        while self.timestamp < SIMULATION_TIME:
            # Getting the temperature reading
            current_temp = self.temp
            # Calculating the control input using PID controller
            control_input = self.pid.update(current_temp, self.setpoint)
            self.heater.voltage = min(max(control_input,self.heater.uMin),self.heater.uMax)
            pid_history.append(self.heater.voltage)
 
 
            # Use a mathematical model to calculate the change in temperature
            temp_change = self.heater.heat_output(self.heater.voltage)
            temp_change = min(max(temp_change,self.heater.pMin),self.heater.pMax)
            # Updating the temperature
            self.update_temp(temp_change, self.mode)
            print(temp_change,self.temp)
            # incrementing the timestamp
            self.timestamp += 1
            # Printing the current temperature, control input and timestamp
            print("Time: {:.2f}, Temperature: {:.2f}, Control input: {:.2f}".format(
                self.timestamp, current_temp, control_input))
 
            time_history.append(self.timestamp)
            temp_history.append(self.temp)
            setpoint_history.append(self.setpoint)
 
 
 
def draw_plot(x, label,  *funk):
    colors = ['red', 'orange', 'green', 'blue',
              'indigo', 'violet', 'pink', 'purple', 'brown']
    czasy = ['temp', 'setpoint', 'cooling', 'zaburzenia','pid']
    plot = figure()
    i = 0
    for f in funk:
        plot.line(x, f, color=colors[i], legend_label=f"{label}:{czasy[i]}")
        i += 1
    plot.legend.title = f"{label}"
 
    show(plot)
 

def main():
    # Initializing the furnace
    furnace = Furnace(initial_temp=start_temp, setpoint=setpoint_temp,Kp_=kp,Kd_=kd,Ki_=ki,uMax_=uMax,uMin_=uMin,pMax_=pMax,pMin_=pMin,mode_=mode)
    # Running the furnace
    furnace.run()
    draw_plot(time_history, 'plot', temp_history,
            setpoint_history, cooling_history, zaburzenia_history,pid_history)
    
main()
# draw_plot(time_history, 'pid', pid_history)
 
# print(cooling_history)