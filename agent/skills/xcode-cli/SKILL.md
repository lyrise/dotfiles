---
name: xcode-cli
description: Rules for iOS/macOS development with xcodebuild, swift, simctl, devicectl, and xcresulttool, without depending on launching Xcode or opening the project beforehand. Covers detecting the project, scheme, and destination; building, testing, and diagnosing; running on Simulator and physical devices; screenshots; and adding files with XcodeGen and to .xcodeproj. Use when asked to build, test, investigate errors in, check the screens of, or run in the simulator Swift/SwiftUI code, or when working in a project that contains .xcodeproj/.xcworkspace/Package.swift/project.yml.
---

# Apple Platform Development with the Xcode CLI

Do not depend on whether the Xcode app is running or which scheme is selected in it.
Treat the repository's configuration as the source of truth, and use `xcodebuild`, `swift`,
`xcrun simctl`, `xcrun devicectl`, and `xcrun xcresulttool`.

Treat a successful build, passing tests, behavior on Simulator, and behavior on a physical
device as separate pieces of evidence.
Do not report a stage that was not run as if it succeeded.

## Check First

At the start of work, check the selected toolchain and the required CLIs.

```bash
xcode-select -p
xcodebuild -version
xcrun --find simctl
xcrun --find xcresulttool
```

When several Xcode installations exist, set `DEVELOPER_DIR` only for the commands that need it.
Do not run a system-wide `xcode-select --switch` unless explicitly asked.

Look for `Package.swift`, root-level `.xcworkspace`, `.xcodeproj`, and `project.yml` in the
repository. Do not count `.xcodeproj/project.xcworkspace` as a separate workspace.

Choose as follows.

- If there is a workspace for an Apple app, use the `.xcworkspace`
- If there is no workspace, use the `.xcodeproj`
- For work on a standalone Swift package, use `Package.swift` and `swift`
- If there are several candidates and the target cannot be identified from the repository, ask the user

Do not guess the scheme or destination. List them first.

```bash
xcodebuild -list -json -workspace App.xcworkspace
xcodebuild -workspace App.xcworkspace -scheme App -showdestinations
```

When using an `.xcodeproj`, replace `-workspace App.xcworkspace` with
`-project App.xcodeproj`.
For a build that needs no runtime environment, use a generic destination such as
`-destination 'generic/platform=iOS Simulator'`.
For tests and launches, use an available ID obtained from `-showdestinations` or `simctl list`.

## Swift Package

When a standalone Swift package is enough, do not go through an Xcode project.

```bash
swift build
swift test
swift test list
swift test --filter 'TargetName.TestType/testName'
```

For work that must pin `Package.resolved`, confirm that it exists and whether it is meant to be
updated, then use `--only-use-versions-from-resolved-file`. Do not implicitly mix in dependency
updates or network access.

## Building and Testing

State the workspace or project, scheme, configuration, and destination explicitly in the command.

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Debug \
  -destination 'generic/platform=iOS Simulator' \
  build
```

For tests, save the result bundle and the log to a temporary directory. Do not reuse a fixed path;
create the directory first with `mktemp -d /tmp/xcode-cli.XXXXXX`.

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  -resultBundlePath "$task_tmp_dir/Test.xcresult" \
  test >"$task_tmp_dir/xcodebuild.log" 2>&1
```

When rerunning all tests is expensive, enumerate the tests and run only the relevant ones.

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  test -enumerate-tests \
  -test-enumeration-format json \
  -test-enumeration-output-path -

xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  -only-testing:AppTests/TestType/testName \
  test
```

To separate building from testing, use `build-for-testing` followed by `test-without-building`.
Use the same container, scheme, destination, configuration, and `-derivedDataPath` for both.

Add `-onlyUsePackageVersionsFromResolvedFile` only when `Package.resolved` is authoritative and
dependency updates are not allowed. Do not add `-skipMacroValidation`,
`-skipPackagePluginValidation`, or options that weaken signature verification by default.

## Diagnosis

First check the command's exit status and the main result, such as `** BUILD SUCCEEDED **` /
`** TEST SUCCEEDED **`. Do not conclude failure from `DVTFilePathFSEvents` or cache-related
warnings alone.

When a result bundle exists, prefer the structured results.

```bash
xcrun xcresulttool get build-results \
  --path "$task_tmp_dir/Build.xcresult"

