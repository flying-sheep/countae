import os

from .io import Dataset, write_text_matrix
from .train import train
from .network import AE_types


def autoencode(count_matrix,
               output_dir,
               kfold=None,
               dimreduce=True,
               reconstruct=True,
               mask=None,
               size_factors=False,
               type='normal',
               activation='relu',
               test_split=False,
               optimizer='Adam',
               learning_rate=None,
               hidden_size=(256,64,256),
               l2_coef=0.,
               hidden_dropout=0.0,
               epochs=200,
               batch_size=32,
               init='glorot_uniform',
               **kwargs):

    x = Dataset()
    x.import_from_text(count_matrix, test_split=test_split)

    net = AE_types[type](x['shape'][1],
              hidden_size=hidden_size,
              l2_coef=l2_coef,
              hidden_dropout=hidden_dropout,
              activation=activation,
              init=init,
              masking=(mask is not None))
    net.build()

    losses = train(x, net, output_dir=output_dir,
                   learning_rate=learning_rate,
                   epochs=epochs, batch_size=batch_size,
                   optimizer=optimizer, size_factors=size_factors,
                   **kwargs)

    res = net.predict(count_matrix, size_factors=size_factors,
                      dimreduce=dimreduce, reconstruct=reconstruct)

    res['losses'] = losses

    return net, res
