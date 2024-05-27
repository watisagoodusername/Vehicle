int enaL = 11;
int enaR = 10;
int in1 = 7;
int in2 = 6;
int in3 = 5;
int in4 = 4;
int idk = 2;

void setup() {
pinMode(idk, OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in2, OUTPUT);
pinMode(in3, OUTPUT);
pinMode(in4, OUTPUT);
pinMode(enaL, OUTPUT);
pinMode(enaR, OUTPUT);

Serial.begin(9600);
}

void loop() {
  int number;
  int Lval;
  int Rval;
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    number = data.toInt();
    Lval = 4*number/4 + 80;
    Rval = -4*number/4 + 80;
    if (number == 100) {
        Lval = 0;
        Rval = 80;
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        digitalWrite(in3,HIGH);
        digitalWrite(in4,LOW);
    } else if(number == -100) {
        Lval = 80;
        Rval = 0;
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        digitalWrite(in3,LOW);
        digitalWrite(in4,HIGH);
    } else {
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        digitalWrite(in3,LOW);
        digitalWrite(in4,HIGH);
    }
    if (Rval < 10) {
       digitalWrite(in4, LOW);
    }
    analogWrite(enaL, Lval);
    analogWrite(enaR, Rval);
  }


}
