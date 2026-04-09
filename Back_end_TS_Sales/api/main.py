from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utils.database import init_db

# Import all models to register them with SQLAlchemy
from api.models import (
    Staff, Customer, Product, PaymentTerm, Incoterm,
    Quotation, QuotationItem, ProformaInvoice,
    Contract, ContractItem, SaleOrder, ExportDocumentSet
)

# Import routers
from api.routers import customer_router, product_router, quotation_router, contract_router, sale_order_router

# Create FastAPI application
app = FastAPI(
    title="GC Food TS Sales API",
    description="Backend API for GC Food Trading System",
    version="1.0.0"
)

# ===== CORS Configuration =====
# Allow frontend to call API from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",          # Local development
        "http://localhost:3000",          # Alternative dev port
        "http://26.110.112.160:3001",     # VPN IP for remote dev
        "http://26.110.112.160:3000",     # VPN IP alternative
        "http://192.168.1.*",              # Local network
        # Allow all (WARNING: Only for development!)
        "*"
    ],
    allow_credentials=True,
    # Allow all HTTP methods (GET, POST, PUT, DELETE, PATCH)
    allow_methods=["*"],
    allow_headers=["*"],                   # Allow all headers
)

# ===== Event Handlers =====


@app.on_event("startup")
async def startup_event():
    """
    Initialize database when application starts.
    Creates all tables defined in models if they don't exist.
    """
    print("🚀 Initializing database...")
    init_db()
    print("✅ Database initialization complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when application shuts down."""
    print("🛑 Application shutting down...")

# ===== Health Check Endpoint =====


@app.get("/health", tags=["Health"])
async def health_check():
    """Check if API is running."""
    return {
        "status": "healthy",
        "message": "GC Food TS Sales API is running"
    }


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to GC Food TS Sales API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# ===== Import and Register Routers =====
# Register all API routers with their prefixes
app.include_router(customer_router.router, prefix="/api")
app.include_router(product_router.router, prefix="/api")
app.include_router(quotation_router.router, prefix="/api")
app.include_router(contract_router.router, prefix="/api")
app.include_router(sale_order_router.router, prefix="/api")

# ===== Error Handlers =====


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    return {
        "detail": str(exc),
        "error": "Internal server error",
        "status_code": 500
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",         # Listen on all network interfaces
        port=8000,              # Port to run on
        reload=True,            # Auto-reload on file changes (dev mode)
        log_level="info"
    )
