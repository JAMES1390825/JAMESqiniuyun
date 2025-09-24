# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base, get_db # get_db 现在从这里导入
from app import models, schemas, auth
from datetime import timedelta
from typing import List
import uuid

app = FastAPI()

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 在应用启动时创建默认角色
# 注意：这只会在表首次创建时运行，如果表已存在，不会重复创建角色
db = SessionLocal()
try:
    models.create_default_roles(db)
finally:
    db.close()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI Backend!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None, db: Session = Depends(get_db)):
    # 示例：现在你可以在这里使用 db 会话进行数据库操作
    # 例如：users = db.query(models.User).all()
    return {"item_id": item_id, "q": q}

# --- 用户认证相关的 API 路由 ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = auth.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    db_user_by_email = auth.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"username": user.username, "user_id": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

# --- 角色相关的 API 路由 ---

@app.post("/roles/", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    # 为了简化，这里暂时不验证用户权限，任何登录用户都可以创建角色
    # 在实际项目中，这里会添加逻辑来检查 current_user 是否是管理员
    db_role = models.Role(
        name=role.name,
        description=role.description,
        system_prompt=role.system_prompt,
        few_shot_examples=role.few_shot_examples,
        is_active=role.is_active
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@app.get("/roles/", response_model=List[schemas.RoleResponse])
def get_roles(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    # 同样，这里我们允许任何登录用户获取角色列表
    roles = db.query(models.Role).filter(models.Role.is_active == True).all()
    return roles

@app.get("/roles/{role_id}", response_model=schemas.RoleResponse)
def get_role(role_id: uuid.UUID, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    role = db.query(models.Role).filter(models.Role.id == role_id, models.Role.is_active == True).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found or inactive")
    return role

# ... (main.py 文件后面已有的 /users/me/ 接口) ...    