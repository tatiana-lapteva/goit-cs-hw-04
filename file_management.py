
from pathlib import Path


def divide_files(file_paths, num_chunks):
    """Break a list of files into chunks of requested size"""
    return [file_paths[i * num_chunks:(i + 1) * num_chunks] for i in range((len(file_paths) + num_chunks - 1) // num_chunks)]


def get_files(directory='files'):
    """Get .txt files from current project/files directory"""
    files_dir = Path(__file__).parent/directory
    return [f for f in files_dir.iterdir() if f.suffix =='.txt']


def search_in_file(file_path, keywords, results=None):
    """Search keywords in file, append results to dictionary"""
    if not results:
        results = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(str(file_path))
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return results



