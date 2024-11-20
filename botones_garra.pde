import processing.serial.*;

Serial myPort;
PButton derechaBtn, izquierdaBtn;

void setup() {
  size(300, 200);               // Tamaño de la ventana
  println(Serial.list());       // Imprimir los puertos disponibles
  myPort = new Serial(this, Serial.list()[0], 9600);  // Conectar al puerto correcto
  // Crear botones
  derechaBtn = new PButton("Soltar", 50, 50, 100, 50);
  izquierdaBtn = new PButton("Presionar", 150, 50, 100, 50);
}

void draw() {
  background(255);
  
  // Mostrar botones
  derechaBtn.display();
  izquierdaBtn.display();
}

void mousePressed() {
  if (derechaBtn.isClicked(mouseX, mouseY)) {
    myPort.write('D');  // Enviar comando 'Derecha'
  } else if (izquierdaBtn.isClicked(mouseX, mouseY)) {
    myPort.write('I');  // Enviar comando 'Izquierda'
  }
}

void mouseReleased() {
  myPort.write('S');  // Detener el motor cuando se suelta el botón
}

// Clase para manejar botones
class PButton {
  String label;
  int x, y, w, h;
  
  PButton(String label, int x, int y, int w, int h) {
    this.label = label;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }
  
  void display() {
    fill(200);
    rect(x, y, w, h);
    fill(0);
    textAlign(CENTER, CENTER);
    text(label, x + w/2, y + h/2);
  }
  
  boolean isClicked(int mx, int my) {
    return mx > x && mx < x + w && my > y && my < y + h;
  }
}