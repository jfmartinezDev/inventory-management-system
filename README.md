# Inventory Management System

A full-stack inventory management system built with modern technologies and best practices. This application provides secure user authentication and comprehensive CRUD operations for managing product inventory.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **Product Management**: Complete CRUD operations for inventory items
- **Advanced Search**: Search, filter, and sort products
- **Stock Monitoring**: Real-time low stock alerts
- **Responsive Design**: Modern UI with dark mode support
- **Data Export**: Export inventory data to CSV
- **Image Support**: Product image management
- **Category Organization**: Organize products by categories
- **Dashboard Analytics**: Inventory value and statistics
- **Repository Pattern**: Clean architecture with separation of concerns
- **Comprehensive Testing**: Unit and integration tests with high coverage

## 🛠️ Technology Stack

### Backend
- **Python 3.11** - Programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM with Repository Pattern implementation
- **JWT** - Secure authentication tokens
- **Pytest** - Testing framework with coverage reporting
- **Alembic** - Database migrations
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **React 18** - UI library for building user interfaces
- **Vite** - Next generation frontend build tool
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Re-usable components built with Radix UI and Tailwind
- **React Query** - Powerful data synchronization for React
- **Zustand** - Small, fast state management solution
- **React Router v6** - Declarative routing for React
- **React Hook Form** - Performant forms with easy validation
- **Zod** - TypeScript-first schema validation

### DevOps
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications
- **Nginx** - High-performance web server and reverse proxy
- **GitHub Actions** - CI/CD pipeline automation
- **Azure App Service** - Cloud hosting platform
- **PostgreSQL on Azure** - Managed database service

## 📋 Prerequisites

- **Python** 3.11 or higher
- **Node.js** 20.19 or higher
- **PostgreSQL** 16 or higher
- **Docker** & Docker Compose (optional but recommended)
- **Git** for version control
- **VS Code** or any preferred IDE

## 🔧 Installation

### Quick Start with Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/jfmartinezDev/inventory-management-system.git
cd inventory-management-system
```

2. **Run with Docker Compose**
```bash
# Windows PowerShell
.\scripts\run-local.ps1

# Linux/Mac
./scripts/run-local.sh

# Or directly with docker-compose
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup (Without Docker)

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your database credentials
# Make sure PostgreSQL is running locally
```

5. **Initialize the database**
```bash
python -m app.init_db
```

6. **Run the development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

4. **Run the development server**
```bash
npm run dev
```

5. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Using Development Scripts

For convenience, use the provided scripts in the `scripts/` directory:

```bash
# Windows - Run both frontend and backend
.\scripts\dev.ps1

# Run only backend
.\scripts\dev.ps1 -Component backend

# Run only frontend
.\scripts\dev.ps1 -Component frontend
```

## 🧪 Testing

### Backend Tests

The backend includes comprehensive unit and integration tests:

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run only unit tests
pytest app/tests/unit/

# Run only integration tests
pytest app/tests/integration/

# Run specific test file
pytest app/tests/unit/test_security.py -v

# Open coverage report in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux
```

### Test Structure
```
backend/app/tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (no database)
│   ├── test_security.py    # Password hashing and JWT tests
│   └── test_schemas.py     # Pydantic schema validation tests
└── integration/             # Integration tests (with test database)
    ├── test_auth.py         # Authentication endpoint tests
    └── test_products.py     # Product CRUD endpoint tests
```

### Frontend Tests

```bash
cd frontend

# Run tests (when implemented)
npm test
```

## Project Structure

