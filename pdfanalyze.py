import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from io import BytesIO


def count_characters(pdf_path):
    total_characters = 0
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            total_characters += len(page.extract_text())
    return total_characters


def count_words(pdf_path):
    total_words = 0
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            total_words += len(page.extract_text().split())
    return total_words


def count_sentences(pdf_path):
    total_sentences = 0
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            total_sentences += len(page.extract_text().split('.'))
    return total_sentences


def extract_images(pdf_path):
    images = []
    pdf_reader = PyPDF2.PdfFileReader(pdf_path)
    for page_number in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_number)
        if '/XObject' in page['/Resources']:
            x_objects = page['/Resources']['/XObject'].getObject()
            for obj in x_objects:
                if x_objects[obj]['/Subtype'] == '/Image':
                    image = x_objects[obj]
                    if '/Filter' in image:
                        if image['/Filter'] == '/FlateDecode':
                            img_data = image._data
                            img = Image.open(BytesIO(img_data))
                            images.append(img)
    return images


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        action_selection_window(file_path)


def count_characters_action(file_path):
    character_count = count_characters(file_path)
    output_text.insert(tk.END, f"Total Characters: {character_count}\n")


def count_words_action(file_path):
    word_count = count_words(file_path)
    output_text.insert(tk.END, f"Total Words: {word_count}\n")


def count_sentences_action(file_path):
    sentence_count = count_sentences(file_path)
    output_text.insert(tk.END, f"Total Sentences: {sentence_count}\n")


def extract_images_action(file_path):
    images = extract_images(file_path)
    output_text.insert(tk.END, f"Total Images: {len(images)}\n")


root = tk.Tk()
root.title("SAR High Performance-PDF Analyzer")
root.geometry("500x400")


def action_selection_window(file_path):
    action_frame = tk.Frame(root)
    action_frame.pack(pady=10)

    lbl_select_action = tk.Label(action_frame, text="Select an action:")
    lbl_select_action.grid(row=0, column=0, padx=5, pady=5)

    btn_characters = tk.Button(action_frame, text="Count Characters",
                               command=lambda: count_characters_action(file_path))
    btn_characters.grid(row=1, column=0, padx=5, pady=5)

    btn_words = tk.Button(action_frame, text="Count Words", command=lambda: count_words_action(file_path))
    btn_words.grid(row=1, column=1, padx=5, pady=5)

    btn_sentences = tk.Button(action_frame, text="Count Sentences", command=lambda: count_sentences_action(file_path))
    btn_sentences.grid(row=2, column=0, padx=5, pady=5)

    btn_images = tk.Button(action_frame, text="Extract Images", command=lambda: extract_images_action(file_path))
    btn_images.grid(row=2, column=1, padx=5, pady=5)


lbl_select_file = tk.Label(root, text="Select a PDF file:")
lbl_select_file.pack(pady=10)

btn_select_file = tk.Button(root, text="Browse", command=select_file)
btn_select_file.pack(pady=5)

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

root.mainloop()
