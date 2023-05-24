import socket
import pygame
import gui
import time
import math

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Frontend")

clock = pygame.time.Clock()
switch1 = gui.Switch(pygame.Vector2(30, 30), False, "Click me")
button1 = gui.Button(pygame.Vector2(90, 30), False, "Click me")
label1 = gui.Label(pygame.Vector2(150, 30), "Test")
fps = gui.Label(pygame.Vector2(500, 500), "60")

def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()

        return local_ip
    except socket.error:
        return "Unable to retrieve local IP address."



HOST = get_local_ip()

print(HOST)

PORT = 6969


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()


def sw():
    switch1.label += " More Clicking"
def btn():
    pass


while True:
    try:
        client_socket, address = server_socket.accept()
        break
    except:
        pass

done = False

client_socket.setblocking(False)
last = [0, 0, 0, 0]

screen.fill((50, 50, 50))

while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for i in range(100): 
                try:
                    client_socket.send(b'quit')
                    time.sleep(0.1)
                except:
                    pass
            done = True
            
     
        
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


    try:
        client_socket.send((str(steer[0])+" "+str(steer[1])+" ").encode('utf-8'))
    except:
        pass




    
    
    try:
        data = client_socket.recv(128)
        mm = data.decode().split("x")
        del mm[0]
          


        l = [0, 0]
        fff = 0
        for u in mm:
            try:
                u = u.split(" ")
                l[0] += float(u[0])
                l[1] += float(u[1])
                fff += 1
            except:
                pass
        try:
            l[0] /= fff
            l[1] /= fff
        except:
            pass


        height = int(50000 / (l[1] * math.cos(l[0]/140)))


        x = (l[0]+70)*(1280/140)


        color = max(min(height/1.5, 255), 20)
        pygame.draw.polygon(screen, (0 ,0 , 0), [(x, 0), (last[1], 0), (last[1], 720), (x, 720)])
        pygame.draw.polygon(screen, (color, color, color), [(x, 360-height), (last[1], 360-last[0]), (last[1], 360+last[0]), (x, 360+height)])

        
        

        last = [height, x, l[0], l[1]]


        switch1.show(screen, sw)
        button1.show(screen, btn)
        label1.show(screen)
        

        pygame.display.update()
    except:
        pass
    
    
    #pygame.display.update()

server_socket.close()
