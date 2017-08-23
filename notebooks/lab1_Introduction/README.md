# Lab 1: Dense Feed-Forward Networks

Lab 1 demonstrates how to implement neural networks in several different ways using the simple Two-Moons problem.

After having completed this lab you should ...
* know how inference and training are performed in neural networks
* know how computaions are speed up using linear algebra
* be able to use basic TensorFlow functionalities
* be able to setup and train a simple deep learning model

## Assignments
<!-- * `1_FFN_Intro_Basic.ipynb`: 
	* **Start here if linear algebra and machine learning is new to you**
	* Demonstrates how to implement a neural network the simplest way possible - no fancy libraries, no linear algebra.
-->
* `Installation verification`
	* Simple test of whether everything is installed and configured correctly.
* `demo - Introduction to NN (and linear algebra)`
	* [Only Numpy]
	* How the input to each unit is computed
	* How 
	* How the input to a layer is computed, and why it is equivalent
* `demo - Introduction to TensorFlow`
	* Basic TensorFlow operations, and how to use it for simple computations.
	* Using TensorBoard to visualize the computational graph and the learning process.
	* Simple linear regression example.
* `??? - Backpropagation` **Optional, advanced**
	* [How it REALLY works]
* `tut - FFN with TensorFlow - low level`
	* Manual forward
	* Manual backwards
* `demo - Introduction to High-level APIs (Keras)`
	* Automatic differentiation
	* Advanced optimizers
	* Layer abstractions (Keras)
	* ?? Supervisor ??
* `exe_The_IRIS_dataset` Solve IRIS dataset 
	* Manual forward
	* Manual backpropagation
	* Visualize the implementation, and describe it


## Jupyter tips
In the menue bar in the top you can go to `Help >> Keyboard Shortcuts` and see a list of shortcuts.
Here is a convenient shortlist:

| Shortcut        	| Action                                                                                  	|
|-----------------	|-----------------------------------------------------------------------------------------	|
| `CTRL + Enter`  	| Execute current cell                                                                    	|
| `Shift + Enger` 	| Execute current cell, and select to next                                                	|
| `Esc`           	| Leave **edit mode** and enter **command mode**                                          	|
| `a`             	| while in **command** mode: Create new cell above current                                    	|
| `b`             	| while in **command** mode: Create new cell below current                                    	|
| `dd`            	| while in **command** mode: Delete current cell                                              	|
| `ii`            	| while in **command** mode: Interrupt kernel (same as `CTRL + c` when using Python normally) 	|
| `Shift + Tab`   	| while in **edit** mode: Inspect element (useful for **debugging!**)                        	|
| `l`   	 	 	| while in **edit** mode: Display line numblers (useful for **debugging!**)         


## Credits
are listed in the the individual files.


