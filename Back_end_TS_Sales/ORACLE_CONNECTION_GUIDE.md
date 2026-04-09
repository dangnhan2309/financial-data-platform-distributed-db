# 🚀 Quick Start - Connect to Oracle GCFood_Project

Your Oracle configuration found:
- **Connection**: GCFood_Project
- **Database Type**: Oracle
- **Username**: gcf_user
- **Host**: localhost
- **Port**: 1521
- **Service**: project_db

---

## ✨ Everything is configured! Follow these 3 steps:

### Step 1: Install Dependencies (1 minute)

```bash
# Navigate to Back_end_TS_Sales folder
cd Back_end_TS_Sales

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM for database
- `python-oracledb` - Oracle client
- `python-dotenv` - Environment variables loader

---

### Step 2: Verify Connection (2 minutes)

```bash
# Test Oracle connection
python test_oracle_connection.py
```

**Expected output:**
```
✅ CONNECTION SUCCESSFUL!
✅ SESSION CREATED!
✅ QUERY EXECUTED!
✅ SESSION CLOSED!

🎉 ALL TESTS PASSED - Oracle is ready to use!
```

If connection fails, check:
1. Oracle service `project_db` is running
2. `.env` file exists with correct values
3. Password is correct (123456)

---

### Step 3: Start Backend Server (2 minutes)

```bash
# Start the API server
python run.py
```

**Expected output:**
```
✅ Database connection successful

🚀 Starting GC Food TS Sales API...
📍 API will run at: http://localhost:8000
📚 Swagger Docs: http://localhost:8000/docs
📖 ReDoc: http://localhost:8000/redoc

⏹️  Press Ctrl+C to stop the server
```

Server is now running! ✅

---

## 📚 Access API Documentation

When server is running, open in browser:

### **Interactive Testing (Swagger UI)**
```
http://localhost:8000/docs
```
- Try endpoints interactively
- See request/response formats
- Test with real data

### **API Documentation (ReDoc)**
```
http://localhost:8000/redoc
```
- Complete endpoint documentation
- See all available operations

### **Health Check**
```
http://localhost:8000/health
```
- Returns: `{"status": "healthy", "message": "..."}`

---

## 📁 What's Configured

✅ **`.env` file** - Oracle credentials loaded automatically
✅ **`api/utils/database.py`** - Oracle connection string ready
✅ **`api/dependencies/db.py`** - Database session injection ready
✅ **`api/main.py`** - FastAPI app with CORS (for frontend VPN connection)
✅ **`api/repositories/base_repository.py`** - Generic CRUD operations ready
✅ **`requirements.txt`** - All dependencies listed

---

## ⚙️ Environment File (.env)

Your `.env` file is already created with:

```env
# Database Configuration - GCFood_Project
DB_USER=gcf_user
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=project_db

# Optional: Enable SQL logging
SQL_ECHO=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

**If you need to change:**
1. Edit `.env` file
2. Restart `python run.py`

---

## 🔧 Troubleshooting

### "Cannot connect to database"
```bash
# 1. Check .env file exists
ls -la .env

# 2. Verify Oracle service is running
lsnrctl status

# 3. Try connecting with SQL*Plus
sqlplus gcf_user/123456@//localhost:1521/project_db

# 4. Check credentials in your SQL Developer connection
```

### "Module not found" error
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### "Port 8000 already in use"
Edit `run.py` and change:
```python
uvicorn.run(..., port=8001)  # Use 8001 instead
```

---

## 🎯 Next Steps - Create Your First Endpoint

Once server is running, on the next step we will:

1. Create Customer Model (10 lines)
2. Create Customer Router (API endpoints)
3. Test in Swagger UI
4. Connect to Frontend

**Result**: Full CRUD API for customers! ✨

---

## 📝 File Reference

| File | Purpose |
|------|---------|
| `.env` | Oracle credentials (loaded automatically) |
| `api/utils/database.py` | Oracle connection engine |
| `api/main.py` | FastAPI app with CORS |
| `api/repositories/base_repository.py` | Generic CRUD class |
| `run.py` | Server entry point |
| `test_oracle_connection.py` | Test connection script |
| `requirements.txt` | All Python dependencies |

---

## ✅ Verification Checklist

```
[ ] 1. Installed dependencies with: pip install -r requirements.txt
[ ] 2. Tested connection with: python test_oracle_connection.py
[ ] 3. Started server with: python run.py
[ ] 4. Accessed http://localhost:8000/health (got response)
[ ] 5. Accessed http://localhost:8000/docs (Swagger UI loaded)
```

---

## 🚀 Ready?

```bash
# Copy-paste sequence to get started:
cd Back_end_TS_Sales
pip install -r requirements.txt
python test_oracle_connection.py
python run.py
```

Then open: **http://localhost:8000/docs**

**That's it!** Your backend API is ready! 🎉

---

## 💬 For Frontend Connection

Frontend is at: `TS_Sales/frontend`
- Already configured for backend: http://26.110.112.160:8000
- Update if needed in: `.env.local`

Both frontend and backend now connected! ✨
