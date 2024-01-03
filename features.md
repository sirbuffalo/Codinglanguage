# Programming Language Features
## Good
### AST Library
* [Go `ast`](https://pkg.go.dev/go/ast)
  * API is really complex
### Compile-Time Code Generation
* [Go `generate`](https://go.dev/blog/generate)
  * Compiles from strings -- AST or hybrid would be nicer
  * Or some inline generation syntax?
### Runtime Code Generation
* [C libtcc](https://bellard.org/tcc/)
  * Compiles from strings -- AST or hybrid would be nicer
  * Or some inline generation syntax?
### Reflection
* [Go `reflect`](https://pkg.go.dev/reflect)
### Struct Tags
* [Go struct tags](https://pkg.go.dev/reflect#StructTag)
### Decorators
* [Python decorators](https://peps.python.org/pep-0318/)
### Automatic Object-Level Concurrency Isolation
* [Swift `actor`](https://developer.apple.com/documentation/swift/actor)
  * This is broken for `async`
### Reference Counting
* [Python garbage collector](https://devguide.python.org/internals/garbage-collector/)
* [Swift automatic reference counting](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/)
### Channels
* [Go channel basics](https://go.dev/tour/concurrency/2)
* [Go channel buffering](https://go.dev/tour/concurrency/3)
  * The constant here has always seemed a bit sloppy
  * Usually you want 0, 1, or infinite
* [Go channel `range`, `close`](https://go.dev/tour/concurrency/4)
### Inclusive and Exclusive Range
* [Swift range](https://developer.apple.com/documentation/swift/range)
### Select
* [Go `select`](https://go.dev/tour/concurrency/5)
* [Go `select` default](https://go.dev/tour/concurrency/6)
### Hidden Event Loop Singleton
* [libuv](https://docs.libuv.org/en/v1.x/api.html)
  * Efficient (epoll on Linux, kqueue on Darwin/BSD)
  * Timeouts (min heap)
  * File descriptors
  * Signals ([signalfd](https://man7.org/linux/man-pages/man2/signalfd.2.html) on Linux)
  * Processes ([pidfd](https://man7.org/linux/man-pages/man2/pidfd_open.2.html) on Linux)
### Async Semaphore / Mutex
* [JavaScript async mutex](https://www.npmjs.com/package/async-mutex)
### Async Sleep
* [Python `asyncio.sleep` vs `time.sleep`](https://stackoverflow.com/questions/56729764/asyncio-sleep-vs-time-sleep)
### Every Value Can Hold An Error
* [C++ `ErrorOr<>`](https://grammatech.github.io/gtirb/cpp/classgtirb_1_1_error_or.html)
* Should propagate up automatically
  * Attempt to operate on an error value returns immediately with the same error
### Composable Errors
* [Go ￼`errors.Join`￼](https://pkg.go.dev/errors#Join)
* [Go `errors.As`](https://pkg.go.dev/errors#As)
### List Comprehensions
* [Python list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
* Encapsulates filter and map
### Type Inference In All Directions
* Function arguments (bidirectional)
* Return types (bidirectional)
### Trailing Closure Syntax
* [Swift trailing closure syntax](https://www.hackingwithswift.com/example-code/language/what-is-trailing-closure-syntax)
### Automatic Parallelization
* [Wikipedia: Automatic parallelization](https://en.wikipedia.org/wiki/Automatic_parallelization)
### Protocols
* [Swift protocols](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/)
### Any Type
* [Go `any`](https://medium.com/@curiousinquirer/gos-any-the-type-that-can-hold-anything-2d0528b1133)
### Automatic Named Tuple Types
* [Swift tuples](https://abhimuralidharan.medium.com/tuple-in-swift-a9ddeb314c79)
### Argument Name Overloading
* [Swift argument name overloading](https://www.includehelp.com/swift/implement-function-overloading-based-on-argument-label.aspx)
## Bad
### Explicit `async`/`await`
* Should be automatic like Go
* [Swift `async`/`await`](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)
* [JavaScript `async`/`await`](https://javascript.info/async-await)
### Explicit `try`
* Should be automatic like JavaScript
* [Swift `try`](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/)
### Explicit range
* Should be automatic like [Swift](https://developer.apple.com/documentation/swift/range)
* [Go `range`](https://go.dev/tour/moretypes/16)
### Getters & Setters
* Function calls should look like function calls
* [Swift computed properties](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/properties/#Computed-Properties)
