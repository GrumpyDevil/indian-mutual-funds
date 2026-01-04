# Indian Mutual Funds Portfolio Tracker

A comprehensive, full-stack portfolio analytics platform for Indian mutual fund investors. Track your investments, analyze performance, and compare against market benchmarks with beautiful visualizations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-19.2.0-blue.svg)

## ✨ Features

### 📊 Portfolio Analytics
- **Accurate XIRR Calculation**: Industry-standard returns calculation using `pyxirr`
- **Holdings Breakdown**: Detailed view of all your mutual fund investments
- **Real-time NAV Updates**: Automatic fetching of latest NAV data from AMFI
- **Profit/Loss Tracking**: Track absolute and percentage returns for each fund

### 📈 Benchmark Comparison
- **Nifty 50 & Nifty 50 TRI**: Compare your portfolio against market indices
- **Virtual SIP Simulation**: See how index investments would have performed
- **Alpha Calculation**: Measure your outperformance vs benchmarks

### 💰 SIP Performance Dashboard
- **Investment Trajectory**: Visualize wealth accumulation over time
- **Multi-line Charts**: Compare portfolio vs Nifty 50 (Price) vs Nifty 50 TRI
- **Outperformance Metrics**: See exactly how much you've beaten the market
- **Time-series Analysis**: Track performance across different time periods

### 📄 CAS PDF Parser
- **Multi-format Support**: Parse CAMS, KFintech, and NSDL CAS statements
- **Auto-detection**: Automatically identifies CAS provider
- **Encrypted PDF Support**: Handles password-protected statements (PAN + DOB)
- **Data Validation**: Ensures mathematical consistency of parsed data

### 🎨 Premium UI/UX
- **Modern Dark Theme**: Beautiful, eye-friendly interface
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Interactive Charts**: Powered by Recharts with smooth animations
- **Tab Navigation**: Easy switching between Overview and SIP Performance views

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/GrumpyDevil/indian-mutual-funds.git
cd indian-mutual-funds
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start the backend server**
```bash
# Windows PowerShell
$env:PYTHONPATH="."
python -m src.main

# Linux/Mac
export PYTHONPATH="."
python -m src.main
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## 📁 Project Structure

```
indian-mutual-funds/
├── src/
│   ├── api/                    # FastAPI routes
│   │   └── routes/
│   │       ├── portfolio.py    # Portfolio endpoints
│   │       ├── benchmark.py    # Benchmark endpoints
│   │       └── cas.py          # CAS upload endpoint
│   ├── services/               # Business logic layer
│   │   ├── portfolio_service.py
│   │   └── benchmark_service.py
│   ├── cas_parser/             # CAS PDF parsing module
│   │   ├── decrypt.py
│   │   ├── detect.py
│   │   ├── parsers/
│   │   └── normalize.py
│   ├── finance.py              # Core financial calculations
│   ├── benchmark.py            # Benchmark simulation logic
│   ├── data_manager.py         # Data fetching & caching
│   └── main.py                 # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── SipDashboard.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   ├── HoldingsTable.jsx
│   │   │   └── PortfolioChart.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   └── package.json
├── data/                       # Transaction data & CAS files
├── scripts/                    # Utility scripts
└── requirements.txt
```

## 🔌 API Endpoints

### Portfolio Endpoints
- `GET /portfolio/summary` - Get portfolio summary with XIRR and total value
- `GET /portfolio/holdings` - Get detailed holdings breakdown
- `GET /portfolio/sip-performance` - Get SIP trajectory with benchmark comparisons

### Benchmark Endpoints
- `GET /benchmark/compare` - Compare portfolio vs Nifty 50 and Nifty 50 TRI

### CAS Endpoints
- `POST /cas/parse` - Upload and parse CAS PDF (supports encrypted PDFs)

## 📊 Data Sources

- **NAV Data**: AMFI India via `mftool`
- **Index Data**: Yahoo Finance via `yfinance`
- **CAS Statements**: User-uploaded PDF files (CAMS/KFintech/NSDL)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **pandas**: Data manipulation and analysis
- **pyxirr**: Accurate XIRR calculations
- **yfinance**: Market data fetching
- **camelot-py**: PDF table extraction

### Frontend
- **React 19**: Latest React with hooks
- **Vite**: Lightning-fast build tool
- **Tailwind CSS 4**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **Framer Motion**: Smooth animations
- **Axios**: HTTP client

## 📝 Usage

### 1. Prepare Your Transaction Data
Create an Excel file (`MF Transactions.xlsx`) with the following columns:
- Date
- Scheme Name
- Units
- Actual Amount

### 2. Upload CAS Statement (Optional)
- Navigate to the CAS upload section
- Upload your CAMS/KFintech/NSDL CAS PDF
- If encrypted, provide PAN and DOB

### 3. View Analytics
- **Overview Tab**: See portfolio summary, holdings, and XIRR comparison
- **SIP Performance Tab**: Analyze investment trajectory vs benchmarks

## 🎯 Roadmap

- [x] Phase A: Calculation Engine
- [x] Phase B: Data Ingestion & CAS Parser
- [x] Phase C: Backend Services (API)
- [x] Phase D: Frontend & Visualization
- [ ] Phase E: User Authentication & Multi-folio Support
- [ ] Phase F: Account Aggregator Integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- AMFI India for NAV data
- Yahoo Finance for index data
- The open-source community for amazing libraries

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This tool is for educational and personal use only. Always verify calculations independently before making investment decisions.
