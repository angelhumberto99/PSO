import random
import matplotlib.pyplot as plt
import numpy as np
  
def plot(x, y, title):
    fig = plt.figure(figsize=(5, 5))
    fig.tight_layout()
    plt1 = fig.add_subplot(1,1,1)
    plt1.plot(x, y)
    plt1.set_title(title)
    plt.show()

class Particle:
    def __init__(self, cognitive, social, inertia, bound):
        # miembros privados
        self.__c1 = cognitive  # tasa cognitiva
        self.__c2 = social  # tasa social
        self.__w = inertia # tasa de inercia
        self.__min_pos = bound[0]
        self.__max_pos = bound[1]
        # la velocidad maxima y minima esta definida por
        # el 20% en la diferencia del rango de la función benchmark
        self.__min_vel = -0.2 * (self.__max_pos - self.__min_pos)
        self.__max_vel = -1 * self.__min_vel
        self.__velocity = random.uniform(-1, 1) # velocidad aleatoria entre -1 y 1
        self.__lbest = []  # mejores posiciones locales de la particula
        self.__lbest_fitness = float("inf")  # valor "fitness" de la mejor posición local
        self.__iter = 0 # iterador

        # miembros publicos
        self.position = random.uniform(self.__min_pos, self.__max_pos)
        self.current_fitness = float("inf")  # valor "fitness" de la posición por generación
    
    # función absoluta (absolute function)
    def benchmark(self, x):
        return np.sum(np.abs(np.array(x)))
  
    def selection(self):
        # obtenemos el costo de la posición actual
        self.current_fitness = self.benchmark(self.position)
        # comparamos la posición actual con la mejor particula local
        if self.current_fitness < self.__lbest_fitness:
            self.__lbest = self.position
            self.__lbest_fitness = self.current_fitness

    def update_velocity(self, gbest):
        r1 = random.random()
        r2 = random.random()
        c = self.__c1 * r1 * (self.__lbest - self.position)
        s = self.__c2 * r2 * (gbest - self.position)
        self.__velocity = self.__w[self.__iter] * self.__velocity + c + s
        self.__iter += 1
        # evitamos que se salga del rango
        if self.__velocity > self.__max_vel:
            self.__velocity = self.__max_vel
        if self.__velocity < self.__min_vel:
            self.__velocity = self.__min_vel

    def update_position(self):
        self.position = self.position + self.__velocity
        # evitamos que se salga del rango
        if self.position > self.__max_pos:
            self.position = self.__max_pos
        if self.position < self.__min_pos:
            self.position = self.__min_pos

def main():
    # parametros
    particle_amount = 50  # cantidad de particulas
    gen = 100  # número maximo de generaciones
    c1 = 1 # tasa cognitiva
    c2 = 2 # tasa social
    # la inercia disminuira paulatinamente hasta llegar a 0.4
    w = np.linspace(0.9,0.4,gen) # tasa de inercia
    bound = (-10, 10) # rango de la función absoluta

    # guarda el valor "fitness" de la mejor posición
    gbest_fitness = float("inf")

    # guarda las mejores posiciones encontradas
    gbest = float("inf")

    # representa todas las particulas
    particles = []
    y = []
    x = list(range(gen))

    # creamos las particulas
    for i in range(particle_amount):
        particles.append(Particle(c1, c2, w, bound))

    # generaciones
    for i in range(gen):
        # iteramos por cada particula
        for j in range(particle_amount):
            particles[j].selection()
            # revisamos si la posición actual es mejor que la posición global
            if particles[j].current_fitness < gbest_fitness:
                gbest = particles[j].position
                gbest_fitness = float(particles[j].current_fitness)
        # actualizamos posiciones y velocidades
        for k in range(particle_amount):
            particles[k].update_velocity(gbest)
            particles[k].update_position()
        # añadimos el mejor valor global para ser graficado
        y.append(gbest_fitness)

    print("Solución optima: ", gbest)
    print("Mejor valor global: ", gbest_fitness)
    plot(x,y,"PSO")

if __name__ == "__main__":
    main()