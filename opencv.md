# opencv-python

## Verwerken foto
Inlezen foto

## Calibratie

### RGB --> HSV
HSV komt van pas om image processing toe te passen op onderdelen op basis van kleur.  
HSV (hue, saturation, value)  
* Hue: het kleurtype. Wordt uitgezet op een cirkel: van 0 tot 360 graden
* Saturation: grijs waarde, hoeveelheid van een kleur. In procent: 0% (flets, grijs) - 100%(volle kleur)
* Value: helderheid, intensiteit, lichtheid van het kleur. In procenten: 0% (zwart) - 100% (Wit)

![HSV uitleg](./images/HSV_uitleg.jpg "via Wikimedia Commons")  
Via Wikimedia Commons


Vervolgens op zoek gaan naar de rode en groene pixels

### Object segmentation
Bepaalde objecten uit een afbeelding halen. Hier dus de bedoeling om het dartboard (cirkelvorming) er uit te selecteren. Daarna de verschillende punten regio's

### [HoughCircles()](https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)
Manier in OpenCV om cirkels te herkennen op een afbeelding