import os
import sys
import shutil

from functions import log, run_command

XCFRAMEWORK_PATH = "./output/XCF/"

project_dir = os.getcwd()
log(f"Creating Carthage archive in {project_dir}")

framework_file_name = "aws-sdk-ios-carthage.framework"

shutil.make_archive(framework_file_name, 'zip', XCFRAMEWORK_PATH)
