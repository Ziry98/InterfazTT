import functools
from tkinter import *
from tkinter import filedialog as FileDialog
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox as MessageBox
import cv2
import imutils
from pyfirmata import Arduino
import time
import matplotlib.pyplot as plt

# Presiona ctrl+b para ver la app

## Se declara una variable para almacenar el numero del PIN
IN1 = 7 # A1
IN2 = 8 # A2
IN3 = 2 # B1
IN4 = 4 # B2
paso = 1.8
# arduino = Arduino("COM3") # Puerto del Arduino 

def SumaX():
	global x
	print("Se suma 1 en x")
	x += 1
	print("x: ", x)
	# Se mueve en dirección horaria
	CCW()

def RestaX():
	global x
	print("Se resta 1 en x")
	x -= 1
	print("x: ", x)
	# Se mueve en dirección antihoraria
	ACW()

def SumaY():
	global y
	print("Se suma 1 en y")
	y += 1
	print("y: ", y)


def RestaY():
	global y
	print("Se resta 1 en y")
	y -= 1
	print("y: ", y)

def CCW():
	conteo_1 = 0
	conteo_2 = 0
	conteo_3 = 0
	conteo_4 = 0
	i = 0
	# while i < 200:
	# 	i += 1
	# 	if (i == conteo_1*4 + 1):
	# 		# print("A1, veces que pasa por aqui: ", conteo_1)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(1)
	# 		time.sleep(0.005)
	# 		conteo_1 += 1

	# 	if(i == conteo_2*4 + 2):
	# 		# print("A2, veces que pasa por aqui: ", conteo_2)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(1)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_2 += 1

	# 	if(i == conteo_3*4 + 3):
	# 		# print("B1, veces que pasa por aqui: ", conteo_3)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(1)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_3 += 1

	# 	if(i == conteo_4*4 + 4):
	# 		# print("B2, veces que pasa por aqui: ", conteo_4)
	# 		arduino.digital[IN1].write(1)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_4 += 1

	# # Se pone al final en ceros las salidas para evitar sobrecalentamiento
	# arduino.digital[IN1].write(0)
	# arduino.digital[IN2].write(0)
	# arduino.digital[IN3].write(0)
	# arduino.digital[IN4].write(0)

def ACW():
	conteo_1 = 0
	conteo_2 = 0
	conteo_3 = 0
	conteo_4 = 0
	i = 0
	# while i < 200:
	# 	i += 1
	# 	if (i == conteo_1*4 + 1):
	# 		# print("A1, veces que pasa por aqui: ", conteo_1)
	# 		arduino.digital[IN1].write(1)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_1 += 1

	# 	if(i == conteo_2*4 + 2):
	# 		# print("A2, veces que pasa por aqui: ", conteo_2)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(1)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_2 += 1

	# 	if(i == conteo_3*4 + 3):
	# 		# print("B1, veces que pasa por aqui: ", conteo_3)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(1)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(0)
	# 		time.sleep(0.005)
	# 		conteo_3 += 1

	# 	if(i == conteo_4*4 + 4):
	# 		# print("B2, veces que pasa por aqui: ", conteo_4)
	# 		arduino.digital[IN1].write(0)
	# 		arduino.digital[IN2].write(0)
	# 		arduino.digital[IN3].write(0)
	# 		arduino.digital[IN4].write(1)
	# 		time.sleep(0.005)
	# 		conteo_4 += 1

	# # Se pone al final en ceros las salidas para evitar sobrecalentamiento
	# arduino.digital[IN1].write(0)
	# arduino.digital[IN2].write(0)
	# arduino.digital[IN3].write(0)
	# arduino.digital[IN4].write(0)

def TomaFoto():
	print("Se toman las fotos")

def visualizar():
	global cap, lbl_video
	if cap is not None:
		ret, frame = cap.read()
		if ret == True:
			frame = imutils.resize(frame, width = 300)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			im = Image.fromarray(frame)
			img = ImageTk.PhotoImage(image = im)

			lbl_video.config(image = img)
			lbl_video.pack(anchor = "center")
			lbl_video.image = img
			lbl_video.after(10, visualizar)
		else:
			lbl_video.image = ""
			cap.release()


def IniciarVideo():
	global cap
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	visualizar()

def FinalizarVideo():
	global cap, lbl_video
	lbl_video.config(bg = "lightblue")
	cap.release()

def inicio():
	global win_control
	print("Se regresa al inicio")
	win_control.destroy()
	root.deiconify()

def Auto():
	print("Iniciando analisis y recorrido automatico") # Sustituir despues con las acciones que debe realizar la función

def ruta():
	fichero = FileDialog.askopenfilename(title = "Abrir un fichero", filetypes=(("Imagenes","*.png"), ("Imagenes","*.jpg"), ("Imagenes","*.bmp"), ("Imagenes","*.tiff")))
	print(fichero)
	# Se muestra la imagen en otra pestaña
	img = Image.open(fichero)
	img.show()


def cerrar():
	# Agregar un pop-up para confirmar que se quiere salir de la interfaz
	cerrar_app = MessageBox.askquestion("Salir","¿Estas seguro de que quieres salir?")
	if cerrar_app == "yes":
		root.destroy()
		root.quit()

