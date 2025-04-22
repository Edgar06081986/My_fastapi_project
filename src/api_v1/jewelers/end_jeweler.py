from fastapi import APIRouter, HTTPException, UploadFile, File,status,Depends
from src.api_v1.jewelers.crud_jew import *
from src.database import SessionDep, async_engine
from src.api_v1.jewelers import crud_jew
from src.api_v1.jewelers.crud_jew import *
from src.models.base import *
from src.config import yc_settings
import boto3
from src.api_v1.jewelers.jew_schemas import JewelersAddDTO
from .deps_jeweler import jeweler_by_id
from src.models.db_helper import db_helper

router = APIRouter(
    prefix="/jewelers",
    tags=["Jewelers"],
)

#
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


# 1. Создаём сессию с настройками доступа к Yandex Cloud
session = boto3.session.Session()

# 2. Создаём клиент для S3, указывая Yandex-эндпоинт
s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",  # Особенность Yandex Cloud
    aws_access_key_id=yc_settings.ACCESS_KEY,  # Key ID из сервисного аккаунта
    aws_secret_access_key=yc_settings.SECRET_KEY,  # Secret Key
)

BUCKET_NAME = "app-3djewelers"


@router.post("/", summary="Добавить ювелира")
async def add_jeweler(
    username: str,
    email: str,
    workload: Workload,
    session: SessionDep,  # Добавляем зависимость сессии
    phone_number: Optional[str] = None,
    address: Optional[str] = None,
    avatar: Optional[UploadFile] = File(None),
):
    avatar_url = None

    if avatar:
        # Проверка типа файла
        if not avatar.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(400, "Only JPG/PNG images allowed")

        # Загрузка в S3
        file_key = f"avatars/{username}_{avatar.filename}"
        s3.upload_fileobj(avatar.file, "app-3djewelers", file_key)
        avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"

        # Создание DTO
        data = JewelersAddDTO(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            workload=workload,
            jeweler_avatar_url=str(avatar_url),
        )

    # Преобразование в SQLAlchemy модель
    new_jeweler = JewelersOrm(**data.model_dump())

    # Сохранение в БД (теперь с асинхронными вызовами)
    session.add(new_jeweler)
    await session.commit()
    await session.refresh(new_jeweler)

    return {"message": "Jeweler created successfully", "new_jeweler": new_jeweler}


@router.get("/", summary="Получить всех ювелиров")
async def get_jewelers(session: SessionDep):
    query = select(JewelersOrm)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{jeweler_id}/", summary="Получить ювелира по ID")
async def get_jeweler(jeweler_id: int, session: SessionDep):
    # Ищем ювелира в базе данных по ID
    query = select(JewelersOrm).where(JewelersOrm.id == jeweler_id)
    result = await session.execute(query)
    jeweler = result.scalars().first()
    return jeweler


@router.put("/{jeweler_id}/", summary="Изменить ювелира по ID")
async def change_jeweler(jeweler_id: int, new_name: str, session: SessionDep):
    # Ищем ювелира в базе данных по ID
    query = select(JewelersOrm).where(JewelersOrm.id == jeweler_id)
    result = await session.execute(query)
    jeweler = result.scalars().first()
    result = crud_jew.update_jeweler(jeweler_id=jeweler_id, new_name=new_name)
    # Если ювелир не найден - возвращаем 404 ошибку
    if not jeweler:
        raise HTTPException(status_code=404, detail="Ювелир не найден")
    return jeweler


@router.get("/", summary="get all jewelers")
async def read_jewelers():
    result = await crud_jew.convert_jewelers_to_dto()
    return result


@router.get("/{jeweler_id}", summary="get one jeweler")
async def get_jeweler(
    jeweler_id: int, session: SessionDep
):  # ← Указываем тип (int, str, UUID и т.д.)

    # return {"jeweler_id": jeweler_id}
    pass

@router.delete("/{jeweler_id}/", status_code=status.HTTP_204_NO_CONTENT,summary="Удалить ювелира")
async def delete_jeweler(jeweler:JewelersOrm=Depends(jeweler_by_id),
    session:SessionDep=Depends(db_helper.scoped_session_dependency))->None:
    await crud_jew.delete_jeweler(session=session,jeweler=jeweler)