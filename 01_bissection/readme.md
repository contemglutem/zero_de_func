# README — Método da Bissecção

## 1. Objetivo

O método da bissecção é uma técnica numérica para encontrar uma raiz (zero) de uma função contínua em um intervalo `[a, b]` quando `f(a)` e `f(b)` têm sinais opostos. Ele é simples, robusto e garante convergência linear enquanto a hipótese de mudança de sinal for válida.

## 2. Quando usar

* Quando a função for contínua no intervalo e você conseguir (ou estimar) um intervalo com mudança de sinal.
* Quando você precisa de um método robusto e não se importa com convergência apenas linear.
* Não é adequado quando você precisa de convergência super-rápida (use Newton/SECANTE) ou quando não é possível localizar um intervalo com mudança de sinal.

## 3. Convergência e custo computacional

* Convergência: linear — a largura do intervalo dobra a precisão por iteração.
* Complexidade por iteração: cálculo de uma avaliação de função (ou poucas avaliações se já tiver f(a), f(b)).
* Número de iterações aproximado para atingir tolerância `tol`: `k ≈ ceil(log2((b-a)/tol))`.

## 4. Resumo do algoritmo

1. Verificar que `f(a)` e `f(b)` tenham sinais opostos (ou forçar tentativa com aviso).
2. Calcular o ponto médio `m = (a + b) / 2`.
3. Avaliar `f(m)`.
4. Substituir o intervalo por `[a, m]` ou `[m, b]` conforme o sinal de `f(m)`.
5. Parar quando `|f(m)| < tol` ou `(b - a)/2 < tol` ou atingir `max_iter`.

---


## 5. Explicação e comentários sobre a implementação

* `initial_guess`: percorre inteiros entre `start` e `end` procurando mudança de sinal entre `T` e `T+1`. É simples e funciona para muitas funções, mas só busca em pontos inteiros e pode falhar se a raiz estiver entre pontos não inteiros ou fora do intervalo.
* Tratamento de `ZeroDivisionError`: o código ignora pontos onde a função lança `ZeroDivisionError` — isso pode ser útil, mas é preciso ter cuidado: outras exceções (ValueError, OverflowError) podem aparecer e hoje não são tratadas.
* `solve`: observa `fa` e `fb`. Caso `f(a)` ou `f(b)` dê `ZeroDivisionError`, o código força `fa, fb = 1, -1` para seguir; isso pode mascarar problemas e produzir resultados inesperados. Recomenda-se registrar/avisar melhor o usuário quando isso acontece.
* Critério de parada: `abs(fm) < tol` **ou** `(b-a)/2 < tol` — critérios padrão e adequados.
* Se `fa * fb > 0`, o método apenas imprime uma mensagem e tenta a iteração — isso às vezes pode convergir se a raiz estiver dentro do intervalo, mas não há garantia matemática; melhor lançar exceção ou fazer uma rotina de busca/expansão do intervalo.
* Valor de retorno padrão ao esgotar `max_iter`: `0.5 * (a + b)` — é razoável retornar o último meio, porém é preferível retornar `None` ou lançar uma exceção sinalizando que não convergiu.

---

## 6. Exemplo de uso

```python
# Exemplo: encontrar raiz de f(x) = x^2 - 2 (raiz: sqrt(2))
import math

def f(x):
    return x**2 - 2

root = Bisection.find_root(f, tol=1e-8)
print('Raiz encontrada (aprox):', root)
print('Erro relativo:', abs(root - math.sqrt(2)))
```

Observação: como `initial_guess` procura em inteiros, para `x^2 - 2` ele encontrará o intervalo `[1,2]` facilmente.

---

## 7. Testes sugeridos

* Teste com funções polinomiais simples (`x^3 - 2x - 5`, `x^2 - 2`).
* Teste com funções que têm singularidade (ver `ZeroDivisionError`) para verificar se o comportamento é o esperado.
* Teste de falha: função sem mudança de sinal — assert que `find_root` imprime aviso ou que uma versão melhorada lance `ValueError`.

---

## 8. Melhorias recomendadas (lista prática)

1. **Tipos e docstrings**: adicionar *type hints* e docstrings mais detalhados.
2. **Logging vs prints**: trocar `print` por `logging` configurável.
3. **Tratamento de exceções**: não mascarar erros com `fa, fb = 1, -1`. Melhor lançar `ValueError` ou `RuntimeError` quando `f(a)`/`f(b)` falhar.
4. **Initial guess mais robusta**: buscar em uma grade mais fina (floats) ou implementar expansão geométrica do intervalo (dobrar `b-a`) até achar mudança de sinal.
5. **Retorno explícito ao falhar**: retornar `None` ou lançar `ConvergenceError` quando `max_iter` for atingido.
6. **Parâmetro para modo seguro/forçado**: permitir `force=True` para forçar bisseção mesmo sem mudança de sinal; `force=False` padrão para segurança.
7. **Testes unitários**: criar `pytest` com casos positivos e negativos.

