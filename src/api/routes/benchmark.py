from fastapi import APIRouter, Depends
import pandas as pd
from ...services.benchmark_service import BenchmarkService
from ...data_manager import DataManager
import os

router = APIRouter(prefix="/benchmark", tags=["Benchmark"])

# Path to transactions file (for start date etc)
TRANSACTIONS_FILE = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
NIFTY_50_TICKER = "^NSEI"
NIFTY_TRI_SCHEME_CODE = "120716"

def get_benchmark_service():
    return BenchmarkService(DataManager())

@router.get("/compare")
async def compare_with_nifty(service: BenchmarkService = Depends(get_benchmark_service)):
    # Load transactions just to get the relevant dates
    df = pd.read_excel(TRANSACTIONS_FILE, sheet_name='Sheet1')
    df['Date'] = pd.to_datetime(df['Date'])
    
    return service.get_benchmark_comparison(df, NIFTY_50_TICKER, NIFTY_TRI_SCHEME_CODE)
