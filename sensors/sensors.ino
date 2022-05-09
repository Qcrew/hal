/*
Board: ESP32-WROOM-32D
HAL cooling water flow and compressed air pressure sensing

Water flow sensor DIGITEN G1/2" CF-B7, F = 11Q (L/min)
Pinout: 3V3 (blue), GND (brown), 25 (orange) 

*/

// flow sensor pulse frequency in L/min, provided by the vendor
const int pulse_frequency = 11;

// microcontroller digital pin (with interrupt) the water flow sensor is connected to
unsigned char flow_sensor_pin = 25;

// count pulses from flow sensor (updated upon interrupt)
volatile int pulse_count;

// calculate flow in L/min
int flow;

// time interval the pulse counts are sensed after and averaged over, in seconds
// this also effectively determines the frequency at which data is logged by sensors.py
const int interval = 60;
// variables to track the time window for flow sensing
unsigned long current_time;
unsigned long previous_time;

void count() // interrupt service routine
{
   pulse_count++;
}

void setup()
 {
   pinMode(flow_sensor_pin, INPUT);
   digitalWrite(flow_sensor_pin, HIGH);
   Serial.begin(9600);
   attachInterrupt(digitalPinToInterrupt(flow_sensor_pin), count, RISING); // Setup Interrupt
   current_time = millis();
   previous_time = current_time;
}

void loop ()
{
   current_time = millis();
   // calculate and print flow reading in L/min over the time specified by 'interval'
   if(current_time >= (previous_time + (interval * 1000)))
   {
      previous_time = current_time;
      flow = (pulse_count / (interval * pulse_frequency));
      pulse_count = 0; // reset count
      Serial.println(flow);
   }
}
