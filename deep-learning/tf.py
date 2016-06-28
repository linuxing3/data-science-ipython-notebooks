# coding: utf-8
import tensorflow as tf
matrix1 = tf.constant([[3., 3.]])
matrix2 = tf.constant([[2.],[2.]])
product = tf.matmul(matrix1, matrix2)
sess = tf.Session()
result = sess.run(product)
print(result)
# Enter an interactive TensorFlow Session.
import tensorflow as tf
sess = tf.InteractiveSession()
x = tf.Variable([1.0, 2.0])
a = tf.constant([3.0, 3.0])
# Initialize 'x' using the run() method of its initializer op.
x.initializer.run()
# Add an op to subtract 'a' from 'x'.  Run it and print the result
sub = tf.sub(x, a)
print(sub.eval())
# ==> [-2. -1.]
# Close the Session when we're done.
sess.close()
