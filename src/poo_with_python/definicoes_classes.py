class Pessoa:
    def __init__(self,nome,idade,apelido) -> None:
        self.nome = nome 
        self.idade = idade
        self.apelido=apelido
        pass
    
    def exi_nam(self):
        print(self.nome)
        
    def exi_id(self):
        print(self.idade)
        
    def exi_as(self)  :
        print(self.apelido)
        

        
pessoa = Pessoa('renan',19,'rzz')
pessoa.exi_nam()
pessoa.exi_as()
pessoa.exi_id()

        