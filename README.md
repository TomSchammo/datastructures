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

### strict

The `strict` function is a function decorator that enforces type hints.

It raises a `TypeError` if the arguments do not have the correct types.

This feature is currently experimental and the current implementation has some problems
and is lacking some core features (see Issues #3 and #4).

I will update this once those are fixed.

## Installation

The module is currently not available on PyPi, so to install it, clone the repository (`git clone https://github.com/TomSchammo/datastructures`),
change into the cloned directory (`cd datastructures`) and install it locally by running `pip install .`.

## Roadmap

*   \[ ] Allow `Result`s to only catch a specific exception. See Issue #1 for details.
*   \[ ] Implement support for the `typing` module for the `strict` function decorator.