xcrun xcresulttool get test-results summary \
  --path "$task_tmp_dir/Test.xcresult"
```

Narrow down the log as a supplement.

```bash
rg -n 'error:|warning:|failed|FAIL' "$task_tmp_dir/xcodebuild.log" | head -50
```

Do not paste the full log into the conversation. Report the first real error, the affected file and
location, the exit status, and which stages succeeded or were not run. Passing compilation does not
guarantee UI or on-device behavior.

## Running on Simulator and Checking Screens

List the available Simulators as JSON and keep the ID, not the device name.

```bash
xcrun simctl list devices available --json
xcrun simctl boot SIMULATOR_ID
xcrun simctl bootstatus SIMULATOR_ID -b
```

If a device is already booted, do not `boot` it again; use its ID. If the Simulator service cannot
be reached, do not assume permissions are the only cause; preserve the reported service, runtime,
or disk image error.

Get the app bundle location and bundle identifier by running `xcodebuild -showBuildSettings -json`
with the same container, scheme, and destination, and reading `TARGET_BUILD_DIR`, `WRAPPER_NAME`,
and `PRODUCT_BUNDLE_IDENTIFIER`.

```bash
xcrun simctl install SIMULATOR_ID /path/to/App.app
xcrun simctl launch SIMULATOR_ID com.example.app
xcrun simctl io SIMULATOR_ID screenshot "$task_tmp_dir/screenshot.png"
```

For SwiftUI appearance, put the real app or a dedicated snapshot/UI test into the target state and
check the image from `simctl io ... screenshot`.
If the app cannot be launched, report the screen check as not done.

## Running on a Physical Device

When a physical device is needed, use `devicectl`. For results read by automation, use the
`--json-output` file, not stdout.

```bash
xcrun devicectl list devices --json-output "$task_tmp_dir/devices.json"
xcrun devicectl device install app --device DEVICE_ID /path/to/App.app
xcrun devicectl device process launch \
  --device DEVICE_ID --terminate-existing com.example.app
```

Do not register devices, change signing assets, or delete apps on your own. `-allowProvisioningUpdates`
can make changes to the Developer Portal, so confirm the need and the target before using it.

## Checking Swift Snippets

Check short code that does not depend on the project with `swift -e`.

```bash
swift -e 'import Foundation; print(ProcessInfo.processInfo.operatingSystemVersion)'
```

Check code that depends on the app's types, resources, or build settings with an existing or newly
added targeted test. Do not leave Git-tracked temporary files or verification-only targets behind
without permission.

Do not refer to the file or selection currently open in the GUI; identify the target from the
repository and the request. If it cannot be identified, ask for the file path or symbol name.

## Adding Files

Check how new files get into a target before adding them.

**When `project.yml` exists**

Treat the `.xcodeproj` as a generated artifact. Check `sources` and `excludes` in `project.yml`,
add the file to the relevant directory, and run `xcodegen generate`.
Do not edit only the generated `.pbxproj` directly.

**When there is no `project.yml`**

If the `.pbxproj` has a `PBXFileSystemSynchronizedRootGroup` and the target directory is
synchronized, add the file under it and confirm inclusion with a build.

For a project with classic groups, use the generator or management tool the repository already uses,
such as `xcodeproj`, if there is one. Otherwise, update the `.pbxproj` to match the format of the
surrounding `PBXFileReference`, `PBXBuildFile`, group, and build phase entries. After the change,
confirm the structure and target membership with `plutil -lint`, `xcodebuild -list`, and a build of
the target.

Edit existing files on the file system as usual.

## Do Not

- Decide the scheme, destination, or Simulator name without a basis
- Make options that weaken security validation the default for the sake of speed
- Automatically delete existing Simulators, devices, or installed apps
- Lump build, test, runtime, and on-device checks into a single "verified working"
- Bring the full build log into the conversation
