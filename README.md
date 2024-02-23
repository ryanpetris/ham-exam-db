# Ham Exam DB

This program takes Amateur Radio License question pool documents downloaded from https://ncvec.org/ and converts them into sqlite databases. These databases are intended to be used as a building block for other applications to use question data for their own purposes.

## Requirements

The only library this application uses outside of the standard python library is [python-docx](https://github.com/python-openxml/python-docx). If not available locally, this will automatically be downloaded and installed into a python virtual environment when running `build.sh`.

## Building

First, if the question pool you're wanting to use isn't included in the source directory, then download it from https://ncvec.org/ (the docx version) and add it to that directory. Consider submitting a pull request if a question pool is indeed missing.

Next, run `./build.sh` from the root of this repository. If all goes well, a `dist` folder should appear with the resulting databases.
