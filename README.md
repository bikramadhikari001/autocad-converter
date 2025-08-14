# Image to AutoCAD Converter

A Flask-based web application that converts images (sketches, blueprints, technical drawings) to AutoCAD files with a clean, minimal interface optimized for desktop users.

## 🌐 Live Demo

**Visit the live application:** [https://autocad-converter-2024.fly.dev/](https://autocad-converter-2024.fly.dev/)

**Login Credentials:**
- Username: `admin`
- Password: `password123`

## ✨ Features

### 🎨 Clean, Minimal Design
- Google-inspired aesthetics with generous white space
- Side-by-side demo examples showing before/after conversions
- Responsive design (desktop-focused with mobile support)
- Minimal color palette with blue accents

### 📤 3-Step Conversion Process
1. **Upload**: Drag & drop file upload with validation (JPG, PNG, PDF, max 10MB)
2. **Configure**: Basic and advanced settings with smart defaults
3. **Convert**: Real-time progress with multi-stage visualization

### 📊 Results Dashboard
- Side-by-side preview (original vs converted)
- Detailed conversion statistics
- Multiple download format options (DWG, DXF, PDF)
- Conversion history tracking

### 🔐 Authentication & Security
- Basic authentication system
- Session management
- File validation and security
- HTTPS enforced in production

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3, Python 3.11
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Docker, Fly.io
- **Storage**: Persistent volumes for file handling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (for deployment)
- Fly.io CLI (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autocad-converter.git
   cd autocad-converter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Visit** `http://localhost:5000`

## 🔒 Security Notes

⚠️ **Important for Production:**
- Change hardcoded credentials in `app.py`
- Use environment variables for sensitive data
- Implement proper user authentication
- Regular security updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Made with ❤️ for converting images to professional CAD files**
