# README — Método de Newton-Raphson

## 1. Objetivo

O método de Newton-Raphson é uma técnica numérica iterativa para encontrar raízes de funções. Ele utiliza a aproximação linear da função no ponto atual para prever a raiz, geralmente apresentando **convergência quadrática** quando a aproximação inicial está próxima da raiz e `f'(x)` não é nula.

## 2. Quando usar

* Quando a função é diferenciável na vizinhança da raiz.
* Quando se deseja alta velocidade de convergência (quadrática).
* Adequado quando se tem uma boa estimativa inicial `x0`.
* Não é recomendado se `f'(x)` for muito pequeno ou se não houver boa estimativa inicial (pode divergir ou convergir para raiz errada).

## 3. Convergência e custo computacional

* Convergência: quadrática (se `f'(x*) ≠ 0` e `x0` próximo da raiz).
* Complexidade por iteração: cálculo de `f(x)` e `f'(x)`.
* Custo extra se `f'(x)` não estiver disponível: aproximação numérica por diferenças centradas.

## 4. Resumo do algoritmo

1. Escolher chute inicial `x0`.
2. Avaliar `f(x0)` e `f'(x0)`.
3. Atualizar `x1 = x0 - f(x0) / f'(x0)`.
4. Repetir até convergir (diferença sucessiva < `tol` ou `|f(x)| < tol`).

---

## 5. Explicação e comentários sobre a implementação

* **Classe parametrizada**: aceita `f`, `df`, tolerância e número máximo de iterações.
* **Derivada numérica**: se `df` não for fornecida, usa diferenças centradas (precisão de ordem 2).
* **Complexidade**: cada iteração requer uma avaliação de `f` e uma de `df` (ou duas de `f` extras se numérica).
* **Critério de parada**: verifica diferença entre iterações ou valor da função.
* **Raízes complexas**: internamente usa `complex`, mas só retorna resultado se raiz for real dentro da tolerância.
* **solve\_multiple**: permite buscar várias raízes a partir de diferentes chutes iniciais, descartando duplicatas próximas.
* **find\_all\_roots**: gera chutes automáticos em uma grade de `[-100, 100]` (ajustável).

---

## 6. Exemplo de uso

```python
import math

# Exemplo 1: raiz quadrada de 2
def f(x):
    return x**2 - 2

def df(x):
    return 2*x

root = NewtonRaphson.find_root(f, df, x0=1.0)
print("Raiz encontrada:", root)
print("Erro relativo:", abs(root - math.sqrt(2)))

# Exemplo 2: múltiplas raízes (f(x) = x^3 - x)
def g(x):
    return x**3 - x

def dg(x):
    return 3*x**2 - 1

roots = NewtonRaphson.find_all_roots(g, dg, x0_list=[-2, -1, 0, 1, 2])
print("Raízes encontradas:", roots)
```

---

## 7. Testes sugeridos

* Polinômios simples (`x^2 - 2`, `x^3 - x`).
* Funções transcendentes (`cos(x) - x`, `sin(x)`).
* Casos degenerados (derivada nula, `f(x) = cte`).
* Funções com raízes múltiplas (para verificar convergência mais lenta).
* Comparação de precisão com método da bissecção.

---

## 8. Melhorias recomendadas

1. **Tipagem explícita**: adicionar *type hints* (`f: Callable[[float], float]`).
2. **Exceções**: lançar exceção clara em vez de retornar `None` quando não converge ou derivada é nula.
3. **Controle de saída**: permitir retorno de raízes complexas quando desejado (`allow_complex=True`).
4. **Critérios de parada configuráveis**: permitir escolher entre tolerância relativa ou absoluta.
5. **Histórico de iterações**: opcionalmente retornar lista de aproximações para análise.
6. **Método híbrido**: implementar fallback para bissecção caso Newton falhe.
7. **Parâmetros adaptativos**: reduzir passo se divergência for detectada.
