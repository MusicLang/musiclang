


class ModelWrapper:


    def train(self, train_data, val_data, epochs=10, criterion=None) -> 'ModelWrapper':
        raise NotImplemented

    def predict(self, tokens):
        raise NotImplemented


    def save_model(self, filepath):
        raise NotImplemented

    @classmethod
    def load_model(cls, filepath):
        raise NotImplemented
