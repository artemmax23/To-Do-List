from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
        "/", 
        response_model=list[schemas.TaskResponse],
        summary="Получить список задач"
)
async def read_tasks(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1, description="Номер страницы"),
        limit: int = Query(10, ge=1, le=100, description="Количество задач на странице"),
        is_completed: bool | None = Query(None, description="Фильтр по статусу выполнения"),
        tag_id : int | None = Query(None, description="Фильтр по ID тега"),
        search: str | None = Query(None, description="Поиск по названию или описанию") 
):
    offset = (page - 1) * limit
    
    return await crud.get_tasks(
                                db, 
                                skip=offset, 
                                limit=limit,
                                is_completed=is_completed,
                                tag_id=tag_id,
                                search=search
    )

@router.post(
        "/", 
        response_model=schemas.TaskResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Создать новую задачу"
)    
async def create_task(
        task: schemas.TaskCreate, 
        db: AsyncSession = Depends(get_db)
):
    if task.tag_id:
        tag = await crud.get_tag(db, task.tag_id)
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task.tag_id} not found"
            )
            
    return await crud.create_task(db, task)
    
@router.get(
        "/{task_id}",
        response_model=schemas.TaskResponse,
        summary="Получить задачу по ID"
)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(get_db)
):
    task = await crud.get_task(db, task_id)
    
    if not task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
        
    return task
    
@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Полное обновление задачи"    
)
async def update_task(
        task_id: int,
        task_data: schemas.TaskUpdate,
        db: AsyncSession = Depends(get_db)
):
    existing_task = await crud.get_task(db, task_id)
   
    if not existing_task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
    
    if task_data.tag_id:
        tag = await crud.get_tag(db, task_data.tag_id)
        
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task_data.tag_id} not found"
            )    
                
    return await crud.update_task(db, task_id, task_data)
    
@router.patch(
        "/{task_id}",
        response_model=schemas.TaskResponse,
        summary="Частично обновить задачу"
)
async def patch_task(
        task_id: int,
        task_data: schemas.TaskPatch,
        db: AsyncSession = Depends(get_db)
):
    existing_task = await crud.get_task(db, task_id)
    
    if not existing_task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
    
    if task_data.tag_id:
        tag = await crud.get_tag(db, task_data.tag_id)
        
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task_data.tag_id} not found"
            )
            
    return await crud.update_task(db, task_id, task_data.model_dump(exclude_unset=True))
    
@router.delete(
        "/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить задачу"
)
async def delete_task(
        task_id: int,
        db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_task(db, task_id)
    
    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
        
    return None