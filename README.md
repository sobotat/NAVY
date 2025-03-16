# Perceptron
## Popis problému
Cílem bylo predikovat, zda se bod nachází pod, nad nebo přímo na přímce:
- Pod přímkou: Label **-1**
- Nad přímkou: Label **1**
- Na přímce: Label **0**

## Proces implementace
1. **Příprava komponent**:
   - Implementace aktivační funkce, vah a biasu.
   
2. **Implementace trénovací metody (`fit`)**:
   - Inicializace vah a biasu.
   - Iterace přes trénovací data v několika epochách.
   - Výpočet predikce a určení chyby oproti skutečné hodnotě.
   - Aktualizace vah a biasu na základě chyby.

3. **Implementace predikční metody (`predict`)**:
   - Výpočet výstupu pomocí vstupu, vah a biasu.
   - Aplikace aktivační funkce pro získání finální predikce.

## Výsledek
Perceptron správně klasifikuje body podle rovnice přímky a dokáže nalézt odpovídající rozhodovací hranici.

---

# XOR problém
## Popis problému
Cílem bylo předpovědět výsledek logické operace XOR, kterou nelze řešit jednoduchým perceptronem, protože není lineárně separovatelná. 

Řešením bylo vytvoření malé neuronové sítě, která rozdělí problém na menší části pomocí více rozhodovacích hranic.

## Proces implementace
1. **Struktura sítě**:
   - Vytvoření tříd: `Neuron`, `Layer` a `NeuralNetwork`.
   - Rozdělení sítě na vrstvy: skrytá vrstva (2 Neurony) a výstupní vrstva (1 Neuron).

2. **Trénovací metoda (`fit`)**:
   - Propagace vstupních dat skrz síť a získání výsledků.
   - Výpočet chyb pomocí zpětné propagace (backpropagation).
   - Aktualizace vah a biasů na základě chyby.

3. **Predikční metoda (`predict`)**:
   - Propagace vstupu sítí až k výstupu.
   - Vrácení výsledku z poslední vrstvy.

## Výsledek
Neuronová síť správně naučila operaci XOR a dokáže ji přesně klasifikovat.
