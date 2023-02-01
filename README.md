# MOSAIX

Thanks for stopping by! You can find anything MOSAIX related on this page. ![tiles_robocorn](https://user-images.githubusercontent.com/29374608/216107454-b68f4db4-6543-4b74-97f2-ef2efb65c9f4.jpeg)

##What is MOSAIX?

MOSAIX is the first swarm robotic system (completely decentralised) desinged and built to be used by members of the public in large numbers (many robots and many people) to help them in social tasks such as decision-making, brainstorming, art-making and education. MOSAIX is made of individual robots called Tiles. As part of my PhD, I designed and built 100 Tiles. 

##How do I build a Tile?

Building a Tile is simple since most components are off the shelf. Tiles run on a Rasberry Pi 4. However, the base of the Tile is a PCB of our design, and there is one more PCB (the adaprter) that is soldered onto the Raspberry Pi's pins. We also designed some 3D printed components to support the robot, found in [a relative link](STL files). The gerber files for both boards can be found in [a relative link](Base_gerberfiles) and [a relative link](Adapter_gerberfiles). 

In order to build a Tile, the following steps need to be taken:
1- Send the PCBs to be manufactured 
2- Obtain off-the-shelf components and solder them onto the base PCB
3- Solder the Adapter PCB onto the Raspberry Pi pins
4- Secure the stack of components using the 3D prints

Here are all the components needed to build a Tile:

1- Raspberry Pi 4 2GB
https://thepihut.com/products/raspberry-pi-4-model-b

2- SD Card 32GB
Any microSD Card for the Raspberry Pi

3- 4-inch LCD touchscreen
https://thepihut.com/products/spi-4-320x480-ips-touch-screen-gpio

4- 4 VL53L0X Time-of-Flight Distance Sensor Carrier with Voltage Regulator, 200cm Max 

5- 10000 mAh power pack 
Any model that is 9.5cm x 6cm x 2cm, with USB A input on the top. 

6- Raspberry Pi Zero camera module 
https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module?variant=37751082058

7- Raspberry Pi Zero camera adapter
https://shop.pimoroni.com/products/camera-cable-adapter?variant=3031293263882

8- 2 Micro metal gearmotor 
https://thepihut.com/products/micro-metal-gearmotor?variant=35654648145

9- Motor brackets 
https://shop.pimoroni.com/products/pololu-micro-metal-gearmotor-bracket-pair-black?variant=471886829

10- TB6612FNG motor driver
https://shop.pimoroni.com/products/sparkfun-motor-driver-dual-tb6612fng-1a-1?variant=2509524533258

11- 2 32mmx7mm Pololu Wheels 
https://shop.pimoroni.com/products/pololu-wheel-32x7mm-pair?variant=390419700

12-  Castor ball
https://www.amazon.co.uk/dp/B083FSLM8Z?psc=1&ref=ppx_pop_dt_b_asin_title

13- 10 Way Flat Ribbon Cable
https://uk.rs-online.com/web/p/ribbon-cable/2899846

14- Molex Right Angle, Through Hole, Plug Type A 2.0 USB Connector
https://uk.rs-online.com/web/p/usb-connectors/8006797

15- Microchip 16-Channel I/O Expander I2C, Serial 28-Pin SOIC, MCP23017-E/SO
https://uk.rs-online.com/web/p/io-expanders/0403816

16- Omron 10-Way Connector Plug for Through Hole Mount, 2-Row
https://uk.rs-online.com/web/p/idc-connectors/2026926

17- ASSMANN WSW 10-Way IDC Connector Socket for Cable Mount, 2-Row
https://uk.rs-online.com/web/p/idc-connectors/6741097

18- PCB Slide Switch Single Pole Double Throw (SPDT) On-Off-On 5 A @ 28 V dc Top
https://uk.rs-online.com/web/p/slide-switches/7347334

19- Molex Straight, SMT, Socket Type B USB Connector
https://uk.rs-online.com/web/p/usb-connectors/8967572

20- USB A to USB micro cable
Any cable

The following are components soldered onto the Base PCB:

<img width="590" alt="image" src="https://user-images.githubusercontent.com/29374608/216159970-e56df0eb-82b4-4b00-9184-0723e87aa5a5.png">

A) Time-of-flight distance sensors.
B) I/O I2C expander microchip. 
C) Cable connector plug. 
D) USB micro connector. 
E) Motor driver.
F) Micro metal gearmotors. 
G) Power switch.
H) Castor ball. 

Here 

After soldering components onto the base PCB, soldering the Adapter PCB onto the pins of the Raspberry Pi, and printing assembly goes as follows:
![stack_explained](https://user-images.githubusercontent.com/29374608/216160143-9257abc1-dcae-4b60-a05f-ac67b7fdff2c.png)




