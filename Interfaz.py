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
diametro_polea = 25.4 # en mm
no_pi = 3.1415
perimetro = no_pi*diametro_polea
i_grade = 0

conteo_1_ccw_x = 0
conteo_2_ccw_x = 0
conteo_3_ccw_x = 0
conteo_4_ccw_x = 0
i_ccw_x = 0
conteo_1_ccw_y = 0
conteo_2_ccw_y = 0
conteo_3_ccw_y = 0
conteo_4_ccw_y = 0
i_ccw_y = 0
conteo_1_ccw_angle = 0
conteo_2_ccw_angle = 0
conteo_3_ccw_angle = 0
conteo_4_ccw_angle = 0
i_ccw_angle = 0

conteo_1_acw_x = 0
conteo_2_acw_x = 0
conteo_3_acw_x = 0
conteo_4_acw_x = 0
i_acw_x = 0
conteo_1_acw_y = 0
conteo_2_acw_y = 0
conteo_3_acw_y = 0
conteo_4_acw_y = 0
i_acw_y = 0
conteo_1_acw_angle = 0
conteo_2_acw_angle = 0
conteo_3_acw_angle = 0
conteo_4_acw_angle = 0
i_acw_angle = 0

# Puerto del Arduino 

def RotDe():
	global grade, i_grade
	if (i_grade < 13):
		i_grade +=1
		if (i_grade < 14 and i_grade > -14):
			grade = i_grade*paso
			print("Grade: ", grade, "°, iteracion en angulo :", i_grade)
			# Se mueve en dirección horaria
			CCW(3)
			# Se imprime la posición en la interfaz
			PosAngle = "Rotación: " + str("{0:0.2f}".format(grade)) + "°"
			textoAng.set(PosAngle)
			lbl_posAng.config(textvariable=textoAng)
			lbl_posAng.pack(anchor = "center")
	else:
		print("No puedes girar más la cámara o dañarás el equipo")

def RotIz():
	global grade, i_grade
	if (i_grade > -13):
		i_grade -=1
		if (i_grade < 14 and i_grade > -14):
			grade = i_grade*paso
			print("Grade: ", grade, "°, iteracion en angulo :", i_grade)
			# Se mueve en dirección antihoraria
			ACW(3)
			# Se imprime la posición en la interfaz
			PosAngle = "Rotación: " + str("{0:0.2f}".format(grade)) + "°"
			textoAng.set(PosAngle)
			lbl_posAng.config(textvariable=textoAng)
			lbl_posAng.pack(anchor = "center")
	else:
		print("No puedes girar más la cámara o dañarás el equipo")

def SumaX():
	global x
	print("Se suma 1 en x")
	x += 1
	print("x: ", x)
	# Se mueve en dirección horaria
	CCW(1)
	# Se calcula la posición
	xl = x*perimetro/200
	coorX = 'X: ' + str("{0:0.2f}".format(xl)) + " mm"
	textoX.set(coorX)
	lbl_posX.config(textvariable=textoX)
	lbl_posX.pack(anchor = "center")

def RestaX():
	global x
	if x < 1:
		print("No se puede realizar esta acción, te encuentras al limite de X")
	else:
		print("Se resta 1 en x")
		x -= 1
		print("x: ", x)
		# Se mueve en dirección antihoraria
		ACW(1)
		# Se calcula la posición
		xl = x*perimetro/200
		coorX = 'X: ' + str("{0:0.2f}".format(xl)) + " mm"
		textoX.set(coorX)
		lbl_posX.config(textvariable=textoX)
		lbl_posX.pack(anchor = "center")


def SumaY():
	global y
	print("Se suma 1 en y")
	y += 1
	print("y: ", y)
	CCW(2)
	# Se calcula la posición
	yl = y*perimetro/200
	coorY = 'Y: ' + str("{0:0.2f}".format(yl)) + " mm"
	textoY.set(coorY)
	lbl_posY.config(textvariable=textoY)
	lbl_posY.pack(anchor = "center")

