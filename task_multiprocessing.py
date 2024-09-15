from multiprocessing import Process, Queue
import time
from file_management import get_files, search_in_file, divide_files


def worker(file_paths, keywords, result_queue):
    partial_results = {keyword: [] for keyword in keywords}
    for file_path in file_paths:
        file_results = search_in_file(file_path, keywords)
        for keyword, files in file_results.items():
            partial_results[keyword].extend(files)
    result_queue.put(partial_results)


def multi_process_search(file_paths, keywords, num_processes=4):
    """Multiprocessing search of keywords in files using Pool"""
    file_chunks = divide_files(file_paths, num_processes)
    result_queue = Queue()
    processes = []
    
    # Start processes
    for file_chunk in file_chunks:
        process = Process(target=worker, args=(file_chunk, keywords, result_queue))
        processes.append(process)
        process.start()
    
    # Get results:
    results = {keyword: [] for keyword in keywords}
    for _ in processes:
        for keyword, files in result_queue.get().items():
            results[keyword].extend(files)

    # Waiting for processes execution:
    for process in processes:
        process.join()
    
    return results


if __name__ == '__main__':

    keywords = ['star','fire', 'project', 'submarine', 'python', 'complain', 'San Antone']
    files = get_files()

    # Execute multiprocessing search
    if files:
        start_time = time.time()
        results = multi_process_search(files, keywords, num_processes=4)
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