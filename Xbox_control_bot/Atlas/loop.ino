void loop()
{
//  if (xb4.readGamepad())
//  {
//    if (xb4.buttonPressed(HOME))
//    {
//      powerOn = !powerOn;
//      Serial.println("POWER : " + String((powerOn) ? "ON" : "OFF"));
//    }
//    if (powerOn)
//    {
//      Lx = map(xb4.axis(LX), 0, 65535, -32768, 32767);
//      Ly = map(xb4.axis(LY), 0, 65535, -32768, 32767);
//      Rx = map(xb4.axis(RX), 0, 65535, -32768, 32767);
//      Ry = map(xb4.axis(RY), 0, 65535, -32768, 32767);
//      Serial.print("LX:\t");
//      Serial.print(Lx);
//      Serial.print("\tLY:\t");
//      Serial.print(Ly);
//      Serial.print("\tRX:\t");
//      Serial.print(Rx);
//      Serial.print("\tRY:\t");
//      Serial.println(Ry);
//
//      if (xb4.button(A))
//      {
//        Serial.println("\tA\t");
//      }
//
//      else if (xb4.button(B))
//      {
//        Serial.println("\tB\t");
//      }
//
//      else if (xb4.button(X))
//      {
//        Serial.println("\tX\t");
//      }
//
//      else if (xb4.button(X))
//      {
//        Serial.println("\tX\t");
//      }
//      else
//      {
//        Serial.println("Nothing recieving currently");
//      }
//    }
//  }
//  else
//  {
//    Serial.println("Not connected");
//  }
//  digitalWrite(led, HIGH);
  if(xb4.readGamepad())
  {
    if(xb4.buttonPressed(HOME))
    {
      powerOn = !powerOn;
      Serial.println("POWER : " + String((powerOn) ? "ON" : "OFF"));
    }
  }
}
