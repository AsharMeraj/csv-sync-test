import time
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil

# Folder where CSVs are generated
SOURCE_FOLDER = r"D:\Demographic and Vitals Showcase\Patient_Dashboard-master\template\public\data"

# Local repo folder
REPO_PATH = r"D:\Demographic and Vitals Showcase\Patient_Dashboard-master\template\public\data\csv-sync-test"

# CSV files to watch
FILES_TO_WATCH = [
    "demographic_data2.csv",
    "MRayDataExport.csv"
]

repo = git.Repo(REPO_PATH)

class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        file_name = os.path.basename(event.src_path)
        if file_name in FILES_TO_WATCH:
            print(f"Detected change in {file_name}")
            try:
                # Copy both CSVs into repo
                for f in FILES_TO_WATCH:
                    shutil.copy(os.path.join(SOURCE_FOLDER, f), os.path.join(REPO_PATH, f))

                repo.git.add(all=True)
                repo.index.commit(f"Auto update: {', '.join(FILES_TO_WATCH)}")
                origin = repo.remote(name="origin")
                origin.push()
                print(f"Pushed {', '.join(FILES_TO_WATCH)} to GitHub ✅")
            except Exception as e:
                print(f"Push failed: {e}")

if __name__ == "__main__":
    event_handler = CSVHandler()
    observer = Observer()
    # Watch the SOURCE_FOLDER where CSVs are generated
    observer.schedule(event_handler, path=SOURCE_FOLDER, recursive=False)
    observer.start()
    print("Watching for CSV updates...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
