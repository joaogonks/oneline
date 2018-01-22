#!/usr/bin/python

import easydriver as ed

MM_PER_STEP = 0.046
MM_COUNTER = 0

cw = True
ccw = !cw

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

stepper_spool = ed.easydriver(18, 0.004, 23, 24, 17, 25)
#stepper_pen = ed.easydriver(18, 0.004, 23, 24, 17, 25)

# Set motor direction to clockwise.

for i in range(0,100):
	stepper_spool.set_direction(cw)
	stepper_spool.set_sixteenth_step()
	MM_COUNTER = MM_COUNTER + MM_PER_STEP



# Clean up (just calls GPIO.cleanup() function.)
stepper.finish()