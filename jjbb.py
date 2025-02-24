import pyxel
import pymunk
import random
import urllib.parse

FPS = 30


class Game:
    def __init__(self):
        pyxel.init(160, 240, title="Jump Jump Bouncing Ball", fps=FPS)

        self.seed = random.randint(0, 100000)  # 乱数のシード値
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """ゲームリセット"""
        pyxel.rseed(self.seed)

        # 物理空間の設定
        self.space = pymunk.Space()
        self.space.gravity = (0, 200)

        # 基本設定
        self.floor_y = pyxel.height - 5  # 地面位置
        self.radius = 5  # 自機半径
        self.body_elasticity = 0.8  # 自機の弾性係数
        self.object_elasticity = 0.6  # 地面や障害物の弾性係数
        self.move_power = 400  # 左右移動の強さ
        self.jump_power = 120  # ジャンプの強さ
        self.item_num = 10  # 生成するアイテム数

        # 自機の作成
        self.create_player()

        # 環境の作成
        self.create_walls()
        self.create_items()
        self.create_platforms()

        self.cleared = False
        self.score = 0  # スコア
        self.start_time = pyxel.frame_count

    def create_player(self):
        """自機の作成"""
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.radius))
        self.body.position = (pyxel.width // 2, self.floor_y - self.radius - 1)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = self.body_elasticity
        self.space.add(self.body, self.shape)

    def create_walls(self):
        """壁と床の作成"""
        # 地面
        floor = pymunk.Segment(
            self.space.static_body, (0, self.floor_y), (160, self.floor_y), 1
        )
        floor.elasticity = self.object_elasticity
        floor.friction = 0.5
        self.space.add(floor)

        # 左の壁
        left_wall = pymunk.Segment(
            self.space.static_body, (5, -100), (5, self.floor_y), 1
        )
        left_wall.elasticity = self.object_elasticity
        self.space.add(left_wall)

        # 右の壁
        right_wall = pymunk.Segment(
            self.space.static_body, (155, -100), (155, self.floor_y), 1
        )
        right_wall.elasticity = self.object_elasticity
        self.space.add(right_wall)

    def create_items(self):
        """アイテムの作成"""
        self.items = []
        for _ in range(self.item_num):
            x = pyxel.rndi(10, pyxel.width - 10)
            y = pyxel.rndi(20, self.floor_y - 20)
            self.add_item(x, y)

    def add_item(self, x, y):
        """アイテムを配置"""
        item_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        item_body.position = (x, y)
        item_shape = pymunk.Poly.create_box(item_body, (8, 8))
        item_shape.sensor = True  # センサーにして、衝突しても影響を与えない
        self.space.add(item_body, item_shape)
        self.items.append((item_body, item_shape))

    def create_platforms(self):
        """足場の作成"""
        self.platforms = []
        rects = []
        for _ in range(20):
            for _ in range(10):
                w = pyxel.rndi(10, 50)
                h = 6
                x = pyxel.rndi(17 + w // 2, pyxel.width - 17 - w // 2)
                y = pyxel.rndi(27 + h // 2, self.floor_y - 17 - h // 2)
                collision = False
                for fx, fy, fw, fh in rects:
                    if abs(x - fx) < w + fw + 12 and abs(y - fy) < h + fh + 12:
                        collision = True
                        break
                if not collision:
                    self.add_platform(x, y, w, h)
                    rects.append((x, y, w, h))
                    break

    def add_platform(self, x, y, width, height):
        """足場を配置"""
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_body.position = (x, y)
        platform_shape = pymunk.Poly.create_box(platform_body, (width, height))
        platform_shape.elasticity = self.object_elasticity
        self.space.add(platform_body, platform_shape)
        self.platforms.append((platform_body, platform_shape, width, height))

    def check_item_collision(self):
        """アイテムとの衝突判定"""
        for item_body, item_shape in self.items[:]:
            item_x, item_y = item_body.position
            dist = (
                (self.body.position.x - item_x) ** 2
                + (self.body.position.y - item_y) ** 2
            ) ** 0.5
            if dist <= 8:
                self.space.remove(item_body, item_shape)
                self.items.remove((item_body, item_shape))
                self.score += 1

    def post_to_x(self, text):
        """X（旧Twitter）に投稿画面を開く"""
        tweet_url = f"https://x.com/intent/post?text={text}"
        try:
            import js  # type: ignore # PyxelのWeb版では `js` モジュールが使える

            js.window.open(tweet_url, "_blank")
        except ImportError:
            import webbrowser

            webbrowser.open(tweet_url)

    def update(self):
        """ゲームの更新処理"""
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER):
            self.reset()
        if pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
            self.seed = random.randint(0, 100000)
            self.reset()
        for i in range(10):
            if pyxel.btnp(getattr(pyxel, f"KEY_{i}")) or pyxel.btnp(
                getattr(pyxel, f"KEY_KP_{i}")
            ):
                self.seed = 10 * self.seed + i if self.seed < 10000 else i
                self.reset()
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.body.apply_force_at_local_point((-self.move_power, 0))
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.body.apply_force_at_local_point((self.move_power, 0))

        # 地面または足場にいるときだけジャンプ
        jump_margin = 5  # 接触判定のマージン
        on_ground = self.body.position.y >= self.floor_y - self.radius - 1 - jump_margin
        for platform_body, _, width, _ in self.platforms:
            px, py = platform_body.position
            if (
                abs(self.body.position.x - px) < width / 2
                and abs(self.body.position.y - (py - self.radius - 1)) < jump_margin
            ):
                on_ground = True

        if on_ground and (
            pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)
        ):
            self.body.apply_impulse_at_local_point((0, -self.jump_power))

        # 物理計算の精度を上げる
        for _ in range(2):
            self.space.step(1 / 60)

        # すり抜けを防ぐ
        if self.body.position.y > self.floor_y:
            self.body.position.y = self.floor_y
            self.body.velocity = (self.body.velocity.x, 0)

        # アイテムとの衝突判定
        self.check_item_collision()

        # クリア時処理
        if (not self.cleared) and self.score >= self.item_num:
            self.cleared = True
            self.clear_time = (pyxel.frame_count - self.start_time) / FPS

        # クリア情報シェア
        if self.cleared and (
            pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)
        ):
            text = urllib.parse.quote(
                f"🎮 Jump Jump Bouncing Ball CLEAR!\n📌 Time: {self.clear_time:.2F} sec [Stage: {self.seed}]\nhttps://github.com/gomatama5/Jump_Jump_Bouncing_Ball\n#Pyxel #Pymunk"
            )
            self.post_to_x(text)

    def draw(self):
        """描画処理"""
        pyxel.cls(0)

        # 地面
        pyxel.rect(0, self.floor_y, 160, 20, 3)

        # 壁
        pyxel.rect(0, 0, 5, self.floor_y, 3)
        pyxel.rect(pyxel.width - 5, 0, 5, self.floor_y, 3)

        # アイテム
        for item_body, _ in self.items:
            x, y = int(item_body.position.x), int(item_body.position.y)
            pyxel.rect(x - 4, y - 4, 8, 8, 10)

        # 足場
        for platform_body, _, width, height in self.platforms:
            x, y = int(platform_body.position.x), int(platform_body.position.y)
            pyxel.rect(x - width // 2, y - height // 2, width, height, 3)

        # ボール
        pyxel.circ(int(self.body.position.x), int(self.body.position.y), self.radius, 9)

        # 操作方法表示
        pyxel.text(10, 5, f"[R]Restart [N]New Stage [0-9]Select", 7)

        # ステージ番号表示
        pyxel.text(100, 15, f"Stage: {self.seed}", 7)

        # タイム表示
        pyxel.text(
            10, 15, f"Time: {(pyxel.frame_count - self.start_time) / FPS:.2F}", 7
        )

        # クリア表示
        if self.cleared:
            pyxel.text(pyxel.width // 2 - 10, pyxel.height // 2 - 10, "CLEAR!", 10)
            pyxel.text(
                pyxel.width // 2 - 30,
                pyxel.height // 2,
                f"Time: {self.clear_time:.2F} sec",
                10,
            )
            pyxel.text(
                pyxel.width // 2 - 40,
                pyxel.height // 2 + 20,
                "Press S to Share on X",
                10,
            )


# ゲームの起動
Game()
