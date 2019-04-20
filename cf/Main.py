
import pandas as pd
import BaseSimilarUser as bsu

'''
1、获取相似用户矩阵
      1.1、根据购买物品的交集    交集数目/(sqrt(user1)*sqrt(user2))
2、获取相似用户的购买物品

'''


udata = pd.read_csv('./resources/u.data',sep='\t',header=None,names=['user_id','item_id','rating','timestamp'])

#1 格式化数据 {user_id1:{item_id1:rating1,item_id2:rating2},user_id2:{item_id1:rating1,item_id2:rating2}}
train = dict()
for _,row in udata.iterrows():
    user_id = row['user_id']
    item_id = row['item_id']
    rating = row['rating']
    if train.get(user_id,-1) == -1:
        train[user_id] = dict()
    train[user_id][item_id] = rating

# print(train)
item_user = bsu.get_item_user(train)
W = bsu.get_similiar_user(item_user)
recommandDict = bsu.recommand(W,train)

i = 0
for key,val in recommandDict.items():
    i += 1
    if i == 20:
        break
    print(key,val)