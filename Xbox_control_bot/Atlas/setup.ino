void setup()
{
  pinMode(led, OUTPUT);
  
  Serial.begin(115200);
  digitalWrite(led, LOW);
  
  Serial.println("Connecting to Controller");
  while (!xb4.readGamepad());
  
  Serial.println("Xbox Controller Connected");
}
