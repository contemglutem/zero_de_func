import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

class NNMethods:
    def __init__(self, f):
        self.f = f

    # ---------------- Estimar intervalo próximo da raiz ----------------
    def estimate_root_interval(self, start=-100, end=100, steps=1000, margin=0.2):
        f = self.f
        H_vals = np.linspace(start, end, steps)
        f_vals = f(H_vals)

        # Procura a primeira troca de sinal
        for i in range(len(H_vals)-1):
            if f_vals[i] * f_vals[i+1] < 0:
                root_guess = (H_vals[i] + H_vals[i+1]) / 2
                H_min = max(root_guess - margin, start)
                H_max = min(root_guess + margin, end)
                return H_min, H_max
        # Se não houver troca de sinal, pega valor mínimo
        idx = np.argmin(np.abs(f_vals))
        root_guess = H_vals[idx]
        H_min = max(root_guess - margin, start)
        H_max = min(root_guess + margin, end)
        return H_min, H_max

    # ---------------- Funções de ativação ----------------
    @staticmethod
    def sin_activation(x, **kwargs):
        return tf.sin(x)

    @staticmethod
    def cos_activation(x, **kwargs):
        return tf.cos(x)

    def choose_activation(self):
        # Estima complexidade para decidir ativação
        complexity = self.function_complexity()
        if complexity > 10:
            return self.sin_activation
        return "tanh"

    # ---------------- Estimar complexidade da função ----------------
    def function_complexity(self, start=-10, end=10, steps=500):
        x_vals = np.linspace(start, end, steps)
        f_vals = self.f(x_vals)
        f_prime = np.diff(f_vals)
        sign_changes = np.sum(np.diff(np.sign(f_prime)) != 0)
        return sign_changes

    # ---------------- Ajuste automático da rede ----------------
    def network_size(self):
        complexity = self.function_complexity()
        if complexity < 3:
            neurons = [16, 8]
        elif complexity < 10:
            neurons = [32, 16, 8]
        else:
            neurons = [64, 32, 16, 8]
        return neurons

    # ---------------- Construir modelo ----------------
    def build_model(self):
        neurons = self.network_size()
        activation = self.choose_activation()

        model = models.Sequential()
        model.add(layers.Input(shape=(1,)))
        for n in neurons:
            model.add(layers.Dense(n, activation=activation))
        model.add(layers.Dense(1))  # saída: raiz
        return model

    # ---------------- Treinar rede e prever raiz ----------------
    def train_and_pred(self, loss_tol=1e-6, max_epochs=5000, lr_init=1e-2):
        f = self.f
        x_min, x_max = self.estimate_root_interval()
        x_train = np.linspace(x_min-5, x_max+5, 1000).reshape(-1, 1).astype(np.float32)

        model = self.build_model()
        optimizer = optimizers.Adam(learning_rate=lr_init)
        loss = tf.constant(10.0)
        epoch = 0
        lr_factor = 0.5
        stuck_epochs = 0
        prev_loss = np.inf

        while loss.numpy() > loss_tol and epoch < max_epochs:
            with tf.GradientTape() as tape:
                x_pred = model(x_train, training=True)
                x_pred = tf.clip_by_value(x_pred, 0.001, 10.0)
                loss = tf.reduce_mean(tf.square(f(x_pred)/25.0))

            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

            # Ajuste automático do learning rate se travar
            if np.abs(loss.numpy() - prev_loss) < 1e-8:
                stuck_epochs += 1
            else:
                stuck_epochs = 0
            if stuck_epochs >= 200:
                old_lr = optimizer.learning_rate.numpy()
                new_lr = max(old_lr * lr_factor, 1e-6)
                optimizer.learning_rate.assign(new_lr)
                print(f"Learning rate ajustado de {old_lr:.6f} para {new_lr:.6f} no epoch {epoch}")
                stuck_epochs = 0

            prev_loss = loss.numpy()
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss={loss.numpy():.6f}")
            epoch += 1

        # Obter raiz aproximada
        x_roots_pred = model(x_train).numpy()
        approx_root = float(x_roots_pred[np.argmin(np.abs(f(x_roots_pred))), 0])
        print("Raiz aproximada (PINN):", approx_root)

        # Refinamento final com Newton-Raphson
        refined_root = NewtonRaphson.find_root(f, x0=approx_root)
        print("Raiz refinada (Newton-Raphson):", refined_root)

        return refined_root
