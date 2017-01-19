import socket, string

HOST = "irc.twitch.tv"
PORT = 6667
CHANNEL = "qjax"
PASS = "oauth:e7gln6fzjmoaoonxp185e5kx920rvo"
IDENT = "chat_chess_bot"

def send_message(message):
	s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))

s = socket.socket()
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

while True:
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
		if message == "Hey":
			send_message("Welcome to my stream, " + username)
		else: 
			send_message("lol")