# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session # 导入 Session
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL)

# 创建一个 SessionLocal 类
# 每次数据库操作时，我们都会创建一个 SessionLocal 实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个 Base 类，ORM 模型将继承自它
Base = declarative_base()

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()