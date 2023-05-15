# AugmentedNet
A Roman Numeral Analysis Network with Synthetic Training Examples and Additional Tonal Tasks

> The `main` branch is now an improved neural network. The source code of the published version (`v1.0.0`) can be found in the [v1](https://github.com/napulen/AugmentedNet/tree/v1) branch. The differences are indicated in any releases > `v1.0.0`. If you report against the published results, you are comparing against `v1.0.0`. If you want to compare against the latest network, train a model using this code.

### ISMIR Paper 

N. Nápoles López, M. Gotham, and I. Fujinaga, "AugmentedNet: A Roman Numeral Analysis Network with Synthetic Training Examples and Additional Tonal Tasks." in *Proceedings of the 22nd International Society for Music Information Retrieval Conference*, 2021, pp. 404–411. https://doi.org/10.5281/zenodo.5624533


```bibtex
@inproceedings{napoleslopez21augmentednet,
  author       = {Nápoles López, Néstor and Gotham, Mark and Fujinaga, Ichiro},
  title        = {{AugmentedNet: A Roman Numeral Analysis Network 
                   with Synthetic Training Examples and Additional
                   Tonal Tasks}},
  booktitle    = {{Proceedings of the 22nd International Society for 
                   Music Information Retrieval Conference}},
  year         = 2021,
  pages        = {404-411},
  publisher    = {ISMIR},
  address      = {Online},
  month        = nov,
  venue        = {Online},
  doi          = {10.5281/zenodo.5624533},
  url          = {https://doi.org/10.5281/zenodo.5624533}
}
```

## Try out the pre-trained network

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/napulen/AugmentedNet/blob/main/notebooks/AugmentedNet.ipynb)


Clone, create a virtual environment, and get the `python` dependencies. 

```bash
git clone https://github.com/napulen/AugmentedNet.git
cd AugmentedNet
python3 -m venv .env 
source .env/bin/activate

(.env) pip install -r requirements.txt
```

> I have experienced that `pip` is sometimes incapable of installing specific package versions depending on your environment. This `requirements.txt` was tested on a vanilla `Ubuntu 20.04`, both in native linux and Windows 10 WSL2. A docker `tensorflow/tensorflow:2.5-gpu` image should also work.

Run the pre-trained model for inference on a `MusicXML` file

```bash
python -m AugmentedNet.inference AugmentedNetv.hdf5 <input_file>.musicxml
```

Two files will be generated:

- `<input_file>_annotated.xml`
- `<input_file>_annotated.csv`

An annotated `MusicXML` file and the `csv` file with the predictions of every time step.

## Training the network from scratch

Clone **recursively** (needed to collect the third-party datasets), create a virtual environment, and get the `python` dependencies

```bash
git clone --recursive https://github.com/napulen/AugmentedNet.git
cd AugmentedNet
python3 -m venv .env 
source .env/bin/activate

(.env) pip install -r requirements.txt
```

### Using accompanying data

To save you some time, we include the preprocessed `tsv` files of the *real* data, as well as the *synthetic* block-chord templates for texturization. These are available in the release of the latest version.

```bash
wget https://github.com/napulen/AugmentedNet/releases/latest/download/dataset.zip
unzip dataset.zip
```

Now you are ready to train the network.

### Generating synthetic examples

There are two ways to generate texturizations: at the tsv-level (legacy) and at the numpy-level (newer).

#### Texturizations at the tsv-level (legacy)

You can generate one texturization per file in the dataset with this script

```python
(.env) python -m AugmentedNet.dataset_tsv_generator --synthesize --texturize
```

Originally, this is how I trained `v1.0.0`. The network was trained with exactly twice the amount of *real* training data.

#### Texturizations at the npz-level (newer)

After `v1.5.0`, the tsv-dataset only includes the templates (i.e., **block chords**). The texturization is done when encoding the numpy arrays for the neural network. Right before training.

There are two options for texturization in this way
1. Generate one texturization per file
2. Generate one texturization per **transposition**

In the second approach, every time you transpose a synthetic example to a different key, you re-texturize it. The amount of "new" training examples seen by the network is much larger this way.

You can control those settings when training the network.

