import pandas as pd

data = pd.read_excel('./demo.xlsx', sheet_name=0, header=0)
# 查找指定列的数据
print(data['得分'])
# .values获取DataFrame原始数据
# print(data.values)
# 显示全部列名
print(data.columns)
# 显示索引
print(data.index)
# 查看行列数
print(data.shape)
# 修改列名
# inplace=False就地修改原数据/返回一个新数据
newdata = data.rename(columns={'分类': 'level'}, inplace=False)
# print(newdata)

# 统计元素
print(data['备注'].value_counts())
print(data['分类'].value_counts())

# 将指定列转成列表数据
# print(data['得分'].tolist())

# 查找筛选
print(data.query("项目 != 'A' "))

print(data[data['得分'] == 78])

# for col in data.columns:
#     series = data[col]
#     print(series)
#     print('--------')
