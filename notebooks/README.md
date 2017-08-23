# Notebooks


## External resources
* TensorFlow has some very good tutorials from [introductory](https://www.tensorflow.org/get_started/) to [advanced](https://www.tensorflow.org/programmers_guide/) levels.


## Debugging tips
 * **InternalError: Blas GEMM launch failed**: Your GPU ran out of memory. This is most likely because you have multiple instances of TensorFlow running. Go to the `Running` tab in Jupyter, and shutdown all unused notebooks.
