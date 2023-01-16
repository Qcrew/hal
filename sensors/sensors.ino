/*
Board: ESP32-WROOM-32D
HAL cooling water flow and compressed air pressure sensing

Water flow sensor DIGITEN G1/2" CF-B7, F = 11Q (L/min)
Pinout: 3V3 (blue), GND (brown), 25 (orange) 

Pressure sensor HONEYWELL 40PC100G (max 100 psi)
Supply voltage 4.75-5.25V
Output 0.5-4.5V (40.0mV/psi)(0.5V at 1 atm = 14.7 psi)
Pinout: 5V (red), GND (black), 15 (yellow)

Sensor values sent in serial in this format:
<water flow in L/min>,<air pressure in bar>
*/

// flow sensor pulse frequency in L/min, provided by the vendor
int pulse_frequency = 11;

// ESP32 digital pin (with interrupt) the water flow sensor is connected to
int flow_sensor_pin = 25;

// count pulses from flow sensor (updated upon interrupt)
volatile int pulse_count;

// calculate flow in L/min
int flow;

// ESP32 ADC pin the air pressure sensor is connected to
int pressure_sensor_pin = 15;

// raw air pressure sensor value
int pressure_sensor_analog_value;

// processed absolute pressure in bar
float abs_pres_bar;

// factors for converting raw air pressure sensor value to absolute pressure in bar
int adc_offset = 450;  // approx. adc value when pressure sensor pin receives atm pressure
float adc_to_volt = (3.3 / 4095);  // 3.3V is the reference voltage and 4095 refers to ESP32's ADC resolution of 12 bits 
int volt_to_psi = 25;  // reciprocal of pressure sensor sensitivity of 40 mV/psi
float psi_to_bar = 0.0689476;  // conversion factor between psi and bar

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
      pressure_sensor_analog_value = analogRead(pressure_sensor_pin);
      abs_pres_bar = (pressure_sensor_analog_value - adc_offset) * adc_to_volt * volt_to_psi * psi_to_bar;
      Serial.print(flow);
      Serial.print(",");
      Serial.println(abs_pres_bar);
     
      pulse_count = 0; // reset pulse count of water flow sensor
   }
}
