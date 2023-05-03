import socket
import pygame
import gui

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Frontend")

clock = pygame.time.Clock()
switch1 = gui.Switch(pygame.Vector2(30, 30), False, "Click me")
button1 = gui.Button(pygame.Vector2(90, 30), False, "Click me")
label1 = gui.Label(pygame.Vector2(150, 30), "Testwefliuwelifuhwlieuh")
fps = gui.Label(pygame.Vector2(500, 500), "60")
def sw():
    switch1.label += " More Clicking"
def btn():
    print("e;woifhw;e")


# socket stuff
HOST = '127.0.0.1'
PORT = 6969

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

client, addr = server.accept()

def getclientmsg() -> str:
    return client.recv(1024).decode('utf-8')
def sendclientmsg(msg):
    client.send(msg.encode('utf-8'))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill((50, 50, 50))
    
    keys = pygame.key.get_pressed()

    # socket
    msg = getclientmsg()
    if msg == 'quit':
        done = True
    else:
        if msg != "":
            print(msg)
    
    if keys[pygame.K_SPACE]:
        sendclientmsg('space')
    
    switch1.show(screen, sw)
    button1.show(screen, btn)
    label1.show(screen)
    fps.text = f"FPS: { clock.get_fps() }"
    fps.show(screen)

    clock.tick(60)
    pygame.display.update()

client.close()
server.close()
