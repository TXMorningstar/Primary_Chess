# Primary chess
* 目录
  * [简介](#1)
  * [使用说明](#2)
  * [函数-类-方法](#3)
    * [cprint()](3.1)
    * [Board()](#3.2)
  * [版本规划](#4)
  * [测试](#5)

<h2 id="1">简介</h2>
Primary Chess 是一个基于蒙特利尔树搜索算法的深度学习象棋AI，
可以在对战中不断调整自身策略达到与真实棋手相匹敌的实力。  
Primary Chess 需要完成四个模式：  
1. 同台电脑对战
2. 局域网内多人对战
3. 玩家与AI对战
4. AI与AI对战




<h2 id="2">使用说明</h2>
运行`main.py`后，输入命令即可执行对应的功能。




<h2 id="3">类-方法</h2>

<h3 id="3.1">cprint()</h3>

`def cprint(msg: str, fg: str = "white", bg: str = "black", end: str = "\n")`  
打印一个带颜色的字符串到终端上，支持end参数  
使用范例：  
`cprint("hello,world", "red", "black", end="==========")`


<h3 id="3.2">Board()</h3>

Game类包含了操作棋盘和棋子的最底层的方法。  
其中有一些方法不建议从外部调用，这些方法会以`_`开头。  
1. `print_board(self, board: tuple)`  
   这个方法可以将棋盘**打印**到控制台上
   

2. `print_board_raw(self, board: tuple)`  
   这个方法可以将棋盘以数值的形式**打印**到控制台上
   

3. `get_ally_chess(self, king: int, board: tuple = None) -> tuple`  
   调用这个方法会**返回**某一阵营的所有友方棋子坐标




<h2 id="4">版本规划</h2>
v 0.1:  
完成Game类，包含:  
```游戏棋盘、棋子、操作棋子方法```  
  
v 0.2:  
完成最小游戏结构，包含:  
```指令控制：下棋  
交替落子  
自动胜负判定    
```

v 0.3:  
完成完整命令控制，包含:  
```开始新游戏  
投降  
反悔  
退出游戏  
```

v 0.4:  
完成基本的AI控制随机下棋  

v 0.5:  
完成玩家与AI的对战模式，包含:  
```游戏模式切换命令```

v 0.6:  
完善AI，使用Minimax Tree Search算法寻找解法  

v 0.7:  
优化AI，使用Monte Carole Rollout算法减少计算量  

v 0.8:  
完成深度学习，根据游戏结果调整权重

v 0.9:  
完成AI与AI对战自主学习  

v 0.10:  
完成局域网双人对战  

v. 1.0:  
修复bug，完善玩家命令，打包游戏