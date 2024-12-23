from uuid import UUID
from fastapi import APIRouter, Depends, Body
from app import daos, schemas
from app.db import models


router = APIRouter()