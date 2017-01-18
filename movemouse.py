import win32api
import win32gui
import time
import math
import ctypes
from pynput.mouse import Button, Controller, Listener
import time

'''for i in range(500):
	x = int(500+math.sin(math.pi*i/100)*500)
	y = int(500+math.cos(i)*100)
	win32api.SetCursorPos((x,y))
	time.sleep(.01)'''

	
p = win32gui.GetCursorPos()	
	
ctypes.windll.user32.SetCursorPos(100, 20)
ctypes.windll.user32.SetCursorPos(p[0], p[1])
#mouse.click((p[0], p[1]), "right")
#ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) #left down
#ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)	#left up

mouse = Controller()
rcCount = 0
boardSize = []
board_64 = []
isMoving = False
print('The current pointer position is {0}'.format(mouse.position))

# convert - one square to another square
# assuming you are white
def convert(coord):
	if len(coord) != 4:
		return
	x = ord(coord[0]) - ord('a')
	y = 8 - int(coord[1])
	dx = ord(coord[2]) - ord('a')
	dy = 8 - int(coord[3])
	print(x, y, dx, dy)
	return [x + 8*y, dx + 8*dy]
	




# needs input from Twitch
def move_piece(move):
	global isMoving
	isMoving = True
	ctypes.windll.user32.SetCursorPos(int(board_64[move[0]][0]), int(board_64[move[0]][1]))
	time.sleep(.4)
	ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) #left down
	time.sleep(.4)
	ctypes.windll.user32.SetCursorPos(int(board_64[move[1]][0]), int(board_64[move[1]][1]))
	time.sleep(.4)
	ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) #left up
	print("moving")
	isMoving = False


def def_board():
	global board_64
	board_xlen = abs(boardSize[1][0] - boardSize[0][0]) / 7
	board_ylen = abs(boardSize[1][1] - boardSize[0][1]) / 7
	for i in range(0, 8):
		for j in range(0,8):
			board_64.append([board_xlen * j + boardSize[0][0], board_ylen * i + boardSize[0][1]])
	print("THIS IS THE TEST: ", board_xlen, " ", board_ylen, " ", boardSize[0][0], " ", board_64[0], " ", board_64[1], board_64[63])

def on_click(x, y, button, pressed):
	global rcCount
	global boardSize
	print(rcCount)
	print('{0} at {1} with {2}'.format(
		'Pressed' if pressed else 'Released',
		(x, y), button))
	if (rcCount > 1 and button == Button.left and pressed == False and isMoving == False):
		#print(boardSize[0], " ", boardSize[1])
		move = convert('e2e4')
		move_piece(move)
	elif (button == Button.right and pressed != True):
		rcCount += 1
		boardSize.append([x,y])
		if rcCount == 2:
			def_board()
		
# Stop listener
def on_scroll(x, y, dx, dy):
	return False

# collect events until released
with Listener(
	on_click=on_click,
	on_scroll=on_scroll) as listener:
	listener.join()
	

