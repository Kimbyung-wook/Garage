#define GPIO_S3 10
#define GPIO_S2  9
#define GPIO_D6 12
#define GPIO_D5 14
#define GPIO_D4  2

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(GPIO_D6, OUTPUT);
  pinMode(GPIO_D4, OUTPUT);
  pinMode(GPIO_D5, INPUT );

  digitalWrite(GPIO_D6, HIGH);  // turn the LED on (HIGH is the voltage level)
  digitalWrite(GPIO_D5, HIGH);  // turn the LED on (HIGH is the voltage level)

}

// the loop function runs over and over again forever
void loop() {
  int t = (int)digitalRead(GPIO_D5);
  digitalWrite(LED_BUILTIN, t);  // turn the LED on (HIGH is the voltage level)
  digitalWrite(GPIO_D6, t);  // turn the LED on (HIGH is the voltage level)
  delay(1000);                      // wait for a second
  digitalWrite(LED_BUILTIN, t);   // turn the LED off by making the voltage LOW
  digitalWrite(GPIO_D6, t);   // turn the LED off by making the voltage LOW
  delay(1000);                      // wait for a second
}
