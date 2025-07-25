# 🧭 ThreadSpace

A modern full-stack web application for managing AI assistants, MCP (Model Context Protocol) servers, and external service integrations.

## 🚀 Features

- **AI Provider Management**: Support for OpenAI, Anthropic, DeepSeek, Qwen, and local models
- **MCP Server Configuration**: Add, edit, and manage Model Context Protocol servers
- **Theme Support**: Light/dark mode with system preference detection
- **External Integrations**: Stub implementations for Notion and Google services
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **RESTful API**: FastAPI backend with automatic documentation

## 📁 Project Structure

```
threadspace/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI application entry point
│   │   ├── routers/     # API route handlers
│   │   ├── models/      # Pydantic data models
│   │   └── services/    # Business logic services
│   ├── requirements.txt # Python dependencies
│   └── .env.example    # Environment variables template
├── frontend/            # Vite + React + TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom React hooks
│   │   ├── api/         # API client functions
│   │   └── types/       # TypeScript type definitions
│   ├── package.json    # Node.js dependencies
│   └── vite.config.ts  # Vite configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- **Python 3.8+** for the backend
- **Node.js 18+** for the frontend
- **Git** for version control

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd threadspace/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Start the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd threadspace/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🔧 API Endpoints

### Settings Management
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update user settings
- `POST /api/settings/reset` - Reset settings to defaults

### MCP Server Management
- `GET /api/mcp/servers` - List MCP servers
- `POST /api/mcp/servers` - Add new MCP server
- `PUT /api/mcp/servers/{id}` - Update MCP server
- `DELETE /api/mcp/servers/{id}` - Delete MCP server
- `POST /api/mcp/run` - Execute MCP tool
- `GET /api/mcp/servers/{id}/tools` - Get server tools

### Notion Integration (Stub)
- `GET /api/notion/databases` - List Notion databases
- `POST /api/notion/page` - Create Notion page
- `GET /api/notion/page/{id}` - Get Notion page
- `PUT /api/notion/page/{id}` - Update Notion page

### Google Services Integration (Stub)
- `POST /api/google/gmail/send` - Send Gmail
- `GET /api/google/gmail/messages` - Get Gmail messages
- `GET /api/google/drive/files` - Get Drive files
- `POST /api/google/calendar/events` - Create calendar event
- `GET /api/google/auth/status` - Check auth status

## 🎨 Frontend Components

### Core Components
- **SettingsPanel**: Main settings management interface
- **ThemeToggle**: Light/dark mode switcher
- **ProviderSelector**: AI provider configuration
- **MCPConfig**: MCP server management interface

### Custom Hooks
- **useSettings**: Settings state management
- **useTheme**: Theme management with localStorage persistence

## 🔐 Environment Variables

### Backend (.env)
```bash
# API Keys
NOTION_API_KEY=your_notion_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Application Settings
DEBUG=true
LOG_LEVEL=info
DATA_STORAGE_PATH=./threadspace_data
HOST=0.0.0.0
PORT=8000
```

## 🚀 Development Scripts

### Backend
```bash
# Start development server
python -m uvicorn app.main:app --reload

# Run tests (when implemented)
pytest

# Format code
black app/
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🏗️ Architecture

### Backend Architecture
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **File-based Storage**: JSON files for settings persistence
- **Modular Design**: Separated routers, models, and services

### Frontend Architecture
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Custom Hooks**: Reusable state management

## 🔌 MCP Server Integration

ThreadSpace supports Model Context Protocol (MCP) servers for enhanced functionality:

1. **Add Server**: Configure command, arguments, and environment
2. **Manage Tools**: View and execute available tools
3. **Enable/Disable**: Toggle servers on/off
4. **Environment Variables**: JSON-based configuration

### Example MCP Server Configuration
```json
{
  "name": "MemoryOS Server",
  "command": "python",
  "args": ["server.py", "--config", "config.json"],
  "env": {
    "API_KEY": "your-api-key",
    "DEBUG": "true"
  },
  "enabled": true,
  "description": "Memory management server"
}
```

## 🎯 Integration Status

- ✅ **Settings Management**: Fully implemented
- ✅ **Theme System**: Light/dark mode with persistence
- ✅ **MCP Servers**: Configuration and management
- 🟡 **Notion Integration**: Stub implementation (ready for API keys)
- 🟡 **Google Services**: Stub implementation (ready for OAuth)
- 🟡 **Authentication**: Basic structure (can be extended)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `http://localhost:8000/docs`
- Review the component documentation in the source code
- Open an issue for bugs or feature requests

## 🔮 Future Enhancements

- [ ] Real-time MCP server status monitoring
- [ ] Advanced authentication and user management
- [ ] Plugin system for custom integrations
- [ ] Database backend option
- [ ] Docker containerization
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline setup

---

**ThreadSpace** - Empowering AI assistant management with modern web technologies.
