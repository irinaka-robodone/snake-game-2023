import pyxel
import random

class SnakeGame:
    def __init__(self):
        pyxel.init(160, 120)
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.timer = 30

    def spawn_food(self):
        while True:
            food = (random.randint(0, 159), random.randint(0, 119))
            if food not in self.snake:
                return food

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
                return

            # self.timer -= 1 / 30
            # if self.timer <= 0:
            #     self.game_over = True

        # self.update_snake()
        if self.snake[0] == self.food:
            self.score += 1
            self.timer += 1
            self.snake.append(self.snake[-1])
            self.food = self.spawn_food()
        if self.score % 5 == 0:
        # ステージ変更（省略）
            pass
    
    def update_snake(self):
        new_head = pyxel.wrap(
        self.snake[0][0] + self.direction[0], 
        self.snake[0][1] + self.direction[1], 
        160, 120
        )

        if new_head in self.snake[1:]:
            self.game_over = True

        self.snake = [new_head] + self.snake[:-1]

        if pyxel.btnp(pyxel.KEY_LEFT): self.direction = (-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT): self.direction = (1, 0)
        if pyxel.btnp(pyxel.KEY_UP): self.direction = (0, -1)
        if pyxel.btnp(pyxel.KEY_DOWN): self.direction = (0, 1)

    def draw(self):
        pyxel.cls(0)
        if self.game_over:
            pyxel.text(55, 45, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(48, 55, "Press R to Restart", 7)
            return

        for x, y in self.snake:
            pyxel.rect(x, y, 1, 1, 11)
        pyxel.rect(self.food[0], self.food[1], 1, 1, 8)

        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Time: {int(self.timer)}", 7)

SnakeGame()