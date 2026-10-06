from src.db.database import engine, Base
# ⚠️ IMPORTANT: You MUST import your model files here. 
# SQLAlchemy only creates tables for models it knows about.
# Change the line below to match your actual model file and class names!
# Example: from src.models.review import Review 

print("Connecting to Neon database and creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
