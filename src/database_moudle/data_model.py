from peewee import *
import time
import os
from playhouse.shortcuts import model_to_dict , dict_to_model
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# if os.path.exists('./works.db'):
#     os.remove('./works.db')

db = SqliteDatabase(r'\\10.10.1.10\研发中心-人工智能部\项目文件\FT190019_广汽本田_发动机外壳检测\works.db')
# tmp_database_name = '{}.db'.format(time.time())
#连接数据库
db.connect()
# db_tmp.connect()


#项目总表的ORM类
class General_Table(Model):
    id = AutoField(column_name = 'ID',null = True) #内部数据id
    log = CharField(null = True) #数据创建日期
    project_number = CharField(null = True) #项目号
    project_name = CharField(null = True) #项目名称
    manager = CharField(null = True) #项目负责人
    label_manager = CharField(null = True) #标注负责人
    state = CharField(null = True) #数据状态(原始、未标注、已标注、训练)
    station = CharField(null = True) #工位
    Ai_model = CharField(null = True) #模型
    camera = CharField(null = True) #相机
    data_path = CharField(null = True) #数据路径
    tip = CharField(null = True) #备注

    class Meta:
        database = db


#创建存储数据的表
db.create_tables([General_Table])



#数据基本类，实现增改删查的功能
class DataBaseTool():

    def __init__(self):
        pass


    def format_commend(self,kwargs):
        commend = ""
        for attr , info in kwargs.items():
            single_commend = "(" + "General_Table." + attr  + "==" + "\"" + str(info) + "\"" + ")"
            commend += single_commend
            commend += " & "
        return commend[:-3]

    def get_total_count(self):  # 获取数据总数

        logger.info("TOTAL_COUNT")
        results = (General_Table
                   .select()
                   .count()
                   )  # 调用query语句进行查询，返回调用结果
        return results

    def insert(self , **kwargs ): #新增条例
        logger.info("INSERT：{}".format(kwargs))
        return General_Table.create(**kwargs)

    def insertmany(self , kwargs ): #新增多个条例
        logger.info("INSERT：{}".format(kwargs))
        with db.atomic():
            for batch in chunked(kwargs, 50):
                General_Table.insert_many(batch).execute()

    def update(self,id , kwargs): #更新条例
        # print(id, kwargs)
        logger.info("UPDATE：{}".format(kwargs))
        General_Table.update(kwargs).where(General_Table.id == id).execute()


    def delte(self,id): #删除条例
        General_Table.delete().where(General_Table.id == id).execute()
        logger.info("DELETE：{}".format(id))

    def search(self,attr,data): #单因素查询条例，返回二维列表
        logger.info("SEARCH：{}".format(attr + ":" + data ))
        result = []
        results =  (General_Table
        .select()
        .where( eval("General_Table." + attr) == data)) #调用query语句进行查询，返回调用结果
        for i in results:
            result.append([str(i.id),
                           i.project_number,
                           i.project_name,
                           i.manager,
                           i.state,
                           i.station,
                           i.Ai_model,
                           i.camera,
                           i.data_path,
                           i.tip]) #添加至数据类模型中
        return result

    def advance_search(self,kwargs): #高级查询条例,多条件查询，返回二维列表
        result = []
        commend = self.format_commend(kwargs)
        logger.info("ADVANCE_SEARCH：{}".format(commend))
        results =  (General_Table
        .select()
        .where( eval(commend))
        .order_by(General_Table.id)
        ) #调用query语句进行查询，返回调用结果
        for i in results:
            result.append([str(i.id),
                           i.project_number,
                           i.project_name,
                           i.manager,
                           i.label_manager,
                           i.state,
                           i.station,
                           i.Ai_model,
                           i.camera,
                           i.data_path,
                           i.tip]) #添加至数据类模型中
        print(result)
        return result

    def advance_search_count(self,kwargs): #高级查询条例,多条件查询，返回查询个数
        commend = self.format_commend(kwargs)
        logger.info("ADVANCE_SEARCH：{}".format(commend))
        results =  (General_Table
        .select()
        .where( eval(commend))
        .order_by(General_Table.id)
        .count()
        ) #调用query语句进行查询，返回调用结果
        return results

    def get_page_count(self, per_page = None):
        total_count = self.get_total_count()
        if total_count % per_page == 0:
            return (total_count % per_page)
        else:
            return (total_count % per_page + 1)

    def paginate_search(self,kwargs=None ,current_page = None, per_page = None):
        result = []
        if kwargs:
            commend = self.format_commend(kwargs)
            logger.info("PAGINATE_SEARCH：{}".format(commend))
            results =  (General_Table
            .select()
            .order_by(General_Table.id)
            .where( eval(commend))
            .paginate(current_page , per_page)
            ) #调用query语句进行查询，返回调用结果
            for i in results:
                result.append([str(i.id),
                               i.project_number,
                               i.project_name,
                               i.manager,
                               i.label_manager,
                               i.state,
                               i.station,
                               i.Ai_model,
                               i.camera,
                               i.data_path,
                               i.tip]) #添加至数据类模型中
        else:

            results =  (General_Table
            .select()
            .order_by(General_Table.id)
            .paginate(current_page,per_page)
            ) #调用query语句进行查询，返回调用结果
            for i in results:
                result.append([str(i.id),
                               i.project_number,
                               i.project_name,
                               i.manager,
                               i.label_manager,
                               i.state,
                               i.station,
                               i.Ai_model,
                               i.camera,
                               i.data_path,
                               i.tip]) #添加至数据类模型中
        # logger.info("PAGINATE_SEARCH：{}".format(result))
        return result




if __name__ == "__main__":
    from database_moudle.datajson import static_data,get_static_data
    static_data = get_static_data(static_data)
    worker = DataBaseTool()
    worker.insertmany(static_data)
    # a = worker.paginate_search(current_page = 1 , per_page = 10)
    # print(a,len(a))
    worker.update(25,{'标注负责人':'文冰'})