def RestaY():
	global y
	if y < 1:
		print("No se puede realizar esta acción, te encuentras al limite de Y")
	else:
		print("Se resta 1 en y")
		y -= 1
		print("y: ", y)
		ACW(2)
		# Se calcula la posición
		yl = y*perimetro/200
		coorY = 'Y: ' + str("{0:0.2f}".format(yl)) + " mm"
		textoY.set(coorY)
		lbl_posY.config(textvariable=textoY)
		lbl_posY.pack(anchor = "center")

def CCW(u):
	global conteo_1_ccw_x, conteo_2_ccw_x, conteo_3_ccw_x, conteo_4_ccw_x, conteo_1_ccw_y, conteo_2_ccw_y, conteo_3_ccw_y, conteo_4_ccw_y, i_ccw_x, i_ccw_y
	global i_ccw_angle, conteo_1_ccw_angle, conteo_2_ccw_angle, conteo_3_ccw_angle, conteo_4_ccw_angle
	iteracion = 0
	if u == 1:	
		print("X")
		i_ccw = i_ccw_x
	elif u == 3:
		print("Cámara")
		i_ccw = i_ccw_angle
	else:
		print("Y")
		i_ccw = i_ccw_y

	while iteracion < 1:
		iteracion += 1
		i_ccw += 1
		if ((i_ccw == conteo_1_ccw_x*4 + 1) or (i_ccw == conteo_1_ccw_y*4 + 1) or (i_ccw == conteo_1_ccw_angle*4 + 1)):
			if u == 1:	
				print("A1 X, veces que pasa por aqui: ", conteo_1_ccw_x)
				conteo_1_ccw_x += 1
				i_ccw_x = i_ccw
			elif u == 3:	
				print("A1 Cam, veces que pasa por aqui: ", conteo_1_ccw_angle)
				conteo_1_ccw_angle += 1
				i_ccw_angle = i_ccw
			else:
				print("A1 Y, veces que pasa por aqui: ", conteo_1_ccw_y)
				conteo_1_ccw_y += 1
				i_ccw_y = i_ccw

		if ((i_ccw == conteo_2_ccw_x*4 + 2) or (i_ccw == conteo_2_ccw_y*4 + 2) or i_ccw == conteo_2_ccw_angle*4 + 2):
			if u == 1:	
				print("A2 X, veces que pasa por aqui: ", conteo_2_ccw_x)
				conteo_2_ccw_x += 1
				i_ccw_x = i_ccw
			elif u == 3:	
				print("A2 Cam, veces que pasa por aqui: ", conteo_2_ccw_angle)
				conteo_2_ccw_angle += 1
				i_ccw_angle = i_ccw
			else:
				print("A2 Y, veces que pasa por aqui: ", conteo_2_ccw_y)
				conteo_2_ccw_y += 1
				i_ccw_y = i_ccw

		if ((i_ccw == conteo_3_ccw_x*4 + 3) or (i_ccw == conteo_3_ccw_y*4 + 3) or (i_ccw == conteo_3_ccw_angle*4 + 3)):
			if u == 1:	
				print("B1 X, veces que pasa por aqui: ", conteo_3_ccw_x)
				conteo_3_ccw_x += 1
				i_ccw_x = i_ccw
			elif u == 3:	
				print("B1 Cam, veces que pasa por aqui: ", conteo_3_ccw_angle)
				conteo_3_ccw_angle += 1
				i_ccw_angle = i_ccw
			else:
				print("B1 Y, veces que pasa por aqui: ", conteo_3_ccw_y)
				conteo_3_ccw_y += 1
				i_ccw_y = i_ccw

		if ((i_ccw == conteo_4_ccw_x*4 + 4) or (i_ccw == conteo_4_ccw_y*4 + 4) or (i_ccw == conteo_4_ccw_angle*4 + 4)):
			if u == 1:	
				print("B2 X, veces que pasa por aqui: ", conteo_4_ccw_x)
				conteo_4_ccw_x += 1
				i_ccw_x = i_ccw
			elif u == 3:	
				print("B2 Cam, veces que pasa por aqui: ", conteo_4_ccw_angle)
				conteo_4_ccw_angle += 1
				i_ccw_angle = i_ccw
			else:
				print("B2 Y, veces que pasa por aqui: ", conteo_4_ccw_y)
				conteo_4_ccw_y += 1
				i_ccw_y = i_ccw

	# Se pone al final en ceros las salidas para evitar sobrecalentamiento
	if (i_ccw == 200):
		if u == 1:	
			i_ccw_x = 0;
			conteo_1_ccw_x = 0
			conteo_2_ccw_x = 0
			conteo_3_ccw_x = 0
			conteo_4_ccw_x = 0
		elif u == 3:	
			i_ccw_angle = 0;
			conteo_1_ccw_angle = 0
			conteo_2_ccw_angle = 0
			conteo_3_ccw_angle = 0
			conteo_4_ccw_angle = 0
		else:
			i_ccw_y = 0;
			conteo_1_ccw_y = 0
			conteo_2_ccw_y = 0
			conteo_3_ccw_y = 0
			conteo_4_ccw_y = 0
	


