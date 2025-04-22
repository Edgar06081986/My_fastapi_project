from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
import boto3

from src.database import SessionDep
from src.api_v1.clients.cli_schemas import ClientsAddDTO
from typing import Optional
from src.models.models import ClientsOrm

from sqlalchemy import select
from src.api_v1.clients import crud_cli


app = FastAPI()

router = APIRouter(prefix="/clients", tags=["Clients"])


# 1. Создаём сессию с настройками доступа к Yandex Cloud
session = boto3.session.Session()

# 2. Создаём клиент для S3, указывая Yandex-эндпоинт
s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",  # Особенность Yandex Cloud
    aws_access_key_id="YOUR_ACCESS_KEY",  # Key ID из сервисного аккаунта
    aws_secret_access_key="YOUR_SECRET_KEY",
)  # Secret Key


@router.post("/", summary="add client")
async def add_client(
    username: str,
    email: str,
    session: SessionDep,  # Добавляем зависимость сессии
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
        s3.upload_fileobj(avatar.file, "app-3djewelers", file_key)
        avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"

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


@router.get("/", summary="Получить всех клиентов")
async def get_clients(session: SessionDep):
    query = select(ClientsOrm)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/", summary="Получить всех клиентов")
async def read_clients():
    clients = await crud_cli.convert_clients_to_dto()
    return clients




# @router.post("/add", ,summary="Добавить клиента")
# async def add_client(data: ClientsAddDTO,session:SessionDep,avatar: Optional[UploadFile] = File(None),
# ):
#     avatar_url = None
#
#     if avatar:
#         # Проверка типа файла
#         if not avatar.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#             raise HTTPException(400, "Only JPG/PNG images allowed")
#
#         # Загрузка в S3
#         file_key = f"avatars/{data.username}_{avatar.filename}"
#         s3.upload_fileobj(data.avatar.file, "app-3djewelers", file_key)
#         avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"
#         data.client_avatar_url=avatar_url
#
#     new_client=ClientsOrm(username=data.username,email=data.email,phone_number=data.phone_number)
#     session.add(new_client)
#     await session.commit()
#     return {"Клиент создан":True}
