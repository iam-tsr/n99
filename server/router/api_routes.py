from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from server.model.core.showg_spider import movies_showing
from server.model.core.avail_spider import avail_movies

from datetime import datetime

from loguru import logger

router = APIRouter()

# API endpoints