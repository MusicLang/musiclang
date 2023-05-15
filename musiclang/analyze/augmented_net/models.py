"""Definition of the Roman numeral analysis deep neural network(s)."""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def AugmentedNet(inputs, outputs, blocks=6):
    """Definition of the AugmentedNet architecture.

    Parameters
    ----------
    inputs :
        
    outputs :
        
    blocks :
         (Default value = 6)

    Returns
    -------

    """
    x = []  # (raw) inputs of the network
    xprime = []  # inputs after initial convolutional blocks
    for i in inputs:
        sequenceLength = i.array.shape[1]
        inputFeatures = i.array.shape[2]
        name = i.name.replace("training_", "")
        xi = layers.Input(shape=(sequenceLength, inputFeatures), name=name)
        x.append(xi)
        for i in range(blocks):
            filters = 2 ** (blocks - 1 - i)
            kernel = 2 ** i
            h = layers.Conv1D(filters, kernel, padding="same")(xi)
            h = layers.BatchNormalization()(h)
            h = layers.Activation("relu")(h)
            xi = layers.Concatenate()([xi, h])
        xprime.append(xi)
    if len(x) > 1:
        inputs = layers.Concatenate()(xprime)
    else:
        inputs = xprime[0]
    h = layers.Dense(64)(inputs)
    h = layers.BatchNormalization()(h)
    h = layers.Activation("relu")(h)
    h = layers.Dense(32)(h)
    h = layers.BatchNormalization()(h)
    h = layers.Activation("relu")(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    y = []
    for output in outputs:
        outputFeatures = output.outputFeatures
        out = layers.Dense(outputFeatures, name=output.shortname)(h)
        y.append(out)
    model = keras.Model(inputs=x, outputs=y)
    return model


def Micchi2020(inputs, outputs):
    """The model by Micchi et al. (2020).

    Parameters
    ----------
    inputs :
        
    outputs :
        

    Returns
    -------

    """

    def DenseNetLayer(x, b, f, n=1):
        """

        Parameters
        ----------
        x :
            
        b :
            
        f :
            
        n :
             (Default value = 1)

        Returns
        -------

        """
        with tf.name_scope(f"denseNet_{n}"):
            for _ in range(b):
                y = layers.BatchNormalization()(x)
                y = layers.Conv1D(
                    filters=4 * f,
                    kernel_size=1,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                y = layers.BatchNormalization()(y)
                y = layers.Conv1D(
                    filters=f,
                    kernel_size=8,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                x = layers.Concatenate()([x, y])
        return x

    def PoolingLayer(x, k, s, n=1):
        """

        Parameters
        ----------
        x :
            
        k :
            
        s :
            
        n :
             (Default value = 1)

        Returns
        -------

        """
        with tf.name_scope(f"poolingLayer_{n}"):
            y = layers.BatchNormalization()(x)
            y = layers.Conv1D(
                filters=k,
                kernel_size=1,
                padding="same",
                data_format="channels_last",
            )(y)
            y = layers.Activation("relu")(y)
            y = layers.BatchNormalization()(y)
            y = layers.MaxPooling1D(
                s, s, padding="same", data_format="channels_last"
            )(y)
        return y

    def MultiTaskLayer(h, outputs):
        """

        Parameters
        ----------
        h :
            
        outputs :
            

        Returns
        -------

        """
        y = []
        for output in outputs:
            outputFeatures = output.outputFeatures
            out = layers.Dense(outputFeatures, name=output.shortname)(h)
            y.append(out)
        return y

    _, sequenceLength, inputFeatures = inputs[0].array.shape
    notes = layers.Input(shape=(sequenceLength, inputFeatures))

    x = DenseNetLayer(notes, b=4, f=8, n=1)
    x = PoolingLayer(x, 32, 2, n=1)
    x = DenseNetLayer(x, 4, 5, n=2)
    x = PoolingLayer(x, 48, 2, n=1)

    x = layers.Bidirectional(
        layers.GRU(64, return_sequences=True, dropout=0.3)
    )(x)

    # I don't think we need the TimeDistributed
    # however, leaving as is
    # https://stackoverflow.com/questions/47305618
    # https://github.com/keras-team/keras/issues/11547
    x = layers.TimeDistributed(layers.Dense(64, activation="tanh"))(x)
    y = MultiTaskLayer(x, outputs)

    model = keras.Model(inputs=[notes], outputs=y)
    return model


available_models = {
    "AugmentedNet": AugmentedNet,
    "Micchi2020": Micchi2020,
}
