import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# Carregar o conjunto de dados MNIST
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalizar as imagens para o intervalo de 0 a 1
train_images = train_images / 255.0
test_images = test_images / 255.0

# Converter os rótulos em categorias one-hot
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

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
model.fit(train_images, train_labels, epochs=5, batch_size=32)

# Avaliar o modelo
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
test_accuracy
