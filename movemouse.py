import win32api
import win32gui
import time
import math
import ctypes
from pynput.mouse import Button, Controller, Listener
import time
import socket, string
import threading

HOST = "irc.twitch.tv"
PORT = 6667
CHANNEL = "qjax"
PASS = "oauth:e7gln6fzjmoaoonxp185e5kx920rvo"
IDENT = "chat_chess_bot"

p = win32gui.GetCursorPos()	
	
#ctypes.windll.user32.SetCursorPos(100, 20)
#ctypes.windll.user32.SetCursorPos(p[0], p[1])
#mouse.click((p[0], p[1]), "right")
#ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) #left down
#ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)	#left up

mouse = Controller()
boardSize = []
board_64 = []
isMoving = False
print('The current pointer position is {0}'.format(mouse.position))

# convert - one square to another square
# assuming you are white
def convert(coord):
	
	x = ord(coord[0]) - ord('a')
	if(not coord[1].isdigit() or not coord[3].isdigit()):
		return 'null'
	y = 8 - int(coord[1])
	dx = ord(coord[2]) - ord('a')
	dy = 8 - int(coord[3])
	print(x, y, dx, dy)
	if(x+8*y < 0 or x+8*y > 63 or dx+8*dy < 0 or dx+8*dy > 63):
		return null
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

'''if (rcCount > 1 and button == Button.left and pressed == False and isMoving == False):
#print(boardSize[0], " ", boardSize[1])
move = convert('e2e4')
move_piece(move)'''
rcCount = 0
def on_click(x, y, button, pressed):
	global rcCount
	global boardSize
	'''print('{0} at {1} with {2}'.format(
		'Pressed' if pressed else 'Released',
		(x, y), button))'''
	print(rcCount)
	if (button == Button.right and pressed != True and rcCount < 3):
		rcCount += 1
		boardSize.append([x,y])
		if rcCount == 2:
			def_board()
		
# Stop listener
def on_scroll(x, y, dx, dy):
	return False

def listener():
	# collect events until released
	with Listener(
		on_click=on_click,
		on_scroll=on_scroll) as listener:
		listener.join()
	

##############################################	

s = socket.socket()

def send_message(message):
	s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))

def connect_to_twitch():
	
	s.connect((HOST, PORT))
	s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
	s.send(bytes("NICK " + IDENT + "\r\n", "UTF-8"))
	s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))


	while True:
		line = str(s.recv(1024))
		print(line)
		if "End of /NAMES list" in line:
			send_message("Successfully joined chat")
			break
	truth = True
	while truth:
		for line in str(s.recv(1024)).split('\\r\\n'):
			parts = line.split(':')
			if len(parts) < 3:
				continue
				
			if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
				message = parts[2][:len(parts[2])]
			if "PING" in message:
				s.send(line.replace("PING", "PONG"))
				
			usernamesplit = parts[1].split("!")
			username = usernamesplit[0]

			print(username + ": " + message)
			
			if len(message) == 4:
				#print(boardSize[0], " ", boardSize[1])
				move = convert(message)
				if move == 'null':
					break
				move_piece(move)
				
			elif message == "Hey":
				send_message("Welcome to my stream, " + username)
			elif message == "End Stream Now":
				truth = False

##################################################
t1 = threading.Thread(target = listener, args = ())
t2 = threading.Thread(target = connect_to_twitch, args=())

t1.start()
t2.start()

t1.join()
t2.join()
