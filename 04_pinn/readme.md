# README — Método NNMethods (PINN para raízes)

## 1. Objetivo

O `NNMethods` é uma abordagem inspirada em **PINNs (Physics-Informed Neural Networks)** adaptada para encontrar raízes de funções. A ideia é treinar uma rede neural para aproximar regiões próximas à raiz da função, aproveitando a capacidade da rede de modelar funções não lineares. Após o treino, a raiz aproximada é **refinada com Newton-Raphson**.

---

## 2. Quando usar

* Quando se deseja testar abordagens de aprendizado de máquina aplicadas a problemas numéricos.
* Quando a função tem comportamento altamente não linear ou difícil para métodos tradicionais.
* Para comparar desempenho entre métodos clássicos (Bissecção, Newton, Secante) e métodos baseados em redes neurais.
* Não é recomendado quando rapidez e simplicidade são prioridade, pois o treinamento da rede pode ser custoso.

---

## 3. Funcionamento

1. **Estimativa de intervalo**: identifica uma região provável da raiz a partir da troca de sinal da função.
2. **Escolha da arquitetura**: decide número de camadas/neuronios conforme a complexidade da função.
3. **Funções de ativação adaptativas**: seleciona automaticamente entre `tanh` ou senóides (`sin`/`cos`).
4. **Treinamento**: a rede é treinada para minimizar o valor da função em torno da raiz (perda quadrática sobre `f(x)` normalizada).
5. **Raiz aproximada**: após treino, pega-se o ponto onde `f(x_pred)` é mínimo.
6. **Refinamento**: aplica Newton-Raphson no valor estimado.

---

## 4. Comentários importantes sobre a implementação

* **Intervalo inicial**: obtido por troca de sinal, mas com fallback para menor valor absoluto de `f(x)`.
* **Ativações adaptativas**: escolhe `tanh` para funções simples e senóides para funções oscilatórias.
* **Arquitetura adaptativa**: número de camadas cresce conforme a complexidade da função.
* **Treinamento com ajuste dinâmico de learning rate**: reduz LR se perda estagnar.
* **Clipping da saída**: evita valores inválidos durante treino (`0.001` a `10.0`).
* **Refino final**: chama `NewtonRaphson.find_root` para obter raiz precisa.

---

## 5. Exemplo de uso

```python
import numpy as np

def f(x):
    return np.cos(x) - x

nn_solver = NNMethods(f)
root = nn_solver.train_and_pred()
print("Raiz encontrada:", root)
```

---

## 6. Testes sugeridos

* Funções simples (`x^2 - 2`, `cos(x) - x`).
* Funções oscilatórias (`sin(x)`).
* Funções com múltiplas raízes — verificar se consegue convergir para a correta.
* Comparação com Bissecção, Newton-Raphson e Secante.

---

## 7. Melhorias recomendadas

1. **Critérios de parada mais robustos** (ex: perda relativa ou erro na raiz).
2. **Suporte a múltiplas raízes** em um único treino (ex: com perda multi-ponto).
3. **Histórico de treino** armazenado (loss curve, roots aproximados por epoch).
4. **Batching inteligente** em vez de grid fixo.
5. **Integração com outros métodos** (ex: fallback para Secante ou Bissecção).
6. **Opção de aceitar raízes complexas**.
