from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# 1. Cấu hình thông tin kết nối ORACLE (Theo chuẩn HQ_API)
# Lấy từ app.config.py
# SQLALCHEMY_DATABASE_URL = DATABASE_URL

# 2. Tạo Engine
# Chế độ 'thick_mode=False' là mặc định trong oracledb (Thin Mode)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log các câu lệnh SQL ra terminal (hữu ích khi debug)
    pool_pre_ping=True  # Tự động kiểm tra kết nối còn sống hay không
)

# 3. Tạo SessionLocal
# Mỗi instance của SessionLocal sẽ là một database session thực tế
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tạo Base class
# Các Model (Table) sau này sẽ kế thừa từ class này
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
