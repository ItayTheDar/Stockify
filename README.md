# Stock Management API

This application, built with the PyNest framework, provides a robust suite of services for managing stock data within a financial system. It integrates PostgreSQL for database management and Redis for caching, enhancing performance by reducing repetitive database queries.

## Features

- **Dynamic Stock Queries**: Search and retrieve stocks based on symbols or custom criteria.
- **Stock and Officer Management**: Add, update, and delete information about stocks and company officers.
- **Efficient Caching**: Implement Redis caching to minimize database queries and speed up response times.
- **Background Processing**: Use background tasks for non-blocking data operations.
- **Timeframe Analysis**: Analyze stock price movements over selectable time periods.

## Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher
- PostgreSQL
- Redis

## Installation

### Clone the Repository

```bash
git clone https://github.com/ItayTheDar/Stockify.git
cd Stockify
```

## Local Deployment

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application

```base
uvicorn src.app_module:http_server --host "0.0.0.0" --port 8000
```

## Docker Deployment
```bash
docker-compose up --build
```

## Usage
Access the API at http://localhost:8000 upon deployment. Explore API endpoints through the integrated Swagger UI or Redoc.

## API Endpoints
GET `/stocks`: Fetch a list of stocks.

POST `/stocks`: Register a new stock.

PUT `/stocks/:{id}`: Modify details of an existing stock.

DELETE `/stocks/:{id}`: Erase a stock record.

Endpoints also include functions for managing company officers and detailed stock price data.
