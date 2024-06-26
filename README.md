# Realizácia návrhu na tvorbu jednoduchého programovacieho jazyka
**Diplomová práca**

---

**Požiadavky:**
- Python (verzia 3.10)
- Graphviz package
---


**Ako si spustiť projekt:**
1. Stiahnuť si package Graphviz [tu](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_msbuild_Release_graphviz-10.0.1-win32.zip)
2. Extrahovať si zip súbor
3. V `main.py` si treba do riadku `2` doplniť cestu ku priečinku `bin` z extrahovaného súboru Graphviz


![path](https://github.com/LukasHajda/custom-language-python/assets/41372194/94a2a774-76bb-4fbc-bfd0-b8cda3fd2f40)


5. Clonuť si projekt:
   - `git clone <link na repozitár>` alebo si projekt stiahnuť ako `zip`
6. `pip install -r requirements.txt` (keď potrebujete môžete si vytvoriť `venv`)
   - Nainštalujú sa potrebné dependencies, ktoré sa v projekte využívajú
7. Môžete začať písať kód do súboru `source_code.txt`

---
**Vizualizácia AST**<br />
Pri každom spustení programu sa vygeneruje ```AST.pdf``` súbor, ktorý obsahuje AST pre zdrojový kód.
Ak nechcete generovať tento súbor stačí len zakomentovať tieto riadky v ```main.py```
```
visualizer = Visualizer(root)
visualizer.visualize_tree()
```

---
Ako písať kód:

**Priradenie:**
```
do x1 prirad "Ahoj svet".

do x2 prirad 10 + 20.

do x4 prirad foo().

do x5 prirad 67.6.

do x6 prirad pravda.
```
**Podmienky**

```
do x1 prirad 15.

ak (x1 < 10) tak {
    ukaz("pravda").
} inak {
    ak (x1 == 15) tak {
        ukaz("Je to 15").
    }
}
```

**Cyklus**
```
do x1 prirad 15.

pokial (x1 < 40) tak {
    ukaz(x1).
    do x1 prirad x1 + 1.
}
```

**Funkcie**
```
funkcia foo(x, y) {
    vrat x + y.
}

funkcia goo(x, y) {
    vrat x - y.
}

do x1 prirad foo(10, 5) + goo(4, 2).

ukaz(x1).
```

