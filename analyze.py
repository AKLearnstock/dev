import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Function to format sizes
def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return size

# Analyze folder and subfolders
def analyze_folder(root_dir):
    file_types = defaultdict(int)
    file_sizes = defaultdict(int)
    all_files = []
    subfolders_sizes = defaultdict(int)
    duplicate_names = defaultdict(list)
    duplicate_sizes = defaultdict(list)
    folder_count = 0

    for root, dirs, files in os.walk(root_dir):
        folder_size = 0
        folder_count += len(dirs)  # Count subfolders

        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file)[1].lower()

            # File Types and Size
            file_types[file_ext] += 1
            file_sizes[file_ext] += file_size

            # Largest to Smallest
            all_files.append((file_path, file_size))

            # Redundant Names
            duplicate_names[file].append(file_path)

            # Redundant Sizes
            duplicate_sizes[file_size].append(file_path)

            # Folder Size
            folder_size += file_size

        subfolders_sizes[root] = folder_size

    return (file_types, file_sizes, all_files, duplicate_names, duplicate_sizes, subfolders_sizes, folder_count)

# Plot pie chart for file types and space occupied
def plot_file_types(file_sizes):
    labels = [f"{ext if ext else 'Unknown'} ({format_size(size)})" for ext, size in file_sizes.items()]
    sizes = list(file_sizes.values())

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Space Occupied by File Types")
    plt.show()

# Main function to execute
def main():
    folder_path = input("Enter the folder path to analyze: ")

    (file_types, file_sizes, all_files, duplicate_names, duplicate_sizes, subfolders_sizes, folder_count) = analyze_folder(folder_path)

    # Sort files by size (largest to smallest)
    all_files_sorted = sorted(all_files, key=lambda x: x[1], reverse=True)

    # List of redundant files by name
    redundant_by_name = {name: paths for name, paths in duplicate_names.items() if len(paths) > 1}

    # List of redundant files by size
    redundant_by_size = {size: paths for size, paths in duplicate_sizes.items() if len(paths) > 1}

    # Sort subfolders by size
    subfolders_sorted = sorted(subfolders_sizes.items(), key=lambda x: x[1], reverse=True)

    # Display Total Number of Subfolders
    print(f"\nTotal Number of Subfolders: {folder_count}\n")

    # Display Top 10 Largest Files
    print("Top 10 Largest Files (from largest to smallest):")
    for file, size in all_files_sorted[:10]:
        print(f"{file}: {format_size(size)}")

    # Redundant Files (Same Name)
    if redundant_by_name:
        print("\nRedundant Files (Same Name):")
        for name, paths in redundant_by_name.items():
            print(f"{name}:")
            for path in paths:
                print(f"  {path}")
    else:
        print("\nNo Redundant Files with Same Name.")

    # Redundant Files (Same Size)
    if redundant_by_size:
        print("\nRedundant Files (Same Size):")
        for size, paths in redundant_by_size.items():
            print(f"{format_size(size)}:")
            for path in paths:
                print(f"  {path}")
    else:
        print("\nNo Redundant Files with Same Size.")
        
    # Total number of redundant files and total size occupied by redundant files
    redundant_files_total_count = 0
    redundant_files_total_size = 0

    # Calculate total redundant files by name
    for paths in redundant_by_name.values():
        redundant_files_total_count += len(paths)
        for path in paths:
            redundant_files_total_size += os.path.getsize(path)

    # Calculate total redundant files by size
    for size, paths in redundant_by_size.items():
        redundant_files_total_count += len(paths)
        for path in paths:
            redundant_files_total_size += os.path.getsize(path)

    print(f"\nTotal number of redundant files: {redundant_files_total_count}")
    print(f"Total size occupied by redundant files: {format_size(redundant_files_total_size)}")            

    # Display Largest to Smallest Subfolders
    print("\nSubfolders (from largest to smallest):")
    for folder, size in subfolders_sorted:
        print(f"{folder}: {format_size(size)}")

    # Plot File Types based on Space Occupied
    plot_file_types(file_sizes)

if __name__ == "__main__":
    main()
