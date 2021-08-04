NOTE: This issue can be resolved by adding `parallel_show_output = true` to
your tox environment; it's still very strange that this behavior is the
default, though.

---

Tox's parallel output isn't buffered.

The script in `tox_parallel_example/__main__.py` writes a color, a random
number of `#` characters, and then resets the color; the color is specified in
command-line arguments.

The tox file `tox.ini` runs that script twice; once with a green foreground
color and a foreground color reset, and once with a blue background color and a
background color reset. When invoked with `tox --parallel --parallel-live`,
both commands write to the same STDOUT stream, and, because they're not managed
at all, output is interwoven.

If Tox correctly line-buffered output between the two commands, the output
would be sequences of green-on-black `#` characters and sequences of
white-on-blue `#` characters, like so:

![Sequences of green-on-black pound sign characters interleaved with sequences of
white-on-blue pound sign characters](./buffered_output.png)

However, Tox just lets both commands write to the same stream, even within
lines, so the actual result is much messier:

![Pound sign characters, numbers, and left-brackets in a variety of colors and
backgrounds.](./unbuffered_output.png)

To simulate the buffered output, you can use `tox --parallel --parallel-live --
--buffered` to not flush stdout between each character written, reducing the
likelihood of the two streams overwriting each other, but note that because the
bug lies in Tox, the problem isn't removed, just mitigated; in this image, we
can see Tox's own output interleaved with one of the commands, even in `--
--buffered` mode:

![Tox's log messages interwoven with white pound sign characters on a blue
background.](./buffered_output_bug.png)

If Tox captures its subcommands' output and prints them itself, either
interleaved with a header showing which line came from which test environment,
or printing the output from an entire environment once each environment is
finished running, this problem will be solved.
