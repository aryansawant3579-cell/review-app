@echo off
REM Review Management System - Windows Auto Setup
REM This script creates all necessary folders and files automatically

echo.
echo ========================================
echo Review Management System - Auto Setup
echo ========================================
echo.

REM Set base directory
set BASE_DIR=C:\Users\Aryan\review-app
cd /d %BASE_DIR%

echo Creating folder structure...
if not exist backend mkdir backend
if not exist frontend mkdir frontend
if not exist frontend\src mkdir frontend\src
if not exist frontend\public mkdir frontend\public
echo Folders created!

echo.
echo Creating frontend/package.json...
(
echo {
echo   "name": "review-management-system",
echo   "version": "1.0.0",
echo   "private": true,
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0",
echo     "react-scripts": "5.0.1",
echo     "recharts": "^2.10.3",
echo     "lucide-react": "^0.294.0",
echo     "axios": "^1.6.2"
echo   },
echo   "scripts": {
echo     "start": "react-scripts start",
echo     "build": "react-scripts build",
echo     "test": "react-scripts test",
echo     "eject": "react-scripts eject"
echo   },
echo   "eslintConfig": {
echo     "extends": ["react-app"]
echo   },
echo   "browserslist": {
echo     "production": [">0.2%%", "not dead", "not op_mini all"],
echo     "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
echo   },
echo   "devDependencies": {
echo     "@testing-library/react": "^13.4.0",
echo     "@testing-library/jest-dom": "^5.16.5"
echo   }
echo }
) > frontend\package.json
echo package.json created!

echo.
echo Creating frontend/.env...
(
echo REACT_APP_API_URL=http://localhost:5000/api
echo REACT_APP_ENV=development
) > frontend\.env
echo .env created!

echo.
echo Creating frontend/public/index.html...
(
echo ^<!DOCTYPE html^>
echo ^<html lang="en"^>
echo   ^<head^>
echo     ^<meta charset="utf-8" /^>
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1" /^>
echo     ^<meta name="theme-color" content="#667eea" /^>
echo     ^<title^>Review Management System^</title^>
echo   ^</head^>
echo   ^<body^>
echo     ^<noscript^>You need to enable JavaScript to run this app.^</noscript^>
echo     ^<div id="root"^>^</div^>
echo   ^</body^>
echo ^</html^>
) > frontend\public\index.html
echo index.html created!

echo.
echo Creating frontend/src/index.js...
(
echo import React from 'react';
echo import ReactDOM from 'react-dom/client';
echo import App from './App';
echo import './App.css';
echo.
echo const root = ReactDOM.createRoot(document.getElementById('root'^)^);
echo root.render(
echo   ^<React.StrictMode^>
echo     ^<App /^>
echo   ^</React.StrictMode^>
echo ^);
) > frontend\src\index.js
echo index.js created!

echo.
echo Creating backend/.env...
(
echo DATABASE_URL=sqlite:///review_system.db
echo JWT_SECRET_KEY=your-secret-key-change-in-production
echo FLASK_ENV=development
echo FLASK_DEBUG=False
) > backend\.env
echo .env created!

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Verify files were created:
echo    - Check C:\Users\Aryan\review-app\frontend\package.json exists
echo    - Check C:\Users\Aryan\review-app\backend\.env exists
echo.
echo 2. Copy app code files:
echo    - Copy app.py to backend\
echo    - Copy requirements.txt to backend\
echo    - Copy App.jsx to frontend\src\
echo    - Copy App.css to frontend\src\
echo.
echo 3. Setup Backend:
echo    cd backend
echo    python -m venv venv
echo    .\venv\Scripts\Activate.ps1
echo    pip install -r requirements.txt
echo    python app.py
echo.
echo 4. Setup Frontend (in NEW terminal):
echo    cd frontend
echo    npm install
echo    npm start
echo.
echo ========================================
pause
