class NewtonRaphson:
    def __init__(self, f, df=None, tol=1e-6, max_iter=1000):
        """
        Inicializa o método de Newton-Raphson.
        f: função alvo
        df: derivada de f. Se None, será aproximada numericamente
        tol: tolerância
        max_iter: número máximo de iterações
        """
        self.f = f
        self.df = df
        self.tol = tol
        self.max_iter = max_iter

    def _numerical_derivative(self, x, h=None):
        """Calcula a derivada numérica usando diferenças centradas"""
        if h is None:
            # Escolhe h baseado na magnitude de x
            h = max(1e-8, abs(x) * 1e-8)
        return (self.f(x + h) - self.f(x - h)) / (2 * h)

    def solve(self, x0):
        """Resolve para um único chute inicial"""
        x = complex(x0)  # Garante que x seja complexo para manipulação
        f, df = self.f, self.df

        for iteration in range(self.max_iter):
            fx = f(x)

            # Calcula a derivada
            if df:
                dfx = df(x)
            else:
                dfx = self._numerical_derivative(x)

            # Verifica se a derivada é quase nula
            if abs(dfx) < 1e-14:
                return None  # derivada quase nula

            # Iteração de Newton-Raphson
            x_new = x - fx / dfx

            # Verifica convergência
            if abs(x_new - x) < self.tol or abs(f(x_new)) < self.tol:
                # Aceita apenas raízes reais (com tolerância para erro numérico)
                if abs(x_new.imag) < 1e-8:
                    return round(x_new.real, 8)  # Mais precisão
                else:
                    return None

            x = x_new

        return None  # não convergiu

    def solve_multiple(self, x0_list):
        """Resolve para vários chutes iniciais e retorna raízes únicas"""
        roots = []
        for x0 in x0_list:
            root = self.solve(x0)
            if root is not None:
                # Verifica se a raiz já foi encontrada (com tolerância mais rigorosa)
                is_duplicate = any(abs(root - existing) < max(1e-6, self.tol * 100)
                                 for existing in roots)
                if not is_duplicate:
                    roots.append(root)
        return sorted(roots)

    @staticmethod
    def find_root(f, df=None, x0=1.0, tol=1e-10, max_iter=1000):
        """Atalho para resolver uma raiz a partir de um único chute inicial"""
        solver = NewtonRaphson(f, df, tol, max_iter)
        return solver.solve(x0)

    @staticmethod
    def find_all_roots(f, df=None, x0_list=None, tol=1e-10, max_iter=1000):
        """Atalho para resolver múltiplas raízes a partir de vários chutes"""
        if x0_list is None:
            # Chutes mais espaçados e em maior quantidade
            import numpy as np
            x0_list = list(np.linspace(-100, 100, 5000))
        solver = NewtonRaphson(f, df, tol, max_iter)
        return solver.solve_multiple(x0_list)
        