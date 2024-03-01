from classes.scanner import Scanner




if __name__ == '__main__':
    # test = DullRepetitiveClass(4)
    # test.somemethod()
    # scanner = Scanner()

    scanner = Scanner()

    with open('source_code.txt', 'r') as file:
        source = file.read()
    file.close()

    scanner.scanner.input(source)

    while True:
        token = scanner.scanner.token()
        if not token:
            break
        print(f"TOKEN: {token}")



