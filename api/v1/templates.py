from fastapi import APIRouter, HTTPException
from models.models import TemplateCreate, TemplateUpdate
from services.mongo_service import MongoService
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel


router = APIRouter()

mongo_client = MongoService()
@router.get("/")
async def get_templates():

    templates = await mongo_client.get_all_templates()
    if templates:
        return templates
    
    else:
        raise HTTPException(status_code=400, detail="Template list is empty")
    
@router.post("/")
async def create_template(template_data: TemplateCreate):
    """
    Создаёт новый шаблон.
    """
    # Проверка содержимого
    if not template_data.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty.")
    if not template_data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty.")
    
    # Подготовка данных для MongoDB
    template = {
        "name": template_data.name,
        "content": template_data.content,  # HTML-контент
        "stage": template_data.stage, 
        "type": template_data.type, 
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Вставка данных в MongoDB
    result = await mongo_client.insert_template(template)

    # Проверяем результат
    if not result:
        raise HTTPException(status_code=400, detail="Template not created")

    # Возвращаем ID нового шаблона
    return {"id": str(result.inserted_id)}


@router.get("/{template_id}")
async def get_template(template_id: str):
    """
    Возвращает шаблон по ID.
    """
    
    template = await mongo_client.find_themplate_by_id(template_id)

    if not template: 
        raise HTTPException(status_code=400, detail=f"Template with id {template_id} not found")

    return template

@router.put("/{template_id}")
async def update_template(template_id: str, template_data: TemplateUpdate):
    """
    Обновляет шаблон по ID.
    """
    update_data = {}

    if template_data.content: 
        update_data["content"] = template_data.content
    
    if template_data.name: 
        update_data["name"] = template_data.name

    if template_data.stage: 
        update_data["stage"] = template_data.stage

    if template_data.type: 
        update_data["type"] = template_data.type

    if update_data: 
        update_data["updated_at"] = datetime.utcnow()

    result = await mongo_client.update_template(update_data , template_id) 

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template updated", "updated_fields": update_data}

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """
    Удаляет шаблон по ID.
    """
    result = await mongo_client.delete_template(template_id)

    if result:
        print({
            "acknowledged": result.acknowledged,
            "deleted_count": result.deleted_count
        })

    if result.deleted_count != 1:
        return {"message": "No template found with the given ID."}

    return {"message": f"Template {template_id} deleted successfully."}