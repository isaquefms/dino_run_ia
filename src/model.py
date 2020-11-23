import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class RedeNeural(nn.Module):
    def __init__(self, gen=None):
        super(RedeNeural, self).__init__()
        self.conv1 = nn.Conv2d(2,4,6)
        self.conv2 = nn.Conv2d(4,8,3)
        self.fc1 = nn.Linear(2752, 32)
        self.fc2 = nn.Linear(32, 3)
        if gen!=None:
            self.setGenome(gen)
    def foward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.softmax(x, dim=1)
        return x
    def getGenome(self):

        p11 = self.conv1.weight.detach().numpy().flatten()
        #print(len(p11))
        p12 = self.conv1.bias.detach().numpy()
        gen = np.append(p11, p12)
        #print(len(p12))
        p21 = self.conv2.weight.detach().numpy().flatten()
        gen = np.append(gen, p21)
        #print(len(p21))
        p22 = self.conv2.bias.detach().numpy()
        gen = np.append(gen, p22)
        #print(len(p22))
        p31 = self.fc1.weight.detach().numpy().flatten()
        gen = np.append(gen, p31)
        #print(len(p31))
        p32 = self.fc1.bias.detach().numpy()
        gen = np.append(gen, p32)
        #print(len(p32))
        p41 = self.fc2.weight.detach().numpy().flatten()
        gen = np.append(gen, p41)
        #print(len(p41))
        p42 = self.fc2.bias.detach().numpy()
        gen = np.append(gen, p42)
        #print(len(p42))
        #print(len(gen))
        return gen
        #return np.append([p11,p12,p21,p22,p31,p32,p41,p42])
    def setGenome(self, gen):
        p1 = gen[:292]
        #print(len(p1))
        p2 = gen[292:588]
        #print(len(p2))
        p3 = gen[588:88684]
        #print(len(p3))
        p4 = gen[88684:]
        #print(len(p4))

        w1 = np.reshape(p1[:-4], (4, 2, 6, 6))
        b1 = np.array(p1[-4:])
        self.conv1.weight = nn.Parameter(torch.from_numpy(w1).float(),requires_grad=True)
        self.conv1.bias = nn.Parameter(torch.from_numpy(b1).float(),requires_grad=True)

        w2 = np.reshape(p2[:-8], (8, 4, 3, 3))
        b2 = np.array(p2[-8:])
        self.conv2.weight = nn.Parameter(torch.from_numpy(w2),requires_grad=True)
        self.conv2.bias = nn.Parameter(torch.from_numpy(b2),requires_grad=True)

        w3 = np.reshape(p3[:-32], (32, 2752))
        b3 = np.array(p3[-32:])
        self.fc1.weight = nn.Parameter(torch.from_numpy(w3),requires_grad=True)
        self.fc2.bias = nn.Parameter(torch.from_numpy(b3),requires_grad=True)

        w4 = np.reshape(p4[:-3], (3, 32))
        b4 = np.array(p4[-3:])
        self.fc2.weight = nn.Parameter(torch.from_numpy(w4),requires_grad=True)
        self.fc2.bias = nn.Parameter(torch.from_numpy(b4),requires_grad=True)

        

expl_img = [[0.5 for i in range(50)] for j in range(15)]
test = np.stack((expl_img, expl_img), axis=0).reshape(1, 2, 15, 50)
#print(test)
a = RedeNeural()
b = RedeNeural()
#print(a.foward(torch.tensor(test).float()).tolist()[0])
#print(a.getGenome())
x = a.getGenome()
b.setGenome(x)
y = b.getGenome()

print(x[14500:14510])
print(y[14500:14510])

print(a.foward(torch.tensor(test).float()))
print(b.foward(torch.tensor(test).float()))