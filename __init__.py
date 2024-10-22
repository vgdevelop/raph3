import utime
from raph3.action import Action
from raph3 import system
from raph3.raph import Raph



try:
    
    if system.start():
        raph = Raph()
        raph.run()

except Exception as e:
    print("aaaaaaa")
    if system.DME: print("Error: ", e)