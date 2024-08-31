# PDF Tools

PDF Tools è un'applicazione versatile e intuitiva progettata per migliorare la gestione dei file PDF. Con PDF Tools, gli utenti possono non solo ridurre le dimensioni dei file per una condivisione più semplice ma anche personalizzare i loro documenti con filigrane protettive e visualizzare i PDF direttamente all'interno dell'app. Questo strumento è particolarmente utile per professionisti e studenti che lavorano frequentemente con documenti PDF e cercano una soluzione tutto-in-uno per ottimizzare il loro workflow.

## Caratteristiche Principali

- **Comprimere PDF**: Ottimizza i file PDF per una condivisione facile e veloce.
- **Aggiungere Filigrana**: Proteggi i tuoi documenti inserendo filigrane personalizzabili.
- **Visualizzare PDF**: Apri e visualizza PDF direttamente nell'app senza bisogno di software esterni.


## Requisiti

- Python 3.10 o superiore
- PyQt6
- PyMuPDF
- PikePDF

## Installazione

1. Clona il repository:
    ```bash
    git clone https://github.com/blackeyes972/PdfTools
    cd PdfTools
    ```

2. Crea un ambiente virtuale e attivalo:
    ```bash
    python -m venv PdfToolsEnv
    source PdfToolsEnv/bin/activate  # Su Windows usa `PdfToolsEnv\Scripts\activate`
    ```

3. Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

4. Avvia l'applicazione:
    ```bash
    python PdfTools.py
    ```

## Utilizzo

### Compress PDF

1. Seleziona un file PDF cliccando su "Sfoglia".
2. Specifica il nome del file di output.
3. Clicca su "Riduci" per comprimere il PDF.

### Aggiungi Filigrana

1. Seleziona un file PDF cliccando su "Sfoglia".
2. Specifica il nome del file di output.
3. Inserisci il testo della filigrana.
4. Clicca su "Aggiungi Filigrana".

### Visualizza PDF

1. Seleziona un file PDF cliccando su "Sfoglia".
2. Il file PDF verrà visualizzato nella finestra dell'applicazione.

### Informazioni sull'App

1. Vai al menu `Aiuto`.
2. Seleziona `Informazioni` per visualizzare la finestra di dialogo "About" con informazioni sull'applicazione.

## Contribuire

Contributi sono benvenuti! Sentiti libero di aprire un issue o una pull request.

## Licenza

Questo progetto è licenziato sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.


