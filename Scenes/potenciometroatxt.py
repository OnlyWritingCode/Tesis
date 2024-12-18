import serial
import time
import os  # Importamos el módulo os para trabajar con rutas

# Configura el puerto serial (ajusta '/dev/ttyACM0' al puerto correspondiente de tu Arduino si es diferente)
SerialObj = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  

# Obtener la ruta absoluta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Nombre del archivo donde se guardarán los datos (en la misma carpeta que el script)
output_file = os.path.join(script_dir, "MlxInfo.txt")

while True:
    try:
        # Lee una línea de datos del Arduino
        Line = SerialObj.readline()
        
        # Decodifica la línea y elimina saltos de línea y espacios
        Decoded = Line.decode().strip()

        # Verifica que el dato recibido sea un número válido
        if Decoded.isdigit():
            pot_value = int(Decoded)
            distance_value = pot_value/1023.0 * 60

            # Guarda el valor en el archivo de texto
            with open(output_file, "w") as file:
                file.write(f"{pot_value},{distance_value}")

            print(f"Valor del potenciómetro guardado: {pot_value}, {distance_value}")

        # Espera un breve momento antes de leer nuevamente
        time.sleep(0)
        
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        break
    except Exception as e:
        print(f"Error de lectura o guardado: {e}")
        pass

