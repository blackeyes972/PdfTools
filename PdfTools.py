import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QStatusBar,
    QMenuBar,
    QMenu,
    QDialog
)
from PyQt6.QtGui import QAction
from PyQt6 import uic
from PyPDF2 import PdfReader, PdfWriter
import pikepdf  # Libreria per la compressione reale del PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load ui file
        uic.loadUi("ui/PdfTools.ui", self)

        # Define our widgets
        self.Pdf1 = self.findChild(QLineEdit, "Pdf1")  # Assuming input file field
        self.Pdf2 = self.findChild(QLineEdit, "Pdf2")  # Assuming output filename field
        self.PasswordField = self.findChild(QLineEdit, "PasswordField")  # Password field
        self.FiligranaField = self.findChild(QLineEdit, "FiligranaField")  # Watermark field
        self.statusbar = self.findChild(QStatusBar, "statusbar")
        self.PushButtonSfoglia = self.findChild(QPushButton, "PushButtonSfoglia")  # Assuming browse button
        self.PushButtonRiduci = self.findChild(QPushButton, "PushButtonRiduci")
        self.PushButtonUnisci = self.findChild(QPushButton, "PushButtonUnisci")  # Assuming merge button
        self.PushButtonProteggi = self.findChild(QPushButton, "PushButtonProteggi")  # Protect button
        self.PushButtonRimuoviProtezione = self.findChild(QPushButton, "PushButtonRimuoviProtezione")  # Remove protection button
        self.PushButtonFiligrana = self.findChild(QPushButton, "PushButtonFiligrana")  # Watermark button
        self.PushButtonCancellaCampi = self.findChild(QPushButton, "PushButtonCancellaCampi")  # Reset button

        # Connect button clicks
        self.PushButtonSfoglia.clicked.connect(self.choose_file)
        self.PushButtonRiduci.clicked.connect(self.compress_pdf_action)
        self.PushButtonUnisci.clicked.connect(self.merge_pdfs_action)  # Connect merge button
        self.PushButtonProteggi.clicked.connect(self.protect_pdf_action)  # Connect protect button
        self.PushButtonRimuoviProtezione.clicked.connect(self.remove_protection_action)  # Connect remove protection button
        self.PushButtonFiligrana.clicked.connect(self.add_watermark_action)  # Connect watermark button
        self.PushButtonCancellaCampi.clicked.connect(self.reset_fields)  # Connect reset button

        self.statusbar.showMessage("Pronto... ")  # Status bar message

        # Creare il menu
        self.create_menu()

    def create_menu(self):
        # Creare le azioni del menu
        open_action = QAction("Sfoglia", self)
        open_action.triggered.connect(self.choose_file)
        
        compress_action = QAction("Comprimi", self)
        compress_action.triggered.connect(self.compress_pdf_action)

        merge_action = QAction("Unisci", self)
        merge_action.triggered.connect(self.merge_pdfs_action)

        protect_action = QAction("Proteggi", self)
        protect_action.triggered.connect(self.protect_pdf_action)

        remove_protection_action = QAction("Rimuovi Password", self)
        remove_protection_action.triggered.connect(self.remove_protection_action)
        
        watermark_action = QAction("Aggiungi Filigrana", self)
        watermark_action.triggered.connect(self.add_watermark_action)

        reset_action = QAction("Cancella Campi", self)
        reset_action.triggered.connect(self.reset_fields)
        
        exit_action = QAction("Esci", self)
        exit_action.triggered.connect(self.close)

        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(self.show_about_dialog)

        # Creare la barra del menu
        menu_bar = self.menuBar()

        # Creare i menu
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("?")
        
        # Aggiungere le azioni ai menu
        file_menu.addAction(open_action)
        file_menu.addAction(compress_action)
        file_menu.addAction(merge_action)
        file_menu.addAction(protect_action)
        file_menu.addAction(remove_protection_action)
        file_menu.addAction(watermark_action)
        file_menu.addAction(reset_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu.addAction(about_action)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()


    def choose_file(self):
        """Apre una finestra di dialogo per selezionare il file PDF di input."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:  # Controlla se un file è stato selezionato
            self.Pdf1.setText(file_path)  # Imposta il percorso del file selezionato nel campo di input
            self.Pdf2.setText('compressed.pdf')  # Imposta il nome predefinito per il file di output
            self.statusbar.showMessage("File selezionato: " + file_path, 5000)

    def compress_pdf_action(self):
        """Gestisce il clic sul pulsante "Riduci", controlla i campi e chiama la compressione."""
        input_file = self.Pdf1.text()
        output_filename = self.Pdf2.text()

        if not input_file:
            QMessageBox.warning(self, "Attenzione", "Seleziona un file PDF da comprimere.")
            self.statusbar.showMessage("Errore: nessun file PDF selezionato per la compressione.", 5000)
            return

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        try:
            self.compress_pdf(input_file, output_filename)
            QMessageBox.information(self, "Successo", f"PDF compresso e salvato in '{output_filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante la compressione: {e}")

    def compress_pdf(self, input_file, output_file):
        """Comprime un PDF e lo salva con un nuovo nome.

        Args:
            input_file (str): Il percorso del file PDF in input.
            output_file (str): Il percorso del file PDF di output.
        """
        # Usare pikepdf per la compressione
        with pikepdf.open(input_file) as pdf:
            pdf.save(output_file, compress_streams=True)

    def merge_pdfs_action(self):
        """Gestisce il clic sul pulsante "Unisci"."""
        input_files, _ = QFileDialog.getOpenFileNames(
            self, "Seleziona i PDF da unire", "", "PDF Files (*.pdf)"
        )
        output_filename = QFileDialog.getSaveFileName(
            self, "Salva PDF Unito", "", "PDF Files (*.pdf)"
        )[0]

        if not input_files:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno un file PDF da unire.")
            return

        if not output_filename:
            QMessageBox.warning(self, "Attenzione", "Specifica un nome per il file unito.")
            return

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        try:
            self.merge_pdfs(input_files, output_filename)
            QMessageBox.information(self, "Successo", f"PDF unito e salvato in '{output_filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante l'unione: {e}")

    def merge_pdfs(self, input_files, output_file):
        """Unisce più PDF e li salva in un nuovo file.

        Args:
            input_files (list): Lista dei percorsi dei file PDF in input.
            output_file (str): Il percorso del file PDF di output.
        """
        writer = PdfWriter()

        for file in input_files:
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_file, 'wb') as out_file:
            writer.write(out_file)


    def protect_pdf_action(self):
        """Gestisce il clic sul pulsante "Proteggi"."""
        input_file = self.Pdf1.text()
        output_filename = self.Pdf2.text()
        password = self.PasswordField.text()

        if not input_file:
            QMessageBox.warning(self, "Attenzione", "Seleziona un file PDF da proteggere.")
            return

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        if not password:
            QMessageBox.warning(self, "Attenzione", "Specifica una password per proteggere il PDF.")
            return

        try:
            self.protect_pdf(input_file, output_filename, password)
            QMessageBox.information(self, "Successo", f"PDF protetto e salvato in '{output_filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante la protezione: {e}")

    def protect_pdf(self, input_file, output_file, password):
        """Protegge un PDF con una password e lo salva con un nuovo nome.

        Args:
            input_file (str): Il percorso del file PDF in input.
            output_file (str): Il percorso del file PDF di output.
            password (str): La password per proteggere il PDF.
        """
        with pikepdf.open(input_file) as pdf:
            pdf.save(output_file, encryption=pikepdf.Encryption(owner=password, user=password, R=4))
        self.PasswordField.clear()  # Resetta il campo di password

    def remove_protection_action(self):
        """Gestisce il clic sul pulsante "Rimuovi Protezione"."""
        input_file = self.Pdf1.text()
        output_filename = self.Pdf2.text()
        password = self.PasswordField.text()

        if not input_file:
            QMessageBox.warning(self, "Attenzione", "Seleziona un file PDF da cui rimuovere la protezione.")
            return

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        if not password:
            QMessageBox.warning(self, "Attenzione", "Specifica la password per rimuovere la protezione del PDF.")
            return

        try:
            self.remove_protection(input_file, output_filename, password)
            QMessageBox.information(self, "Successo", f"Protezione del PDF rimossa e salvato in '{output_filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante la rimozione della protezione: {e}")

    def remove_protection(self, input_file, output_file, password):
        """Rimuove la protezione di un PDF e lo salva con un nuovo nome.

        Args:
            input_file (str): Il percorso del file PDF in input.
            output_file (str): Il percorso del file PDF di output.
            password (str): La password per rimuovere la protezione del PDF.
        """
        with pikepdf.open(input_file, password=password) as pdf:
            pdf.save(output_file)
        self.PasswordField.clear()  # Resetta il campo di password

    def add_watermark_action(self):
        """Gestisce il clic sul pulsante "Filigrana"."""
        input_file = self.Pdf1.text()
        output_filename = self.Pdf2.text()
        watermark_text = self.FiligranaField.text()

        if not input_file:
            QMessageBox.warning(self, "Attenzione", "Seleziona un file PDF a cui aggiungere una filigrana.")
            return

        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        if not watermark_text:
            QMessageBox.warning(self, "Attenzione", "Specifica un testo per la filigrana.")
            return

        try:
            self.add_watermark(input_file, output_filename, watermark_text)
            QMessageBox.information(self, "Successo", f"Filigrana aggiunta e PDF salvato in '{output_filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante l'aggiunta della filigrana: {e}")

    def add_watermark(self, input_file, output_file, watermark_text):
        """Aggiunge una filigrana a un PDF e lo salva con un nuovo nome.

        Args:
            input_file (str): Il percorso del file PDF in input.
            output_file (str): Il percorso del file PDF di output.
            watermark_text (str): Il testo della filigrana da aggiungere.
        """
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Crea una filigrana come PDF
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 40)
        can.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)
        can.saveState()
        can.translate(300, 500)
        can.rotate(45)
        can.drawCentredString(0, 0, watermark_text)
        can.restoreState()
        can.save()

        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output_file, 'wb') as out_file:
            writer.write(out_file)

        self.FiligranaField.clear()  # Resetta il campo di filigrana
    
    def reset_fields(self):
        self.Pdf1.clear() # Reset input file field
        self.Pdf2.clear()  # Reset output filename field
        self.PasswordField.clear() # Reset Password field
        self.FiligranaField.clear()  # Resetta il campo di filigrana


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        uic.loadUi("ui/AboutDialog.ui", self)

# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
UIWindow.show()
app.exec()
