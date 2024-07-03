from tkinter import *
from tkinter import messagebox
import backend


def train():
    sentence = train_entry.get()
    ac = backend.AutoComplete()
    ac.train(sentence)

def predict_word():
    word = predict_word_entry.get()
    ac = backend.AutoComplete()
    print(ac.predict(word))

if __name__ == "__main__":
    root = Tk()
    root.title("输入笔记")
    root.geometry('300x300')

    train_label = Label(root, text="训练")
    train_label.pack()
    train_entry = Entry(root)
    train_entry.pack()

    train_button = Button(root, text="训练", command=train)
    train_button.pack()

    predict_word_label = Label(root, text="输入要预测的词")
    predict_word_label.pack()
    predict_word_entry = Entry(root)
    predict_word_entry.pack()

    predict_button = Button(root, text="预测", command=predict_word)
    predict_button.pack()

    root.mainloop()