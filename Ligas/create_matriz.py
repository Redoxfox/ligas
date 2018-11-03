
class CreateMatix:
    def matrix(self, fil, col):
        self.fil = fil
        self.col = col
        self.matrix=[]
        for i  in range(self.fil):
            self.matrix.append([0]*self.col)

        return self.matrix

miMatrix = CreateMatix()
print(miMatrix.matrix(100,100))

