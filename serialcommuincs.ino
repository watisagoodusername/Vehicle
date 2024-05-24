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
    Lval = 2*number/5 + 40;
    Rval = -2*number/5 + 40;
    analogWrite(enaL, Lval);
    analogWrite(enaR, Rval);
  }


}
