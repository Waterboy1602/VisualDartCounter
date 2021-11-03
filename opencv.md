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


[Vervolgens op zoek gaan naar de rode en groene pixels]

### Blur
Een afbeelding blurren komt van toepassing om de achtergrond of scherpe contouren minder duidelijk te laten zijn op de afbeelding. Op die manier zullen bepaalde details minder een doorslag geven bij de volgende bewerkingen.

Afbeelding blurren kan door een convolutie uit te voeren met een convolutie kernel (Matrix).
Convolutie kernel: vierkante matrix [MxN] met M en N oneven getallen.
Blur kernel: 5x5 matrix met allemaal 1. Vervolgens gedeeld door 25 (aantal elementen in de kernel) om de matrix te normalizeren


`cv2.filter2D(src, ddepth, kernel)`: voert een lineaire filter operatie uit op de afbeelding adhv de kernel.

`cv2.blur(src, ksize)`: ksize=grootte van de kernel (M,N)

### Split
3D-matrix (Afbeelding) opsplitsen in 3 aparte 2D-matrices. Elk met een aparte waarde: h, s en v.

### Thresholding
Voorbeeld van image segmentation. Een van de simpelste segmentation methodes. Als de intensiteits waarde (V-value|HSV) van een pixel onder een bepaalde grens (threshold) is, krijgt die pixel een vooraf ingestelde waarde. Alle pixels die zich boven de grens bevinden, krijgen een andere vooraf ingestelde waarde.

`cv2.threshold(src, thresh, maxval, type)`:
* src: input image --> Only the V-values of the HSV image
* thresh: threshold value
* maxValue: maximum value, wordt gebruikt met `THRESH_BINARY`
* type: `THRESH_BINARY` wordt gebruikt: onder thresh = 0; boven thresh = maxValue. `THRESH_OTSU` is een algoritme dat de ideale threshValue bepaald op basis van de afbeelding. [Otsu algorithm](https://en.wikipedia.org/wiki/Otsu%27s_method)


### Canny
Vind randen op een afbeelding. [Canny edge algoritme](https://en.wikipedia.org/wiki/Canny_edge_detector). Multi stage algorithm

The smallest value between threshold1 and threshold2 is used for edge linking. The largest value is used to find initial segments of strong edges.

`cv2.Canny(image, threshold1, threshold2)`
* threshold1: gekozen voor de `OTSU_Value`
* threshold2: 0.5*`OTSUThreshVal`

### Contouren
Vind contouren in een afbeelding

`contours, hierarchy = cv2.findContours(image, mode, method)`
* contours: de gevonden contouren. Worden opgeslagen als een vector van punten
* hierarchy: optionele output vector. Bevat info over de afbeelding topologie. (wordt niet gebruikt in VisualDartCounter)
* mode: `cv2.RETR_LIST`: verzamel alle contouren zonder hierarisch onderscheid
* method: `cv2.CHAIN_APPROX_SIMPLE`: compresseerd hor, vert en diag delen. Slaat enkel de eindpunten op. Vb vierkant = opgeslagen met 4 punten

### Object segmentation
Bepaalde objecten uit een afbeelding halen. Hier dus de bedoeling om het dartboard (cirkelvorming) er uit te selecteren. Daarna de verschillende punten regio's

### [HoughCircles()](https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)
Manier in OpenCV om cirkels te herkennen op een afbeelding

### Ellips
`cv2.ellipse(image, ellipse, color, line_type)`
