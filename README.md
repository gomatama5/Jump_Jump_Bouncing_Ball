# Jump_Jump_Bouncing_Ball
## Overview / 概要
物理演算ライブラリPymunkを使ったジャンプアクションゲームです。  
全てのアイテム（■）を取るまでのタイムを競います。  
ルールはシンプルですが、**操作が難しい高難度ゲームです**。
## Play Online / Web版URL
https://gomatama5.github.io/Jump_Jump_Bouncing_Ball/jjbb.html
## How to Play / 操作方法
Jump : A / Pad A / Pad X  
Move : Arrow Key / Pad Digital Arrow  
Restart : R / Pad LB  
New Stage : N / Pad RB  
Stage Select : 0-9 / NumPad 0-9  
Share(only after CLEAR) : S / Pad Start  
## Screenshots / スクリーンショット
![play movie](https://github.com/gomatama5/Jump_Jump_Bouncing_Ball/blob/main/screenshots/pyxel-20250224-155134.gif)
## Development History / 開発経緯
https://qiita.com/shiromofufactory/items/433f056ccc7c5bddc46f  
こちらの記事のPyxel先生を試しに使ってみたら、一応ゲームっぽいものが出来ました。
それを元に、まともに遊べそうな形に調整したのが上記のゲームです。
Pyxel先生が作ってくれたゲームっぽいもののオリジナルはこちらから遊べます。  
https://gomatama5.github.io/Jump_Jump_Bouncing_Ball/jjbb_ai.html  
Pyxel先生とのやり取りはこちら。  
https://chatgpt.com/share/67b8e799-36d8-8005-aae0-c3ef1941a296  
短いコードであればサクッと動くものを作ってくれるので、とても勉強になるなと思いました。
ただ、コードが長くなってくると、上手く動かなかったり勝手に機能が削られることもあって、その辺は仕方ないかなと思いました。

完成版を作るにあたっては、元々のパラメタだとクリアが難しすぎたのでクリア出来そうなくらいに調整しましたが、**元々の「操作が難しいアクション」という雰囲気はあえて残しました**。
また、元々はジャンプできない障害物もあったのですが、それを入れると流石にクリアが難しすぎたので、削除しました。
## Hints / ゲームのヒント
ジャンプボタンを押すタイミングが非常に重要です。
## Libraries / 使用したライブラリ
[Pyxel](https://github.com/kitao/pyxel)  
[Pymunk](http://www.pymunk.org/en/latest/)  
