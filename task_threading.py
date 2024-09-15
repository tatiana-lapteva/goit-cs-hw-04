import threading
import time
from file_management import get_files, search_in_file, divide_files



def multi_threaded_search(file_paths, keywords, num_threads=4):
    """Multi-Threading function for processing files from queue"""
    file_chunks = divide_files(file_paths, num_threads)
    results = {keyword: [] for keyword in keywords}

    def worker(file_chunk, keywords, results):
        for file_path in file_chunk:
            search_in_file(file_path, keywords, results)

    threads = []

    # Create and start threads
    for file_chunk in file_chunks:
        thread = threading.Thread(target=worker, args=(file_chunk, keywords, results))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    return results


if __name__ == "__main__":

    keywords = ['star','fire', 'project', 'submarine', 'python', 'complain', 'San Antone']

    files = get_files()

    # Execute multithreading search
    if files:
        start_time = time.time()
        results = multi_threaded_search(files, keywords, num_threads=4)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")

        # Print results
        for keyword, files in results.items():
            if files:
                print(f"\nKeyword '{keyword}' found in:")
                for file in files:
                    print(f"  {file}")
            else:
                print(f"\nKeyword '{keyword}' not found")
    else:
        print("No text files found in the directory.")