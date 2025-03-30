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


# Hopfield Network
## Popis problému
Cílem bylo vytvořit Hopfieldovu síť, která dokáže ukládat a následně rekonstruovat binární vzory. Síť funguje jako asociativní paměť, která se dokáže vrátit k nejbližšímu uloženému vzoru i při částečně poškozeném vstupu.

## Proces implementace
1. **Struktura sítě**:
   - Implementace třídy `HopfieldNetwork` s metodami pro učení a rekonstrukci vzorů.
   - Reprezentace neuronů pomocí binárních hodnot (1 a -1).

   ```python
   class HopfieldNetwork:
      def __init__(self, size):
         self.size = size
         self.weights = None
         self.pattern_weights = None
   ```

2. **Trénovací metoda (`train`)**:
   - Použití Hebbova pravidla pro aktualizaci vah.
   - Vytvoření symetrické váhové matice bez vlastních smyček.

   ```python
   def train(self, patterns):
      self.weights = np.zeros((self.size, self.size))
      self.pattern_weights = []
      
      for pattern in patterns:
         # Konverze na binární reprezentaci (1 a -1)
         pattern = np.where(pattern.flatten() > 0, 1, -1).reshape(-1, 1)
         
         # Výpočet váhové matice pro daný vzor pomocí vnějšího součinu
         pattern_weight = pattern @ pattern.T
         
         # Přidání do celkové váhové matice
         self.weights += pattern_weight
         self.pattern_weights.append(pattern_weight)
      
      # Odstranění vlastních smyček (nulová diagonála)
      np.fill_diagonal(self.weights, 0)
   ```

3. **Rekonstrukční metoda (`recall`)**:
   - Iterativní aktualizace stavů neuronů na základě vstupního vzoru.
   - Stabilizace sítě do jednoho z uložených vzorů.

   ```python
   def recover(self, pattern, steps=5, async_method=False):
      pattern = pattern.flatten()

      if async_method:
         # Asynchronní aktualizace - jeden neuron po druhém
         for _ in range(steps):
               for i in range(self.size):
                  pattern[i] = np.sign(np.dot(self.weights[i], pattern))
      else:
         # Synchronní aktualizace - všechny neurony najednou
         for _ in range(steps):
               pattern = np.sign(self.weights @ pattern)
      
      # Přetvarování výsledku zpět na 2D matici
      return pattern.reshape(int(np.sqrt(self.size)), -1)
   ```

### Synchronní a Asynchronní Aktualizace

**Synchronní aktualizace**:
- Všechny neurony v síti jsou aktualizovány současně v jednom kroku.
- Implementováno pomocí maticového násobení: `pattern = np.sign(self.weights @ pattern)`
- Může být rychlejší pro výpočet, ale někdy vede k oscilacím stavu místo konvergence.

**Asynchronní aktualizace**:
- Neurony se aktualizují postupně, jeden po druhém.
- Implementováno pomocí cyklu přes všechny neurony: `pattern[i] = np.sign(np.dot(self.weights[i], pattern))`
- Tento přístup často umožňuje lepší konvergenci k uloženým vzorům.

## Výsledek
Hopfieldova síť úspěšně ukládá a rekonstruuje binární vzory. Dokáže opravit poškozené vstupy a vrátit se k nejbližšímu uloženému vzoru.

## Obrázky
### Hopfieldova síť - Před a po Rekonstrukci
![Hopfield Network before Recall](res/screenshots/hopfield_2.png)
![Hopfield Network after Recall](res/screenshots/hopfield_1.png)

# QLearning
## Popis problému
Cílem bylo implementovat algoritmus Q-Learning, který umožňuje agentovi (hráči) naučit se optimální strategii pro dosažení cíle v prostředí s odměnami a penalizacemi.

