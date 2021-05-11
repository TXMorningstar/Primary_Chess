# from ai import *
#
# tree = Tree()
# print("=================================拓展节点测试==================================")
# tree.expand(node())  # 1
# tree.expand(node())  # 2
# tree.expand(node(), "1")  # 11
# tree.expand(node(), "1")  # 12
# tree.expand(node(), "2")  # 21
# tree.expand(node(), "21")  # 211
# tree.expand(node(), "12") # 121
# tree.expand(node(), "121") # 1211
#
# print()
# print("=================================获取节点测试=================================")
#
# print("2:", tree.get_node("2", True))
# print("1:", tree.get_node("1", True))
# print("21:", tree.get_node("21"))
#
# print()
# print("=================================节点数据测试=================================")
#
# print("2:", tree.get_node("2").location)
# print("1:", tree.get_node("1").location)
# print("21:", tree.get_node("21").location)
#
# print()
# print("=================================搜索节点测试=================================")
#
# print("level:2")
# print(tree.get_node_by_level(2))
#
# print("level:4")
# print(tree.get_node_by_level(4))
#
# print()
# print("=================================节点删除测试=================================")
#
# print("删除节点21")
# tree.del_node("21")
# print(tree.tree)
#
# print("删除节点1")
# tree.del_node("1")
# print(tree.tree)
#
# print("删除根节点")
# tree.del_node("")
# print(tree.tree)