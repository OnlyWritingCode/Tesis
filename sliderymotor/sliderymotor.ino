#include <AFMotor.h>

// Inicializar el motor en el puerto 1
AF_DCMotor motor(1);

// Definir el pin del potenciómetro
int potPin = A1;
int potValue = 0;

void setup() {
  // Iniciar la comunicación serial a 9600 bps
  Serial.begin(9600);
  
  // Configurar la velocidad del motor al máximo inicial
  motor.setSpeed(255); 
}

void loop() {
  // ===== CONTROL DEL MOTOR CON PROCESSING =====
  // Si hay datos disponibles desde Processing, leer el comando
  if (Serial.available()) {
    char command = Serial.read();  // Lee el comando enviado desde Processing

    if (command == 'D') {
      motor.setSpeed(255);  // Configura la velocidad máxima
      motor.run(FORWARD);   // Mueve el motor hacia la derecha
    } 
    else if (command == 'I') {
      motor.setSpeed(255);  // Configura la velocidad máxima
      motor.run(BACKWARD);  // Mueve el motor hacia la izquierda
    } 
    else if (command == 'S') {
      motor.run(RELEASE);   // Detiene el motor
    }
  }
  
  // ===== LECTURA DEL SLIDER (POTENCIÓMETRO) =====
  // Leer el valor del potenciómetro (entre 0 y 1023)
  potValue = analogRead(potPin);
  
  // Enviar el valor del potenciómetro al puerto serial para Python
  Serial.println(potValue);
  
  // Pausa para evitar lecturas excesivas (ajusta el delay según sea necesario)
  delay(100);
}