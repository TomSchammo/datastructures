# Datastructures

A small repository containing an array of datastructures for my personal use.

## Features

### Result

The `Result` datastructure can be used to run functions that are expected/can
throw and Exception.

The return value of the function (if it ran successfully) is saved and can be accessed
using the `get`, `get_or` or `get_or_any` methods.

The exception can be raised using the `raise_error` function.
The type can be accessed using the internal `_get_error_type` function.

This is kind of inspired by my understanding of the `Result` of the Rust language.

## Roadmap

*   \[ ] Allow `Result`s to only catch a specific exception.
