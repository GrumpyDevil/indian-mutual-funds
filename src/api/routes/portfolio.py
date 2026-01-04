from fastapi import APIRouter, Depends
from ...services.portfolio_service import PortfolioService
from ...analyze_portfolio import MANUAL_MAPPING # Reuse existing mapping
import os

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

# Path to transactions file
TRANSACTIONS_FILE = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'

def get_portfolio_service():
    return PortfolioService(TRANSACTIONS_FILE, manual_mapping=MANUAL_MAPPING)

@router.get("/summary")
async def get_summary(service: PortfolioService = Depends(get_portfolio_service)):
    return service.get_portfolio_summary()

@router.get("/holdings")
async def get_holdings(service: PortfolioService = Depends(get_portfolio_service)):
    res = service.get_portfolio_summary()
    return res.get("holdings", [])

@router.get("/sip-performance")
async def get_sip_performance(service: PortfolioService = Depends(get_portfolio_service)):
    return service.get_sip_performance()
