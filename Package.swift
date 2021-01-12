// swift-tools-version:5.3
import PackageDescription

let sdkVersion = "2.22.0"
let checksum = "a81b741b2ecf8644dfa90c43ebd4b41cd87f3c621ab2dd84b3b3022491678509"
let zipFileURL = "https://sdk-for-ios.amazonwebservices.com/aws-ios-sdk-\(sdkVersion).zip"

let package = Package(
    name: "AWSiOSSDKV2",
    platforms: [
        .iOS(.v9)
    ],
    products: [
        .library(
            name: "AWSCore",
            targets: ["AWSCore"])
    ],
    targets: [
        .binaryTarget(
            name: "AWSCore",
            url: zipFileURL,
            checksum: checksum
        )
    ]
)