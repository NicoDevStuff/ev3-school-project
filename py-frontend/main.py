import socket
import pygame
import gui
import os

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Frontend")

clock = pygame.time.Clock()
switch1 = gui.Switch(pygame.Vector2(30, 30), False, "Click me")
button1 = gui.Button(pygame.Vector2(90, 30), False, "Click me")
label1 = gui.Label(pygame.Vector2(150, 30), "Test")
fps = gui.Label(pygame.Vector2(500, 500), "60")



HOST = '192.168.43.173'
PORT = 6969


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()


def sw():
    switch1.label += " More Clicking"
def btn():
    pass#client_socket.send((str(f)+" "+str(i)).encode('utf-8'))

while True:
    try:
        client_socket, address = server_socket.accept()
        break
    except:
        pass

done = False

client_socket.setblocking(False)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_socket.send(b'quit')
            done = True
            
    
    screen.fill((50, 50, 50))
    
    keys = pygame.key.get_pressed()
    
    steer = [0, 0]
    if keys[pygame.K_UP]:
        steer[0] += 1
        steer[1] += 1

    if keys[pygame.K_LEFT]:
        steer[0] += 1
        steer[1] -= 1

    if keys[pygame.K_RIGHT]:
        steer[0] -= 1
        steer[1] += 1

    if keys[pygame.K_DOWN]:
        steer[0] -= 1
        steer[1] -= 1



    client_socket.send((str(steer[0])+" "+str(steer[1])).encode('utf-8'))




    switch1.show(screen, sw)
    button1.show(screen, btn)
    label1.show(screen)
    fps.text = f"FPS: { clock.get_fps() }"
    fps.show(screen)

    try:
        data = client_socket.recv(128)
        l = data.decode().split(" ")
        del l[0]
        l = list(zip(l[::2], l[1::2]))
        for e in l:
            pygame.draw.line(screen, (255, 0, 0), ((float(e[0])+180)*5, 0), ((float(e[0])+180)*5, 720))
        pygame.display.update()
    except:
        pass
    
    
    #pygame.display.update()
os.wait()
server_socket.close()
