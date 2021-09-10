# Docassemble-Mailgun

This package makes it easy to use advanced Mailgun features with docassemble.
This is useful first and foremost for using Mailgun templates but also for using
multiple Mailgun configurations in multiple interviews.

## Usage
The library provides a simple interface that can be instaciated as follows:

```python
from docassemble.mailgun import Mailgun

mailgun = Mailgun()
mailgun.send_email(...)
```

The `send_email` method takes the same parameters as docassemble's native
function.

## Debugging

You can supply values for any configuration value directly
instead of using the docassemble configuration. This may be useful when testing
your code locally.