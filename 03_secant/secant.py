class Secant:
    def __init__(self, f, tol=1e-6, max_iter=1000):
        """
        Inicializa o método da Secante.
        f: função alvo
        tol: tolerância
        max_iter: número máximo de iterações
        """
        self.f = f
        self.tol = tol
        self.max_iter = max_iter

    def solve(self, x0, x1):
        """Resolve para um par de chutes iniciais x0 e x1"""
        f = self.f
        x0, x1 = complex(x0), complex(x1)

        for iteration in range(self.max_iter):
            f0, f1 = f(x0), f(x1)

            # Evita divisão por zero
            if abs(f1 - f0) < 1e-14:
                return None

            # Fórmula da secante
            x_new = x1 - f1 * (x1 - x0) / (f1 - f0)

            # Convergência
            if abs(x_new - x1) < self.tol or abs(f(x_new)) < self.tol:
                if abs(x_new.imag) < 1e-8:  # raiz real
                    return round(x_new.real, 8)
                else:
                    return None

            x0, x1 = x1, x_new

        return None  # não convergiu

    def solve_multiple(self, x0_list, x1_list):
        """Resolve para vários pares de chutes iniciais e retorna raízes únicas"""
        roots = []
        for x0, x1 in zip(x0_list, x1_list):
            root = self.solve(x0, x1)
            if root is not None:
                is_duplicate = any(abs(root - existing) < max(1e-6, self.tol * 100)
                                 for existing in roots)
                if not is_duplicate:
                    roots.append(root)
        return sorted(roots)

    @staticmethod
    def find_root(f, x0, x1, tol=1e-10, max_iter=1000):
        """Atalho para resolver uma raiz a partir de dois chutes"""
        solver = Secant(f, tol, max_iter)
        return solver.solve(x0, x1)

    @staticmethod
    def find_all_roots(f, x0_list=None, x1_list=None, tol=1e-10, max_iter=1000):
        """Atalho para resolver múltiplas raízes a partir de vários pares de chutes"""
        import numpy as np
        if x0_list is None or x1_list is None:
            # Gera pares de chutes igualmente espaçados
            x0_list = np.linspace(-100, 100, 5000)
            x1_list = x0_list + 0.01  # pequeno deslocamento
        solver = Secant(f, tol, max_iter)
        return solver.solve_multiple(x0_list, x1_list)