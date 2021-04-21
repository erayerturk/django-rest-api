import os

from ninja import NinjaAPI


from tayf_auth.api import router as auth_router
from backend.api import router as backend_router


secret = os.environ.get("SECRET_KEY")

api = NinjaAPI()

api.add_router('tayf_auth/', auth_router, tags=["authorization"])
api.add_router('b/', backend_router, tags=["backend"])
