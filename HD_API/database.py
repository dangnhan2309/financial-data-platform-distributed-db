from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Cấu hình thông tin kết nối
DB_USER = "hq_owner"
DB_PASSWORD = "Nhan0944906711#"
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE = "HQ_SITE" # Hoặc tên Service Name của bạn

# URL kết nối cho Oracle sử dụng oracledb
# Định dạng: oracle+oracledb://user:pass@host:port/?service_name=xxx
SQLALCHEMY_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# 2. Tạo Engine
# Chế độ 'thick_mode=False' là mặc định trong oracledb (Thin Mode)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True, # Log các câu lệnh SQL ra terminal (hữu ích khi debug)
    pool_pre_ping=True # Tự động kiểm tra kết nối còn sống hay không
)

# 3. Tạo SessionLocal
# Mỗi instance của SessionLocal sẽ là một database session thực tế
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tạo Base class
# Các Model (Table) sau này sẽ kế thừa từ class này
Base = declarative_base()

# 5. Dependency: get_db
# Hàm này dùng để inject vào các Route của FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()