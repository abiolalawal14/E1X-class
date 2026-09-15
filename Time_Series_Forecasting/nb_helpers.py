"""Small helper for building .ipynb files with nbformat."""
import nbformat as nbf


def new_notebook():
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    }
    return nb


def md(text):
    return nbf.v4.new_markdown_cell(text)


def code(text):
    return nbf.v4.new_code_cell(text.strip("\n"))


def save(nb, path):
    nbf.write(nb, path)
    print("wrote", path)
