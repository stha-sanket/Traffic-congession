#include <Servo.h> // Includes the servo library
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Initialize the LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myservo;

// Define IR sensor pins
#define ir_enter 2
#define ir_back  4
#define ir_car1 5
#define ir_car2 6
#define ir_car3 7
#define ir_car4 8
#define ir_car5 9
#define ir_car6 10

// Variables to store sensor states
int S1=0, S2=0, S3=0, S4=0, S5=0, S6=0;
int flag1=0, flag2=0; 
int slot = 6;  

void setup() {
  Serial.begin(9600);
  
  // Set sensor pins as input
  pinMode(ir_car1, INPUT);
  pinMode(ir_car2, INPUT);
  pinMode(ir_car3, INPUT);
  pinMode(ir_car4, INPUT);
  pinMode(ir_car5, INPUT);
  pinMode(ir_car6, INPUT);
  pinMode(ir_enter, INPUT);
  pinMode(ir_back, INPUT);
  
  // Attach the servo to pin 3 and set its initial position
  myservo.attach(3);
  myservo.write(0);
  
  // Initialize the LCD
  lcd.begin(16, 2);  
  lcd.backlight(); // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("    Car Parking  ");
  lcd.setCursor(0, 1);
  lcd.print("      System     ");
  delay(2000);
  lcd.clear();   
  
  // Read the initial sensor states
  Read_Sensor();
  int total = S1 + S2 + S3 + S4 + S5 + S6;
  slot = slot - total; 

  // Print initial state to Serial Monitor
  Serial.print("Initial slots available: ");
  Serial.println(slot);
}

void loop() {
  Read_Sensor();
  int total = S1 + S2 + S3 + S4 + S5 + S6;
  slot = 6 - total;
  
  // Display available slots on LCD and Serial Monitor
  lcd.setCursor(0, 0);
  lcd.print("   Have Slot: "); 
  lcd.print(slot);
  lcd.print("    ");
  Serial.print("Available slots: ");
  Serial.println(slot);
  
  // Display sensor statuses on LCD and Serial Monitor
  lcd.setCursor(0, 1);
  if (S1 == 1) { lcd.print("S1:F "); Serial.print("S1: Full "); } else { lcd.print("S1:Etm"); Serial.print("S1: Empty "); }
  lcd.setCursor(10, 1);
  if (S2 == 1) { lcd.print("S2:F "); Serial.print("S2: Full "); } else { lcd.print("S2:Etm"); Serial.print("S2: Empty "); }
  delay(500);
  lcd.clear();
  
  lcd.setCursor(0, 0);
  if (S3 == 1) { lcd.print("S3:F "); Serial.print("S3: Full "); } else { lcd.print("S3:Etm"); Serial.print("S3: Empty "); }
  lcd.setCursor(10, 0);
  if (S4 == 1) { lcd.print("S4:F "); Serial.print("S4: Full "); } else { lcd.print("S4:Etm"); Serial.print("S4: Empty "); }
  lcd.setCursor(0, 1);
  if (S5 == 1) { lcd.print("S5:F "); Serial.print("S5: Full "); } else { lcd.print("S5:Etm"); Serial.print("S5: Empty "); }
  lcd.setCursor(10, 1);
  if (S6 == 1) { lcd.print("S6:F"); Serial.print("S6: Full"); } else { lcd.print("S6:Etm"); Serial.print("S6: Empty"); }
  delay(500);
  lcd.clear();

  // Handle entrance logic
  if (digitalRead(ir_enter) == 0) {
    if (slot > 0) {
myservo.write(90);
delay(4000); // Allow some time for the gate to open
        myservo.write(0);
        slot = slot - 1;
        Serial.println("Car entered. Gate opened.");
      
    } else {
      lcd.setCursor(0, 0);
      lcd.print(" Sorry Parking Full ");  
      delay(1500);
      Serial.println("Sorry, parking full.");
    }
  }

  // Handle exit logic
  if (digitalRead(ir_back) == 0 && flag2 == 0) {
    
    if (slot > 0) {
      myservo.write(90);
      delay(4000); // Allow some time for the gate to open
      myservo.write(0);

      slot = slot + 1;
      Serial.println("Car exited. Gate opened.");
    }
  }

  // Close the gate if both entrance and exit were triggered
  if (flag1 == 1 && flag2 == 1) {
    delay(1000);
    myservo.write(0);
    flag1 = 0;

    
    flag2 = 0;
    Serial.println("Gate closed.");
  }
  
  delay(1);
}

void Read_Sensor() {
  // Reset sensor states
  S1 = 0; S2 = 0; S3 = 0; S4 = 0; S5 = 0; S6 = 0;
  
  // Read each sensor and update state
  if (digitalRead(ir_car1) == 0) { S1 = 1; }
  if (digitalRead(ir_car2) == 0) { S2 = 1; }
  if (digitalRead(ir_car3) == 0) { S3 = 1; }
  if (digitalRead(ir_car4) == 0) { S4 = 1; }
  if (digitalRead(ir_car5) == 0) { S5 = 1; }
  if (digitalRead(ir_car6) == 0) { S6 = 1; }  
}
