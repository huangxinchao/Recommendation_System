import  math
import  operator

'''
@:title  建立 item->user的倒排表
@:param  train格式  {user_id1:{item_id1:rating1,item_id2:rating2},user_id2:{item_id1:rating1,item_id2:rating2}}
@:return item_user 物品和用户的倒排表  {item1:(user1,user2),item2:{user2,user3}}
'''
def get_item_user(train):
    item_user = dict()
    for user_id,items in train.items():
        for item_id in items.keys():
            if item_user.get(item_id,-1) == -1:
                item_user[item_id] = set()
            item_user[item_id].add(user_id)
    return item_user

'''
@:title 获取用户相似度矩阵
@:param item_user 物品 -》 用户的倒排表 
@:return W 格式 {user1:{user2:0.9,user3:0.3}}
'''
def get_similiar_user(item_user):
    N = dict()  # 分母、两两用户购买物品的总数    {user1:11,user2:22}
    C = dict()  # 分子、两两用户间的共同购买物品  {user1:{user2:1,user3:4},user2:{user1:1,user4:55}}
    for item, users in item_user.items():
        for user in users:
            if N.get(user, -1) == -1:
                N[user] = 0
            N[user] += 1
            for other_user in users:
                if user == other_user:
                    continue
                if C.get(user, -1) == -1:
                    C[user] = dict()
                if C[user].get(other_user, -1) == -1:
                    C[user][other_user] = 0
                C[user][other_user] += 1

    W = dict()
    for user, item in C.items():
        for other_user, cnt in item.items():
            if W.get(user, -1) == -1:
                W[user] = dict()
            W[user][other_user] = cnt / math.sqrt(N[user] * N[other_user] * 1.0)
    return W


'''
@:tile 获取相似用户的购买物品 
@:param W 相似度矩阵，train 格式化原始数据
@:return recommandDict 推荐列表
'''
def recommand(W,train):
    recommandDict = dict()
    for user, val in W.items():
        for silimity_user in sorted(val.items(), key=operator.itemgetter(1), reverse=True)[:20]:
            if recommandDict.get(silimity_user, -1) == -1:
                recommandDict[user] = set()
            for item_id in train[user].keys():
                recommandDict[user].add(item_id)
    return recommandDict