# 		Cpp Watchdog

This is a simple Python program for **C++** projects. It watches changes in your files and runs build and tests, using [CMake](https://cmake.org/) and [Googletest](https://github.com/google/googletest).

**Cpp Watchdog** also provides pretty interface using [curses](https://docs.python.org/3/howto/curses.html) library.

> Probably, this isn't a good tool for big projects, where it takes too much time to rebuild project. But in small and middle projects it looks pretty nice.

## Project requirements

Your **C++** project should have the next features to successfully use `Cpp Watchdog`:

1. Unix-like system
2. CMake
3. Googletest

See also `example` folder.

## Usage

### Basic

1. (Only once) you have to configure project via `CMake`. Some IDE does it for you, but you also can run something like:

   ```bash
   cmake -Bbuild .
   ```

2. Then run **Cpp Watchdog** and provide your test binary file (more about flags later):

   ```bash
   cpp-watchdog --test-bin=build/test/awsome_lib_test
   ```

3. All done! Now every time you change source (or other) file, watchdog will run build and tests, providing beautiful output.

### Flags and arguments

| Flag                | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| -c,  --config       | Specifies path to the config file (see below). Default is `~/.cppw.json` |
| -b, --build-command | Specifies build command. Default is `cmake --build build --config Debug --target all -- -j 10` |
| -t, --test-bin      | Specifies path to the test binary file from Googletest. Default is `./build/test/test` |
| -i, --ignore        | Specifies files to ignore with regular expression. Default is `\./build/*`. Attention: all paths should starts with watching directory prefix, including `.`. |

Don't forget to add `=` sign after long options!

As *arguments* **Cpp watchdog** takes folders and files to watch. By default it watches current folder. All folders are being watched recursively.

### Configuration file

If you don't want to always type these long options you can use a *config file* to specify it once! It also supports different options for different projects. Config structure is next:

```json
{
  "path/to/project" : {
    "build-command" : "...",
    "test-bin" : "...",
    "files" : [
      "...",
      "..."
    ],
    // By using config you can specify more than one regex to ignore
    "ignore" : [
      "...",
      "..."
    ]
  },
  
  "path/to/other/project" : {
    ...
  }
}
```

## About CMake Generators & Build Systems

*CMake* can generate a lot of different build files for different build systems.

This project was tested only with [Unix Makefiles](https://cmake.org/cmake/help/latest/generator/Unix Makefiles.html) and [Ninja](https://cmake.org/cmake/help/latest/generator/Ninja.html).

## Known issues

Per-file watching is only supported on Linux cause of [watchdog](https://github.com/gorakhargosh/watchdog) library has it implemented only for [pyinotify](http://github.com/seb-m/pyinotify), which is a Linux notifying system.

So, on Mac you can only watch directories, but this doesn't seem like a big problem, because you can always specify which files to ignore, if you want to.



