# Sublime Stata

**Author**: Daniel Fernandes<br>
**Contact**: daniel.fernandes@eui.eu

This package adds some Stata functionality to Sublime Text. It is based on two other packages already available for the platform:

- [Stata Enhanced](https://github.com/andrewheiss/SublimeStataEnhanced), *by Andrew Heiss*
- [Stata Improved Editor](https://github.com/zizhongyan/StataImproved), *by Zizhong Yan*

#### Features removed

- Dropped Windows support (Stata Enhanced only)
- Dropped Matlab-style code blocks (Stata Improved Editor only)
- Dropped support for Stata 11 and Stata 12

#### Features added

- Combines support for interactive mode (<kbd>cmd</kbd> + <kbd>enter</kbd>) and script mode (<kbd>shift</kbd> + <kbd>cmd</kbd> + <kbd>enter</kbd>) or (<kbd>control</kbd> + <kbd>cmd</kbd> + <kbd>enter</kbd>)
- Interactive mode now correctly removes whitespaces when spaces are used for indentation
- Tweaked syntax highlighting for Stata
- Added syntax highlighting for Mata
- Added syntax highlighting for dynamic documents
- Added syntax highlighting for Stata Help Files
- Calling python and mata in .do files changes syntax highlighting dynamically

#### Syntax Specific Settings

For a better experience in .dyndoc and .sthlp files, copy and paste these options to `Settings - Syntax Specific`:

```json
{
  "draw_centered": true,
  "word_wrap": true,
  "wrap_width": 80,
  "highlight_line": false,
  "line_padding_top": 2,
  "line_padding_bottom": 2,
  "gutter": false,
}
```


