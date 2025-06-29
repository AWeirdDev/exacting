# Result

The `Result` class indicates the success/failure of validation.

```python
from exacting import Result

# Success
Result.Ok("some value")

# Error
Result.Err(
    "You bad",
    "literally"
)
```

## Is OK?

This checks if the validation result is OK.

```python
if some_result.is_ok():
    ... # good!
else:
    ... # bad!
```

## Raising

`Result` can help you raise a `ValidationError` if errors are present.

```python
some_result.raise_for_err()
```

## Unwrapping

You can get the data that got through the validation by unwrapping, or the error messages.

```python
ok = Result.Ok(-123)
print(ok.unwrap())  # -123

err = Result.Err("be be nos")
print(err.unwrap_err())  # deque(['be be nos'])
```

## Trace

You can trace errors down using the `trace()` function, making previous errors appear indented.

```python
base_err = Result.Err("Gustavo Fring")

(
    base_err
        .trace("Woah, there's a gustavo down here")
        .trace("Breaking bad!")
        .raise_for_err()
)
```

??? failure "ValidationError: Breaking bad!"

    ```
    ValidationError: 
    Breaking bad!
      • Woah, there's a gustavo down here
        • Gustavo Fring
    ```

## Trace below

Make other errors appear indented below your message.

```python
error1 = Result.Err("ooga", "booga")
error2 = Result.trace_below(
    "Check these out:",
    *error1.unwrap_err()
)

error2.raise_for_err()
```

??? failure "ValidationError: Check these out:"

    ```
    ValidationError: 
    Check these out:
      • ooga
      • booga
    ```
