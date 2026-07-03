from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Body


router = APIRouter(prefix='/promocodes', tags=['Промокоды'])

