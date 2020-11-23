'''
update(): Recebe um array de ações, retorna o próximo estado e se o jogo acabou
'''
def GeraNovaGeração(redes, scores):
    pass

    
class TestControl:
    def __init__(self):
        self.instances = [Agent(Jogo()) for i in range(num_instancias)]
        self.redes = [pass for i in range(num_instancias)]
        self.scores = [0 for i in range(num_instancias)]
    def begin():
        for agent in instances:
            agent.jump()
        self.evaluate()
        for c in range(max_it):
            self.nextGen()
            self.evaluate()
        self.end()
    def evaluate():
        existsAlive = True
        while session <= timeout and existsAlive:
            existsAlive = False
            for i in range(num_instancias):
                if self.instances[i].alive:
                    existsAlive = True
                    out = self.redes[i].process(self.instances[i].update())
                    self.instances[i].doAction(out)
        self.scores = [x.getFinalScore() for x in self.instances]
    def sortRedes():
        self.redes = [x[0] for x in sorted(zip(self.redes,self.scores), key = lambda x: x[1], reverse=True)]
    def nextGen():
        sortRedes()
        self.redes = GeraNovaGeracao(self.redes.copy(), self.scores)
    def end():
        sortRedes()
        return self.redes[0]
