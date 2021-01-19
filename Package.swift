// swift-tools-version:5.3
import PackageDescription

let zipFileDestination = "https://github.com/royjit/aws-sdk-ios/releases/download/1.0.1/aws-sdk-ios-carthage.framework.zip"

let checksum = "761e24623af8e812f9f596e357eeff7044b6b4074c1591e3a6fc65fe74056b54"

let package = Package(
    name: "AWSiOSSDKV2",
    platforms: [
        .iOS(.v9)
    ],
    products: [
        .library(
            name: "AWSCore",
            targets: ["AWSCore"]),
        .library(
            name: "AWSMobileClientXCF",
            targets: ["AWSMobileClientXCF"])    
            
    ],
    targets: [
        .binaryTarget(
            name: "AWSCore",
            url: zipFileDestination,
            checksum: checksum
        ),
        .binaryTarget(
            name: "AWSMobileClientXCF",
            url: zipFileDestination,
            checksum: checksum
        )
    ]
)

