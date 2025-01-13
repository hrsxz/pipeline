"""
This module contains utility functions for the project like converting markdown to html
and pdf and other miscellaneous functions.
"""

import os
from datetime import datetime
from pathlib import Path

import markdown  # type: ignore

# from weasyprint import HTML
from nbconvert import HTMLExporter
from nbformat import read
from nbformat.notebooknode import NotebookNode

# import nbformat


def markdown_to_html(
    markdown_file_path: str, target_file_folder: str, additional_pdf_file: bool = False
):
    """This function converts a markdown file to a pdf file

    Args:
        markdown_file_path (str): full path to the markdown file
        target_file_folder (str): folder name where the pdf file will be saved
    """
    with open(markdown_file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Convert the markdown text to html
    html_text = markdown.markdown(text)
    # Use the os.path.basename function to get the filename from the full path
    filename = os.path.basename(markdown_file_path)
    # Replace the .md extension with .html
    pdf_filename = filename.replace(".md", ".html")
    target_file_path = os.path.join(target_file_folder, pdf_filename)
    # 'wb' mode is used to write binary data to the file
    # 'w' mode is used to write text data to the file
    # Save the html text to a file
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    # Write additional pdf file
    if additional_pdf_file:
        # Convert the html text to pdf
        # HTML(string=html_text).write_pdf(target_file_path)
        pass
    retrun


def find_all_markdown_files(folder_path: str) -> list[str]:
    """Find all .md files within a specified folder path.

    Args:
        folder_path (str): The path to the folder where .md files are stored.

    Returns:
        list: A list of paths to the .md files.
    """
    md_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files


def convert_all_markdown_to_html(
    markdown_folder_path: str,
    target_file_folder: str,
    additional_pdf_file: bool = False,
):
    """This function converts all markdown files under a folder to a html pages.

    Args:
        folder_path (str): folder path where the markdown files are stored
        target_file_folder (str): folder name where the pdf file will be saved
    """
    all_markdown_files = find_all_markdown_files(markdown_folder_path)
    for md_file in all_markdown_files:
        markdown_to_html(md_file, target_file_folder, additional_pdf_file)


def get_markdown_converter(source_path, target_folder, additional_pdf=False):
    """This function use the factory pattern to create the appropriate Notebook
    converter

    Args:
        source_path (_type_): _description_
        target_folder (_type_): _description_
        additional_pdf (bool, optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if os.path.isdir(source_path):
        return FolderNotebookConverter(source_path, target_folder, additional_pdf)
    if os.path.isfile(source_path):
        return FileNotebookConverter(source_path, target_folder, additional_pdf)
    raise ValueError("Source path must be a file or a directory")


# The following code provides a flexible and object-oriented approach to converting
# Jupyter notebook files to HTML.
# It employs polymorphism and encapsulation principles to handle both individual files
# and directories containing multiple files.
# The module defines a base class, `NotebookConverter`, with specialized subclasses
# `FileNotebookConverter` and `FolderNotebookConverter`
# that override the base method for specific use cases. A factory function,
# `get_notebook_converter`, is used to instantiate the appropriate converter
# based on the input's nature, enhancing code modularity and ease of maintenance.
# This structure allows for easy extension, such as adding new types of inputs.


def find_all_ipynb_files(folder_path: str) -> list[str]:
    """Find all .ipynb files within a specified folder path.

    Args:
        folder_path (str): The path to the folder where .ipynb files are stored.

    Returns:
        list: A list of paths to the .ipynb files.
    """
    ipynb_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".ipynb"):
                ipynb_files.append(os.path.join(root, file))
    return ipynb_files


def notebook_to_html(notebook_file: str, target_folder: str) -> None:
    """This function converts a jupyter notebook file to html and pdf files.

    Args:
        notebook_file (str): The path to the jupyter notebook file.
        target_folder (str): The folder where the html and pdf files will be saved.
        Defaults to False.
    """
    # Read the notebook file
    notebook_path = Path(notebook_file)
    notebook: NotebookNode = read(notebook_path, as_version=4)  # type: ignore

    # Create an HTML exporter
    html_exporter: HTMLExporter = HTMLExporter()  # type: ignore
    html_exporter.template_name = "lab"
    # Ensure JavaScript is executed
    html_exporter.exclude_input = False
    html_exporter.exclude_output_prompt = True

    # Ensure Plotly figures and images are embedded
    # html_exporter.template_data = {
    #     "embed_images": True,
    #     "plotly_renderer": "notebook_connected",
    # }

    # export the notebook to HTML
    (body, _) = html_exporter.from_notebook_node(notebook)
    output_file_path = target_folder + f"/{notebook_path.stem}.html"

    # Write the HTML output to a file
    output_path = Path(output_file_path)
    output_path.write_text(body, encoding="utf-8")
    print(f"HTML with embedded Plotly figures saved to {output_path}")


class NotebookConverter:
    """This class is a base class for converting jupyter notebook files to html and/or
    pdf files.
    """

    def __init__(
        self, source_path: str, target_folder: str, additional_pdf: bool = False
    ):
        self.source_path = source_path
        self.target_folder = target_folder
        self.additional_pdf = additional_pdf

    def convert(self):
        """This method converts the jupyter notebook file to html and pdf file."""
        raise NotImplementedError("This method should be overridden by subclasses.")


class FileNotebookConverter(NotebookConverter):
    """This class converts a single Notebook file to html and pdf files.

    Args:
        NotebookConverter (_type_): _description_
    """

    def convert(self) -> None:
        print(f"Converting Notebook file: {self.source_path}")
        notebook_to_html(self.source_path, self.target_folder)


class FolderNotebookConverter(NotebookConverter):
    """This class converts all Notebook files in a folder to html and pdf files."""

    def convert(self) -> None:
        """This method converts all Notebook files in the folder to html and pdf
        files.
        """
        all_notebook_files = find_all_ipynb_files(self.source_path)
        for notebook_file in all_notebook_files:
            print(f"Converting Notebook file: {notebook_file}")
            notebook_to_html(notebook_file, self.target_folder)
        print("last save time:", datetime.now())


def get_notebook_converter(
    source_path, target_folder="./docs/html", additional_pdf=False
):
    """This function use the factory pattern to create the appropriate Notebook
    converter

    Args:
        source_path (str): _description_
        target_folder (str): _description_
        additional_pdf (bool, optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    print("last save time:", datetime.now())
    if os.path.isdir(source_path):
        return FolderNotebookConverter(source_path, target_folder, additional_pdf)
    if os.path.isfile(source_path):
        return FileNotebookConverter(source_path, target_folder, additional_pdf)
    raise ValueError("Source path must be a file or a directory")


# This part used for code2flow in order to generate the call graph of the source code.
# ------------------------------------------------------------------------------------
# PS D:\Digitalization\AnomalyDetectionTimeSeries\MultivariateTimeSeries> code2flow
# src/utils/utils.py --output docs/code2flow/pics_code2flow.png
# ------------------------------------------------------------------------------------
#  import constants
#  if __name__ == "__main__":
#      # path_to_markdown = (constants.project_root_path /
#      #                     "notebook/time-series-gan-with-pytorch.ipynb")
#      print(constants.project_root_path)
#      path_to_markdown = constants.project_root_path / "notebook"
#      target_folder = constants.project_root_path / "docs/html"
#      converter = get_notebook_converter(
#          path_to_markdown,
#          target_folder,
#          additional_pdf=True
#      )
#      converter.convert()
