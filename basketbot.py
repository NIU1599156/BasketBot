import cv2
import time
import numpy as np

from gpiozero import Motor
import board
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685



def detectar_vaso(imagen):
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

	rojo_bajo = np.array([0, 100, 20])
	rojo_alto = np.array([8, 255, 255])

	rojo_bajo2 = np.array([175, 100, 20])
	rojo_alto2 = np.array([179, 255, 255])

	mascara1 = cv2.inRange(hsv, rojo_bajo, rojo_alto)
	mascara2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
	mascara = cv2.bitwise_or(mascara1, mascara2)

	mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

	contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	if (len(contornos)>0):
		max_contorn = max(contornos, key=cv2.contourArea)
		return cv2.boundingRect(max_contorn)
	else:
		return 0,0,0,0
	
def girar_servo(servo, rango):
	rango = list(rango)
	if (len(rango) > 0):
		if rango[-1] > 180:
			rango = range(rango[0], 180)
	for i in rango:
		servo.angle = i
		time.sleep(0.05)
	

if __name__ == "__main__":
	
	# Inicializar motores y cámara
	# Motores DC
	E1 = 13
	M1 = 26
	E2 = 12
	M2 = 16
	m1 = Motor(E1, M1, pwm=True)
	m2 = Motor(E2, M2, pwm=True)
	
	# Servos
	i2c = busio.I2C(board.SCL, board.SDA)
	pca = PCA9685(i2c)
	pca.frequency = 50
	servo_base = servo.Servo(pca.channels[0], actuation_range=180)
	servo_barrera = servo.Servo(pca.channels[3], actuation_range=180)
	
	# Inicializamos valores constantes
	h_taza=1250
	vmax = 1.727
	
	while(True):
		x= input("Start? [y/n]: ")
		if(x == "y"):
			# Ponerlos en posición inicial
			girar_servo(servo_base, range(int(servo_base.angle),0,-1))
			girar_servo(servo_barrera, range(int(servo_barrera.angle),180))
			m1.stop()
			m2.stop()
			
			time.sleep(3)
			
			encontrado = False
			while(not encontrado and servo_base.angle<180):
				# Sacar imagen de la cámara
				cap = cv2.VideoCapture(0)
				ret,imagen = cap.read()
				
				if (not ret):
					print("Error con la camara")
					break
				
				# Buscar vaso
				x, y, w, h = detectar_vaso(imagen)
				
				# Comprovar si hay vaso
				min_area = 1000
				
				if (h*w > min_area):
					min_x = imagen.shape[1]*4/9
					max_x = imagen.shape[1]*5/9
					# Comprovar si se encuentra en el centro
					if (x+w/2>min_x and x+w/2<max_x):
						encontrado=True
					else:
						# Comprovar hacia donde tiene que girar el servo para centrarlo
						if (x+w/2>max_x):
							girar_servo(servo_base, range(int(servo_base.angle),int(servo_base.angle)-5, -1))
						else:
							girar_servo(servo_base, range(int(servo_base.angle),int(servo_base.angle)+5))
				else:
					# Mover servo
					girar_servo(servo_base, range(int(servo_base.angle),int(servo_base.angle)+30))
				
				time.sleep(1)
				cap.release()
			
			# Calcular distancia
			distancia = (h_taza * 515) / h
			print("Distancia: ", distancia)
			
			# Calcular velocidad de los motores
			v = (4.6 * distancia) / (np.cos(30) * np.sin(30) )
			radi = 2.8
			w = v/radi
			p = w / vmax

			if (w /vmax > 1):
				print("Error, el objetivo está demasiado lejos")
				break

			# Activar las ruedas y abrir la barrera
			m1.forward(p)
			m2.forward(p)
			girar_servo(servo_barrera, range(180,60,-1))
			
			time.sleep(5)
			m1.stop()
			m2.stop()
		else:
			break
