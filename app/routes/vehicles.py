from fastapi import APIRouter
from ..services.data_service import get_vehicle_data

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/")
def get_vehicles():
    
    data = get_vehicle_data()
    return data
