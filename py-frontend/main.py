import socket
import pygame
import gui


pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Frontend")

clock = pygame.time.Clock()
switch1 = gui.Switch(pygame.Vector2(30, 30), False, "Click me")
button1 = gui.Button(pygame.Vector2(90, 30), False, "Click me")
label1 = gui.Label(pygame.Vector2(150, 30), "Test")
fps = gui.Label(pygame.Vector2(500, 500), "60")



HOST = '127.0.0.1'
PORT = 6969


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()


def sw():
    switch1.label += " More Clicking"
def btn():
    client_socket.send(b'100')

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
            done = True
    
    screen.fill((50, 50, 50))
    
    keys = pygame.key.get_pressed()

    switch1.show(screen, sw)
    button1.show(screen, btn)
    label1.show(screen)
    fps.text = f"FPS: { clock.get_fps() }"
    fps.show(screen)

    try:
        data = client_socket.recv(1024)
        if data:
            print(f"Received message: {data.decode()}")
    except:
        pass
    
    clock.tick(60)
    pygame.display.update()


