# README — Método de Newton-Raphson

## 1. Objetivo

O método da secante é uma técnica numérica iterativa para encontrar raízes de funções. Ele é semelhante ao método de Newton-Raphson, mas não requer o cálculo explícito da derivada, usando em vez disso uma aproximação baseada em dois pontos anteriores.

## 2. Quando usar

* Quando a função é contínua na vizinhança da raiz.
* Quando não se tem derivada analítica disponível ou ela é difícil de calcular.
* Quando se deseja uma convergência mais rápida que a bissecção, mas sem precisar de f'(x).
* Não recomendado se não for possível obter dois chutes iniciais razoáveis (x0, x1).

## 3. Convergência e custo computacional

* Convergência: geralmente superlinear (≈1.618, taxa áurea), mais rápida que a bissecção, mas em geral mais lenta que Newton-Raphson.
* Complexidade por iteração: duas avaliações de f por passo (reutiliza valores das iterações anteriores).
* Pode divergir se os chutes iniciais não forem adequados.

## 4. Resumo do algoritmo

1. Escolher dois chutes iniciais `x0` e `x1`.
2. Calcular a interseção da reta secante entre `(x0, f(x0))` e `(x1, f(x1))` com o eixo x.
3. Atualizar `x0 ← x1`, `x1 ← x_new`.
4. Repetir até convergir `(diferença < tol ou |f(x)| < tol)`.

## 5. Explicação e comentários sobre a implementação

* **Dois chutes iniciais**: o método precisa de dois pontos distintos para começar.
* **Divisão por zero**: se f(x1) ≈ f(x0), a fórmula falha — o código retorna None.
* **Critério de parada**: aceita convergência por diferença entre iterações ou por valor da função.
* **Raízes complexas**: internamente usa complex, mas só aceita raízes reais.
* **solve_multiple**: permite testar vários pares de chutes, eliminando duplicatas.
* **find\_all\_roots**: gera chutes automáticos em uma grade ampla ([-100,100]) com deslocamento.

## 6. Exemplo de uso

```python

# Exemplo 1: raiz de f(x) = x^2 - 2
import math


def f(x):
    return x**2 - 2


root = Secant.find_root(f, 1.0, 2.0)
print("Raiz encontrada:", root)
print("Erro relativo:", abs(root - math.sqrt(2)))


# Exemplo 2: múltiplas raízes (f(x) = x^3 - x)
def g(x):
    return x**3 - x


roots = Secant.find_all_roots(g, x0_list=[-2, -1, 0, 1, 2], x1_list=[-1.5, -0.5, 0.5, 1.5, 2.5])
print("Raízes encontradas:", roots)
```

---

## 7. Testes sugeridos

* Funções polinomiais simples (x^2 - 2, x^3 - x).
* Funções transcendentes (cos(x) - x).
* Casos em que f(x0) ≈ f(x1) para validar tratamento da divisão por zero.
* Comparação de velocidade e robustez com Bissecção e Newton-Raphson.

## 8. Melhorias recomendadas

1. **Tipagem explícita**: adicionar type hints.
2. **Exceções específicas**: lançar exceções para não convergência ou divisão por zero em vez de retornar None.
3. **Critérios de parada configuráveis**: permitir tolerância relativa.
4. **Fallback**: caso falhe, usar bissecção em [x0, x1].
5. **Histórico opcional**: armazenar valores intermediários para depuração.
6. **Parâmetros automáticos**: heurística mais inteligente para gerar pares de chutes.