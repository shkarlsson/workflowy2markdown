# Workflowy2Markdown
A simple python script for converting Workflowy data to Markdown notes

## Outline to note conversion
The first level lists in workflowy is assumed to correspond to tags in Obsidian (written in that flavor of markdown as `#tagname`). 
The second level lists corresponds to the note title. 
Following levels are headings (1 or 2), plain text or lists depending on the max depth of the note. This can be customized by changing the LEVEL_TO_FORMAT_MAP variable.

## How to use it
1. Make sure you have python3 with pandas installed
2. Export your Workflowy data as plain text (by clicking the three dops in the top-right corner > Export all > Plain text > "click to download") to path/to/repo/import/
3. Run `python3 path/to/repo/wf2md.py`
4. Move the files created in path/to/repo/export/ to wherever you want them
