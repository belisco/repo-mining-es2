import argparse

from pydriller import Repository

parser = argparse.ArgumentParser(prog='')
subparsers = parser.add_subparsers(dest='comando')

buscar = subparsers.add_parser('buscar')
buscar.add_argument('--name', required=True)

sair = subparsers.add_parser('sair')


def buscar(name: str):
    print(f'Iniciando busca pelo repositório: {name}')
    repo = Repository(name)
    commits = repo.traverse_commits()
    for commit in commits:
        print(commit.author.name)


def main():
    args = parser.parse_args()

    name = args.name

    buscar(name)

    # TRATAMENTO DOS COMANDOS.
    # INATIVO ENQUANTO A LOGICA DA BUSCA ESTIVER EM TESTE
    # while True:
    #     try:
    #         linha = input('> ')

    #     except KeyboardInterrupt:
    #         print('\nSaindo')
    #         break

    #     if not linha.strip():
    #         continue

    #     try:
    #         args = parser.parse_args(shlex.split(linha))

    #     except SystemExit:
    #         continue

    #     comando = args.comando

    #     if comando == 'buscar':
    #         name = args.name
    #         buscar(name)

    #     elif comando == 'sair':
    #         print('Saindo')
    #         sys.exit()

    #     elif comando is None:
    #         parser.print_help()


if __name__ == '__main__':
    main()
