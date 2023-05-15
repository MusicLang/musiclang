"""Various utilities used throughout the other modules."""

import os

import numpy as np


def tensorflowGPUHack():
    """ """
    import tensorflow as tf

    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def disableGPU():
    """ """
    # Disabling the GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def padToSequenceLength(arr, sequenceLength, value=0):
    """

    Parameters
    ----------
    arr :
        
    sequenceLength :
        
    value :
         (Default value = 0)

    Returns
    -------

    """
    frames, features = arr.shape
    featuresPerSequence = sequenceLength * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    paddingTimesteps = int(padding / features)
    arr = np.pad(arr, ((0, paddingTimesteps), (0, 0)), constant_values=value)
    arr = arr.reshape(-1, sequenceLength, features)
    return arr


class DynamicArray:
    """ """
    def __init__(
        self,
        shape=(0,),
        dtype=float,
        initial_capacity=1000,
        growth_factor=2,
        memmap="",
    ):
        """First item of shape is ignored, the rest defines the shape."""
        self.shape = shape
        if memmap:
            self.data = np.memmap(
                memmap,
                mode="w+",
                shape=(initial_capacity, *shape[1:]),
                dtype=dtype,
            )
        else:
            self.data = np.zeros((initial_capacity, *shape[1:]), dtype=dtype)
        self.capacity = initial_capacity
        self.growth_factor = growth_factor
        self.memmap = memmap
        self.size = 0
        self.dtype = dtype

    def update(self, x):
        """

        Parameters
        ----------
        x :
            

        Returns
        -------

        """
        if self.size == self.capacity:
            self.capacity = int(self.capacity * self.growth_factor)
            if self.memmap:
                self.data.flush()
                self.data = np.memmap(
                    self.memmap,
                    mode="r+",
                    shape=(self.capacity, *self.data.shape[1:]),
                    dtype=self.dtype,
                )
            else:
                self.data = np.resize(
                    self.data, (self.capacity, *self.data.shape[1:])
                )
        self.data[self.size] = x
        self.size += 1

    def finalize(self):
        """ """
        return self.data[: self.size]
