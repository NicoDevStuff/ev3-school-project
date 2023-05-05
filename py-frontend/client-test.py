
import pygame
import socket


pygame.init()


screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Socket Client")


font = pygame.font.SysFont("Arial", 24)

host = '127.0.0.1'
port = 6969
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.setblocking(False)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                message = "Hello, server!"
                client_socket.send(message.encode())

    try:
        data = client_socket.recv(1024)
        if data:
            message = data.decode()
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (10, 10))
            pygame.display.flip()
    except socket.error:
        pass

    
    pygame.display.update()
    clock.tick(60)

client_socket.close()
pygame.quit()

