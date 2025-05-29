# My_fastapi_project
# для установки зависимости aiogram- откройте pyproject.toml и в секцию [project.dependencies] добавьте aiogram
# uv pip compile pyproject.toml -o requirements.lock
# uv pip sync requirements.lock - установка зависимости  из  requirements.lock
Это гарантирует, что в виртуальном окружении будут точно такие же версии, как в requirements.lock.