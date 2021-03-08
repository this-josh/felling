# Design philosophy

## Dependencies
*   Wherever possible dependencies must be avoided. Felling is intended to always be used and must therefore be as lightweight as possible

## Errors
*   If a process is specifically requested, such as package_versions_to_log then errors should be raised
*   If a process is default operation of felling, such as _get_git_commit_hash errors should be handled and logs written

## Tests
*   As felling is intended to be used everywhere it must have comprehensive tests