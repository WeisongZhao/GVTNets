import tensorflow as tf

def get_loss(labels, inputs, outputs, opts, conf_unet):

	if conf_unet['dimension'] == '2D':
		convolution = convolution_2D
	elif conf_unet['dimension'] == '3D':
		convolution = convolution_3D

	if opts.loss_type == 'MSE':
		if opts.probalistic:
			preds = tf.add(inputs, outputs)
			sigma = convolution(outputs, 1, 1, 1, False, name = 'out_sigma_conv')
			sigma = tf.nn.softplus(sigma) + 1e-3
			loss = tf.reduce_mean(tf.truediv(tf.square(preds-labels), sigma) + tf.log(sigma))
		else:
			loss = tf.losses.mean_squared_error(labels, outputs)

	elif opts.loss_type == 'MAE':
		if opts.probalistic:
			preds = tf.add(inputs, outputs)
			sigma = convolution(outputs, 1, 1, 1, False, name = 'out_sigma_conv')
			sigma = tf.nn.softplus(sigma) + 1e-3
			loss = tf.reduce_mean(tf.truediv(tf.abs(preds-labels), sigma) + tf.log(sigma))
		else:
			loss = tf.losses.absolute_difference(labels, outputs)

	return loss