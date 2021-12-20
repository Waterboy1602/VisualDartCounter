# VISUAL DART COUNTER  
Dit is een project voortgekomen uit het vak Ingenieursbeleving 2 - EICT (B-KUL-JPI13O). Het doel is om een app te maken die de puntentelling van een dartspel automatiseert aan de hand van camera's die gericht zijn naar het dartbord. Op die manier moet de speler niet meer manueel de punten ingeven.

## Planning  
Start (11-10-2021)  
### Week 41-42:  
Opstarten van het project  
- [x] Aanmaken van een Git repository.  
- [x] Informatie opzoeken over opencv-python
- [x] Beeldmateriaal verzamelen  
- [x] Planning opstellen

### Week 43-44-45:
Maken van een eerste versie die een afbeelding van een dartbord kan uitlezen. Puntenregio's vastleggen.  
Vervolgens bollen aanbrengen op het dartbord die de pijltjes voorstellen.   
Punten samenstellen
- [x] Code vormgeven
- [x] Ellipsen/cirkels herkennen/vinden
- [x] Orientatie van het bord vinden (15/11)  
- [x] Puntenregio's definiëren (15/11)  
### Week 46-48:  
Blauwe vierkanten op het dartbord aanbrengen als dartpijlen. De *fake* dartpijlen herkennen en punten tellen.
- [x] Beeldmateriaal aanmaken met *fake* pijltjes
- [x] Code uitbreiden zodat het werkt met blauwe vierkanten
- [x] Punten van een worp optellen
### Week 48-50:  
Uitgebreider testen met de blauwe vierkanten als dartpijl. Daarna blauwe vierkanten vervangen door effectieve dartpijlen
- [x] Extra beeldmateriaal aanmaken met *fake* pijltjes
- [x] Beeldmateriaal verzamelen met *echte* dartpijlen
- [ ] Code uitbreiden zodat de *echte* dartpijlen herkend worden
- [ ] Exacte plaats van de dartpijl bepalen
### Week XX-XX:
Gebruik maken van een effectieve camera. Onderzoeken of 1 camera voldoende is om een accurate puntentelling te verkrijgen. 
- [ ] Afbeeldingen vervangen door livebeeld van een camera
- [ ] Code verder uitwerken
### Week XX-XX
- [ ] GUI ontwerpen. 
- [ ] Verder op punt zetten van de nauwkeurigheid

## Bibliotheken  
* Opencv-python  

## Documentatie
Documentatie over OpenCV terug te vinden in [OpenCV.md](opencv.md).
## Installatie  
* Virtual environment aanmaken: `python -m venv ./venv`
* VENV activeren: `.\venv\Scripts\activate`
* De nodige modules downloaden: `pip install --no-cache-dir -r requirements.txt --upgrade`  

## Info dartboard
Double/Treble ring: 8 mm  
Bull eye: 12.7 mm  
Bull (incl Bull eye): 31.8 mm  
Center - Inside edge Treble: 107 mm  
Center - Outside edge Double: 170 mm  
Diameter point area: 340 mm 
Diameter totale bord: 451 mm  
  
Straal point area: 170 mm   
Straal totale bord: 225 mm  
  
20 segmenten: 360°/20 = 18° || 2*PI/20 = PI/10 = 0.31415  

## Opmerkingen
* Straal wordt meegegeven vanuit het center van het bord, dus NIET vanuit nulpunt afbeelding.  
--> Aanpassen door coordinaat van Dart te verschuiven

* Puntcoordinaten worden WEL bepaald vanuit nulpunt afbeelding


(Laatste update: 21/12/'21)