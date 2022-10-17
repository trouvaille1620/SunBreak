#peewee后台数据库
"""
模型类 数据库表
字段实例 表上的列
模型实例 数据库表中的行

"""

#peewee自动从类的名称推断数据库表名
from peewee import *
from datetime import date
import os

if os.path.exists('./works.db'):
    os.remove('./works.db')

db = SqliteDatabase('works.db')

class Project(Model):
    name = CharField()
    member = DateField()

    class Meta:
        database = db

class Member(Model):
    owner = ForeignKeyField(Project , backref='members')
    name = CharField()
    position = CharField()

    class Meta:
        database = db

#连接数据库
db.connect()

#创建存储数据的表
db.create_tables([Project,Member])

#存储数据
work1 = Project(name='广汽本田' , member = date(2022,8,8))
work1.save() #调用save，返回修改的行数

#也可以通过create()方法，返回模型实例
work2 = Project.create(name='比亚迪' , member = date(2022,8,8))
work3 = Project.create(name='大众' , member = date(2022,10,10))
work4 = Project.create(name='缸体' , member = date(2022,12,12))

#更新行，修改实例并调用save()方法
# work1.name = 'byd'
# work1.save()

#调用关联进行数据添加
ywz  = Member.create(owner = work1 , name = 'ywz',position = 'Ai')
hj = Member.create(owner = work2 , name = 'hj',position = 'Ai')
zmh = Member.create(owner = work3 , name = 'zmh',position = 'label')

#数据库获取单个记录
# gqbt_data = Project.select().where(Project.name == 'gqbt').get()
# print(gqbt_data)

#等价速记法
# gqbt_data = Project.get(Project.name == 'gqbt')
# print(gqbt_data)

#列出数据库所有信息
# for works in Project.select():
#     print('项目：{}'.format(works.name))

#查询指定的符合条件的一些数据
# members = Member.select().where(Member.position== 'Ai')
# for member in members:
#     print('算法工程师：{} , 负责项目：{}'.format(member.name, member.owner.name))

#也可以使用join语句,避免额外的查询
# members = (Member
#          .select(Member , Project)
#          .join(Project)
#          .where(Member.position== 'Ai'))
# for member in members:
#     print('算法工程师：{} , 负责项目：{}'.format(member.name, member.owner.name))

#也可以这么写：
# for member in Member.select().join(Project).where(Project.name == '广汽本田'):
#     print(member.name)

#分选：使用order_by进行筛选排序
# for works in Project.select().order_by(Project.member.desc()):
#     print(works.name , works.member)

#使用组合筛选器表达式
date1 = date(2022,8,1)
date2 = date(2022,12,1)
query = (Project
        .select()
         .where( (Project.member < date1) |  (Project.member > date2 ))
)
for member in query:
    print(member.name , member.member)

