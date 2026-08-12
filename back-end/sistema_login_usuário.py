#from flask import Flask
#
#app=Flask(__name__)
#
#@app.route("")


usuarios=[]
def buscar_cadastro_email(email):
    for usuario in usuarios:
        if usuario["email"] == email:
            return usuario  
    return None 

def senha_valida(senha):
    for letra in senha():
        if letra.isdigt:
            numeros+=1 

    tem_maiuscula=False    
    for c in senha:
        if c.isupper():
            tem_maiuscula=True
            break

    if not tem_maiuscula:
        print("A senha precisa ter pelo menos uma letra maiúscula.")
        return False

    if numeros <10:
        print("A senha precisa ter pelo menos 10 de digitos insuficientes")
        return False

    return True
            
def email_valido(email):
    return "@gmail.com "in email


def cpf_limpo(cpf):
    resultado=0
    for c in cpf:
        if c.isdigit:
            resultado=+1
            return resultado

def cpf_valido(cpf):
    if len(cpf) <11:
        return False






def cadastro():
    
    email=input("Digite seu email").strip()
    if not email_valido(email):
        print("Email inválido. Precisa ser um endereço @gmail.com.")
        return None
    if buscar_cadastro_email:
        return None

    cpf=cpf_limpo(input("Digite seu CPF:"))


    if not cpf_valido(cpf):
        print("CPF inválido")
        return None

    
    nome=input("Digite seu nome: ").strip
        

    senha=input("Digite sua senha: ").strip()
    if not senha_valida(senha):
        return None
  
    

    novo_usuario={
        "nome":nome,
        "senha":senha,
        "email":email
    }
    usuarios.append(novo_usuario) 

    return novo_usuario



#def verificacao_pass(vf)a:
#def verificacao_user(vu)
#def email_amd_valido(email):

