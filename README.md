# 📄 PDF Tools Professional

<div align="center">

![PDF Tools Logo](https://img.shields.io/badge/PDF-Tools-0078d4?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)

**A modern, professional PDF manipulation suite with a beautiful interface and modular architecture**

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat&logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.7+-41cd52?style=flat&logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat)](https://github.com/blackeyes972/PdfTools)

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-features) • [🎨 Screenshots](#-screenshots) • [🔧 Development](#-development) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ **Overview**

PDF Tools Professional is a cutting-edge desktop application for PDF manipulation, featuring a modern interface with **3 professional themes**, **multilingual support** (Italian/English), and a **modular architecture** designed for both end-users and developers.

### 🎯 **Key Highlights**

- **🎨 Modern UI**: Three professional themes (Light, Dark, Corporate Blue)
- **🌐 Multilingual**: Full Italian and English support with real-time switching
- **📁 Smart Organization**: Automatic file organization with date-based directory structure
- **⚡ High Performance**: Background processing with threading for smooth user experience
- **🔧 Modular Architecture**: Reusable components for rapid development of new applications
- **🛡️ Enterprise-Ready**: Professional-grade file management and error handling

---

## 🚀 **Quick Start**

### **Prerequisites**

- **Python 3.8+** installed on your system
- **10 MB** of free disk space

### **Installation**

```bash
# Clone the repository
git clone https://github.com/blackeyes972/PdfTools.git
cd PdfTools

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### **First Launch**

PDF Tools will automatically create:
- 📁 `output/` directory for processed files
- ⚙️ `output_config.json` for file management settings
- 🎨 `theme_settings.json` for user theme preferences

---

## 📖 **Features**

### **🔧 Core PDF Operations**

| Feature | Description | Output Location |
|---------|-------------|----------------|
| **🗜️ Compression** | Reduce PDF file size with advanced algorithms | `output/compressed/YYYY/MM/` |
| **🔗 Merge** | Combine multiple PDFs into a single document | `output/merged/YYYY/MM/` |
| **🔒 Protection** | Add password protection to PDFs | `output/protected/YYYY/MM/` |
| **🔓 Remove Protection** | Remove passwords from protected PDFs | `output/unprotected/YYYY/MM/` |
| **🖋️ Watermark** | Add custom text watermarks to documents | `output/watermarked/YYYY/MM/` |

### **🎨 Interface & Themes**

<table>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/Light-Professional-f8f9fa?style=for-the-badge" alt="Light Theme"/><br/>
<strong>Light Professional</strong><br/>
Elegant light theme for daytime use
</td>
<td align="center">
<img src="https://img.shields.io/badge/Dark-Professional-2d3748?style=for-the-badge&color=2d3748" alt="Dark Theme"/><br/>
<strong>Dark Professional</strong><br/>
Modern dark theme for nighttime work
</td>
<td align="center">
<img src="https://img.shields.io/badge/Corporate-Blue-1e3a8a?style=for-the-badge&color=1e3a8a" alt="Blue Theme"/><br/>
<strong>Corporate Blue</strong><br/>
Professional blue theme for business
</td>
</tr>
</table>

### **🌐 Multilingual Support**

- **🇮🇹 Italian**: Complete interface translation
- **🇺🇸 English**: Full English support
- **🔄 Real-time switching**: Change language instantly from menu
- **📝 Extensible**: Easy to add new languages

### **📁 Smart File Management**

```
output/
├── compressed/
│   ├── 2024/
│   │   └── 12/
│   └── 2025/
│       └── 01/
├── merged/
├── protected/
├── watermarked/
└── unprotected/
```

- **📅 Date-based organization**: Files automatically sorted by year/month
- **🏷️ Intelligent naming**: Timestamps and operation suffixes
- **🧹 Auto-cleanup**: Configurable automatic deletion of old files
- **📊 Statistics**: Detailed reports on processed files

---

## 🎨 **Screenshots**

### **Light Professional Theme**
*Clean, modern interface perfect for daily use*

### **Dark Professional Theme** 
*Elegant dark theme that's easy on the eyes*

### **Corporate Blue Theme**
*Professional blue theme ideal for business environments*

### **Multi-language Support**
*Seamlessly switch between Italian and English*

---

## 🏗️ **Architecture**

PDF Tools is built with a **modular, reusable architecture** that makes it easy to maintain and extend:

```
pdf_tools/
├── main.py                    # Application entry point
├── translations.py            # Multilingual support system
├── pdf_functions.py           # Core PDF processing logic
├── output_manager.py          # Smart file organization
├── theme_manager.py           # Professional theming system
├── menu_manager.py            # Dynamic menu management
├── ui_manager.py              # Modern UI components
└── requirements.txt           # Dependencies
```

### **🔧 Reusable Components**

Each component is designed to be **completely reusable** in other applications:

- **`theme_manager.py`**: Drop-in theming system for any PyQt6 app
- **`menu_manager.py`**: Dynamic menu system with translations
- **`output_manager.py`**: Professional file organization for any app
- **`translations.py`**: Multilingual framework

---

## 🛠️ **Development**

### **Requirements**

```
PyQt6>=6.7.0
PyPDF2>=3.0.1
pikepdf>=9.2.0
reportlab>=4.2.0
Pillow>=10.4.0
chardet>=5.2.0
```

### **Project Structure**

The codebase follows **enterprise-grade patterns**:

- **🏗️ Modular Design**: Each component has a single responsibility
- **🔄 Dependency Injection**: Components are loosely coupled
- **⚡ Threading**: Background processing for smooth UX
- **🎨 Theme System**: Centralized styling with hot-swapping
- **🌐 i18n Ready**: Full internationalization support
- **📁 Smart Defaults**: Zero-configuration file management

### **Creating New Applications**

Use PDF Tools components as a foundation for new apps:

```python
from theme_manager import ThemeManager
from menu_manager import ApplicationMenuManager
from output_manager import OutputManager

# Instant professional UI with themes
theme_mgr = ThemeManager()
menu_mgr = ApplicationMenuManager(window, translations, theme_mgr)
output_mgr = OutputManager("./my_app_output")
```

### **Running Tests**

```bash
# Test individual components
python -m pytest tests/

# Test full application
python main.py
```

---

## 📋 **Usage Examples**

### **Basic Operations**

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Select PDF File**
   - Click "Browse" in toolbar
   - Choose your PDF file

3. **Choose Operation**
   - **Compress**: Reduce file size
   - **Merge**: Combine multiple PDFs
   - **Protect**: Add password
   - **Watermark**: Add custom text

4. **Automatic Processing**
   - Files saved automatically in organized directories
   - Progress shown in status bar
   - Completion notification displayed

### **Advanced Features**

- **Theme Switching**: `Menu → Theme → Select variant`
- **Language Change**: `Menu → Language → Italian/English`
- **Output Configuration**: `Menu → Tools → Configure Directory`
- **Statistics**: `Menu → Tools → Output Statistics`
- **Cleanup**: `Menu → Tools → Cleanup Old Files`

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

### **🐛 Bug Reports**

1. Check existing [issues](https://github.com/blackeyes972/PdfTools/issues)
2. Create detailed bug report with:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### **✨ Feature Requests**

1. Open an [issue](https://github.com/blackeyes972/PdfTools/issues/new) with "Feature Request" label
2. Describe the feature and use case
3. Explain how it fits with the project goals

### **🔧 Development Contributions**

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

### **📝 Code Style**

- Follow **PEP 8** Python style guide
- Use **type hints** where possible
- Add **docstrings** for public methods
- Maintain **modular architecture**
- Test your changes

---

## 🗺️ **Roadmap**

### **🎯 Version 2.1** (Coming Soon)
- [ ] **Batch Processing**: Process multiple files simultaneously
- [ ] **PDF Splitting**: Split large PDFs into smaller documents
- [ ] **OCR Integration**: Extract text from scanned PDFs
- [ ] **Digital Signatures**: Add and verify digital signatures

### **🚀 Version 2.2** (Future)
- [ ] **Cloud Integration**: Direct upload to cloud services
- [ ] **Plugin System**: Third-party extensions support
- [ ] **Advanced Watermarks**: Image watermarks and positioning
- [ ] **PDF Forms**: Fill and extract form data

### **🌟 Version 3.0** (Long-term)
- [ ] **Web Interface**: Browser-based access
- [ ] **API Endpoints**: REST API for automation
- [ ] **Enterprise Features**: User management and audit logs
- [ ] **Mobile Apps**: iOS and Android companions

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Alessandro Castaldi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💬 **Support**

### **📚 Documentation**
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [API Reference](docs/api-reference.md)
- [FAQ](docs/faq.md)

### **🆘 Getting Help**
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/blackeyes972/PdfTools/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/blackeyes972/PdfTools/discussions)
- 📧 **Direct Contact**: [notifiche72@gmail.com](mailto:notifiche72@gmail.com)
- 💬 **Community**: Join our discussions on GitHub

---

## 👨‍💻 **Project Maintainer**

<div align="center">

### **👤 Alessandro Castaldi**

*Software Developer & Open Source Enthusiast*

[![Email](https://img.shields.io/badge/Email-notifiche72%40gmail.com-red?style=flat&logo=gmail&logoColor=white)](mailto:notifiche72@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-blackeyes972-181717?style=flat&logo=github&logoColor=white)](https://github.com/blackeyes972)
[![Twitter](https://img.shields.io/badge/Twitter-blackeyes972-1da1f2?style=flat&logo=twitter&logoColor=white)](https://x.com/blackeyes972)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Alessandro%20Castaldi-0077b5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alessandro-castaldi-663846a5/)

*"Building tools that make developers' lives easier, one line of code at a time."*

</div>

---

## 🙏 **Acknowledgments**

- **PyQt6 Team** for the excellent GUI framework
- **pikepdf Developers** for robust PDF processing capabilities
- **Open Source Community** for inspiration and support
- **Beta Testers** for valuable feedback and bug reports

---

## ⭐ **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=blackeyes972/PdfTools&type=Date)](https://star-history.com/#blackeyes972/PdfTools&Date)

---

<div align="center">

**📄 PDF Tools Professional** - *Making PDF manipulation simple, beautiful, and professional*

[⬆ Back to Top](#-pdf-tools-professional)

</div>