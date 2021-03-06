#!/usr/bin/python

import Easydriver as ed
import threading
import time
import Queue
import test

MM_PER_STEP = 0.036
MM_COUNTER = 0

cw = True
ccw = False

print "AQUI: ", test.test_list

#test_list = [(10,True),(50,False)] #,(100,True),(200,False),(350,True),(500,False)]
"""
Arguments to pass or set up after creating the instance.
Step GPIO pin number.
Delay between step pulses in seconds.
Direction GPIO pin number.
Microstep 1 GPIO pin number.
Microstep 2 GPIO pin number.
Microstep 3 GPIO pin number.
Sleep GPIO pin number.
Enable GPIO pin number.
Reset GPIO pin number.
Name as a string.
"""

# Create an instance of the easydriver class.
# Not using sleep, enable or reset in this example.

# stepper_spool = ed.easydriver(18, 0.004, 23, 24, 17)
# stepper_pen = ed.easydriver(27, 0.001, 22, 26, 19)

# Set motor direction to clockwise.

class Z_Motor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor = ed.easydriver(27, 0.0001, 22, 26, 19)
        self.motor.set_eighth_step()
        self.mm_per_step_z = 0.003636

    def initial_sequence(self):
        self.move_down(6)
        time.sleep(1)
        self.move_up(6)
        time.sleep(1)

    def move_down(self,mm):
        #print "moving down: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_z)
        self.motor.set_direction(cw)
        for i in range(0,self.steps_to_move):
            self.motor.step()
    def move_up(self,mm):
        #print "moving up: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_z)
        self.motor.set_direction(ccw)
        for i in range(0,self.steps_to_move):
            self.motor.step()
    def receive(self, value):
        if value:
            self.move_down(6)
        else:
            self.move_up(6)

    def run(self):
        print "starting pen..."
        self.initial_sequence()


class Spool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor = ed.easydriver(18, 0.00005, 23, 24, 17)
        self.motor.set_eighth_step()
        self.mm_per_step_spool = 0.035

    def initial_sequence(self):
        self.move_forward(5)
        MM_COUNTER = 0
        time.sleep(1)

    def move_forward(self,mm):
        print "moving forward: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_spool)
        self.motor.set_direction(cw)
        for i in range(0,self.steps_to_move):
            self.motor.step()
    def move_back(self,mm):
        #print "moving up: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_spool)
        self.motor.set_direction(ccw)
        for i in range(0,self.steps_to_move):
            self.motor.step()

    def run(self):
        print "starting spool..."
        self.initial_sequence()
        print "[Spool] Starting in:"
        print "[Spool] 3"
        print "[Spool] 2"
        print "[Spool] 1"


class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.spool = Spool()
        self.z_motor = Z_Motor()

    def initial_sequence(self):
        print "Running initial sequence..."
        for i in range(0,3):
            self.z_motor.receive(True)
            self.spool.move_forward(5)
            self.z_motor.receive(False)
            self.spool.move_forward(5)


    def update_value(self, info):
        self.queue.put(info)

    def run(self):
        self.initial_sequence()
        MM_COUNTER = 0
        print "Counter set to zero. Executing file..."
        for item in test.test_list:
            self.steps_to_take = item[0] - MM_COUNTER
            self.spool.move_forward(10*(self.steps_to_take))
            MM_COUNTER = MM_COUNTER +  self.steps_to_take
            print "This is where I think I am: %smm " % (MM_COUNTER)
            self.z_motor.receive(item[1])
            if MM_COUNTER % 500 is 1:
                print "We're at: %smm" %(MM_COUNTER)
        self.initial_sequence()

main = Main()
main.start()





# spool = Spool()
# spool.start()

# z_motor = Z_Motor()
# z_motor.start()    			





# stepper_spool.set_direction(cw)
# stepper_spool.set_eighth_step()

# stepper_pen.set_direction(cw)
# stepper_pen.set_eighth_step()

# # for i in range (0,999):
# # 	stepper_spool.step()
# # 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# # 	print MM_COUNTER

# for i in range (0,1650):
# 	stepper_pen.step()
# 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# 	print MM_COUNTER

# stepper_pen.set_direction(ccw)

# for i in range (0,1650):
# 	stepper_pen.step()
# 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# 	print MM_COUNTER


# # Clean up (just calls GPIO.cleanup() function.)