```bash
# No synthetic examples
(.env) python -m AugmentedNet.train <compulsory_args>

# Synthetic examples, one texturization per file
(.env) python -m AugmentedNet.train <compulsory_args> --syntheticDataStrategy concatenate

# Synthetic examples, one texturization per transposition
(.env) python -m AugmentedNet.train <compulsory_args> --syntheticDataStrategy concatenate --texturizeEachTransposition
```

See next section for the `<compulsory_args>`.

> At the moment, the code for generating the texturizations is not extremely simple, if you only wanted to do that. However, raise an issue, reach out, and I'll make my best effort to help you on your use case.


### Training the network

If you want to train the network, the minimum call looks like this.

```bash
(.env) python -m AugmentedNet.train debug testexperiment
```

The code is integrated with [mlflow](https://mlflow.org/). In the training script, `debug` and `testexperiment` refer to the *experiment* and *run* names passed down to mlflow. You can access more CLI parameters by running `python -m AugmentedNet.train --help`.

After training the network, you will get a path to the trained `hdf5` model, which looks something like this:

```
The trained model is available in: .model_checkpoint/debug/testexperiment-220101T000000/81-6.000-0.78.hdf5
```

You can use that trained model for inference, using the same workflow shown above.

## About the AugmentedNet

### The neural network architecture

The architecture is a CRNN (Convolutional Recurrent Neural Network) with an alternative representation of pitch spelling at the input.

More information about the neural network architecture can be found in the [paper](https://archives.ismir.net/ismir2021/paper/000050.pdf).

![AugmentedNet Architecture](img/AugmentedNetArchitecture.png)


### Organization of the repo

This repository is organized in the following way

- [AugmentedNet](AugmentedNet) has all the source code of the network
- [img](img) the image diagrams of the network and code organization
- [misc](misc) useful, but non-essential, stand-alone scripts that I wrote while developing this project
- [notebooks](notebooks) Jupyter notebook *playgrounds* used throughout the project (e.g., data exploration)
- [test](test) unit tests for all relevant modules of the network

### The AugmentedNet source code

The general organization of the code is summarized by the following diagram.

![AugmentedNet](img/AugmentedNetCode.png)

Each of the blue rectangles roughly corresponds to a Python module.

The inputs of the network are pairs of ([MusicXML](https://github.com/napulen/AugmentedNet/raw/main/rawdata/corrections/BPS/bps_02_01.mxl), [RomanText](https://raw.githubusercontent.com/napulen/AugmentedNet/main/rawdata/corrections/WiR/Corpus/Piano_Sonatas/Beethoven%2C_Ludwig_van/Op002_No2/1/analysis.txt?token=ABXMCX76PQLK7FU4FBXXCRDBCUPRW)) files.

The inputs pairs are converted into [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) objects, stored as `.tsv` files.

Later on, these are encoded in a representation that can be dispatched to the neural network.

The module documentation is located [here](https://napulen.github.io/AugmentedNet).

## Experiments

### Visualizing the results with [mlflow](https://mlflow.org/)

All the experiments presented in the paper were monitored using `mlflow`.

If you want to visualize the experiments with the [mlflow ui](https://www.mlflow.org/docs/latest/quickstart.html#viewing-the-tracking-ui): 

1. `pip install mlflow`
2. Download our [mlruns](https://github.com/napulen/AugmentedNet/releases/download/v1.0.0/mlruns.zip) with the AugmentedNet experiments
3. Unzip anywhere
4. Run `mlflow ui` from the terminal; make sure that `./mlruns/` is reachable from the current directory
5. Visit `localhost:5000`
6. That's it! The experiments should be available in the browser

For extra convenience, I also uploaded the logs to [TensorBoard.dev](https://tensorboard.dev/).

Here are the tables of the paper and a link to see the runs of each model in Tensorboard.dev.

### Paper results and tensorboard visualizations

#### AugmentedNet configurations

These are the results for the four different configurations of the AugmentedNet.

| Model                      | Key           | Deg.          | Qual.         | Inv.          | Root          | RN            |
|----------------------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AugmentedNet`6`              | 82.7          | 64.4          | 76.6          | 77.4          | 82.5          | 43.3          |
| AugmentedNet`6+`             | 83.0          | 65.1          | 77.5          | **78.6**      | 83.0          | 44.6          |
| AugmentedNet`11`             | 81.3          | 64.2          | 77.2          | 76.1          | 82.9          | 43.1          |
| AugmentedNet`11+`            | **83.7**      | **66.0**      | **77.6**      | 77.2          | **83.2**      | **45.0**      |

**[Visualize experiments in TensorBoard.dev!](https://tensorboard.dev/experiment/l6CPJ7TdSdOjxCbibzQJwA/#scalars)**

`6` and `11` indicate the number of tasks in the multitask learning layout.

`+` indicates the use of synthetic training data.




#### AugmentedNet vs. other models

These are the results for the best AugmentedNet configuration (11+) against other models.

| Test set                | Training set | Model        | Key                            | Degree                | Quality               | Inversion               | Root                  | ComRN                 | RN*conv*                       | RN*alt*               |
|-------------------------|--------------|--------------|--------------------------------|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|--------------------------------|-----------------------|
| Full test set           | Full dataset | AugN         | 82.9                           | 67.0                  | 79.7                  | 78.8                  | 83.0                  | 65.6                  | 46.4                           | 51.5                  |
| WiR                     | Full dataset | AugN         | 81.8                           | 69.2                  | 85.9                  | 90.3                  | 90.3                  | 70.2                  | 56.4                           | 62.4                  |
| HaydnSun                | Full dataset | AugN         | 81.2                           | 62.9                  | 80.2                  | 82.7                  | 86.5                  | 60.4                  | 48.6                           | 52.1                  |
| ABC                     | Full dataset | AugN         | 83.6                           | 65.6                  | 78.0                  | 76.9                  | 78.9                  | 62.6                  | 44.5                           | 48.4                  |
| TAVERN                  | Full dataset | AugN         | 88.7                           | 60.0                  | 77.4                  | 78.8                  | 81.5                  | 66.3                  | 42.6                           | 52.9                  |
| WTC                     | Full dataset | AugN         | 77.2                           | 69.7                  | 75.0                  | 74.4                  | 82.7                  | 61.7                  | **46.2**                       | 47.9                  |
| WTC*crossval*           | BPS+WTC      | AugN         | **85.1(4.0)**                  | 62.9(5.5)             | 69.1(1.9)             | 70.1(3.7)             | 79.2(1.8)             | 59.9(3.4)             | **42.9(4.2)**                  | 46.9(4.7)             |
| WTC*crossval*           | BPS+WTC      | CS21         | 56.3(2.5)                      | -                     | -                     | -                     | -                     | -                     | 26.0(1.7)                      | -                     |
| BPS                     | Full dataset | AugN         | **85.0**                       | **73.4**              | **79.0**              | **73.4**              | 84.4                  | 68.3                  | **45.4**                       | 49.3                  |
| BPS                     | All data     | Mi20         | 82.9                           | 68.3                  | 76.6                  | 72.0                  | -                     | -                     | 42.8                           | -                     |
| BPS                     | BPS+WTC      | AugN         | **82.9**                       | 70.9                  | 80.7                  | 72.0                  | 85.3                  | 67.6                  | **44.1**                       | 47.5                  |
| BPS                     | BPS+WTC      | CS21         | 79.0                           | -                     | -                     | -                     | -                     | -                     | 41.7                           | -                     |
| BPS                     | BPS          | AugN         | **83.0**                       | **71.2**              | **80.3**              | **71.1**              | 84.1                  | 68.5                  | **44.0**                       | 47.4                  |
| BPS                     | BPS          | Mi20         | 80.6                           | 66.5                  | 76.3                  | 68.1                  | -                     | -                     | 39.1                           | -                     |
| BPS                     | BPS          | CS19         | 78.4                           | 65.1                  | 74.6                  | 62.1                  | -                     | -                     | -                              | -                     |
| BPS                     | BPS          | CS18         | 66.7                           | 51.8                  | 60.6                  | 59.1                  | -                     | -                     | 25.7                           | -                     |

**[Visualize experiments in TensorBoard.dev!](https://tensorboard.dev/experiment/fXVA71nWTkSZh6CqTXCeCw/#scalars)**
