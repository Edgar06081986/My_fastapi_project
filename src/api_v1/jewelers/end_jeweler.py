from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.api_v1.jewelers.crud_jew import update_jeweler as crud_update_jeweler
from src.models.models import JewelersOrm
from src.api_v1.jewelers.jew_schemas import JewelersAddDTO, UpdateJewelersDTO
from .deps_jeweler import jeweler_by_id
import boto3
import logging
from src.models.db_helper import db_helper
from  src.models.models import Workload

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(
    prefix="/jewelers",
    tags=["Jewelers"],
)

# Initialize Yandex Cloud S3 client
session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
)
BUCKET_NAME = "app-3djewelers"


# ---------------------------
# Endpoint: Add a new jeweler
# ---------------------------
@router.post("/", summary="Добавить ювелира")
async def add_jeweler(
    username: str,
    email: str,
    workload: str,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # No default value
    phone_number: str = None,
    address: str = None,
    avatar: UploadFile = File(None),
):
    """Add a new jeweler to the database."""
    avatar_url = None

    if avatar:
        # Validate file type
        if not avatar.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(
                status_code=400, detail="Only JPG/PNG images are allowed"
            )

        # Upload avatar to S3
        try:
            file_key = f"avatars/{username}_{avatar.filename}"
            s3.upload_fileobj(avatar.file, BUCKET_NAME, file_key)
            avatar_url = f"https://storage.yandexcloud.net/{BUCKET_NAME}/{file_key}"
        except Exception as e:
            logger.error(f"Error uploading avatar to S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload avatar")

    # Create DTO for the new jeweler
    data = JewelersAddDTO(
        username=username,
        email=email,
        phone_number=phone_number,
        address=address,
        workload=workload,
        jeweler_avatar_url=avatar_url,
    )

    # Convert DTO to SQLAlchemy model and save to the database
    try:
        new_jeweler = JewelersOrm(**data.model_dump())
        session.add(new_jeweler)
        await session.commit()
        await session.refresh(new_jeweler)
        return {"message": "Jeweler created successfully", "new_jeweler": new_jeweler}
    except Exception as e:
        logger.error(f"Error adding jeweler: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to add jeweler")


# ---------------------------
# Endpoint: Get  all jewelers 
# ---------------------------

