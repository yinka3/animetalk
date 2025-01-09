import os
from datetime import datetime, timedelta
from typing import Optional, List

import fastapi
import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Response

app = FastAPI()