```
inventory-management-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py           # Dependencies for endpoints
│   │   │   ├── api_v1.py         # API router configuration
│   │   │   └── endpoints/        # API endpoint modules
│   │   │       ├── auth.py       # Authentication endpoints
│   │   │       ├── users.py      # User management endpoints
│   │   │       └── products.py   # Product CRUD endpoints
│   │   ├── core/
│   │   │   ├── config.py         # Application configuration
│   │   │   ├── database.py       # Database connection setup
│   │   │   └── security.py       # Security utilities
│   │   ├── models/
│   │   │   ├── base.py           # Base model class
│   │   │   ├── user.py           # User model
│   │   │   └── product.py        # Product model
│   │   ├── repositories/
│   │   │   ├── base.py           # Base repository pattern
│   │   │   ├── user.py           # User repository
│   │   │   └── product.py        # Product repository
│   │   ├── schemas/
│   │   │   ├── user.py           # User Pydantic schemas
│   │   │   ├── product.py        # Product Pydantic schemas
│   │   │   └── token.py          # Token schemas
│   │   ├── tests/
│   │   │   ├── conftest.py       # Test configuration
│   │   │   ├── unit/             # Unit tests
│   │   │   └── integration/      # Integration tests
│   │   ├── main.py               # FastAPI application entry
│   │   └── init_db.py            # Database initialization
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Backend container configuration
│   ├── .env.example              # Environment variables example
│   └── .env                      # Environment variables (not in git)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # Reusable UI components
│   │   │   ├── auth/            # Authentication components
│   │   │   ├── products/        # Product-related components
│   │   │   └── layout/          # Layout components
│   │   ├── pages/
│   │   │   ├── Login.jsx        # Login page
│   │   │   ├── Register.jsx     # Registration page
│   │   │   ├── Dashboard.jsx    # Dashboard page
│   │   │   ├── Products.jsx     # Products list page
│   │   │   ├── ProductDetail.jsx # Product detail page
│   │   │   ├── ProductForm.jsx  # Product create/edit form
│   │   │   └── Profile.jsx      # User profile page
│   │   ├── services/
│   │   │   ├── api.js           # Axios configuration
│   │   │   ├── auth.service.js  # Authentication service
│   │   │   └── product.service.js # Product API service
│   │   ├── store/
│   │   │   └── useAuthStore.js  # Zustand auth store
│   │   ├── config/
│   │   │   └── constants.js     # Application constants
│   │   ├── lib/
│   │   │   └── utils.js         # Utility functions
│   │   ├── App.jsx               # Main application component
│   │   ├── main.jsx              # Application entry point
│   │   └── index.css             # Global styles
│   ├── public/                   # Static assets
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   ├── Dockerfile                # Frontend container configuration
│   └── nginx.conf                # Nginx configuration
├── scripts/
│   ├── run-local.sh              # Run with Docker (Linux/Mac)
│   ├── run-local.ps1             # Run with Docker (Windows)
│   ├── dev.ps1                   # Development script (Windows)
│   └── deploy.ps1                # Azure deployment script
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD
├── docker-compose.yml            # Docker compose for development
├── docker-compose.prod.yml       # Docker compose for production
├── .env.production              # Production environment example
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

## 🔐 Default Credentials

After running the initialization script, you can login with:

- **Username**: `admin`
- **Password**: `admin123456`

⚠️ **Important**: Change these credentials immediately in production!

## 🌐 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID (admin only)
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

#### Products
- `GET /api/v1/products/` - List products with pagination
- `POST /api/v1/products/` - Create new product
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `PATCH /api/v1/products/{id}/stock` - Update stock quantity
- `GET /api/v1/products/categories` - List all categories
- `GET /api/v1/products/low-stock` - Get low stock items
- `GET /api/v1/products/inventory-value` - Get inventory statistics

## 🚀 Deployment

### Docker Production Build

```bash
# Build and run production containers
docker-compose -f docker-compose.prod.yml up --build
```

### Azure Deployment

1. **Prerequisites**
   - Azure CLI installed
   - Azure account with active subscription
   - Docker Hub account (for container registry)

2. **Run deployment script**
```powershell
# Windows PowerShell
.\scripts\deploy.ps1 -ResourceGroup "inventory-rg" -AppName "my-inventory-app"
```

3. **Manual deployment steps**
```bash
# Login to Azure
az login

# Create resource group
az group create --name inventory-rg --location eastus

# Create PostgreSQL server
az postgres server create \
  --resource-group inventory-rg \
  --name inventory-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password SecurePassword123! \
  --sku-name B_Gen5_1

# Create App Service plan
az appservice plan create \
  --name inventory-plan \
  --resource-group inventory-rg \
  --sku B1 \
  --is-linux

# Deploy backend and frontend apps
# See deployment script for detailed commands
```

## 📈 Performance Optimization

- **Database**: Indexes on frequently queried fields (SKU, category)
- **API**: Pagination for all list endpoints
- **Frontend**: 
  - Lazy loading for React components
  - React Query for efficient data caching
  - Image optimization and lazy loading
- **Infrastructure**:
  - Gzip compression for static assets
  - Docker multi-stage builds for smaller images
  - Connection pooling for database

## 🔒 Security Features

- **Authentication**: JWT tokens with expiration
- **Password Security**: Bcrypt hashing with salt
- **API Security**: 
  - CORS configuration
  - Rate limiting ready
  - Input validation with Pydantic
- **Database**: 
  - SQL injection prevention via SQLAlchemy ORM
  - Parameterized queries
- **Frontend**: 
  - XSS prevention
  - Secure token storage
  - HTTPS enforcement in production

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=Inventory Management System
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Environment
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Common Issues

1. **Docker not running**
   - Ensure Docker Desktop is running
   - Check Docker service: `docker info`

2. **Port already in use**
   - Check ports 8000 (backend) and 80 (frontend)
   - Stop conflicting services or change ports in docker-compose.yml

3. **Database connection failed**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists and user has permissions

4. **Frontend can't connect to backend**
   - Check VITE_API_URL in frontend .env
   - Verify backend is running on correct port
   - Check CORS settings in backend

## 👥 Authors

- José Francisco Martínez Amaya - [GitHub Profile](https://github.com/jfmartinezDev)