@router.get("/", summary="Получить всех ювелиров")
async def get_jewelers(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    query = select(JewelersOrm)
    result = await session.execute(query)
    return result.scalars().all()



# ---------------------------
# Endpoint: Get jeweler by ID
# ---------------------------
@router.get("/{jeweler_id}/", summary="Получить ювелира по ID")
async def get_jeweler(
    jeweler_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get a jeweler by ID."""
    try:
        query = select(JewelersOrm).where(JewelersOrm.id == jeweler_id)
        result = await session.execute(query)
        jeweler = result.scalars().first()

        if not jeweler:
            raise HTTPException(status_code=404, detail="Jeweler not found")

        return jeweler
    except Exception as e:
        logger.error(f"Error fetching jeweler: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch jeweler")


# ---------------------------
# Endpoint: Update jeweler by ID
# ---------------------------
@router.put("/{jeweler_id}/", summary="Обновить ювелира по ID")
async def update_jeweler(
    jeweler_update: UpdateJewelersDTO,
    jeweler: JewelersOrm = Depends(jeweler_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # No default value
):
    """Update a jeweler's details."""
    try:
        updated_jeweler = await crud_update_jeweler(
            session=session,
            jeweler=jeweler,
            jeweler_update=jeweler_update,
        )
        return {
            "message": "Jeweler updated successfully",
            "updated_jeweler": updated_jeweler,
        }
    except Exception as e:
        logger.error(f"Error updating jeweler: {e}")
        raise HTTPException(status_code=500, detail="Failed to update jeweler")


# ---------------------------
# Endpoint: Delete jeweler by ID
# ---------------------------
@router.delete(
    "/{jeweler_id}/", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить ювелира"
)
async def delete_jeweler(
    jeweler_id: int,
    jeweler: JewelersOrm = Depends(jeweler_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),
):
    """Delete a jeweler by ID."""
    try:
        await session.delete(jeweler)
        await session.commit()
    except Exception as e:
        logger.error(f"Error deleting jeweler: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete jeweler")


# @router.post("/setup/", summary="Установка базы")
# async def setup_database():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     return {"ok": True}


# @router.post("/", summary=" Добавить ювелира")
# async def add_jeweler(data: JewelersAddDTO, session: SessionDep):
#     # add_jew = await  AsyncORM.insert_jewelers(username=data.username,workload=data.workload,address=data.address,email=data.email,phone_number=data.phone_number,jeweler_avatar=data.jeweler_avatar)
#     # return {"ok":True}
#     new_jeweler = JewelersOrm(
#         username=data.username,
#         workload=data.workload,
#         address=data.address,
#         email=data.email,
#         phone_number=data.phone_number,
#     )
#     session.add(new_jeweler)
#     await session.commit()
#     return {"ok": True}


# # 1. Создаём сессию с настройками доступа к Yandex Cloud
# session = boto3.session.Session()

# # 2. Создаём клиент для S3, указывая Yandex-эндпоинт
# s3 = session.client(
#     service_name="s3",
#     endpoint_url="https://storage.yandexcloud.net",  # Особенность Yandex Cloud
#     aws_access_key_id=yc_settings.ACCESS_KEY,  # Key ID из сервисного аккаунта
#     aws_secret_access_key=yc_settings.SECRET_KEY,  # Secret Key
# )

# BUCKET_NAME = "app-3djewelers"


# @router.post("/", summary="Добавить ювелира")
# async def add_jeweler(
#     username: str,
#     email: str,
#     workload: str,
#     session: SessionDep,  # Добавляем зависимость сессии
#     phone_number: Optional[str] = None,
#     address: Optional[str] = None,
#     avatar: Optional[UploadFile] = File(None),
# ):
#     avatar_url = None

#     if avatar:
#         # Проверка типа файла
#         if not avatar.filename.lower().endswith((".jpg", ".jpeg", ".png")):
#             raise HTTPException(400, "Only JPG/PNG images allowed")

#         # Загрузка в S3
#         file_key = f"avatars/{username}_{avatar.filename}"
#         s3.upload_fileobj(avatar.file, "app-3djewelers", file_key)
#         avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"

#         # Создание DTO
#         data = JewelersAddDTO(
#             username=username,
#             email=email,
#             phone_number=phone_number,
#             address=address,
#             workload=workload,
#             jeweler_avatar_url=str(avatar_url),
#         )

#     # Преобразование в SQLAlchemy модель
#     new_jeweler = JewelersOrm(**data.model_dump())

#     # Сохранение в БД (теперь с асинхронными вызовами)
#     session.add(new_jeweler)
#     await session.commit()
#     await session.refresh(new_jeweler)

#     return {"message": "Jeweler created successfully", "new_jeweler": new_jeweler}


# @router.get("/{jeweler_id}/")
# async def get_jeweler(jeweler_id:int=Depends(jeweler_by_id)):
#     return jeweler_id



#


# @router.put("/{jeweler_id}/", summary="Изменить ювелира по ID")
# async def change_jeweler(jeweler_id: int, new_name: str, session: SessionDep):
#     # Ищем ювелира в базе данных по ID
#     query = select(JewelersOrm).where(JewelersOrm.id == jeweler_id)
#     result = await session.execute(query)
#     jeweler = result.scalars().first()
#     result = crud_jew.update_jeweler(jeweler_id=jeweler_id, new_name=new_name)
#     # Если ювелир не найден - возвращаем 404 ошибку
#     if not jeweler:
#         raise HTTPException(status_code=404, detail="Ювелир не найден")
#     return jeweler

#
# @router.get("/", summary="get all jewelers")
# async def read_jewelers():
#     result = await crud_jew.convert_jewelers_to_dto()
#     return result

#
# @router.get("/{jeweler_id}", summary="get one jeweler")
# async def get_jeweler(
#     jeweler_id: int, session: SessionDep
# ):  # ← Указываем тип (int, str, UUID и т.д.)
#
#     # return {"jeweler_id": jeweler_id}
#     pass


# @router.delete(
#     "/{jeweler_id}/", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить ювелира"
# )
# async def delete_jeweler(
#     jeweler_id: int = (jeweler_by_id),
#     jeweler: JewelersOrm = Depends(jeweler_by_id),
#     session: SessionDep = Depends(db_helper.scoped_session_dependency),
# ):
#     await crud_jew.delete_jeweler(session=session, jeweler=jeweler)
