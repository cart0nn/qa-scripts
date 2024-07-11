# CS_Squared (powered by ĀYŌDÈ) QA Automation Scripts
This is a collection of Python scripts that can be used internally to expedite certain parts of the QA process. The intention of this project is to automate as much of the QA process as possible. This collection will be added to and updated as time goes on.

## Descriptions
### link_validator.py
This script uses Selenium and geckodriver to validate all links on a webpage. **You must download geckodriver and place it in the pkg directory for this script to function.**
#### Dependencies:
- Selenium
- geckodriver [(Download here)](https://github.com/mozilla/geckodriver/releases)
#### Issues:
- Currently relies on a webdriver that the user must download and place into a directory manually. Will later automate this.

### web_grammar_check.py
This script uses BeautifulSoup to parse the embedded HTML in .jsx/.tsx files and pull the text inside its divs. It then uses language_tool_python to grammar and spell check the content.
#### Dependencies:
- BeautifulSoup
- language_tool_python
- tkinter
#### Issues:
- Currently outputs lots of slop due to whitespace.
- Many false positives to sift through, however no false negatives.
- Currently probably less efficient than just checking manually.