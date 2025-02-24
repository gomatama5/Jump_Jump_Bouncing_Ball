import pyxel
import pymunk

pyxel.init(160, 120)

space = pymunk.Space()
space.gravity = (0, 200)

body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 5))
body.position = (80, 50)
shape = pymunk.Circle(body, 5)
shape.elasticity = 0.8
space.add(body, shape)

# 地面
floor = pymunk.Segment(space.static_body, (0, 100), (160, 100), 1)
floor.elasticity = 0.6
floor.friction = 0.5
space.add(floor)

# 左の壁
left_wall = pymunk.Segment(space.static_body, (5, 0), (5, 100), 1)
left_wall.elasticity = 0.8
space.add(left_wall)

# 右の壁
right_wall = pymunk.Segment(space.static_body, (155, 0), (155, 100), 1)
right_wall.elasticity = 0.8
space.add(right_wall)

# アイテムリスト
items = []
score = 0  # アイテム取得数（スコア）


def create_item(x, y):
    """アイテム（STATICボディ）を作成"""
    item_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    item_body.position = (x, y)
    item_shape = pymunk.Poly.create_box(item_body, (8, 8))  # 8x8の四角
    item_shape.sensor = True  # センサーにして、衝突しても影響を与えない
    space.add(item_body, item_shape)
    items.append((item_body, item_shape))


# アイテムを配置
create_item(80, 60)
create_item(40, 40)
create_item(120, 30)

# 障害物リスト
obstacles = []


def create_obstacle(x, y, width, height):
    """障害物（STATICボディ）を作成"""
    obstacle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    obstacle_body.position = (x, y)
    obstacle_shape = pymunk.Poly.create_box(obstacle_body, (width, height))
    obstacle_shape.elasticity = 0.5  # ある程度跳ね返るようにする
    space.add(obstacle_body, obstacle_shape)
    obstacles.append((obstacle_body, obstacle_shape, width, height))


# 障害物を配置
create_obstacle(60, 50, 30, 5)
create_obstacle(100, 70, 40, 5)
create_obstacle(80, 30, 50, 5)

# 足場（ジャンプ可能ブロック）リスト
platforms = []


def create_platform(x, y, width, height):
    """足場（STATICボディ）を作成"""
    platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    platform_body.position = (x, y)
    platform_shape = pymunk.Poly.create_box(platform_body, (width, height))
    platform_shape.elasticity = 0.0  # 跳ね返らず、その上に立てる
    space.add(platform_body, platform_shape)
    platforms.append((platform_body, platform_shape, width, height))


# 足場を配置
create_platform(50, 80, 40, 5)
create_platform(110, 60, 40, 5)


def update():
    global score

    if pyxel.btn(pyxel.KEY_LEFT):
        body.apply_force_at_local_point((-100, 0))  # 左に力を加える
    if pyxel.btn(pyxel.KEY_RIGHT):
        body.apply_force_at_local_point((100, 0))  # 右に力を加える

    # 地面または足場にいるときだけジャンプ
    on_ground = body.position.y >= 90  # 地面
    for platform_body, _, width, _ in platforms:
        px = platform_body.position.x
        py = platform_body.position.y
        if (
            abs(body.position.x - px) < width / 2
            and abs(body.position.y - (py - 6)) < 2
        ):
            on_ground = True  # 足場の上にいると判定

    if pyxel.btnp(pyxel.KEY_SPACE) and on_ground:
        body.apply_impulse_at_local_point((0, -100))

    # 物理計算の精度を上げる
    for _ in range(2):
        space.step(1 / 60)

    # すり抜けを防ぐ
    if body.position.y > 100:
        body.position.y = 100
        body.velocity = (body.velocity.x, 0)

    # アイテムとの衝突判定（距離でチェック）
    global items
    new_items = []
    for item_body, item_shape in items:
        item_x, item_y = item_body.position
        dist = (
            (body.position.x - item_x) ** 2 + (body.position.y - item_y) ** 2
        ) ** 0.5
        if dist > 8:
            new_items.append((item_body, item_shape))
        else:
            space.remove(item_body, item_shape)
            score += 1

    items = new_items


def draw():
    pyxel.cls(0)

    # 地面
    pyxel.rect(0, 100, 160, 20, 3)

    # 壁
    pyxel.rect(0, 0, 5, 100, 3)
    pyxel.rect(155, 0, 5, 100, 3)

    # アイテム
    for item_body, _ in items:
        x, y = int(item_body.position.x), int(item_body.position.y)
        pyxel.rect(x - 4, y - 4, 8, 8, 10)

    # 障害物
    for obstacle_body, _, width, height in obstacles:
        x, y = int(obstacle_body.position.x), int(obstacle_body.position.y)
        pyxel.rect(x - width // 2, y - height // 2, width, height, 8)

    # 足場
    for platform_body, _, width, height in platforms:
        x, y = int(platform_body.position.x), int(platform_body.position.y)
        pyxel.rect(x - width // 2, y - height // 2, width, height, 11)  # 色11（黄色）

    # ボール
    pyxel.circ(int(body.position.x), int(body.position.y), 5, 9)

    # Y座標を表示
    pyxel.text(10, 10, f"Y: {int(body.position.y)}", 7)

    # スコアを画面上部に表示
    pyxel.text(120, 10, f"Score: {score}", 7)


pyxel.run(update, draw)
