import sys
sys.path.insert(0,"/home/castanheira/v3s_ws/fbot_vss_python/src")
from Communication import Communication
from go_to import go_to

while True:
    ball = Communication().ball()
    go = go_to(0, True, ball.x, ball.y, 0)
    go.go_to()
