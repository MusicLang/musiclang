


class ModelWrapper:
    """ """


    def train(self, train_data, val_data, epochs=10, criterion=None) -> 'ModelWrapper':
        """

        Parameters
        ----------
        train_data :
            
        val_data :
            
        epochs :
             (Default value = 10)
        criterion :
             (Default value = None)

        Returns
        -------

        """
        raise NotImplemented

    def predict(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        raise NotImplemented


    def save_model(self, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        raise NotImplemented

    @classmethod
    def load_model(cls, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        raise NotImplemented
