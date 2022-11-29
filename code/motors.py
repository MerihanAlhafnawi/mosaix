
def dir(direction):
    if (direction == "forward"):
        in1 = True
        in2 = False
        in3 = True
        in4 = False
    elif (direction == "backward"):
        in1 = False
        in2 = True
        in3 = False
        in4 = True
    elif (direction == "left"):
        in1 = False
        in2 = True
        in3 = True
        in4 = False
    elif (direction == "right"):
    	in1 = True
    	in2 = False
    	in3 = False
    	in4 = True
    elif (direction == "stop"):
        in1 = False
        in2 = False
        in3 = False
        in4 = False
    return (in1, in2, in3, in4)


