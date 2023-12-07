import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# Carregar os dados
(x_train, y_train), (x_test, y_test) = mnist.load_data()


# Normalizar as imagens para o intervalo de 0 a 1
x_train = x_train / 255.0
x_test = x_test / 255.0

# Converter os rótulos em categorias one-hot
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Construir o modelo da rede neural
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# Compilar o modelo
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Treinar o modelo
model.fit(x_train, y_train, epochs=5, batch_size=32)

# Avaliar o modelo
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Perda: {loss}, Precisão: {accuracy}")
