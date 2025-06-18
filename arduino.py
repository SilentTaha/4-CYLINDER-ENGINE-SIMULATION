const int fsEngineSound = 2; // +1 to the cylinder order
const int sdEngineSound = 3;
const int tdEngineSound = 4;
const int ftEngineSound = 5;
const int throttlingSensor = 8;
const int warningTest = 7;
const int trLimit = 4000;
const int throttlingInput = A5;
const int gearUpSensor = 10;
const int gearDownSensor = 9;
int acceleration = 410;
int controlTrLimit = 4000;
bool engineOn = false;
const int alwaysOn = 11;
const int engineOnOffInput = 6;
int gearNumber = 0;

int trPerMinute = 1200;// kawasaki z750 (749cc)
int trPerMinuteAddThrottling = 410;
int trPerMinuteRemoveThrottling = 200;
// added tr per minute
float exploseSpeed = (trPerMinute / 120);
float exploseTime = 1 / exploseSpeed;

void setup()
{
  Serial.begin(9600);
  //OUTPUT:
  pinMode(fsEngineSound, OUTPUT);
  pinMode(sdEngineSound, OUTPUT);
  pinMode(tdEngineSound, OUTPUT);
  pinMode(ftEngineSound, OUTPUT);
  pinMode(engineOnOffInput, INPUT);
  pinMode(warningTest, OUTPUT);
  pinMode(alwaysOn, OUTPUT);
  pinMode(throttlingInput, INPUT);
  pinMode(gearDownSensor, INPUT);
  pinMode(gearUpSensor, INPUT);
  
  //INPUT:
  pinMode(throttlingSensor, INPUT_PULLUP);
 
}

void cylinder1Loop()
{
  digitalWrite(fsEngineSound, HIGH);
  delay(exploseTime * 1000 / 4);
  
  digitalWrite(fsEngineSound, LOW);
  delay(exploseTime * 1000 / 4);
  
}
void cylinder2Loop()
{
  digitalWrite(sdEngineSound, HIGH);
  delay(exploseTime * 1000 /4 );
  
  digitalWrite(sdEngineSound, LOW);
  delay(exploseTime * 1000 / 4);
  
}
void cylinder3Loop()
{
  digitalWrite(tdEngineSound, HIGH);
  delay(exploseTime * 1000 /4);
  
  digitalWrite(tdEngineSound, LOW);
  delay(exploseTime * 1000 /4);
  
}
void cylinder4Loop()
{
  digitalWrite(ftEngineSound, HIGH);
  delay(exploseTime * 1000 /4);
  
  digitalWrite(ftEngineSound, LOW);
  delay(exploseTime * 1000 /4);
  
}

void engineOneCycle()
{
  exploseSpeed = (trPerMinute / 120);
  exploseTime = 1 / exploseSpeed;
  
  cylinder1Loop();
  cylinder2Loop();
  cylinder3Loop();
  cylinder4Loop();
}

void throttling()
{
  
  
  trPerMinute += trPerMinuteAddThrottling;
}



void unHoldThrottling()
{
  if(trPerMinute > 900)
  {
    trPerMinute -= trPerMinuteRemoveThrottling;
  }
}



void accelerate()
{
  
  trPerMinuteAddThrottling = analogRead(throttlingInput) * 4;
  trPerMinute += trPerMinuteAddThrottling;
}


void gearShiftUP()
{
  gearNumber++;
  
  if(trPerMinute > 1500)
  {
    trPerMinute -= 1200;
  }

}

void gearShiftDown()
{
  gearNumber--;
  if(trPerMinute < 3200)
  {
    trPerMinute += 1200;
  }
  

}

void actualGear(int appliedGear)
{
  if(appliedGear == 1)
  {
    trPerMinuteAddThrottling = 150;
    trPerMinuteRemoveThrottling = 150;
  }
  else if(appliedGear == 2)
  {
    trPerMinuteAddThrottling = 90;
    trPerMinuteRemoveThrottling = 90;
  }
  else if(appliedGear == 3)
  {
    trPerMinuteAddThrottling = 70;
    trPerMinuteRemoveThrottling = 70;
  }
  else if(appliedGear == 4)
  {
    trPerMinuteAddThrottling = 60;
    trPerMinuteRemoveThrottling = 60;
  }
  else if(appliedGear == 5)
  {
    trPerMinuteAddThrottling = 50;
    trPerMinuteRemoveThrottling = 50;
  }
  else if(appliedGear == 6)
  {
    trPerMinuteAddThrottling = 30;
    trPerMinuteRemoveThrottling = 30;
  }
  else // it can be 7 for example
  {
    // in this case the selected gear is: N
    trPerMinuteAddThrottling = 410;
    trPerMinuteRemoveThrottling = 200;
  }
}


void checkGearInput()
{
  if(digitalRead(gearUpSensor) == HIGH)
  {
    if(gearNumber < 6)
    {
      gearShiftUP();
      
      Serial.print("debug through gearUpSensor");
    }
    
  }
  else if(digitalRead(gearDownSensor) == HIGH)
  {
    if(gearNumber > 0)
    {
      gearShiftDown();
      Serial.print("debug through gearDownSensor");
    }
    
  }
}



void loop()
{
  checkGearInput();
  engineOn = digitalRead(engineOnOffInput);
  digitalWrite(alwaysOn, HIGH);
  controlTrLimit = analogRead(throttlingInput) * 4;
  if (digitalRead(throttlingSensor) == 1 && trPerMinute < trLimit)
  {
    throttling();
    Serial.print("BOOOOOOOOOOOOOOOOOOOST");
    
  }
  
  // real throttling:
  if (analogRead(throttlingInput) != 0 && trPerMinute < controlTrLimit)
  {
    accelerate();
    Serial.print("BOOOOOOOOOOOOOOOOOOOST");
   
  }
  
  if(!engineOn)
  {
    engineOneCycle();
    
  }
  
  
  if(digitalRead(throttlingSensor) == 0)
  {
    unHoldThrottling();
    
  }
 
  
  
  Serial.print("the trPerMinute is: ");
  
  Serial.println(trPerMinute);
  acceleration = analogRead(throttlingInput);
  Serial.print("the  GEAR IS: ");
  Serial.println(gearNumber);
  Serial.print("Moins: ");
  Serial.println(digitalRead(gearUpSensor));
  Serial.print("Plus: ");
  Serial.println(digitalRead(gearDownSensor));
  
  actualGear(gearNumber);
  
  
  // reinitialization to 410.
  controlTrLimit = 4000; // reinitialization to 4000.
  
}