## Proces implementace
1. **Struktura programu**:
   - `qlearning_player`: Třída reprezentující hráče, který se učí na základě Q-Learning algoritmu.
   - `q_table`: Tabulka Q-hodnot, která uchovává odhady budoucích odměn pro jednotlivé akce ve stavech.
   - `qlearning_app`: Aplikace, která simuluje prostředí a umožňuje interakci hráče s prostředím.

2. **Algoritmus Q-Learning**:
   - Inicializace Q-tabulky s nulovými hodnotami.
   - Iterativní učení na základě interakce hráče s prostředím:
     - Hráč pozoruje aktuální stav.
     - Na základě Q-hodnot a průzkumné strategie (např. greedy) vybírá akci.
     - Prostředí vrací odměnu a nový stav.
     - Aktualizace Q-hodnot podle rovnice.

      ### Princip trénování

      Trénování je založeno na implementaci Q-Learning algoritmu. Tento algoritmus umožňuje agentovi iterativně zlepšovat své rozhodování na základě zkušeností získaných interakcí s prostředím.

      #### Hlavní kroky trénování:
      1. **Inicializace Q-tabulek**:
         - Q-tabulka je reprezentována jako slovník s stavem kolem hrače a hodnoty jsou Q-hodnoty.

      2. **Výběr akce**:
         - Agent vybírá akci na základě greedy strategie:
           - S pravděpodobností ε zvolí náhodnou akci (průzkum).
           - Jinak zvolí akci s nejvyšší Q-hodnotou (exploatace).

         ```python
         if random.random() <= self.table.epsilon:
            selected_action = random.choice(actions)
            selected_by_random = True
         else:            
            selected_value = -1
            for i, s_value in enumerate(current_state_data):
                if s_value > selected_value:
                    selected_action = actions[i]
                    selected_value = s_value
         ```

       - Po provedení akce agent obdrží odměnu a přejde do nového stavu.

      3. **Aktualizace Q-Hodnoty**:
         ```python
         reward = self.get_reward(self.last_action, self.last_state)

         last_state_data = self.table.get(self.last_state)
         last_value = last_state_data[actions.index(self.last_action)]            
         new_value = (1 - self.learning_rate) * last_value + self.learning_rate * (reward + max_value * 0.6)
         last_state_data[actions.index(self.last_action)] = new_value
         self.table.set(self.last_state, last_state_data)
         ```
       - Kde:
         - `reward` je odměna získaná za provedenou akci.
         - `last_state_data` obsahuje Q-hodnoty pro předchozí stav.
         - `last_value` je původní Q-hodnota pro danou akci ve stavu.
         - `new_value` je nově vypočítaná Q-hodnota na základě odměny a maximální hodnoty budoucího stavu.
         - `learning_rate` určuje, jak rychle se agent přizpůsobuje novým informacím.
         - `max_value` je maximální Q-hodnota pro budoucí stav.
         - `0.6` je discount rate

      #### Parametry trénování:
      - `learning_rate` Určuje, jak rychle se agent přizpůsobuje novým informacím.
      - `discount rate` Určuje, jak moc agent zohledňuje budoucí odměny.
      - `epsilon` Určuje, jak často agent zkoumá nové akce.

      #### Výsledek:
      Po dostatečném počtu epizod agent optimalizuje své rozhodování a Q-tabulka obsahuje hodnoty, které odpovídají nejlepším akcím pro každý stav. Tento proces umožňuje agentovi efektivně dosáhnout cíle v prostředí.

3. **Vizualizace a interakce**:
   - Hráč vidí prostředí jako mřížku s překážkami, cílem a aktuální pozicí.
   - Q-hodnoty jsou vizualizovány, aby bylo možné sledovat proces učení.

## Výsledek
Agent se úspěšně naučil optimální strategii pro dosažení cíle v prostředí. Q-tabulka obsahuje hodnoty, které odpovídají nejlepším akcím pro každý stav.

## Obrázek
### Vizualizace Q-Learningu
![QLearning Visualization](res/screenshots/qlearning_1.png)