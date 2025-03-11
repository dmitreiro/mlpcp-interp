# mlpcp-interp
**Machine Learning** for **Prediction** of **Constitutive Parameters** - **Interpolation** study

## :open_book: Abstract

Given the extensive use of sheet metal forming processes in the industry and
the constant emergence of new materials, the accurate prediction of material constitutive
parameters is extremely important to enhance and optimise these processes. Machine
learning techniques have proven to be highly promising for predicting these parameters
using data obtained either experimentally or through numerical simulations. However, ML
models are often constrained by the limited dataset coverage from numerical simulations,
which restricts their predictive capability to specific finite element meshes, leading to
potential dependency on the discretisation scheme. To address this challenge, a new
approach is proposed that integrates ML with interpolation and extrapolation of strain data
from numerical simulations to a grid of points within the specimen domain, expanding
the dataset coverage and reducing dependency on discrete mesh points. The current work
explores this approach by interpolating and extrapolating manipulated data obtained from
a Finite Element Analysis considering a biaxial tensile test on a cruciform-shaped sample.
Models are trained and evaluated for performance and robustness. The results show the
high accuracy of the interpolated data, along with the excellent performance metrics and
robustness of the trained models, ensuring the successful implementation of this approach.

## :gear: Setup

### Clone

Open terminal, change your current working directory to the location where you want the cloned directory and then clone this repository to your local machine

```
git clone https://github.com/dmitreiro/MLCCM.git
```

### Config

Inside your repository home folder, edit ```config/config.ini``` file to define your paths.

### Environment

Next, install **Anaconda** for managing your Python environments. You can check documentation [here](https://docs.anaconda.com/anaconda/install/).\
After the installation, create an empty environment using **Python 3.11.10**

```
conda create --name <your_env_name> python=3.11.10
conda activate <your_env_name>
```

Then, navigate to your repository home folder and install dependencies

```
pip install -r requirements.txt
```

### Run your code

Now, you are ready to rock :sunglasses:\
Just run

```
python main.py
```

## :balance_scale: License

This project is licensed under the MIT License, which allows anyone to use, modify, and distribute this software for free, as long as the original copyright and license notice are included. See the [LICENSE](LICENSE) file for more details.
