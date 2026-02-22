from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from apps.api.settings import settings 

# Base class for SQLAAlchemy models 
# All database models will inherit from this class
# It uses the DeclarativeBase from SQLAlchemy to enable the ORM features 
class Base(DeclarativeBase): 
    pass 

# Create the Database Engine 
# This is the connection point to your database 
# 'pool_pre_ping=True' ensures that the connection is alive before using it, which helps prevent "MySQL server has gone away" errors.
engine = create_engine(settings.database_url, pool_pre_ping=True) 

# Create a session factory 
# SessionLocal creates new dabatase session objects 
# autoflush=False prevents send changes to DB until explicitly committed, which can help with performance and control over transactions
# autocommit=False means that you have to explicitly commit transactions, which can help prevent accidental data loss
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency function to get a database session
# This funcction (generator) ensures each requests gets its own connection 
# Connection is closed after the request is done, preventing connection leaks and ensuring efficient use of database resources
def get_db():
    db = SessionLocal() 
    try: 
        yield db #This is where execution "pauses" while the route uses the DB 
    finally: 
        db.close() #Closing the connection, even if an error occured during the request handling, ensuring that connections are not left open unintentionally.