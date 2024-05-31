import tkinter
import customtkinter
from pytube import YouTube
from tkinter import filedialog

def startdownload():
    try:
        ytlink = link.get()
        if not ytlink:
            raise ValueError("Por favor ingresa una URL.")
        
        ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        original_title = title.cget("text")  # Guardar el título original
        title.configure(text=ytObject.title, text_color="black")
        finishlabel.configure(text="")
        download_path = filedialog.askdirectory()
        if download_path:
            video.download(download_path)
            finishlabel.configure(text="Descargado", text_color="blue")
            link.delete(0, 'end')  # Limpiar el campo de URL después de la descarga
            title.configure(text=original_title, text_color="black")  # Restaurar el título original
        else:
            finishlabel.configure(text="La descarga fue cancelada.", text_color="red")
            title.configure(text=original_title, text_color="black")  # Restaurar el título original
    except ValueError as ve:
        finishlabel.configure(text=str(ve), text_color="red")
    except Exception as e:
        finishlabel.configure(text="Error: " + str(e), text_color="red")
        title.configure(text=original_title, text_color="black")  # Restaurar el título original
    
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pporcentaje.configure(text=per + '%')
    pporcentaje.update()

    # Actualización de la barra de progreso
    barraprogreso.set(float(percentage_of_completion)/100)

# Diseño de la ventana
app = customtkinter.CTk()
app.geometry("720x480")
app.title("PyVideoLink")

# Elementos de la interfaz de usuario
title = customtkinter.CTkLabel(app, text="Inserta la URL de YouTube",text_color="black")
title.pack(padx=10, pady=10)

# Campo de texto para la URL
urlvar = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=urlvar)
link.pack()

# Etiqueta para mostrar el estado de finalización de la descarga
finishlabel = customtkinter.CTkLabel(app, text="")
finishlabel.pack()

# Porcentaje de progreso
pporcentaje = customtkinter.CTkLabel(app,text="0%",text_color="black")
pporcentaje.pack()

# Barra de progreso
barraprogreso = customtkinter.CTkProgressBar(app,width=400)
barraprogreso.set(0)
barraprogreso.pack(padx=10,pady=10)

# Botón para iniciar la descarga
download = customtkinter.CTkButton(app, text="Descargar", command=startdownload)
download.pack(padx=10,pady=10)

# Ejecución de la aplicación
app.mainloop()
