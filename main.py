import random
import math
import matplotlib.pyplot as plt
import numpy as np
  
# parametros
bounds = [(-10, 10), (-10, 10)]  # rangos de la función absoluta
nv = 2  # numero de variables
initial_fitness = float("inf") # valor inicial de las particulas
particle_size = 50  # cantidad de particulas
gen = 100  # numero maximo de generaciones
w = 0.75  # constante de inercia
c1 = 1  # tasa cognitiva
c2 = 2  # tasa social

def plot(x, y, title):
    fig = plt.figure(figsize=(5, 5))
    fig.tight_layout()
    plt1 = fig.add_subplot(1,1,1)
    plt1.plot(x, y)
    plt1.set_title(title)
    plt.show()

class Particle:
    def __init__(self, bounds):
        self.position = []
        self.velocity = []
        self.l_best = []  # mejores posiciones de la particula
        self.fitness_l_best = initial_fitness  # initial objective function value of the best particle position
        self.fitness_position = initial_fitness  # objective function value of the particle position
  
        for i in range(nv):
            self.position.append(
                random.uniform(bounds[i][0], bounds[i][1]))  # genera posiciones aleatorias
            self.velocity.append(random.uniform(-1, 1))  # genera velocidades iniciales aleatorias
    
    def fitness(self, X):
        return np.sum(np.abs(np.array(X)))
  
    def evaluate(self):
        self.fitness_position = self.fitness(self.position)
        # comparamos la posición actual con la mejor particula local
        if self.fitness_position < self.fitness_l_best:
            self.l_best = self.position
            self.fitness_l_best = self.fitness_position

    def update_velocity(self, g_best):
        for i in range(nv):
            r1 = random.random()
            r2 = random.random()
            cognitive_velocity = c1 * r1 * (self.l_best[i] - self.position[i])
            social_velocity = c2 * r2 * (g_best[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, bounds):
        for i in range(nv):
            self.position[i] = self.position[i] + self.velocity[i]
            maxPos = bounds[i][1]
            minPos = bounds[i][0]

            if self.position[i] > maxPos:
                self.position[i] = maxPos
            if self.position[i] < minPos:
                self.position[i] = minPos

def main():
    # guarda el valor "fitness" de la mejor posición
    fitness_g_best = initial_fitness
    # guarda las mejores posiciones encontradas
    g_best = []
    # representa todas las particulas
    swarm_particle = []
    y = []
    x = list(range(gen))

    # creamos las particulas
    for i in range(particle_size):
        swarm_particle.append(Particle(bounds))

    # generaciones
    for i in range(gen):
        # iteramos por cada particula
        for j in range(particle_size):
            swarm_particle[j].evaluate()
            # revisamos si la posición actual es mejor que la posición global
            if swarm_particle[j].fitness_position < fitness_g_best:
                g_best = list(swarm_particle[j].position)
                fitness_g_best = float(swarm_particle[j].fitness_position)
        # actualizamos posiciones y velocidades
        for k in range(particle_size):
            swarm_particle[k].update_velocity(g_best)
            swarm_particle[k].update_position(bounds)
        # añadimos el mejor valor global para ser graficado
        y.append(fitness_g_best)

    

    print("Solución optima: ", g_best)
    print("Valor de la función objetivo: ", fitness_g_best)
    plot(x,y,"PSO")

if __name__ == "__main__":
    main()