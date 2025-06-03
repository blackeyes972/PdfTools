# 🚀 PDF Tools - Guida Rapida

## ⚡ **Installazione Immediata**

### **1. Requisiti Minimi**
- **Python 3.8+** installato
- **10 MB** spazio disco disponibile
- **Windows/macOS/Linux** supportati

### **2. Setup Rapido**
```bash
# 1. Scarica tutti i file del progetto
# 2. Apri terminal nella directory
# 3. Installa dipendenze
pip install PyQt6 PyPDF2 pikepdf reportlab Pillow chardet

# 4. Avvia l'applicazione
python main.py
```

### **3. Prima Esecuzione**
Al primo avvio, l'app creerà automaticamente:
- 📁 `output/` → Directory per file processati
- ⚙️ `output_config.json` → Configurazione gestione file
- 🎨 `theme_settings.json` → Preferenze tema utente

## 🎯 **Utilizzo Rapido**

### **🔥 Workflow Standard**
1. **Apri PDF** → Clicca "Sfoglia" nella toolbar
2. **Scegli Operazione** → Comprimi/Unisci/Proteggi/Filigrana
3. **Automatico!** → File salvato in `output/[tipo]/[anno]/[mese]/`

### **📋 Operazioni Disponibili**

| Operazione | Descrizione | Risultato |
|------------|-------------|-----------|
| **🗜️ Comprimi** | Riduce dimensioni PDF | `output/compressed/` |
| **🔗 Unisci** | Combina più PDF | `output/merged/` |
| **🔒 Proteggi** | Aggiunge password | `output/protected/` |
| **🔓 Rimuovi Password** | Rimuove protezione | `output/unprotected/` |
| **🖋️ Filigrana** | Aggiunge watermark | `output/watermarked/` |

### **🎨 Personalizzazione Temi**
```
Menu → Tema → Seleziona:
├── 🌟 Chiaro Professionale    # Uso diurno
├── 🌙 Scuro Professionale     # Uso notturno  
└── 🏢 Blu Aziendale          # Ambiente business
```

### **🌐 Cambio Lingua**
```
Menu → Lingua → Seleziona:
├── 🇮🇹 Italiano
└── 🇺🇸 English
```

## 🔧 **Gestione Avanzata**

### **📁 Configurazione Directory**
```
Menu → Strumenti → Configura Directory Output
```
- Cambia cartella base di output
- Struttura automatica mantenuta

### **📊 Monitoraggio File**
```
Menu → Strumenti → Statistiche Output
```
- Conteggio file per tipo
- Spazio occupato
- Distribuzione temporale

### **🧹 Pulizia Automatica**
```
Menu → Strumenti → Pulisci File Vecchi
```
- Elimina file più vecchi di 30 giorni
- Libera spazio disco automaticamente

### **🔍 Apertura Directory**
```
Menu → Strumenti → Apri Cartella Output
```
- Apre file manager nella directory output
- Accesso diretto ai file processati

## ⚙️ **Configurazione Avanzata**

### **🎛️ File output_config.json**
```json
{
    "base_output_dir": "./output",
    "auto_cleanup_days": 30,
    "create_subdirectories": true,
    "add_timestamp": true,
    "preserve_original_names": true,
    "max_files_per_directory": 1000
}
```

### **📝 Personalizzazioni Utili**

**Disabilita timestamp nei nomi:**
```json
"add_timestamp": false
```
Risultato: `documento_compressed.pdf` invece di `documento_compressed_20250101_143022.pdf`

**Directory flat (senza sottocartelle):**
```json
"create_subdirectories": false
```
Risultato: tutto in `output/` invece che `output/compressed/2025/01/`

**Pulizia personalizzata:**
```json
"auto_cleanup_days": 60
```
Elimina file più vecchi di 60 giorni invece che 30

## 🚨 **Risoluzione Problemi**

### **❌ Errore "Module not found"**
```bash
# Reinstalla dipendenze
pip install --upgrade PyQt6 PyPDF2 pikepdf reportlab Pillow chardet
```

### **📁 Directory output non creata**
- Verifica permessi di scrittura nella cartella
- Esegui come amministratore se necessario

### **🐌 App lenta con molti file**
- Configura `"auto_cleanup_days": 7` per pulizia frequente
- Riduci `"max_files_per_directory": 500`

### **🎨 Tema non si applica**
- Riavvia l'applicazione
- Elimina `theme_settings.json` per reset

## 💡 **Tips & Tricks**

### **⌨️ Scorciatoie Utili**
- `Ctrl+O` → Apri file
- `Ctrl+C` → Comprimi PDF
- `Ctrl+M` → Unisci PDF
- `Ctrl+P` → Proteggi PDF
- `Ctrl+W` → Aggiungi filigrana
- `Ctrl+R` → Cancella campi
- `F1` → Informazioni

### **🔄 Operazioni Batch**
Per processare molti file:
1. Usa il PDF processor direttamente:
```python
from pdf_functions import PDFProcessor
from output_manager import OutputManager

processor = PDFProcessor()
result = processor.batch_process_directory(
    "/path/to/pdfs", 
    "compress"
)
```

### **📈 Export Statistiche**
Per generare report:
```python
from output_manager import OutputManager

output_mgr = OutputManager()
export_path = output_mgr.export_file_list()
# Crea file_list.json con tutti i dettagli
```

## 🎯 **Esempi Pratici**

### **📄 Scenario: Ufficio Piccolo**
- **50 PDF al mese** da comprimere
- **Directory separata** per ogni progetto
- **Pulizia automatica** dopo 90 giorni

### **🏢 Scenario: Studio Professionale**
- **Centinaia di documenti** con filigrana aziendale
- **Tema blu aziendale** per coerenza brand
- **Backup periodico** della cartella output

### **👨‍💻 Scenario: Sviluppatore**
- **Riutilizzo OutputManager** in altri progetti
- **Customizzazione temi** per diverse app
- **API integration** con sistemi esistenti

## 🚀 **Prossimi Passi**

L'applicazione è completamente funzionale e pronta per:

1. **📦 Distribuzione** → Crea executable con PyInstaller
2. **🔌 Integrazione** → Usa componenti in altri progetti
3. **⚡ Estensione** → Aggiungi nuove funzioni PDF
4. **📱 Mobile** → Adatta UI per tablet/mobile

Hai ora una **soluzione professionale completa** per la gestione PDF! 🎉