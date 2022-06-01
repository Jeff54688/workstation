#!/usr/bin/python  
# -*- coding: utf-8 -*-  
 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import unittest
 
# HOSTNAME = "192.168.1.223"
# PORT = "33061"
# DATABASE = "mysql"
# USERNAME = "root"
# PASSWORD = "Wangjinfu123."
 
# DB_URI = "mysql+mysqldb://{username}:{password}@{host}:{port}/{db}?charset=utf8".\
#     format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)
 
#连接数据库
connect = create_engine('mysql+mysqlconnector://root:Wangjinfu123.@192.168.1.223:33061/mysql?auth_plugin=mysql_native_password')
 
#生成ORM基类
Base = declarative_base()  
#生成数据库表模型
class User(Base):
    __tablename__ = "user_login_table"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))
 
#创建表结构	
def creat_table():
    Base.metadata.create_all(connect)  

#删除表结构
def rm_table():
    Base.metadata.drop_all(connect)
 
def creat_session():
    #创建与数据库的会话session class ,这里返回给session的是class
    session_class = sessionmaker(bind=connect)  
    #生成session实例
    return session_class()    
 
#增加数据
def orm_insert(name_value, password_value):
	obj = User(name = name_value, password = password_value)  #生成数据对象
	session.add(obj) #把要创建的数据对象添加到session里
	session.commit() #创建数据
 
#查询数据，查不到情况下异常处理
def orm_password_query(name_key):
    try:
        ret = session.query(User).filter_by(name = name_key).first().password
    except AttributeError:
        print '\n********************'
        return 1
    else:        
        return ret
    finally:
        print '\n================='
 
#删除一条数据		
def orm_delete_by_name(name_key):
    session.query(User).filter(User.name == name_key).delete() 
    session.commit() 
 
#修改密码
def orm_modify_by_name(name_key, password_modify):
    session.query(User).filter(User.name == name_key).update({User.password: password_modify}, synchronize_session=False)
    session.commit() 
	
# class MysqlOperationTest(unittest.TestCase):
#     """Test mathfuc.py"""
#     def test_orm_insert(self):
#         """Test method orm_insert(a, b)"""
#         orm_insert("34443", "44rfdfd")
#         password = orm_password_query("34443")
#         self.assertEqual("44rfdfd", password)
 
#     def test_orm_delete(self):
#         orm_delete_by_name("34443")
#         password = orm_password_query("34443")
#         self.assertEqual(1, password)
		
#     def test_orm_modify(self):
#         orm_insert("34443", "44rfdfd")
#         orm_modify_by_name("34443", "fdsdsds")
#         password = orm_password_query("34443")
#         self.assertEqual("fdsdsds", password)
 
#     def test_orm_query(self):
#         #其实增删改操作已测试了查询,此处用例完整性
#         orm_insert("ff444", "44rfdfd")
#         password = orm_password_query("ff444")
#         self.assertEqual("44rfdfd", password)
 
if __name__ == '__main__':
    # rm_table()
    # creat_table() 
    session = creat_session()
    # orm_insert("34443", "44rfdfd")
    orm_password_query("34443")    #print输出
 
    # suite = unittest.TestSuite()
    # suite.addTest(MysqlOperationTest("test_orm_insert"))
    # suite.addTest(MysqlOperationTest("test_orm_delete"))
    # suite.addTest(MysqlOperationTest("test_orm_modify"))
    # suite.addTest(MysqlOperationTest("test_orm_query"))
    # runner = unittest.TextTestRunner(verbosity=1)
    # runner.run(suite)
	
	
	
	