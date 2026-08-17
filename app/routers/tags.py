from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get(
        "/",
        response_model=list[schemas.TagResponse],
        summary="Получить список всех тегов"
)
async def read_tags(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1, description="Номер страницы"),
        limit: int = Query(10, ge=1, le=100, description="Количество тэгов на странице"),
):
    offset = (page - 1) * limit
  
    return await crud.get_tags(db, offset, limit)
    
@router.get(
        "/{tag_id}",
        response_model=schemas.TagResponse,
        summary="Получение тэга по id"
)  
async def get_tag(
        tag_id: int,
        db: AsyncSession = Depends(get_db)
):
    tag = await crud.get_tag(db, tag_id)
    
    if not tag:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
    
    return tag
    
@router.get(
        "/name/{tag_name}",
        response_model=list[schemas.TagResponse],
        summary="Поиск тэгов по названию"
)
async def get_tag_by_name(
        tag_name: str,
        db: AsyncSession=Depends(get_db)
):
    return await crud.get_tag_by_name(db, tag_name)

@router.post(
        "/",
        response_model=schemas.TagResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Создание тэга"
)
async def create_tag(
        tag: schemas.TagCreate,
        db: AsyncSession=Depends(get_db),
):
    return await crud.create_tag(db, tag)
    
@router.put(
        "/{tag_id}",
        response_model=schemas.TagResponse,
        summary="Обновление тэга"
)
async def update_tag(
        tag_id: int,
        tag: schemas.TagUpdate,
        db: AsyncSession=Depends(get_db)
):
    existing_tag = await crud.update_tag(db, tag_id, tag)
    
    if not existing_tag:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
        
    return existing_tag
    
@router.delete(
        "/{tag_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить тэг"
)
async def delete_tag(
        tag_id: int,
        db: AsyncSession=Depends(get_db)
):
    deleted = await crud.delete_tag(db, tag_id) 
    
    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
        
    return None