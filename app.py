import pyxel
import random



class SnakeGame:
    def __init__(self):
        # Pyxelウィンドウの初期化（160x120のサイズで）
        pyxel.init(160, 120)
        # ゲームの初期状態を設定
        self.reset_game()
        # Pyxelのアップデート（ロジック）とドロー（描画）メソッドを設定
        pyxel.run(self.update, self.draw)
        

    def reset_game(self):
        # ヘビの初期位置と初期方向を設定
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        # 食べ物の初期位置を生成
        self.food = self.spawn_food()
        # スコアとゲームオーバーフラグの初期化
        self.score = 0
        self.game_over = False
        # ゲームのタイマーを設定（30秒）
        self.timer = 30

    def spawn_food(self):
        # 食べ物をランダムな位置に生成
        while True:
            food = (random.randint(0, 159), random.randint(0, 119))
            # ヘビの体と重ならない位置に食べ物を配置
            if food not in self.snake:
                return food

    def update(self):
        self.update_snake()
        # ゲームオーバー時の処理
        if self.game_over:
            # Rキーでゲームをリセット
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
                return

        # ヘビの頭が食べ物に触れた場合の処理
        if self.snake[0] == self.food:
            self.score += 1
            self.timer += 1
            # ヘビの長さを増やす
            self.snake.append(self.snake[-1])
            # 新しい食べ物を生成
            self.food = self.spawn_food()

        # スコアが一定値に達した時のステージ変更は省略

    def update_snake(self):
        
        # ヘビの新しい頭の位置を計算
        new_head_x = (self.snake[0][0] + self.direction[0]) % pyxel.width
        new_head_y = (self.snake[0][1] + self.direction[1]) % pyxel.height
        new_head = (new_head_x, new_head_y)
        # ヘビが自分自身に触れた場合、ゲームオーバー
        if new_head in self.snake[1:]:
            self.game_over = True

        # ヘビの位置を更新
        self.snake = [new_head] + self.snake[:-1]

        # キーボード入力によるヘビの方向の変更
        if pyxel.btnp(pyxel.KEY_LEFT): self.direction = (-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT): self.direction = (1, 0)
        if pyxel.btnp(pyxel.KEY_UP): self.direction = (0, -1)
        if pyxel.btnp(pyxel.KEY_DOWN): self.direction = (0, 1)

    def draw(self):
        # 画面をクリア
        pyxel.cls(0)
        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(55, 45, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(48, 55, "Press R to Restart", 7)
            return

        # ヘビと食べ物の描画
        for x, y in self.snake:
            pyxel.rect(x, y, 1, 1, 11)
        pyxel.rect(self.food[0], self.food[1], 1, 1, 8)

        # スコアとタイマーの表示
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Time: {int(self.timer)}", 7)
        
    

SnakeGame()