def ACW(u):
	global conteo_1_acw_x, conteo_2_acw_x, conteo_3_acw_x, conteo_4_acw_x, conteo_1_acw_y, conteo_2_acw_y, conteo_3_acw_y, conteo_4_acw_y, i_acw_x, i_acw_y
	global i_acw_angle, conteo_1_acw_angle, conteo_2_acw_angle, conteo_3_acw_angle, conteo_4_acw_angle
	iteracion = 0
	if u == 1:	
		print("X")
		i_acw = i_acw_x
	elif u == 3:
		print("Cámara")
		i_acw = i_acw_angle
	else:
		print("Y")
		i_acw = i_acw_y

	while iteracion < 1:
		iteracion += 1
		i_acw += 1
		if ((i_acw == conteo_1_acw_x*4 + 1) or (i_acw == conteo_1_acw_y*4 + 1) or (i_acw == conteo_1_acw_angle*4 + 1)):
			if u == 1:	
				print("A1 X, veces que pasa por aqui: ", conteo_1_acw_x)
				conteo_1_acw_x += 1
				i_acw_x = i_acw
			elif u == 3:	
				print("A1 Cam, veces que pasa por aqui: ", conteo_1_acw_angle)
				conteo_1_acw_angle += 1
				i_acw_angle = i_acw
			else:
				print("A1 Y, veces que pasa por aqui: ", conteo_1_acw_y)
				conteo_1_acw_y += 1
				i_acw_y = i_acw

		if ((i_acw == conteo_2_acw_x*4 + 2) or (i_acw == conteo_2_acw_y*4 + 2) or (i_acw == conteo_2_acw_angle*4 + 2)):
			if u == 1:	
				print("A2 X, veces que pasa por aqui: ", conteo_2_acw_x)
				conteo_2_acw_x += 1
				i_acw_x = i_acw
			elif u == 3:	
				print("A2 Cam, veces que pasa por aqui: ", conteo_2_acw_angle)
				conteo_2_acw_angle += 1
				i_acw_angle = i_acw
			else:
				print("A2 Y, veces que pasa por aqui: ", conteo_2_acw_y)
				conteo_2_acw_y += 1
				i_acw_y = i_acw

		if ((i_acw == conteo_3_acw_x*4 + 3) or (i_acw == conteo_3_acw_y*4 + 3) or (i_acw == conteo_3_acw_angle*4 + 3)):
			if u == 1:	
				print("B1 X, veces que pasa por aqui: ", conteo_3_acw_x)
				conteo_3_acw_x += 1
				i_acw_x = i_acw
			elif u == 3:	
				print("B1 Cam, veces que pasa por aqui: ", conteo_3_acw_angle)
				conteo_3_acw_angle += 1
				i_acw_angle = i_acw
			else:
				print("B1 Y, veces que pasa por aqui: ", conteo_3_acw_y)
				conteo_3_acw_y += 1
				i_acw_y = i_acw

		if ((i_acw == conteo_4_acw_x*4 + 4) or (i_acw == conteo_4_acw_y*4 + 4) or (i_acw == conteo_4_acw_angle*4 + 4)):
			if u == 1:	
				print("B2 X, veces que pasa por aqui: ", conteo_4_acw_x)
				conteo_4_acw_x += 1
				i_acw_x = i_acw
			elif u == 3:	
				print("B2 Cam, veces que pasa por aqui: ", conteo_4_acw_angle)
				conteo_4_acw_angle += 1
				i_acw_angle = i_acw
			else:
				print("B2 Y, veces que pasa por aqui: ", conteo_4_acw_y)
				conteo_4_acw_y += 1
				i_acw_y = i_acw

	# Se pone al final en ceros las salidas para evitar sobrecalentamiento
	if (i_acw == 200):
		if u == 1:	
			i_acw_x = 0;
			conteo_1_acw_x = 0
			conteo_2_acw_x = 0
			conteo_3_acw_x = 0
			conteo_4_acw_x = 0
		elif u == 3:	
			i_acw_angle = 0;
			conteo_1_acw_angle = 0
			conteo_2_acw_angle = 0
			conteo_3_acw_angle = 0
			conteo_4_acw_angle = 0
		else:
			i_acw_y = 0;
			conteo_1_acw_y = 0
			conteo_2_acw_y = 0
			conteo_3_acw_y = 0
			conteo_4_acw_y = 0

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

