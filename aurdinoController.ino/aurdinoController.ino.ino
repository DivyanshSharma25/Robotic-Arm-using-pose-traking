#include<Servo.h>
Servo s1_a;
Servo s1_b;
Servo s2_a;
Servo s2_b;
Servo s3;
Servo s4;

int newv[]={0,0,0,0,0};
int old[]={0,0,0,0,0};

int sgn(int newv,int old){
  if(newv>old){
    return 1;
  }
  else if(newv==old){
    return 0;
  }
  else{
    return -1;
  }
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  s1_a.attach(8);
  s1_b.attach(9);
  s2_a.attach(10);
  s2_b.attach(11);
  s3.attach(12);
  s4.attach(13);
}

void loop() {
  if (Serial.available() > 0) {
    for(int i=0;i<5;i++){
    String str = Serial.readStringUntil(' ');
    str.trim();
    int a=str.toInt();
    newv[i]=a;
    }
  }
  s1_a.write(old[0]+sgn(newv[0],old[0]));
  s1_b.write(180-(old[0]+sgn(newv[0],old[0])));

  s2_a.write(old[1]+sgn(newv[1],old[1]));
  s2_b.write(180-(old[1]+sgn(newv[1],old[1])));

  s3.write(180-newv[2]);
  s4.write(newv[3]);

  delay(10);
  for(int i=0;i<5;i++){
    old[i]=old[i]+sgn(newv[i],old[i]);
  }
  
}
