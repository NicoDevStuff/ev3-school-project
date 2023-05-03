import socket
import pygame

HOST = '127.0.0.1'
PORT = 6969

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Client")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

done = False

client.send('Client connected'.encode('utf-8'))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))
    
    keys = pygame.key.get_pressed()

    msg = client.recv(1024).decode('utf-8')
    if msg == 'quit':
        done = True
    else:
        if msg != "":
            print(msg)
    
    if keys[pygame.K_SPACE]:
        client.send('space'.encode('utf-8'))

    pygame.display.update()
client.close()
