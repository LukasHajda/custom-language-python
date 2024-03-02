from classes.scanner import Scanner
from classes.token import TokenVariant



if __name__ == '__main__':
    # test = DullRepetitiveClass(4)
    # test.somemethod()
    # scanner = Scanner()

    scanner = Scanner()

    with open('source_code.txt', 'r') as file:
        source = file.read()
    file.close()

    scanner.scanner.input(source)
    token = scanner.get_token()

    while token.token_variant != TokenVariant.T_EOF:
        print(f"TOKEN: {token}")
        token = scanner.get_token()


