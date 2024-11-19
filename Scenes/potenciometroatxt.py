import serial
import time

# Configura el puerto serial (ajusta '/dev/ttyACM0' al puerto correspondiente de tu Arduino si es diferente)
SerialObj = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  

# Nombre del archivo donde se guardarán los datos
output_file = "../MlxInfo.txt"

while True:
    try:
        # Lee una línea de datos del Arduino
        Line = SerialObj.readline()
        
        # Decodifica la línea y elimina saltos de línea y espacios
        Decoded = Line.decode().strip()

        # Verifica que el dato recibido sea un número válido
        if Decoded.isdigit():
            pot_value = int(Decoded)

            # Guarda el valor en el archivo de texto
            with open(output_file, "w") as file:
                file.write(f"{pot_value}")

            print(f"Valor del potenciómetro guardado: {pot_value}")

        # Espera un breve momento antes de leer nuevamente
        time.sleep(0)
        
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        break
    except Exception as e:
        print(f"Error de lectura o guardado: {e}")
        pass