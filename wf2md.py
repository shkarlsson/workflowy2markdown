#%%
from pathlib import Path
import pandas as pd

root_dir = Path(__file__).parent
import_dir = root_dir / 'import'
try:
    import_path = list(import_dir.glob('*.txt'))[0]
except IndexError:
    raise FileNotFoundError(f'No txt file found in {import_dir}. You need to export your Workflowy notes to txt first. See the README for instructions.')
export_dir = root_dir / 'export'

#%% Conversing nested list in txt to nested json

with open(import_path, 'r') as f:
    lines = f.readlines()

note_dfs = []

for i, line in enumerate(lines):
    # Get hierarchy level by counting how many double-spaces the line starts with
    level = int((len(line) - len(line.lstrip(' '))) / 2)
    
    text = line.strip()[2:]
    
    if level == 0:
        
        tag = text
        continue
    if level == 1:
        if i > 1:
            # Here, data for a complete note has been collected and we can create a dataframe for it.
            note_df = pd.DataFrame(note_rows, columns=['Tag', 'Title', 'Level', 'Text'])
            note_dfs.append(note_df)
        
        # Initializing or resetting the note
        note_rows = []
        title = text
        continue
    
    h1 = text
    note_rows.append([tag, title, level-1, text])


#%% 

# This decides which format should be used for each level of note, based on the max level of the note.
LEVEL_TO_FORMAT_MAP = {
    # In notes with only one level, that level should be plain text
    1: {
        1: '',
    },
    # In notes with two levels, the first level should be a header and the second level should be plain text
    2: {
        1: '# ',
        2: '',
    },
    # In notes with three levels, the first level should be a header, the second level should be a subheader, and the third level should be plain text
    3: {
        1: '# ',
        2: '## ',
        3: '',
    },
    # In notes with four levels, level 1-3 should be as above, and level 4 should be bullet points
    4: {
        1: '# ',
        2: '## ',
        3: '',
        4: '* ',
    },
    # In notes with five levels, level 1-4 should be as above, and level 5 should be level 2 bullet points
    5: {
        1: '# ',
        2: '## ',
        3: '',
        4: '* ',
        5: '\t* ',
    },
    # In notes with six levels, level 1-3 should be headers, level 4 text and level 5-6 bullet points
    6: {
        1: '# ',
        2: '## ',
        3: '### ',
        4: '',
        5: '* ',
        6: '\t* ',
    },
}


df = (
    pd.concat(note_dfs, ignore_index=True)
    
    # Drop empty rows
    .loc[lambda x: x.Text.str.len() > 0]

    # Assign max level of each Title
    .assign(MaxLevel=lambda x: x.groupby('Title').Level.transform('max'))
    
    # TODO: Figure out workflowy "mirrors" by identically named rows in different places in the tree and apply Obsidian's linkage between them instead.
    
    # Assign the prefix for each row
    .assign(Prefix=lambda x: x.apply(lambda row: LEVEL_TO_FORMAT_MAP[row.MaxLevel][row.Level], axis=1))
    
    # Finalize the output text
    .assign(Output=lambda x: x.Prefix + x.Text)

    # Replace "/" with "-" in titles because filenames cannot contain "/"
    .assign(Title=lambda x: x.Title.str.replace('/', '-'))
)
   
#%% Export to markdown files

for title, note_df in df.groupby('Title'):
    with open(export_dir / f'{title}.md', 'w') as f:
        # Adding imported from workflowy tag
        f.write('#WorkflowyImport ')

        # Write the tag as a hashtag
        f.write(f'#{note_df.Tag.iloc[0]}\n')

        # Write the note
        f.write(note_df.Output.str.cat(sep='\n'))

print(f'Exported {len(df.Title.unique())} notes to {export_dir}')

#%%