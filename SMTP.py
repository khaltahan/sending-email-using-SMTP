# Necessary imports.
from socket import *
from base64 import *
import ssl

# Prompt user to enter information needed for email.
email = input("Enter the sending email address: ")
emailPassword = input("Enter the GMAIL app password: ")
destinationEmail = input("Enter the email you would like to send to: ")
subjectEmail = input("Enter the subject of the email: ")
bodyEmail = input("Enter a message you woud like to send: ")

# Messages to be displayed in email body.
msg = '{}. \r\nI love computer networks!'.format(bodyEmail)
endmsg = '\r\n.\r\n'

# Select a mail server and its port.
mailServer = 'smtp.gmail.com'
mailPort = 587

# Create socket called clientSocket and establish a TCP connection with mailserver.
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))

recv = clientSocket.recv(1024).decode()
print (recv)
if recv[:3] != '220':
	print ('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'.encode()
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024).decode()
print (recv1)
if recv1[:3] != '250':
	print ('250 reply not received from server.')

# Send STARTTLS command.
starTlsCommand = "STARTTLS\r\n".encode()
clientSocket.send(starTlsCommand)
recv2 = clientSocket.recv(1024).decode()
sslClientSocket = ssl.wrap_socket(clientSocket)

# Use binary-to-text encoding for email and emailPassword
emailAddress = b64encode(email.encode())
emailPassword = b64encode(emailPassword.encode())

# Send AUTH LOGIN command and print the server response.
authorizationCommand = "AUTH LOGIN\r\n"
sslClientSocket.send(authorizationCommand.encode())
recv2 = sslClientSocket.recv(1024).decode()
print(recv2)

# Send emailAddress and print the server response.
sslClientSocket.send(emailAddress + "\r\n".encode())
recv3 = sslClientSocket.recv(1024).decode()
print(recv3)

# Send emailPassword and print the server response.
sslClientSocket.send(emailPassword + "\r\n".encode())
recv4 = sslClientSocket.recv(1024).decode()
print(recv4)
	
# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <{}>\r\n".format(email)
sslClientSocket.send(mailFrom.encode())
recv5 = sslClientSocket.recv(1024).decode()
print(recv5)

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <{}>\r\n".format(destinationEmail)
sslClientSocket.send(rcptTo.encode())
recv6 = sslClientSocket.recv(1024).decode()

# Send DATA command and print server response. 
data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv7 = sslClientSocket.recv(1024).decode()
print(recv7)

# Send message data.
sslClientSocket.send("Subject: {}\n\n{}".format(subjectEmail, msg).encode())

# Message ends with a single period.
sslClientSocket.send(endmsg.encode())
recv8 = sslClientSocket.recv(1024).decode()
print(recv8)

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
sslClientSocket.send(quitcommand.encode())
recv9 = sslClientSocket.recv(1024).decode()
print(recv9)

# Exit upon completion
sslClientSocket.close()
print('Successfuly complete')