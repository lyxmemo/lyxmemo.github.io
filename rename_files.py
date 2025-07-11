import os
import re
import frontmatter
import logging

logging.basicConfig(filename='rename.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clean_title(title):
    title = re.sub(r'\[待录入\]', '', title)
    title = re.sub(r'\[已认领待录入\]', '', title)
    # Replace characters that are invalid in filenames
    title = title.replace('/', '-')
    return title.strip()

def rename_files():
    base_dir = 'docs'
    for dirpath, _, filenames in os.walk(base_dir):
        if '_battles_history' in dirpath or \
           '_liaos_tele' in dirpath or \
           '_liaos_writings' in dirpath or \
           '_n6a_memorial' in dirpath or \
           '_n22d_memorial' in dirpath or \
           '_ten_year_memorial' in dirpath:
            for filename in filenames:
                if filename.endswith('.md'):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            post = frontmatter.load(f)
                            if 'title' in post.metadata:
                                title = post.metadata['title']
                                new_title = clean_title(title)
                                if new_title:
                                    new_filename = f"{new_title}.md"
                                    new_filepath = os.path.join(dirpath, new_filename)
                                    
                                    if filepath != new_filepath:
                                        # Create subdirectory if it doesn't exist
                                        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
                                        logging.info(f"Renaming '{filepath}' to '{new_filepath}'")
                                        os.rename(filepath, new_filepath)
                    except Exception as e:
                        logging.error(f"Error processing file {filepath}: {e}")

if __name__ == '__main__':
    rename_files()
