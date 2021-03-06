from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Initialize application
app = FastAPI()

# Initialize allowed origins for CORS middleware
origins = [
    "http://localhost:3000",
]

# Add CORS middleware to the application to allow
# the origins specified above to access the endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    """
    get_db: Generator for database session instances

    :returns: Session instances
    :rtype: sqlalchemy.orm.Session
    """
    # Generates session instances to allow communication with the database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Regular items endpoints

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Defines the GET /items/ endpoint that returns a list of all regular items

    :param skip: The skip-th item will be skipped
    :type skip: int
    :param limit: The maximum number of items returned from the GET request
    :type limit: int
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :returns: List of all regular items
    :rtype: list[schemas.Item]
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Defines the POST /items/ endpoint that creates a new item

    :param item: The Pydantic model representation of an item
    :type item: int
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :returns: The created item
    :rtype: schemas.Item
    """
    return crud.create_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Defines the PUT /items/ endpoint that updates an item

    :param item_id: The id of the item to be updated
    :type item_id: int
    :param item: The Pydantic model representation of an item
    :type item: int
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :returns: The created item
    :rtype: schemas.Item
    """
    try:
        updated_item = crud.update_item(db, item_id, item)
    except Exception as excp:
        raise HTTPException(status_code=404, detail=str(excp))

    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, comment: str = "", db: Session = Depends(get_db)):
    """
    Defines the DELETE /items/ endpoint that deletes an item

    :param item_id: The id of the item to be deleted
    :type item_id: int
    :param comment: The deletion comment
    :type comment: str
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :rtype: None
    """
    try:
        crud.delete_item_with_undelete(db, item_id, comment)
    except Exception as excp:
        raise HTTPException(status_code=404, detail=str(excp))

# Deleted items endpoints

# Read all deleted items
@app.get("/deleted/", response_model=list[schemas.DeletedItem])
def get_deleted_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Defines the GET /deleted/ endpoint that returns a list of all deleted items

    :param skip: The skip-th item will be skipped
    :type skip: int
    :param limit: The maximum number of items returned from the GET request
    :type limit: int
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :returns: List of all deleted items
    :rtype: list[schemas.DeletedItem]
    """
    deleted_items = crud.get_deleted_items(db, skip=skip, limit=limit)
    return deleted_items

# Undelete endpoint
@app.post("/deleted/{deleted_id}", response_model=schemas.Item)
def undelete(deleted_id: int, db: Session = Depends(get_db)):

    """
    Defines the POST /deleted/ endpoint that undeletes a deleted item

    :param deleted_id: The id of the deleted item to be undeleted 
    :type deleted_id: int
    :param db: The database connection session, autogenerated by get_db
    :type db: sqlalchemy.orm.Session

    :returns: The undeleted item, which is now a "regular" item
    :rtype: schemas.Item
    """

    cur_item = crud.get_deleted_item(db, deleted_id).first()

    if cur_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.undelete(db, deleted_id)
