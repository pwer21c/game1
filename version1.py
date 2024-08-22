# 
# 랜덤숫자 생성 적의 미사일, 구름을 랜덤하게 발생
# 파이썬에서 제공하는 파이썬게임 모듈을 import 한다 
import random
import pygame

# 화살표 조작 관련 변수를 로딩한다.
# 키다운과 퀴트는 키가 눌려졌는지 그리고 게임의 윈도우가 닫히거나 종료되었는지를 체크 할때 쓰인다. RLEACCEL은 이미지를 처리할때 사용
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

# 게임 오락의 크기를 설정한다.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
# Player 클래스는 pygame.sprite.Sprite  를 상속받는다.

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() 
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        # 부모클래스를 초기화하고
        # pygame.image.load 를 불러오는데  만들어진 jet.png 이미지를 불러와서 이미지를 포맷한다.
        #그리고 만들어진 이미지의 칼라에서 흰색을 투명색으로 설정한다.
        # 이지지의 사각형 영역 위치를 기억한다.

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
            # 비행기가 올라갈때 나는 소리
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
            # 비행기가 내려갈때 나는 소리
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # 플레어이가 화면에 계속 보여지도록 한다.
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Enemy class 부분

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        # 화면 밖에서 미사일을 생성한다. 
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # 미사일 오른쪽에서 왼쪽으로 이동해온다. 
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# 구름 클래스
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # 구름은 일정한 속도로 오른쪽에서 왼쪽으로 이동한다.
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# 사운드 시스템 초기화
pygame.mixer.init()

# 게임 시작 준비
pygame.init()

# 게임의 프레임 속도를 관리하기 위해 Clock object 를 만든다.
clock = pygame.time.Clock()

# 화면 오브젝트를 만든다. 이것은 게임 화면의 크기를 설정한다.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 새로운 적과 새로운 구름을 추가한다. 새로운 적은 0.25초마다 새로운 구름은 1초마다 생성
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) # miliseconde
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create our 'player' 플레이어 객체를 만든다.
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
#스프라이트는 게임에서 각종 객체를 표현하고, 개별적인 움직임과 충돌 감지 등을 관리한다. 이렇게 그룹으로 관리하면 더 쉽게 관리한다. 
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
#배경음악을 로드하고 loops=-1 무한반복한다.
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# 업,다운,충돌 사운드 표현
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# 사운드를 50퍼센트롤 설정한다.
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Variable to keep our main loop running
running = True

# Our main loop 게임을 무한히 계속한다. 충돌할때까지
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue 화면을 하늘색으로 채운다.
    screen.fill((135, 206, 250))

    # Draw all our sprites 모든 스프라이트를 화면에 그린다.
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Stop the loop
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()