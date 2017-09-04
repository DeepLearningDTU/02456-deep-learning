## Python 2/3 compatability
from __future__ import absolute_import, division, print_function
import tensorflow as tf
import numpy as np
from IPython.display import clear_output, Image, display, HTML
import matplotlib
import matplotlib.pyplot as plt

def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def.
    Created by Alex Mordvintsev
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb
    """

    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add()
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = "<stripped %d bytes>"%size
    return strip_def


def rename_nodes(graph_def, rename_func):
    """
    Created by Alex Mordvintsev
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb
    """

    res_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = res_def.node.add()
        n.MergeFrom(n0)
        n.name = rename_func(n.name)
        for i, s in enumerate(n.input):
            n.input[i] = rename_func(s) if s[0]!='^' else '^'+rename_func(s[1:])
    return res_def


def show_graph(graph_def, max_const_size=32):
    """Visualize TensorFlow graph.
    Created by Alex Mordvintsev
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb
    """


    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    code = """
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
          }}
        </script>
        <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
        <div style="height:600px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format(data=repr(str(strip_def)), id='graph'+str(np.random.rand()))

    iframe = """
        <iframe seamless style="width:800px;height:620px;border:0" srcdoc="{}"></iframe>
    """.format(code.replace('"', '&quot;'))
    display(HTML(iframe))


def plot_decision_boundary(pred_func, X, y):
    #from https://github.com/dennybritz/nn-from-scratch/blob/master/nn-from-scratch.ipynb
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    yy = yy.astype('float32')
    xx = xx.astype('float32')
    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])[:,0]
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    # plt.figure()
    plt.contourf(xx, yy, Z, cmap=plt.cm.RdBu)
    plt.scatter(X[:, 0], X[:, 1], s=40, c=-y, cmap=plt.cm.Spectral)
    
def onehot(t, num_classes):
    out = np.zeros((t.shape[0], num_classes))
    for row, col in enumerate(t):
        out[row, col] = 1
    return out

class ConfusionMatrix:
    """
       Simple confusion matrix class
       row is the true class, column is the predicted class
    """
    def __init__(self, num_classes, class_names=None):
        self.n_classes = num_classes
        if class_names is None:
            self.class_names = map(str, range(num_classes))
        else:
            self.class_names = class_names

        # find max class_name and pad
        max_len = max(map(len, self.class_names))
        self.max_len = max_len
        for idx, name in enumerate(self.class_names):
            if len(self.class_names) < max_len:
                self.class_names[idx] = name + " "*(max_len-len(name))

        self.mat = np.zeros((num_classes,num_classes),dtype='int')

    def __str__(self):
        # calucate row and column sums
        col_sum = np.sum(self.mat, axis=1)
        row_sum = np.sum(self.mat, axis=0)

        s = []

        mat_str = self.mat.__str__()
        mat_str = mat_str.replace('[','').replace(']','').split('\n')

        for idx, row in enumerate(mat_str):
            if idx == 0:
                pad = " "
            else:
                pad = ""
            class_name = self.class_names[idx]
            class_name = " " + class_name + " |"
            row_str = class_name + pad + row
            row_str += " |" + str(col_sum[idx])
            s.append(row_str)

        row_sum = [(self.max_len+4)*" "+" ".join(map(str, row_sum))]
        hline = [(1+self.max_len)*" "+"-"*len(row_sum[0])]

        s = hline + s + hline + row_sum

        # add linebreaks
        s_out = [line+'\n' for line in s]
        return "".join(s_out)

    def batch_add(self, targets, preds):
        assert targets.shape == preds.shape
        assert len(targets) == len(preds)
        assert max(targets) < self.n_classes
        assert max(preds) < self.n_classes
        targets = targets.flatten()
        preds = preds.flatten()
        for i in range(len(targets)):
                self.mat[targets[i], preds[i]] += 1

    def get_errors(self):
        tp = np.asarray(np.diag(self.mat).flatten(),dtype='float')
        fn = np.asarray(np.sum(self.mat, axis=1).flatten(),dtype='float') - tp
        fp = np.asarray(np.sum(self.mat, axis=0).flatten(),dtype='float') - tp
        tn = np.asarray(np.sum(self.mat)*np.ones(self.n_classes).flatten(),
                        dtype='float') - tp - fn - fp
        return tp, fn, fp, tn

    def accuracy(self):
        """
        Calculates global accuracy
        :return: accuracy
        :example: >>> conf = ConfusionMatrix(3)
                  >>> conf.batchAdd([0,0,1],[0,0,2])
                  >>> print conf.accuracy()
        """
        tp, _, _, _ = self.get_errors()
        n_samples = np.sum(self.mat)
        return np.sum(tp) / n_samples

    def sensitivity(self):
        tp, tn, fp, fn = self.get_errors()
        res = tp / (tp + fn)
        res = res[~np.isnan(res)]
        return res

    def specificity(self):
        tp, tn, fp, fn = self.get_errors()
        res = tn / (tn + fp)
        res = res[~np.isnan(res)]
        return res

    def positive_predictive_value(self):
        tp, tn, fp, fn = self.get_errors()
        res = tp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def negative_predictive_value(self):
        tp, tn, fp, fn = self.get_errors()
        res = tn / (tn + fn)
        res = res[~np.isnan(res)]
        return res

    def false_positive_rate(self):
        tp, tn, fp, fn = self.get_errors()
        res = fp / (fp + tn)
        res = res[~np.isnan(res)]
        return res

    def false_discovery_rate(self):
        tp, tn, fp, fn = self.get_errors()
        res = fp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def F1(self):
        tp, tn, fp, fn = self.get_errors()
        res = (2*tp) / (2*tp + fp + fn)
        res = res[~np.isnan(res)]
        return res

    def matthews_correlation(self):
        tp, tn, fp, fn = self.get_errors()
        numerator = tp*tn - fp*fn
        denominator = np.sqrt((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn))
        res = numerator / denominator
        res = res[~np.isnan(res)]
        return res


def mnist_summary(mnist_data):
    print("""Information on dataset
    ----------------------""")
    print("Training size:\t", mnist_data.train.num_examples)
    print("Test size\t", mnist_data.test.num_examples)
    print("Validation size\t", mnist_data.validation.num_examples)

    print('\nData summaries')
    print("Image shape\t\t", mnist_data.train.images[0].shape)
    print("Image type\t\t", type(mnist_data.train.images[0][0]))
    print("Image min/max value\t", np.min(mnist_data.train.images), '/', np.max(mnist_data.train.images))
    print("Label shape\t\t", mnist_data.train.labels[0].shape
)
    print("Label type\t\t", type(mnist_data.train.labels[0][0]))


    ## Plot a few MNIST examples
    img_to_show = 15
    idx = 0
    canvas = np.zeros((28*img_to_show, img_to_show*28))
    for i in range(img_to_show):
        for j in range(img_to_show):
            canvas[i*28:(i+1)*28, j*28:(j+1)*28] = mnist_data.train.images[idx].reshape((28, 28))
            idx += 1
    plt.figure(figsize=(4,4))
    plt.axis('off')
    plt.imshow(canvas, cmap='gray')
    plt.title('MNIST handwritten digits')
    plt.show()


def num_params():
    total_parameters = 0
    for variable in tf.trainable_variables():
        # shape is an array of tf.Dimension
        shape = variable.get_shape()
#         print(shape)
#         print(len(shape))
        variable_parameters = 1
        for dim in shape:
#             print(dim)
            variable_parameters *= dim.value
#         print(variable_parameters)
        total_parameters += variable_parameters
#     print(total_parameters)
    return total_parameters

