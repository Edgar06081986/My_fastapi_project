from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Depends, status
import boto3
from src.config import yc_settings
import logging

# from src.database import SessionDep
from src.api_v1.clients.cli_schemas import ClientsAddDTO
from src.models.models import ClientsOrm
from src.models.db_helper import db_helper
from sqlalchemy import select
from src.api_v1.clients import crud_cli
from .deps_client import client_by_id
from .cli_schemas import *
from sqlalchemy.ext.asyncio import AsyncSession


# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clients", tags=["Clients"])


session = boto3.session.Session()

# 2. Создаём клиент для S3, указывая Yandex-эндпоинт
s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",  # Особенность Yandex Cloud
    aws_access_key_id=yc_settings.ACCESS_KEY,  # Key ID из сервисного аккаунта
    aws_secret_access_key=yc_settings.SECRET_KEY,  # Secret Key
)

BUCKET_NAME = "app-3djewelers"


@router.post("/", summary="Добавить клиента")
async def add_client(
    username: str,
    email: str,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # Добавляем зависимость сессии
    phone_number: Optional[str] = None,
    avatar: Optional[UploadFile] = File(None),
):
    avatar_url = None

    if avatar:
        # Проверка типа файла
        if not avatar.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(400, "Only JPG/PNG images allowed")

        # Загрузка в S3
        file_key = f"avatars/{username}_{avatar.filename}"
        s3.upload_fileobj(avatar.file, f"{BUCKET_NAME}", file_key)
        avatar_url = f"https://storage.yandexcloud.net/{BUCKET_NAME}/{file_key}"

        # Создание DTO
        data = ClientsAddDTO(
            username=username,
            email=email,
            phone_number=phone_number,
            client_avatar_url=str(avatar_url),
        )

    # Преобразование в SQLAlchemy модель
    new_client = ClientsOrm(**data.model_dump())

    # Сохранение в БД (теперь с асинхронными вызовами)
    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)

    return {"message": "Client created successfully", "new_client": new_client}


# @router.post("/add", summary="Добавить клиента")
# async def add_client(data: ClientsAddDTO,session:SessionDep,avatar: Optional[UploadFile] = File(None),
# ):
#     avatar_url = None

#     if avatar:
#         # Проверка типа файла
#         if not avatar.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#             raise HTTPException(400, "Only JPG/PNG images allowed")

#         # Загрузка в S3
#         file_key = f"avatars/{data.username}_{avatar.filename}"
#         s3.upload_fileobj(data.avatar.file, "app-3djewelers", file_key)
#         avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"
#         data.client_avatar_url=avatar_url

#     new_client=ClientsOrm(username=data.username,email=data.email,phone_number=data.phone_number)
#     session.add(new_client)
#     await session.commit()
#     return {"Клиент создан":True}
# 1. Создаём сессию с настройками доступа к Yandex Cloud


# @router.get("/", summary="Получить всех клиентов")
# async def get_clients(session: SessionDep):
#     query = select(ClientsOrm)
#     result = await session.execute(query)
#     return result.scalars().all()


# @router.get("/", summary="Получить всех клиентов")
# async def read_clients():
#     clients = await crud_cli.convert_clients_to_dto()
#     return clients


@router.get("/", summary="Получить всех клиентов")
async def read_clients(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    clients = await crud_cli.get_clients(
        session=session,
    )
    return clients


@router.delete(
    "/{client_id}/", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить клиента"
)
async def delete_client(
    client: ClientsOrm = Depends(client_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    """Delete a client by ID."""
    try:
        await crud_cli.delete_client(session=session, client=client)
        logger.info(f"Client with ID {client.id} deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting client with ID {client.id}: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete client")
