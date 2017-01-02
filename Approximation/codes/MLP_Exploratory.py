from numpy import mat, loadtxt, zeros, exp, multiply, sum, square, sqrt, hstack, linspace, vstack
from numpy.random import uniform
import matplotlib.pyplot as plt
import sys

# Program for MLP
# Update weights for an epoch

data = mat(loadtxt('bj.tra'))
n_train = data.shape[0]

# Initialize the algorithm parameters
inp = 2
# hid = 6
out = 1
lam = 1e-2
n_epoch = 1001

x = data[:, 0:inp].T                # Input parameters
t = data[:, inp:inp+out].T          # Targets



# W_xz = DW_xz =    inp x hid
# W_zy = DW_zy =    hid x out
# x =               inp x n_train
# Z_in = Z_out =    hid x n_train
# Y_in = Y_out =    out x n_train

# Network : X -> Z -> Y
line_handles = []
line_labels = []
# Train the network
for hidden_neuron in range(inp+1,inp+11):
    error = []
    # Initialize weights
    W_xz = mat(uniform(low=-1, high=1, size=(inp, hidden_neuron)))
    W_zy = mat(uniform(low=-1, high=1, size=(hidden_neuron, out)))
    for epoch in range(1,n_epoch):
        # Prepare inputs for each neuron in hidden layer (Z)
        Z_in = W_xz.T * x
        # Pass through activation function (binary sigmoid) and prepare output of hidden layer
        Z_out = 1.0 / (1 + exp(-Z_in))

        # Prepare input for each neuron in output layer (Y)
        Y_in = W_zy.T * Z_out
        # Pass through activation function (identity) and prepare output of output layer
        Y_out = Y_in

        # Calculate delta for ZY weight matrix
        DW_zy = lam * Z_out * (t - Y_out).T

        # Calculate delta for XZ weight matrix
        DW_xz = lam * x * multiply(multiply(W_zy * (t - Y_out), Z_out), 1-Z_out).T
        
        # Sum of squared errors in output
        sumerr = sum(square(t - Y_out))

        # Update weight matrices XZ and ZY
        W_xz = W_xz + DW_xz
        W_zy = W_zy + DW_zy

        # print sqrt(sumerr/n_train)
        if epoch%200==0:
            error.append(sqrt(sumerr/n_train))
            print(str(hidden_neuron) + ' ' + str(epoch) + ' ' + str(sqrt(sumerr/n_train)))

    # sys.stdout.write("\r" + str(hidden_neuron) + " " + str(epoch))
    # sys.stdout.flush()
    # print str(hidden_neuron) + ' ' + str(number_epoch)
    # print()
    # print(len(error))
    # print(len(xrange(1000,15001,1000)))
    handle, = plt.plot(xrange(200,n_epoch,200),error)
    line_handles.append(handle)
    line_labels.append('Hidden neurons = ' + str(hidden_neuron))
plt.legend(line_handles, line_labels)
plt.xlabel('Number of epochs')
plt.ylabel('Error')
plt.grid(True)
plt.show()

# Validate the network
rms_training = mat(zeros((out, 1)))
res_training = mat(zeros((n_train, 2)))
Z_out = 1.0 / ( 1 + exp(-W_xz.T * x))
Y_out = W_zy.T * Z_out
rms_training = rms_training + sum(square(t-Y_out), axis=1)
res_training = hstack([t.T, Y_out.T])
# print sqrt(rms_training/n_train)

# Test the network
test = mat(loadtxt('bj.tes'))
n_test = test.shape[0]
test_x = data[:, 0:inp].T
test_t = data[:, inp:inp+out].T
Z_out = 1.0 / ( 1 + exp(-W_xz.T * test_x))
Y_out = W_zy.T * Z_out
rms_testing = sum(square(test_t-Y_out), axis=1)
res_testing = hstack([test_t.T, Y_out.T])
# print sqrt(rms_training/n_test)