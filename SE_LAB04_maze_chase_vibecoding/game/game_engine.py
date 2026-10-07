import random
import pygame
from game.maze import generate_maze, build_wall_rects, CELL
from game.entities import Player, Enemy, BASE_MOVE_INTERVAL, FREEZE_FRAMES

COLS, ROWS = 13, 11
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 50
FPS = 60
RAMP_MS = 15000        # enemies speed up every 15 seconds
RAMP_STEP = 2          # frames removed from move_interval each time
MIN_INTERVAL = 5
MAX_STEPS = 8          # 20 -> 18 -> ... -> 6 -> 5 (capped)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Chase")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18)
        self.small_font = pygame.font.SysFont("monospace", 13, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 38, bold=True)
        self.reset()

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.wall_rects = build_wall_rects(self.walls, ROWS, COLS)
        self.bounds = pygame.Rect(0, 0, COLS*CELL, ROWS*CELL)
        self.player = Player(0, 0)
        # Task 1: three enemies, one in each of the other corners
        self.enemies = [Enemy(ROWS-1, COLS-1)]
        self.exit_rect = pygame.Rect((COLS//2)*CELL+5, (ROWS//2)*CELL+5, CELL-10, CELL-10)
        self._place_pellet()
        self.caught = False
        self.won = False
        self.score = 0                       # Task 4: frames survived
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_ms = 0
        self.speed_tier = 1                  # Task 2

    def _place_pellet(self):
        # Task 3: random cell that isn't a spawn point or the exit
        banned = {(0,0), (ROWS-1,COLS-1), (ROWS-1,0), (0,COLS-1), (ROWS//2, COLS//2)}
        cells = [(r,c) for r in range(ROWS) for c in range(COLS) if (r,c) not in banned]
        r, c = random.choice(cells)
        cx, cy = c*CELL+CELL//2, r*CELL+CELL//2
        self.pellet_rect = pygame.Rect(cx-8, cy-8, 16, 16)
        self.pellet_active = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
        return True

    def _update_difficulty(self):
        self.elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        steps = self.elapsed_ms // RAMP_MS
        interval = max(MIN_INTERVAL, BASE_MOVE_INTERVAL - RAMP_STEP * steps)
        self.speed_tier = min(steps, MAX_STEPS) + 1
        for e in self.enemies:
            e.move_interval = interval

    def update(self):
        if self.caught or self.won: return
        self.score += 1
        self._update_difficulty()
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.wall_rects, self.bounds)
        for e in self.enemies:
            e.update(self.walls, self.player, ROWS, COLS)
        if self.pellet_active and self.player.rect.colliderect(self.pellet_rect):
            self.pellet_active = False
            for e in self.enemies:
                e.freeze(FREEZE_FRAMES)
        if any(self.player.rect.colliderect(e.rect) for e in self.enemies):
            self.caught = True
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True

    def draw(self):
        self.screen.fill((230, 220, 210))
        wc=(50,40,60)
        for r in range(ROWS):
            for c in range(COLS):
                x,y=c*CELL,r*CELL
                w=self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen,wc,(x,y),(x+CELL,y),3)
                if w[1]: pygame.draw.line(self.screen,wc,(x,y+CELL),(x+CELL,y+CELL),3)
                if w[2]: pygame.draw.line(self.screen,wc,(x+CELL,y),(x+CELL,y+CELL),3)
                if w[3]: pygame.draw.line(self.screen,wc,(x,y),(x,y+CELL),3)
        pygame.draw.rect(self.screen,(80,200,80),self.exit_rect,border_radius=4)
        lbl=self.small_font.render("EXIT",True,(20,80,20))
        self.screen.blit(lbl,lbl.get_rect(center=self.exit_rect.center))
        if self.pellet_active:
            pygame.draw.circle(self.screen,(250,210,20),self.pellet_rect.center,8)
            pygame.draw.circle(self.screen,(160,120,0),self.pellet_rect.center,8,2)
        self.player.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        self._draw_hud()
        if self.caught:
            self._overlay("CAUGHT!", (220,60,60))
        if self.won:
            self._overlay("ESCAPED!", (80,220,80))
        pygame.display.flip()

    def _draw_hud(self):
        pygame.draw.rect(self.screen,(30,30,50),pygame.Rect(0,ROWS*CELL,WIDTH,50))
        tier = f"Speed: Tier {self.speed_tier}" + (" MAX" if self.speed_tier >= 9 else "")
        frozen = max((e.freeze_timer for e in self.enemies if e.frozen), default=0)
        line1 = f"Survived: {self.score//60}s   {tier}"
        if frozen: line1 += f"   FROZEN {frozen/60:.1f}s"
        line2 = "Reach EXIT! Grab the yellow pellet.  R=Restart"
        self.screen.blit(self.font.render(line1,True,(230,230,230)),(8,ROWS*CELL+5))
        self.screen.blit(self.font.render(line2,True,(160,160,180)),(8,ROWS*CELL+27))

    def _overlay(self, text, color):
        surf=pygame.Surface((WIDTH,ROWS*CELL),pygame.SRCALPHA)
        surf.fill((0,0,0,140))
        self.screen.blit(surf,(0,0))
        msg=self.big_font.render(text,True,color)
        score=self.font.render(f"Final score: Survived {self.score//60}s",True,(240,240,240))
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        cy=ROWS*CELL//2
        self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,cy-50))
        self.screen.blit(score,(WIDTH//2-score.get_width()//2,cy))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,cy+28))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()