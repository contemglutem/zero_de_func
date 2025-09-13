class Bisection:
    def __init__(self, f, a, b, tol=1e-6, max_iter=1000):
        self.f = f
        self.a = a
        self.b = b
        self.tol = tol
        self.max_iter = max_iter

    @staticmethod
    def initial_guess(f, start=0, end=500):
        """Encontra intervalo [a, b] com mudança de sinal"""
        for T in range(start, end):
            try:
                if f(T) * f(T + 1) < 0:
                    return T, T + 1
            except ZeroDivisionError:
                continue  # ignora pontos inválidos

        # Se não houver troca de sinal, retorna intervalo padrão
        print("Não foi encontrada troca de sinal! Usando intervalo padrão [0, 1].")
        return 0, 1

    def solve(self):
        a, b = self.a, self.b
        f = self.f

        try:
            fa, fb = f(a), f(b)
        except ZeroDivisionError:
            fa, fb = 1, -1  # força sinais opostos para continuar

        # Se não houver troca de sinal, apenas tenta a bisseção
        if fa * fb > 0:
            print("f(a) e f(b) têm o mesmo sinal! Tentando bisseção mesmo assim...")

        for _ in range(self.max_iter):
            m = 0.5 * (a + b)
            try:
                fm = f(m)
            except ZeroDivisionError:
                fm = 0  # força a parada se divisão por zero

            if abs(fm) < self.tol or (b - a) / 2 < self.tol:
                return m

            if fa * fm < 0:
                b = m
                fb = fm
            else:
                a = m
                fa = fm

        return 0.5 * (a + b)

    @staticmethod
    def find_root(f, tol=1e-10):
        """Resolve uma função f usando bisseção e retorna a raiz"""
        a, b = Bisection.initial_guess(f)
        solver = Bisection(f, a, b, tol=tol)
        return solver.solve()
