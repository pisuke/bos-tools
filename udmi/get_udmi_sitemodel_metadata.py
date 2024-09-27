#!/usr/bin/env python3

import subprocess
from absl import flags
from absl import app
import os
import shutil

FLAGS = flags.FLAGS

flags.DEFINE_string('site_id', None, 'ID of the site', required=True)
flags.DEFINE_string('repo_url', None, 'URL of the private Git repository', required=True)
flags.DEFINE_string('destination_path', './destination_folder', 'Destination path for the cloned repository')

def clone_git_repo(repo_url, destination_path, site_id):
    """Clones a private Git repo to a specified destination."""
    cloned_repos_folder = os.path.join(destination_path,"cloned_repos")
    if not os.path.exists(cloned_repos_folder):
        os.makedirs(cloned_repos_folder)
    site_model_folder = os.path.join(cloned_repos_folder, site_id)
    subprocess.run(["git", "clone", repo_url, site_model_folder], check=True)

def copy_metadata_files(source_dir, destination_dir):
    """Copies files with specified names from the source directory to the destination directory, maintaining the folder structure."""
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        destination_sub_dir = os.path.join(destination_dir, relative_path)
        os.makedirs(destination_sub_dir, exist_ok=True)
        for f in files:
            if f == "metadata.json" or f == "site_metadata.json" or f == "cloud_iot_config.json":
                print(os.path.join(root, f))
                shutil.copy(os.path.join(root, f), os.path.join(destination_sub_dir, f))

def main(argv):
    # flags.parse()

    site_id = FLAGS.site_id
    repo_url = FLAGS.repo_url
    destination_path = FLAGS.destination_path

    print(site_id)
    print(repo_url)
    print(destination_path)

    clone_git_repo(repo_url, destination_path, site_id)
    site_model_folder = os.path.join(destination_path,"cloned_repos", site_id)
    metadata_folder = os.path.join(destination_path,"metadata_repos", site_id)
    copy_metadata_files(site_model_folder, metadata_folder)
    
if __name__ == "__main__":
    app.run(main)
