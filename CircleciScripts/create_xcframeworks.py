import os
import sys

from framework_list import frameworks
from functions import log, run_command

EXCLUDE_FROM_XCFRAMEWORK = [
    # This isn't a real framework
    "AWSiOSSDKv2",
    # Legacy frameworks not built or packaged
    "AWSAuth",
    # AWSMobileClient is named as AWSMobileClientXCF and will be added later.
    "AWSMobileClient",
]

IOS_DEVICE_ARCHIVE_PATH = "./output/iOS/"
IOS_SIMULATOR_ARCHIVE_PATH = "./output/Simulator/"
XCFRAMEWORK_PATH = "./output/XCF/"

def is_framework_included(framework):
    return framework not in EXCLUDE_FROM_XCFramework

def create_archive(framework, projectFile, isDevice):
    if isDevice:
        archivePath = IOS_DEVICE_ARCHIVE_PATH + framework
        destination = "generic/platform=iOS"
    else:
        archivePath = IOS_SIMULATOR_ARCHIVE_PATH + framework
        destination = "generic/platform=iOS Simulator"
    cmd = [
        "xcodebuild",
        "archive",
        "-project",
        projectFile,
        "-scheme",
        framework,
        "-destination",
        destination,
        "-archivePath",
        archivePath,
        "SKIP_INSTALL=NO",
        "BUILD_LIBRARY_FOR_DISTRIBUTION=YES"

    ] 
    (exit_code, out, err) = run_command(cmd, keepalive_interval=300, timeout=7200)
    if exit_code == 0:
        log(f"Created iOS archive {framework}")
    else:
        log(f"Could not create XCFramework archive: {framework} output: {out}; error: {err}")
        sys.exit(exit_code)

def mapFrameworkToProject(frameworkList):
    frameworkMap = {}
    cmd = [
        "xcodebuild",
        "-project",
        "AWSiOSSDKv2.xcodeproj",
        "-list",
    ] 
    (exit_code, out, err) = run_command(cmd, keepalive_interval=300, timeout=7200)
    if exit_code == 0:
        log(f"List of schema found")
    else:
        log(f"Xcodebuild list failed: output: {out}; error: {err}")
        sys.exit(exit_code)

    for framework in frameworkList:
        if framework not in str(out):
            frameworkMap[framework] = "./AWSAuthSDK/AWSAuthSDK.xcodeproj"
        else:
            frameworkMap[framework] = "AWSiOSSDKv2.xcodeproj"
    return frameworkMap

project_dir = os.getcwd()
log(f"Creating XCFrameworks in {project_dir}")

framework_file_name = "aws-sdk-ios-xcframework.zip"

filtered_frameworks = list(filter(is_framework_included, frameworks))
filtered_frameworks.append("AWSMobileClientXCF")
frameworkMap = mapFrameworkToProject(filtered_frameworks)

# Archive all the frameworks.
for framework in filtered_frameworks:
    create_archive(framework, frameworkMap[framework], True)
    create_archive(framework, frameworkMap[framework], False)

# Create XCFramework using the archived frameworks.
for framework in filtered_frameworks:
    iosDeviceFramework = "{}{}.xcarchive/Products/Library/Frameworks/{}.framework".format(IOS_DEVICE_ARCHIVE_PATH, framework, framework)
    iosSimulatorFramework = "{}{}.xcarchive/Products/Library/Frameworks/{}.framework".format(IOS_DEVICE_ARCHIVE_PATH, framework, framework)
    xcframework = "{}{}.xcframework".format(XCFRAMEWORK_PATH, framework)
    cmd = [
            "xcodebuild",
            "-create-xcframework",
            "-framework",
            iosDeviceFramework,
             "-framework",
            iosSimulatorFramework,
            "-output",
            xcframework
        ] 
    (exit_code, out, err) = run_command(cmd, keepalive_interval=300, timeout=7200)
    if exit_code == 0:
        log(f"Created XCFramework for {framework}")
    else:
        log(f"Could not create XCFramework archive: {framework} output: {out}; error: {err}")
        sys.exit(exit_code)
