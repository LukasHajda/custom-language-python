from classes.parser import Parser, Scanner, TokenVariant


if __name__ == '__main__':
    scanner = Scanner()
    token = scanner.get_token()

    parser = Parser(scanner)

    while token.token_variant != TokenVariant.T_EOF:
        print(f"TOKEN: {token}")
        token = scanner.get_token()


