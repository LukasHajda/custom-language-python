# Realizácia návrhu na tvorbu jednoduchého programovacieho jazyka
**Diplomová práca**

---

**Požiadavky:**
- Python (verzia 3.10)
---


**Ako si spustiť projekt:**
1. Clonuť si projekt:
   - `git init` vo vašom prázdnom priečinku kde chcete mať projekt
   - `git clone <link na repozitár>`
2. `pip install -r requirements.txt`
   - Nainštalujú sa potrebné dependencies, ktoré sa v projekte využívajú
3. Môžete začať písať kód do súboru `source_code.txt`

---
Ako písať kód:

**Priradenie:**
```
do x1 prirad 10.

do x2 prirad 10 + 20.

do x4 prirad foo().
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