def EmergenciaLim():
	MessageBox.showwarning("Cuidado", "Estas en el límite de carrera, si sigues el sistema podría dañarse")

def EmergenciaTem():
	MessageBox.showwarning("Cuidado", "La temperatura del sistema es demasiado alta, utilizarlo en estas condiciones puede ser perjudicial para su funcionamiento")

def Manual():
	global win_control, lbl_video, lbl_posX, lbl_posY,lbl_posAng, textoX, textoY, textoAng
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


	# Se pone texto arriba de los controles
	lbl_posX = Label(win_control, bg = "lightblue")
	lbl_posY = Label(win_control, bg = "lightblue") 
	lbl_posAng = Label(win_control, bg = "lightblue") 

	textoX = StringVar()
	textoX.set("X: 0.00 mm")
	lbl_posX.config(textvariable=textoX)
	lbl_posX.pack(anchor = "center")

	textoY = StringVar()
	textoY.set("Y: 0.00 mm")
	lbl_posY.config(textvariable=textoY)
	lbl_posY.pack(anchor = "center")

	textoAng = StringVar()
	textoAng.set("Rotación: 0.00°")
	lbl_posAng.config(textvariable=textoAng)
	lbl_posAng.pack(anchor = "center")

	# Se van a agregar frames
	Con_Control = Frame(win_control)
	Con_Control.pack(side = RIGHT, padx = 30) # Por defecto no tiene tamaño
	# win_control.config(width=800,heigh=500) # Se define la dimensión
	Con_Control.config(cursor="arrow") # Se define un cursor
	Con_Control.config(bg = "lightgray")
	Con_Control.config(bd = 12)
	Con_Control.config(relief="ridge")
	
	# Se crea un frame para controles de camara
	Con_Cam = Frame(Con_Control)
	Con_Cam.pack(side = TOP, pady = 3) # Por defecto no tiene tamaño
	# win_control.config(width=800,heigh=500) # Se define la dimensión
	Con_Cam.config(cursor="arrow") # Se define un cursor
	Con_Cam.config(bg = "lightgray")

	# Botones para girar la cámara
	Button(Con_Cam,text="Rotar derecha", font = ("Century Gothic",12), command = RotDe).pack(side = RIGHT, pady = 3, padx = 6)
	Button(Con_Cam,text="Rotar izquierda", font = ("Century Gothic",12), command = RotIz).pack(side = LEFT, pady = 3)

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
grade = 0

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
