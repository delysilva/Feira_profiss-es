from implicit import QuadTree
from Vector import StaticVector 
import math

def topologist_sine_curve(x, y):
	if (abs(x-400) < 10**(-6)):
		return 400
	else:
		return 200*math.sin(1/(0.001*(x-400))) - y + 400

AVAILABLE_FUNCTIONS = StaticVector(5)
AVAILABLE_FUNCTIONS.append(lambda x,y : (x-400)**2 + (y-400)**2 - 10000) # circle
AVAILABLE_FUNCTIONS.append(lambda x,y: max(abs(x-400), abs(y-400)) - 200) # square
AVAILABLE_FUNCTIONS.append(lambda x,y: 200*math.sin(x/100) + 400 - y) # sine wave
AVAILABLE_FUNCTIONS.append(lambda x,y: 
	((x-400)**2 + (y-400)**2)**2 + 4*80*(x-400)*((x-400)**2+(y-400)**2) - 4*80**2*(y-400)**2 - 400) # cardioid
AVAILABLE_FUNCTIONS.append(topologist_sine_curve)

def main():
    global AVAILABLE_FUNCTIONS
    win_x = 800
    win_y = 800

    # only now import app and pyglet, otherwise it will start window before getting the params
    from app import App
    import pyglet
    window = pyglet.window.Window(win_x, win_y)
    tree = QuadTree(window.width, window.height, 7)
    tree.build_tree()

    # initial_depth = 2
    myApp = App(window, 
                tree, 
                AVAILABLE_FUNCTIONS, 
                (255,255,255), 
                (0,0,255),
                (255,0,0),
                2,
                (0, 0, 0),
                (255, 255, 255)
                )
    myApp.gameloop()

if __name__ == '__main__':
    main()
