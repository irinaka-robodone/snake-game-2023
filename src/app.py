import pyxel
import random

class SnakeGame:
    def __init__(self):
        # Pyxelウィンドウの初期化（40x40のサイズで、フレームレートは60）
        self.width = 90
        self.height = 45
        pyxel.init(self.width, self.height, fps=60)

        # ゲームの初期状態の設定
        self.speed = 2  # 蛇の移動速度
        self.food_count = 9    # 食べ物の数
        self.foods = []
        self.reset_game()  # ゲームのリセット
        self.stage = 1  # ステージの初期設定
        self.obstacles = []  # 障害物の初期リスト
        self.bg_color_change_speed = 0.005
        pyxel.load("resource.pyxres")
        pyxel.play(0, 0)
        # Pyxelのアップデート（ゲームロジック）とドロー（描画）メソッドの設定
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # ヘビの初期位置と方向の設定
        self.snake = [(10, 10)]
        self.direction = (1, 0)

        # 食べ物の初期位置を生成
        self.foods = [self.spawn_food() for _ in range(self.food_count)]

        # スコア、ゲームオーバーフラグ、タイマーの初期化
        self.score = 0
        self.game_over = False
        self.timer = 60
        self.frame_counter = 0

        # ステージ2への変更処理（スコアが20を超えたら）
        if self.score > 20 and self.stage == 1:
            self.stage = 2
            self.change_stage()
            
    def spawn_food(self):
    # 食べ物をランダムな位置に生成（ヘビの体と重ならない位置）
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            
            esa_rand = random.random()
            kind_food = "esa"
            color = 8
            if esa_rand < 0.2:
                kind_food = "doku"
            elif esa_rand < 0.3:
                kind_food = "mumi"
            if kind_food == "esa":
                color = 8
            elif kind_food == "doku":
                color =7
            elif kind_food == "mumi":
                color = 6
            food = [x, y, color, kind_food]  # 食べ物の情報に色を追加
            if food[:2] not in [f[:2] for f in self.foods] and food[:2] not in self.snake:
                return food

    def update(self):
        self.frame_counter += 1

        # 一定のフレーム間隔でヘビを更新
        if self.frame_counter % self.speed == 0:
            self.update_snake()

        # タイマーとゲームオーバーの処理
        if self.timer <= 0:
            self.game_over = True
        if self.frame_counter % 60 == 0:
            self.timer -= 1

        # ゲームオーバー時のリセット処理
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
                return
        
        print("snake[0]:", self.snake[0])
        print("self.foods[0][:2]", self.foods[0][:2])

        for food in self.foods:
            head = list(self.snake[0])
            if head == food[:2]:  # 食べ物の位置を確認
                self.score += 1
                self.timer += 15
                # food の種類によって、ヘビの長さを伸ばしたり短くしたりする。
                if food[3] == "doku":  # 食べ物が体を短くする効果を持つ場合
                    print(food)
                    if len(self.snake) > 1:
                        self.snake.pop()  # ヘビの長さを1つ減らす
                else:
                    self.snake.append(self.snake[-1])  # 通常の食べ物の場合は長さを増やす
                self.foods.remove(food)
                self.foods.append(self.spawn_food())
                return
            
    def change_stage(self):
        # ステージに応じた設定
        if self.stage < 2:
            return
        # ステージ2での障害物の配置
        self.obstacles = [(random.randint(0, self.width-1), random.randint(0, self.height-1)) for _ in range(10)]

    def update_snake(self):
        # ヘビの新しい頭の位置を計算
        new_head_x = (self.snake[0][0] + self.direction[0]) % self.width
        new_head_y = (self.snake[0][1] + self.direction[1]) % self.height
        new_head = (new_head_x, new_head_y)

        # ヘビが自分自身または障害物に触れた場合のゲームオーバー処理
        if new_head in self.snake[1:] or new_head in self.obstacles:
            self.game_over = True

        # ヘビの位置を更新
        self.snake = [new_head] + self.snake[:-1]

        # キーボード入力によるヘビの方向の変更
        if pyxel.btn(pyxel.KEY_LEFT): self.direction = (-1, 0)
        if pyxel.btn(pyxel.KEY_RIGHT): self.direction = (1, 0)
        if pyxel.btn(pyxel.KEY_UP): self.direction = (0, -1)
        if pyxel.btn(pyxel.KEY_DOWN): self.direction = (0, 1)
        
    def draw(self):
        # 背景色の設定
        bg_color_id = int(pyxel.frame_count * self.bg_color_change_speed) %  4  # フレームカウントによる色の変更
        if bg_color_id == 0:
            bg_color = 7
        elif bg_color_id == 1:
            bg_color = 6
        elif bg_color_id == 2:
            bg_color = 8
        else:
            bg_color= 10
            
        pyxel.cls(bg_color)
        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(20, 5, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(10, 20, "Press R to Restart", 11)
            pyxel.text(1,35,f"score:{self.score}",11)
            return

        # スコアとタイマーの表示
        pyxel.text(2.5, 2.5, f"Score: {self.score}", 7)
        pyxel.text(2.5, 7.5, f"Time: {int(self.timer)}", 7)

        color_list = [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]  # 例えば、これらの色を使用
        for i, (x, y) in enumerate(self.snake):
            color = color_list[i % len(color_list)]  # 色リストから色を選択
            pyxel.rect(x, y, 1, 1, color)
        # # ヘビと食べ物の描画
        # for x, y in self.snake:
        #     pyxel.rect(x, y, 1, 1, 11)  # ヘビ
        for food in self.foods:
            pyxel.rect(food[0], food[1], 1, 1, food[2])  # 食べ物

        # 障害物の描画
        for obstacle in self.obstacles:
            pyxel.rect(obstacle[0], obstacle[1], 1, 1, 9)  # 障害物

SnakeGame()
# ゲームの実行