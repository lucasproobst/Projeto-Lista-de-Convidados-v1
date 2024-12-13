import time
import db
import bcrypt

convidados = []

def telaInicio():
    while True:
        try:
            print('''
                [SISTEMA - Lista de Convidados]
                [1] - Login
                [2] - Cadastrar
                [3] - Sair
            ''')
            
            opcao = int(input('Opção: '))
            
            match opcao:
                case 1:
                    login()
                case 2:
                    cadastroUsuario()
                case 3:
                    print('Saindo...')
                    break
        except ValueError:
            print('Opcao invalida.')
            telaInicio()

def login():
    user = input('Usuário: ')
    passwd = input('Senha: ')

    user_data = db.collection_login.find_one({'user': user})

    if user_data and bcrypt.checkpw(passwd.encode('utf-8'), user_data['password'].encode('utf-8')):
        print("Login bem-sucedido!")
        menu()
    else:
        print("Usuário ou senha incorretos. Redirecionando para o cadastro.")
        cadastroUsuario()
            
def cadastroUsuario():
    user = input('Novo usuário: ')
    passwd = input('Nova senha: ')

    hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

    db.collection_login.insert_one({'user': user, 'password': hashed_passwd.decode('utf-8')})

    print("Usuário cadastrado com sucesso!")

def adicionarNome():
    nome_convidado = input('Nome Completo: ')
    try:
        idade_convidado = int(input('Idade: '))
        if nome_convidado == '':
            print('Nome vazio. Tente novamente.')
        else:
            db.collection.insert_one({'nome': nome_convidado, 'idade': idade_convidado})
            print(f'''
                  [Lista de Convidados]
                  [{nome_convidado}] foi adicionado com sucesso.
                  ''')
    except ValueError:
        print("Erro: A idade deve ser um número inteiro. Tente novamente.")

def removerNome():
    nome_convidado = input('Nome do convidado a remover: ')
    dadosConvidados = list(db.collection.find({'nome': nome_convidado}))
    
    for convidado in dadosConvidados:
        if convidado['nome'].lower() == nome_convidado.lower():
            db.collection.delete_one({'nome': nome_convidado})
            print(f"[{nome_convidado}] foi removido com sucesso.")
            return
    print(f"Convidado [{nome_convidado}] não encontrado.")

def atualizarNome():
    nome_convidado = input('Nome a atualizar: ')
    
    dadosConvidados = db.collection.find_one({'nome': nome_convidado})
    
    if not dadosConvidados:
        print(f"[{nome_convidado}] não foi encontrado na lista.")
    else:
        novoNome = input('Novo nome: ')
        db.collection.update_one(
            {'nome': nome_convidado},
            {'$set': {'nome': novoNome}}
        )
        print(f"Nome atualizado de [{nome_convidado}] para [{novoNome}].")
    
def verificarNome():
    nome_convidado = input('Nome a verificar: ')
    dadosConvidados = list(db.collection.find({'nome': nome_convidado}))
    
    for convidado in dadosConvidados:
        if convidado['nome'].lower() == nome_convidado.lower():
            print(f"[{nome_convidado}] está na lista.")
            return
    print(f"[{nome_convidado}] não encontrado na lista.")

def listarConvidados():
    print("\n[Lista Completa de Convidados]")
    dadosConvidados = list(db.collection.find())
    for convidado in dadosConvidados:
        print(f"Nome: {convidado['nome']}\nIdade: {convidado['idade']}\n")

def menu():
    while True:
        try:
            print('''
                [Lista de Convidados]

                [1] - Adicionar convidado
                [2] - Remover convidado
                [3] - Atualizar convidado
                [4] - Verificar nome
                [5] - Lista Completa

                [99] - Sair
                ''')
            
            opcao = int(input('Opção: '))
            
            match opcao:
                case 1:
                    adicionarNome()
                case 2:
                    removerNome()
                case 3:
                    atualizarNome()
                case 4:
                    verificarNome()
                case 5:
                    listarConvidados()
                case 99:
                    break
                case _:
                    print("Opção inválida.")
        except ValueError:
            print('Opção inválida. Digite um número correspondente ao menu.')
            time.sleep(1)

telaInicio()
