
## 🔃 Convert jupyter notebook to a report format

---

Find all notebooks and exchange the format to html

    find * -type f -name "*.ipynb"
    find * -type f -name "*.ipynb" -exec jupyter nbconvert --to html --output-dir docs/reports {} \;

Report format could be pdf/html/markdown and save under `docs/reports`

    jupyter nbconvert --to html --output-dir ../docs/reports "target_notebook_name.ipynb"

### **Solving the `application/vnd.plotly.v1+json` Rendering Issue**

#### **Problem Description**

When using `nbconvert` to convert a Jupyter Notebook to an HTML file, the following warning may appear:

   ```plaintext
   UserWarning: Your element with mimetype(s) dict_keys(['application/vnd.plotly.v1+json']) is not able to be represented.
   ```

This indicates that dynamic Plotly charts in the notebook are not being rendered correctly. The issue arises because the default Jupyter environment or template does not support rendering MIME type `application/vnd.plotly.v1+json`.

---

#### **Solution**

Install and enable the **Jupyter Notebook Renderers** extension, which supports rendering Plotly and other dynamic chart types.

- [Jupyter Notebook Renderers - VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter-renderers)