import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os
import logging
from datetime import datetime

fecha_actual = datetime.now().strftime('%m-%d-%G')

logging.basicConfig(
    filename=f'logs_{fecha_actual}.log', 
    filemode='a',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailSender:
    def __init__(self):
        """Inicializa los atributos de configuración de la conexión."""
        self.smtp_server = None
        self.smtp_port = None
        self.sender_email = None
        self.sender_password = None
        self.session = None

# ----------------------------------------------------------------------
# 1. CONFIGURACIÓN
# ----------------------------------------------------------------------

    def configuracion(self, server, port, email, password):
        """
        Configura los parámetros del servidor SMTP y las credenciales del remitente.
        Ejemplo para Gmail: server='smtp.gmail.com', port=465
        """
        self.smtp_server = server
        self.smtp_port = port
        self.sender_email = email
        self.sender_password = password
        logging.info(f"Configuración establecida para el servidor: {server}:{port}")

    def _conectar(self):
        """Método interno para iniciar la conexión SMTP segura."""
        if not all([self.smtp_server, self.sender_email, self.sender_password]):
            raise ValueError("¡Error de configuración! Primero llama a .configuracion()")
            
        try:
            # Crea una sesión SMTP segura (SSL)
            self.session = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            self.session.login(self.sender_email, self.sender_password)
            print("Conexión y autenticación exitosa.")
        except Exception as e:
            print(f"Error al conectar o autenticar: {e}")
            self.session = None

    def _desconectar(self):
        """Método interno para cerrar la conexión SMTP."""
        if self.session:
            self.session.quit()
            self.session = None
            print("Conexión SMTP cerrada.")
        
# ----------------------------------------------------------------------
# 2. ENVÍO BASE Y HTML
# ----------------------------------------------------------------------

    def _enviar_base(self, receiver_email, subject, body_content, is_html=False, attachments=None):
        """
        Método base que construye y envía el correo.
        Permite enviar texto plano o HTML y adjuntos.
        """
        self._conectar()
        if not self.session:
            return False

        # Crear el contenedor del mensaje (MIMEMultipart)
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Adjuntar el cuerpo del mensaje (Texto plano o HTML)
        mime_type = 'html' if is_html else 'plain'
        message.attach(MIMEText(body_content, mime_type, 'utf-8'))
        
        # Adjuntar archivos, si existen
        if attachments:
            for path in attachments:
                if os.path.exists(path):
                    self._adjuntar_archivo(message, path)
                else:
                    print(f"Advertencia: Archivo no encontrado en la ruta: {path}")

        try:
            # Enviar el correo
            text = message.as_string()
            self.session.sendmail(self.sender_email, receiver_email, text)
            print(f"Correo enviado con éxito a {receiver_email}")
            return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False
        finally:
            self._desconectar()
    
    def envio_mensaje_sencillo(self, receiver_email, subject, body_text):
        """Envía un correo con texto plano."""
        return self._enviar_base(
            receiver_email,
            subject,
            body_text,
            is_html=False
        )
        
    def envio_correo_html(self, receiver_email, subject, html_content):
        """Envía un correo renderizando contenido HTML en el cuerpo."""
        return self._enviar_base(
            receiver_email,
            subject,
            html_content,
            is_html=True
        )

# ----------------------------------------------------------------------
# 3. MÉTODOS DE ADJUNTOS
# ----------------------------------------------------------------------

    def _adjuntar_archivo(self, message: MIMEMultipart, file_path: str):
        """Función auxiliar para adjuntar cualquier tipo de archivo."""
        
        filename = os.path.basename(file_path)
        
        # 1. Determinar el tipo MIME del archivo
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)

        # 2. Crear el objeto MIMEBase
        with open(file_path, 'rb') as f:
            part = MIMEBase(maintype, subtype)
            part.set_payload(f.read())
        
        # 3. Codificar en Base64 y configurar encabezados
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        
        # 4. Adjuntar al mensaje
        message.attach(part)
        print(f"Adjuntando archivo: {filename}")


    def envio_mensaje_con_archivos(self, receiver_email, subject, body_text, file_paths: list):
        """Envía un correo con texto plano y lista de archivos adjuntos (cualquier tipo)."""
        return self._enviar_base(
            receiver_email,
            subject,
            body_text,
            is_html=False,
            attachments=file_paths
        )

    def envio_mensaje_con_imagenes(self, receiver_email, subject, body_text, image_paths: list):
        """
        Envía un correo con texto plano y lista de imágenes adjuntas. 
        Nota: Este método es idéntico a envio_mensaje_con_archivos,
        ya que el adjunto de imagen se maneja de la misma forma (Content-Disposition: attachment).
        """
        return self.envio_mensaje_con_archivos(
            receiver_email,
            subject,
            body_text,
            image_paths
        )
# ----------------------------------------------------------------------
# EJEMPLO DE USO (Descomentar para probar)
# ----------------------------------------------------------------------

"""
if __name__ == '__main__':
    # 1. Crea la instancia
    mailer = EmailSender()

    # 2. Configura (¡Usa tus credenciales y revisa si necesitas contraseña de aplicación!)
    # NOTA: Para Gmail, usualmente se requiere una 'App Password' generada en la configuración de seguridad.
    # mailer.configuracion(
    #     server='smtp.gmail.com', 
    #     port=465, 
    #     email='tu_email@gmail.com', 
    #     password='tu_app_password'
    # )

    # receiver = 'destino@ejemplo.com'

    # 3. Envío Sencillo
    # mailer.envio_mensaje_sencillo(
    #     receiver,
    #     "Prueba Sencilla",
    #     "Este es un correo de prueba en texto plano."
    # )

    # 4. Envío con HTML
    # html_body = """
    # <html>
    #   <body>
    #     <h1>Hola desde Python</h1>
    #     <p style="color: blue;">Este es un mensaje en HTML renderizado.</p>
    #   </body>
    # </html>
    # """
    # mailer.envio_correo_html(
    #     receiver,
    #     "Prueba HTML",
    #     html_body
    # )

    # 5. Envío con Archivos/Imágenes
    # NOTA: Crea estos archivos temporales para probar
    # with open("documento.txt", "w") as f: f.write("Contenido del archivo.")
    # paths = ["documento.txt", "imagen.png"] # Cambia 'imagen.png' por una imagen real
    
    # mailer.envio_mensaje_con_archivos(
    #     receiver,
    #     "Prueba con Adjuntos",
    #     "Adjunto un documento y una imagen.",
    #     paths
    # )
    # os.remove("documento.txt")
#"""