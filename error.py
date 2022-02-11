class Error:
    def __init__(self, error_name, description):
        self.error_name = error_name
        self.description = description
    
    def repr(self):
        return (f'{self.error_name}: {self.description}')

