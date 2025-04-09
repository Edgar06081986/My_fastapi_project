from setuptools import setup, find_packages

setup(
    name="src",          # Имя пакета
    version="0.1",              # Версия
    packages=find_packages(),   # Автоматически находит все пакеты
    install_requires=[          # Зависимости
        # "numpy>=1.20",       # Пример зависимости
    ],
)