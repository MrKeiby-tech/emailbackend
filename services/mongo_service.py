import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
# connect global vars
from core.config import Config
from bson import ObjectId


class MongoService:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGO_DB]
        self.collection = self.db[Config.MONGO_COLLECTION]


    # получение шаблона по его id 
    async def find_themplate_by_id(self,id : int): 
        results = self.collection.find({"_id": ObjectId(id)})
        result = [] 
        async for result_data in results: 
            result_data["id"] = str(result_data["_id"])
            result.append(result_data)
            del(result_data["_id"])

        print(result)
        return result
    
    async def get_all_templates(self):
        """
        Возвращает список всех шаблонов из коллекции.
        Если коллекция пуста, возвращает пустой список.
        """
        templates = []

        # Асинхронный перебор документов в коллекции
        async for template in self.collection.find():
            template["id"] = str(template["_id"])  # Конвертация ObjectId в строку
            del template["_id"]  # Удаление _id
            templates.append(template)

        return templates  # Возвращаем список
    
    async def insert_template(self, template_data: dict):
        """
        Вставляет новый шаблон в коллекцию MongoDB.
        """
        # Дожидаемся выполнения асинхронной операции insert_one
        result = await self.collection.insert_one(template_data)
        return result
    
    async def update_template(self, template_data, id): 
        return await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": template_data}
        )

    
    async def delete_template(self, id):
        result = await self.collection.delete_one({"_id": ObjectId(id)}) 
        return result 
            



         