def Manual():
	global win_control, lbl_video
	print("Se hacen visibles los controles y se cierra la ventana principal")
	# Se cierra a ventana principal
	root.withdraw()
	# Se crea una nueva ventana
	win_control = Toplevel()
	win_control.title("NDVI interface") # Se cambia el nombre de la app
	# win_control.resizable(0,0) # Asi ya no es redimensionable
	win_control.resizable(1,1) # Se puede redimensionar en cualquier dimensión
	# win_control.resizable(1,0) # Se dimensiona en una sola dimensión
	win_control.iconbitmap("Hoja.ico") # Se agrega el icono de la app
	win_control.geometry('800x500') # Se define un tamaño de la ventana inicial
	win_control.config(bg = "lightblue")
	label_win = Label(win_control, text="- Controles para manipulación manual -")
	label_win.pack(anchor = "center")
	label_win.config(bg = "lightblue", font = ("Century Gothic",18))

	# Se van a agregar frames
	Con_Control = Frame(win_control)
	Con_Control.pack(side = RIGHT, padx = 30) # Por defecto no tiene tamaño
	# win_control.config(width=800,heigh=500) # Se define la dimensión
	Con_Control.config(cursor="arrow") # Se define un cursor
	Con_Control.config(bg = "lightgray")
	Con_Control.config(bd = 12)
	Con_Control.config(relief="ridge")

	# Botones para subir y bajar
	Button(Con_Control,text="Arriba", font = ("Century Gothic",12), command = SumaY).pack(side = TOP, pady = 1)
	Button(Con_Control,text="Izquierda", font = ("Century Gothic",12), command = RestaX).pack(side = LEFT, padx = 30)
	Button(Con_Control,text="Derecha", font = ("Century Gothic",12), command = SumaX).pack(side = RIGHT, padx = 30)
	Button(Con_Control,text="Abajo",  font = ("Century Gothic",12), command = RestaY).pack(side = BOTTOM, pady = 10)

	# Boton para tomar fotografía
	Button(win_control,text = "Tomar fotografías", font = ("Century Gothic",12), command = TomaFoto).pack(anchor = "center", pady = 5)

	# Zona donde se muestra el video
	lbl_video = Label(win_control)

	# Boton para iniciar y finalizar video
	Button(win_control, text = "Inicial visialización", font = ("Century Gothic",12), command = IniciarVideo).pack(anchor = "center", pady = 5)
	Button(win_control, text = "Finalizar visualización", font = ("Century Gothic",12), command = FinalizarVideo).pack(anchor = "center", pady = 5)

	# Se va a agregar un menú
	menubar = Menu(win_control)
	win_control.config(menu = menubar)
	filemenu = Menu(menubar, tearoff = 0)
	filemenu.add_command(label="Cerrar", command = cerrar)
	filemenu.add_command(label="Inicio", command = inicio)
	automenu = Menu(menubar, tearoff = 0)
	automenu.add_command(label="Empezar analisis y recorrido automatico", command=Auto)
	manualmenu = Menu(menubar, tearoff = 0)
	manualmenu.add_command(label="Mostrar controles", command=Manual)
	fotomenu = Menu(menubar, tearoff = 0)
	fotomenu.add_command(label = "Abrir", command = ruta) # ventanas emergentes para mostrar información al usuario

	menubar.add_cascade(label = "Archivo", menu = filemenu)
	menubar.add_cascade(label = "Control automatico", menu = automenu)
	menubar.add_cascade(label = "Control manual", menu = manualmenu)
	menubar.add_cascade(label = "Fotografias", menu = fotomenu)

root = Tk()
cap = None
x = 0
y = 0

root.title("NDVI interface") # Se cambia el nombre de la app
# root.resizable(0,0) # Asi ya no es redimensionable
root.resizable(1,1) # Se puede redimensionar en cualquier dimensión
# root.resizable(1,0) # Se dimensiona en una sola dimensión
root.iconbitmap("Hoja.ico") # Se agrega el icono de la app
root.geometry('800x500') # Se define un tamaño de la ventana inicial

# Se van a agregar frames
frame = Frame(root)
frame.pack(fill='both', expand=1) # Por defecto no tiene tamaño
# root.config(width=800,heigh=500) # Se define la dimensión
frame.config(cursor="arrow") # Se define un cursor
frame.config(bg = "lightblue")
frame.config(bd = 12)
frame.config(relief="ridge")

label = Label(frame, text="- Bienvenida/o -")
label.pack(anchor = "center")
label.config(bg = "lightblue", font=("Century Gothic",18))
texto_pregunta = Label(frame,text = "¿Qué acción quieres realizar?")
texto_pregunta.pack(anchor = "center")
texto_pregunta.config(bg = "lightblue", font=("Century Gothic",14))

# Se agregan botones
Button(frame,text="Empezar analisis y recorrido automatico", font = ("Century Gothic",12),command=Auto).pack()
Button(frame,text="Modo manual", font = ("Century Gothic",12) , command=Manual).pack()
Button(frame,text="Fotografias", font = ("Century Gothic",12) ,command = ruta).pack()

# Se va a agregar un menú
menubar = Menu(root)
root.config(menu = menubar)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="Cerrar", command = cerrar)
filemenu.add_command(label="Inicio")
automenu = Menu(menubar, tearoff = 0)
automenu.add_command(label="Empezar analisis y recorrido automatico", command=Auto)
manualmenu = Menu(menubar, tearoff = 0)
manualmenu.add_command(label="Mostrar controles", command=Manual)
fotomenu = Menu(menubar, tearoff = 0)
fotomenu.add_command(label = "Abrir", command = ruta) # ventanas emergentes para mostrar información al usuario

menubar.add_cascade(label = "Archivo", menu = filemenu)
menubar.add_cascade(label = "Control automatico", menu = automenu)
menubar.add_cascade(label = "Control manual", menu = manualmenu)
menubar.add_cascade(label = "Fotografias", menu = fotomenu)

# Abajo de todo
root.mainloop()
