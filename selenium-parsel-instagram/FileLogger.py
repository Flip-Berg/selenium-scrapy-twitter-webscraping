import sys

class FileLogger:
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")
        sys.stdout = self

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()  # Salva imediatamente no arquivo
        # Opcional: também pode forçar flush do terminal
        self.terminal.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        sys.stdout = self.terminal
        self.log.close()