class Pessoa:
    def __init__(self,nome,idade,apelido) -> None:
        self.nome = nome 
        self.idade = idade
        self.apelido=apelido
        pass
    
    def exiNam(self):
        print(self.nome)
        
    def exiId(self):
        print(self.idade)
        
    def exiAs(self)  :
        print(self.apelido)
        

        
pessoa = Pessoa('renan',19,'rzz')
pessoa.exiNam()
pessoa.exiAs()
pessoa.exiId()

        