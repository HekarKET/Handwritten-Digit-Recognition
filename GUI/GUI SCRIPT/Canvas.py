import tkinter
import win32gui
from PIL import ImageGrab, Image
import numpy as np
from keras.models import load_model


root = tkinter.Tk()
root.geometry("800x400")


def callback(event):
    #print("clicked at", str(event.x), str(event.y))
    x = event.x
    y = event.y
    r = 12
    canvas.create_oval(x-r, y-r, x + r, y + r, fill='white')


def saveImage():
    HWND = canvas.winfo_id()
    rect = win32gui.GetWindowRect(HWND)
    img = ImageGrab.grab(rect)
    img.save(r'C:\Users\Akhilesh\Desktop\Programs\Projects\Digit Recognition\GUI\Store Images\output.jpg')


def clear():
    canvas.delete("all")


def _predict(img):
    model = load_model(
        r'C:\Users\Akhilesh\Desktop\Programs\Projects\Digit Recognition\Model\Model\DigitRecognizer.h5')
    img = img.resize((28, 28))
    img = img.convert('L')

    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img/255

    pred = model.predict([img])[0]
    result = np.argmax(pred)
    probability = max(pred)

    return result, probability


def Predict():
    label.configure(text='Predicting..')
    HWND = canvas.winfo_id()
    rect = win32gui.GetWindowRect(HWND)
    img = ImageGrab.grab(rect)
    result, probability = _predict(img)
    label.configure(text=str(result)+', ' + str(int(probability*100))+'%')


canvas = tkinter.Canvas(root, width=300, height=300, bg='black')
canvas.bind("<B1-Motion>", callback)
canvas.grid(row=0, column=0)

label = tkinter.Label(root, text="Draw any number", font=("Helvetica", 38))
label.grid(row=0, column=1)

clearButton = tkinter.Button(root, text="Clear", command=clear)
clearButton.grid(row=1, column=0)

predictButton = tkinter.Button(root, text="Predict", command=Predict)
predictButton.grid(row=1, column=1)


saveButton = tkinter.Button(root, text="Save image", command=saveImage)
saveButton.grid(row=1, column=2)

root.mainloop()
