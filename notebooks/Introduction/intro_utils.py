import numpy as np
from sklearn.metrics import precision_score, accuracy_score
import matplotlib.pyplot as plt
import tensorflow as tf

def onehot(t, num_classes):
    out = np.zeros((t.shape[0], num_classes))
    for row, col in enumerate(t):
        out[row, col] = 1
    return out

def mesh_grid(X, step_size=0.08):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    return np.meshgrid(np.arange(x_min, x_max, step_size),
                         np.arange(y_min, y_max, step_size))
    
def prediction_contours(xx, yy, predict):
    Z = predict(np.c_[xx.ravel(), yy.ravel()])
    return Z.reshape(xx.shape)

def predict_with_model(model, x, get_probs=False):
    hidden_weights, hidden_bias, output_weights, output_bias = model['HW'], model['HB'], model['OW'], model['OB']
    
    # Forward propagation
    hidden_values = x.dot(hidden_weights) + hidden_bias
    hidden_activations = np.tanh(hidden_values)
    output_values = hidden_activations.dot(output_weights) + output_bias
    
    probs = softmax(output_values)
    if get_probs:
        return probs
    
    return np.argmax(probs, axis=1)

def prediction_contours_with_model(model, xx, yy):
    Z = predict_with_model(model, np.c_[xx.ravel(), yy.ravel()])
    return Z.reshape(xx.shape)

def extract_data(data):
    X, Y = zip(*data)
    X, Y = np.array(X), np.array(Y)
    return X, Y

def softmax(values):
    exp_scores = np.exp(values)
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

def predict(model, x, get_probs=False):
    hidden_weights, hidden_bias, output_weights, output_bias = model['HW'], model['HB'], model['OW'], model['OB']
    
    # Forward propagation
    hidden_values = x.dot(hidden_weights) + hidden_bias
    hidden_activations = np.tanh(hidden_values)
    output_values = hidden_activations.dot(output_weights) + output_bias
    
    probs = softmax(output_values)
    if get_probs:
        return probs
    
    return np.argmax(probs, axis=1)

def plot(model, ax, X, Y, title, xx=None, yy=None):
    ax.cla()
    preds = predict_with_model(model, X)
    precision = precision_score(Y, preds)
    accuracy = accuracy_score(Y, preds)
    ax.set_title("{0} Precision: {1:0.2f}, {0} Accuracy: {2:0.2f}".format(title, precision, accuracy))
    ax.scatter(X[:, 0], X[:, 1], s=60, c=Y, cmap=plt.cm.coolwarm)
    if xx is not None and yy is not None:
        ax.contourf(xx, yy, prediction_contours_with_model(model, xx, yy), cmap=plt.cm.coolwarm, alpha=0.3)
    return ax

def plot_error(ax, train_error, test_error):
    ax.cla()
    ax.plot(train_error, label='Train Error')
    ax.plot(test_error,  label='Test Error')
    ax.set_title("Train Loss: {0:0.2f}, Test Loss {1:0.2f}".format(np.array(train_error[-10:]).mean(), 
                                                                   np.array(test_error[-10:]).mean()))
    ax.legend()
    return ax

def ffn_layer(name, inputs, output_dimensions):
    # defining our initializer for our weigths from a normal distribution (mean=0, std=0.1)
    weight_initializer = tf.truncated_normal_initializer(stddev=0.1)
    
    input_dimensions = inputs.shape[1]
    
    # Encapsulate the operations in a Tensorflow Scope. Not important 
    # but a nice feature as you will see later
    with tf.variable_scope(name):
        # Define the weights of this particular layer and randomly initialize their weights
        weights = tf.get_variable('{}-weights'.format(name), 
                                  [input_dimensions, output_dimensions],
                                  initializer = weight_initializer)
        
        # Define the biases of this layer and initialize their weights to zero
        biases = tf.get_variable('{}-biases'.format(name), 
                                 [output_dimensions],
                                 initializer = tf.constant_initializer(0.0))
        
        # Do a matrix multiplication on the inputs and the weights and add the biases to the result
        return tf.matmul(inputs, weights) + biases