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

## 🛠️ Technology Stack

### Backend
- **Python 3.11** - Programming language
- **FastAPI** - Modern web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM with Repository Pattern
- **JWT** - Authentication tokens
- **Pytest** - Testing framework

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - UI component library
- **React Query** - Data fetching and caching
- **Zustand** - State management
- **React Router** - Client-side routing

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and static file serving
- **GitHub Actions** - CI/CD pipeline
- **Azure App Service** - Cloud deployment

## 📋 Prerequisites

- Python 3.11+
- Node.js 20.19+
- PostgreSQL 16+
- Docker & Docker Compose
- Git

## 🔧 Installation

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/jfmartinezDev/inventory-management-system.git
cd inventory-management-system
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python -m app.init_db

# Run development server
uvicorn app.main:app --reload
```

3. **Frontend Setup**
```bash
cd frontend
npm install

# Configure environment variables
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

### Docker Setup

1. **Build and run with Docker Compose**
```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

2. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app --cov-report=html  # With coverage report
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Project Structure

```
inventory-management-system/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configurations
│   │   ├── models/       # Database models
│   │   ├── repositories/ # Data access layer
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── tests/        # Test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── store/        # State management
│   │   └── lib/          # Utilities
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔐 Default Credentials

**Demo Admin Account:**
- Username: `admin`
- Password: `admin123456`

⚠️ **Important**: Change these credentials immediately in production!

## 🌐 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/` - List all users (admin)
- `DELETE /api/v1/users/{id}` - Delete user (admin)

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `PATCH /api/v1/products/{id}/stock` - Update stock
- `GET /api/v1/products/categories` - List categories
- `GET /api/v1/products/low-stock` - Get low stock items
- `GET /api/v1/products/inventory-value` - Get inventory statistics

## 🚀 Deployment

### Azure App Service Deployment

1. **Create Azure Resources**
```bash
# Login to Azure
az login

# Create resource group
az group create --name inventory-rg --location eastus

# Create App Service plan
az appservice plan create --name inventory-plan --resource-group inventory-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group inventory-rg --plan inventory-plan --name inventory-app --runtime "PYTHON:3.11"
```

2. **Deploy with Docker**
```bash
# Build and push to Docker Hub
docker build -t yourusername/inventory-backend ./backend
docker build -t yourusername/inventory-frontend ./frontend
docker push yourusername/inventory-backend
docker push yourusername/inventory-frontend

# Configure Azure Web App
az webapp config container set --name inventory-app --resource-group inventory-rg --docker-custom-image-name yourusername/inventory-backend
```

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Redis caching for session management (optional)
- Lazy loading for React components
- Image optimization and CDN integration
- Gzip compression for static assets
- Connection pooling for database

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- SQL injection prevention via ORM
- CORS configuration
- Input validation and sanitization
- Rate limiting (configurable)
- HTTPS enforcement in production

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub Profile](https://github.com/jfmartinezDev)