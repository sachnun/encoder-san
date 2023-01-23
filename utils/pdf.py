import os, io
import WebSite2PDF

# from pyhtml2pdf import converter


# class PDF(object):
#     def __init__(self, timeout=10):
#         self.timeout = timeout

#     def convert(self, url: str, output: str = None):
#         if output is None:
#             # random file name
#             output = os.urandom(24).hex() + ".pdf"

#         # convert to PDF, and save to output, and return the output buffer after that delete the file
#         converter.convert(url, output, timeout=self.timeout)

#         with open(output, "rb") as f:
#             file = io.BytesIO(f.read())

#         os.remove(output)
#         return file


class WebPDF:
    def __init__(self):
        pass

    def convert(self, url: str, output: str = None):
        if output is None:
            # random file name
            output = os.urandom(24).hex() + ".pdf"

        c = WebSite2PDF.Client()
        c.pdf(
            url,
            output,
            seleniumOptions={
                "--no-sandbox",
                "--headless",
                "--disable-gpu",
            },
        )

        with open(output, "rb") as f:
            file = io.BytesIO(f.read())

        os.remove(output)
        return file


if __name__ == "__main__":
    pdf = WebPDF()
    file = pdf.convert("https://google.com")
    with open("test.pdf", "wb") as f:
        f.write(file.read())
