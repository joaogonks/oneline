import spi
import time

spi.amt.set_zero()
last_position = spi.amt.get_position()
direction = None
lap = 0
gap = 3000

while True:
    current_pos = spi.amt.get_position()
    time.sleep(0.001)
    if last_position < current_pos and  current_pos - last_position < gap:
        direction = True
    elif last_position - current_pos > gap:
        direction = True
    else:
        direction = False
    if current_pos < last_position and direction:
        lap = lap + 1
    elif last_position - current_pos < 0 and not direction:
        lap = lap - 1
    last_position = current_pos
    big_value = (lap*4096) + current_pos
    print big_value