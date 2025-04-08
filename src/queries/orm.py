from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from models import JewelersOrm, ClientsOrm, OrdersOrm, Workload
from database import Base, async_engine, async_session_factory


class AsyncORM:
    # Асинхронный вариант, не показанный в видео
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    @staticmethod
    async def insert_jewelers():
        async with async_session_factory() as session:
            worker_jack = JewelersOrm(username="Jack")
            worker_michael = JewelersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_jewelers():
        async with async_session_factory() as session:
            query = select(JewelersOrm)
            result = await session.execute(query)
            jewelers = result.scalars().all()
            print(f"{jewelers=}")

    @staticmethod
    async def update_jeweler(jeweler_id: int = 2, new_username: str = "Misha"):
        async with async_session_factory() as session:
            jeweler_michael = await session.get(JewelersOrm, jeweler_id)
            jeweler_michael.username = new_username
            await session.refresh(jeweler_michael)
            await session.commit()


    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    @staticmethod
    async def insert_clients():
        async with async_session_factory() as session:
            client_jack = ClientsOrm(username="Jack")
            client_michael = ClientsOrm(username="Michael")
            session.add_all([client_jack, client_michael])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_clients():
        async with async_session_factory() as session:
            query = select(ClientsOrm)
            result = await session.execute(query)
            clients = result.scalars().all()
            print(f"{clients=}")

    @staticmethod
    async def update_client(client_id: int = 2, new_username: str = "Misha"):
        async with async_session_factory() as session:
            client_michael = await session.get(ClientsOrm, client_id)
            client_michael.username = new_username
            await session.refresh(client_michael)
            await session.commit()

    @staticmethod
    async def insert_orders():
        async with async_session_factory() as session:
            order_jack_1 = OrdersOrm(
                title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, client_id=1)
            order_jack_2 = OrdersOrm(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, client_id=1)
            order_michael_1 = OrdersOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, client_id=2)
            order_michael_2 = OrdersOrm(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, client_id=2)
            session.add_all([order_jack_1, order_jack_2, 
                             order_michael_1, order_michael_2])
            await session.commit()

    # @staticmethod
    # async def select_resumes_avg_compensation(like_language: str = "Python"):
    #     """
    #     select workload, avg(compensation)::int as avg_compensation
    #     from resumes
    #     where title like '%Python%' and compensation > 40000
    #     group by workload
    #     having avg(compensation) > 70000
    #     """
        # async with async_session_factory() as session:
        #     query = (
        #         select(
        #             OrdersOrm.workload,
        #             # 1 вариант использования cast
        #             # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
        #             # 2 вариант использования cast (предпочтительный способ)
        #             func.avg(OrdersOrm.compensation).cast(Integer).label("avg_compensation"),
        #         )
        #         .select_from(OrdersOrm)
        #         .filter(and_(
        #             OrdersOrm.title.contains(like_language),
        #             OrdersOrm.compensation > 40000,
        #         ))
        #         .group_by(OrdersOrm.workload)
        #         .having(func.avg(OrdersOrm.compensation) > 70000)
        #     )
        #     print(query.compile(compile_kwargs={"literal_binds": True}))
        #     res = await session.execute(query)
        #     result = res.all()
        #     print(result[0].avg_compensation)

    # @staticmethod
    # async def insert_additional_resumes():
    #     async with async_session_factory() as session:
    #         jewelers = [
    #             {"username": """Эдгар"},  # id 3
    #             {"username": "Эдмон"},  # id 4
    #             {"username": "Petr"},   # id 5
    #         ]
    #         resumes = [
    #             {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
    #             {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
    #             {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
    #             {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
    #             {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
    #         ]
    #         insert_jewelers = insert(JewelersOrm).values("jewelers")
    #         insert_orders = insert(OrdersOrm).values("orders")
    #         await session.execute(insert_jewelers)
    #         await session.execute(insert_orders)
    #         await session.commit()

    # @staticmethod
    # async def join_cte_subquery_window_func():
    #     """
    #     WITH helper2 AS (
    #         SELECT *, compensation-avg_workload_compensation AS compensation_diff
    #         FROM 
    #         (SELECT
    #             w.id,
    #             w.username,
    #             r.compensation,
    #             r.workload,
    #             avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
    #         FROM resumes r
    #         JOIN workers w ON r.worker_id = w.id) helper1
    #     )
    #     SELECT * FROM helper2
    #     ORDER BY compensation_diff DESC;
    #     """
    #     async with async_session_factory() as session:
    #         r = aliased(ResumesOrm)
    #         w = aliased(WorkersOrm)
    #         subq = (
    #             select(
    #                 r,
    #                 w,
    #                 func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),
    #             )
    #             # .select_from(r)
    #             .join(r, r.worker_id == w.id).subquery("helper1")
    #         )
    #         cte = (
    #             select(
    #                 subq.c.worker_id,
    #                 subq.c.username,
    #                 subq.c.compensation,
    #                 subq.c.workload,
    #                 subq.c.avg_workload_compensation,
    #                 (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
    #             )
    #             .cte("helper2")
    #         )
    #         query = (
    #             select(cte)
    #             .order_by(cte.c.compensation_diff.desc())
    #         )

    #         res = await session.execute(query)
    #         result = res.all()
    #         print(f"{len(result)=}. {result=}")

    # @staticmethod
    # async def select_workers_with_lazy_relationship():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #         )
            
    #         res = await session.execute(query)
    #         result = res.scalars().all()

    #         # worker_1_resumes = result[0].resumes  # -> Приведет к ошибке
    #         # Нельзя использовать ленивую подгрузку в асинхронном варианте!

    #         # Ошибка: sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. 
    #         # Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
            

    # @staticmethod
    # async def select_workers_with_joined_relationship():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #             .options(joinedload(WorkersOrm.resumes))
    #         )
            
    #         res = await session.execute(query)
    #         result = res.unique().scalars().all()

    #         worker_1_resumes = result[0].resumes
    #         # print(worker_1_resumes)
            
    #         worker_2_resumes = result[1].resumes
    #         # print(worker_2_resumes)

    # @staticmethod
    # async def select_workers_with_selectin_relationship():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #             .options(selectinload(WorkersOrm.resumes))
    #         )
            
    #         res = await session.execute(query)
    #         result = res.scalars().all()

    #         worker_1_resumes = result[0].resumes
    #         # print(worker_1_resumes)
            
    #         worker_2_resumes = result[1].resumes
    #         # print(worker_2_resumes)

    # @staticmethod
    # async def select_workers_with_condition_relationship():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #             .options(selectinload(WorkersOrm.resumes_parttime))
    #         )

    #         res = await session.execute(query)
    #         result = res.scalars().all()
    #         print(result)

    # @staticmethod
    # async def select_workers_with_condition_relationship_contains_eager():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #             .join(WorkersOrm.resumes)
    #             .options(contains_eager(WorkersOrm.resumes))
    #             .filter(ResumesOrm.workload == 'parttime')
    #         )

    #         res = await session.execute(query)
    #         result = res.unique().scalars().all()
    #         print(result)

    # @staticmethod
    # async def select_workers_with_relationship_contains_eager_with_limit():
    #     # Горячо рекомендую ознакомиться: https://stackoverflow.com/a/72298903/22259413 
    #     async with async_session_factory() as session:
    #         subq = (
    #             select(ResumesOrm.id.label("parttime_resume_id"))
    #             .filter(ResumesOrm.worker_id == WorkersOrm.id)
    #             .order_by(WorkersOrm.id.desc())
    #             .limit(1)
    #             .scalar_subquery()
    #             .correlate(WorkersOrm)
    #         )

    #         query = (
    #             select(WorkersOrm)
    #             .join(ResumesOrm, ResumesOrm.id.in_(subq))
    #             .options(contains_eager(WorkersOrm.resumes))
    #         )

    #         res = await session.execute(query)
    #         result = res.unique().scalars().all()
    #         print(result)

    # @staticmethod
    # async def convert_workers_to_dto():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(WorkersOrm)
    #             .options(selectinload(WorkersOrm.resumes))
    #             .limit(2)
    #         )

    #         res = await session.execute(query)
    #         result_orm = res.scalars().all()
    #         print(f"{result_orm=}")
    #         result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
    #         print(f"{result_dto=}")
    #         return result_dto
        
    # @staticmethod
    # async def add_vacancies_and_replies():
    #     async with async_session_factory() as session:
    #         new_vacancy = VacanciesOrm(title="Python разработчик", compensation=100000)
    #         get_resume_1 = select(ResumesOrm).options(selectinload(ResumesOrm.vacancies_replied)).filter_by(id=1)
    #         get_resume_2 = select(ResumesOrm).options(selectinload(ResumesOrm.vacancies_replied)).filter_by(id=2)
    #         resume_1 = (await session.execute(get_resume_1)).scalar_one()
    #         resume_2 = (await session.execute(get_resume_2)).scalar_one()
    #         resume_1.vacancies_replied.append(new_vacancy)
    #         resume_2.vacancies_replied.append(new_vacancy)
    #         await session.commit()

    # @staticmethod
    # async def select_resumes_with_all_relationships():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(ResumesOrm)
    #             .options(joinedload(ResumesOrm.worker))
    #             .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title))
    #         )

    #         res = await session.execute(query)
    #         result_orm = res.unique().scalars().all()
    #         print(f"{result_orm=}")
    #         # Обратите внимание, что созданная в видео модель содержала лишний столбец compensation
    #         # И так как он есть в схеме ResumesRelVacanciesRepliedDTO, столбец compensation был вызван
    #         # Алхимией через ленивую загрузку. В асинхронном варианте это приводило к краху программы
    #         result_dto = [ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO.model_validate(row, from_attributes=True) for row in result_orm]
    #         print(f"{result_dto=}")
    #         return result_dto