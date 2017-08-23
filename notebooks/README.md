# Notebooks

There are three types of notebooks:
* **DEMO**s show how to do something with modest documentation and explanation. They are intended to introduce topics and serve as refrence material.
* **TUT**orials covers a topic thoroughly, and explains how things work, and why things are done the way they are.
* **EXE**ercises are your turn to shine. The notebook guides you through how to implement and solve some prolem.



## External resources
* TensorFlow has some very good tutorials from [introductory](https://www.tensorflow.org/get_started/) to [advanced](https://www.tensorflow.org/programmers_guide/) levels.


## Debugging tips
 * **InternalError: Blas GEMM launch failed**: Your GPU ran out of memory. This is most likely because you have multiple instances of TensorFlow running. Go to the `Running` tab in Jupyter, and shutdown all unused notebooks.
