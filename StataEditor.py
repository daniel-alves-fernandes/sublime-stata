import os, codecs, tempfile, subprocess, time, re
import sublime_plugin, sublime

switch_focus = "activate"

class StataLocal(sublime_plugin.TextCommand):
  def run(self,edit):
    sels = self.view.sel()
    for sel in sels:
      if len(sel) == 0:
        word_sel = self.view.word(sel.a)
      else:
        word_sel = sel
      word_str = self.view.substr(word_sel)
      word_str = "`"+word_str+"'"
      self.view.replace(edit,word_sel,word_str)
class StataMacro(sublime_plugin.TextCommand):
  def run(self,edit):
    sels = self.view.sel()
    for sel in sels:
      if len(sel) == 0:
        word_sel = self.view.word(sel.a)
      else:
        word_sel = sel
      word_str = self.view.substr(word_sel)
      word_str = "${"+word_str+"}"
      self.view.replace(edit,word_sel,word_str)
class StataToggle(sublime_plugin.TextCommand):
  def run(self,edit):
    sels = self.view.sel()
    for sel in sels:
      if len(sel) == 0:
        word_sel = self.view.word(sel.a)
      else:
        word_sel = sel
      word_str = self.view.substr(word_sel)
      word_str = "/* "+word_str+" */"
      self.view.replace(edit,word_sel,word_str)

def get_stata_version():
    cmd = """osascript<< END
      try
        tell me to get application id "com.stata.stata13"
        set stata to 13
        end try
      try
        tell me to get application id "com.stata.stata14"
        set stata to 14
        end try
      try
        tell me to get application id "com.stata.stata15"
        set stata to 15
        end try
      try
        tell me to get application id "com.stata.stata16"
        set stata to 16
        end try
      try
        tell me to get application id "com.stata.stata17"
        set stata to 17
        end try
      return stata
      END"""
    try:
        version = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        sublime.error_message("No version of Stata found.")
        raise Exception("No version of Stata found.")
    version = version.decode("utf-8").strip()
    return((int(version), "com.stata.stata{}".format(version)))

def strip_inline_comments(text):
  clean = text
  clean = re.sub("/{3,}.*\\n", " ", clean)
  def remove_comments(string):
    pattern = r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
    def _replacer(match):
      if match.group(2) is not None:
        return ""
      else:
        return match.group(1)
    return regex.sub(_replacer, string)
  clean = remove_comments(clean)
  return(clean)
class LinesStataInteractive(sublime_plugin.TextCommand):
  def run(self, edit):
    selectedcode = ""
    sels = self.view.sel()
    for sel in sels:
      selectedcode = selectedcode + self.view.substr(sel)
    if len(selectedcode) == 0:
      selectedcode = self.view.substr(self.view.line(sel))
    selectedcode = selectedcode + "\n"
    selectedcode = strip_inline_comments(selectedcode)
    selectedcode = selectedcode.replace('\\', '\\\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', "\\$").strip()
    selectedcode = " ".join(re.split(" +", selectedcode, flags=re.UNICODE))
    version, stata_app_id = get_stata_version()
    cmd = """osascript<< END
     tell application id "{0}"
      {1}
      DoCommandAsync "{2}" with addToReview
     end tell
     END""".format(stata_app_id,switch_focus,selectedcode)
    print(cmd)
    print("stata_app_id")
    print(stata_app_id)
    os.system(cmd)

class LinesStataDo(sublime_plugin.TextCommand):
  def run(self, edit):
    selectedcode = ""
    sels = self.view.sel()
    for sel in sels:
      selectedcode = selectedcode + self.view.substr(sel)
    if len(selectedcode) == 0:
      selectedcode = self.view.substr(self.view.line(sel))
    dofile_path = tempfile.gettempdir()+'/sublime.do'
    with codecs.open(dofile_path, 'w', encoding='utf-8') as out:
        out.write(selectedcode)
    version, stata_app_id = get_stata_version()
    cmd = """osascript<< END
     tell application id "{0}"
        {1}
        DoCommandAsync "do {2}"  with addToReview
     end tell
     END""".format(stata_app_id,switch_focus,dofile_path)
    print(cmd)
    print("stata_app_id")
    print(stata_app_id)
    os.system(cmd)
class LinesStataRun(sublime_plugin.TextCommand):
  def run(self, edit):
    selectedcode = ""
    sels = self.view.sel()
    for sel in sels:
      selectedcode = selectedcode + self.view.substr(sel)
    if len(selectedcode) == 0:
      selectedcode = self.view.substr(self.view.line(sel))
    dofile_path = tempfile.gettempdir()+'/sublime.do'
    with codecs.open(dofile_path, 'w', encoding='utf-8') as out:
        out.write(selectedcode)
    version, stata_app_id = get_stata_version()
    cmd = """osascript<< END
     tell application id "{0}"
      {1}
      DoCommandAsync "run {2}" with addToReview
     end tell
     END""".format(stata_app_id,switch_focus,dofile_path)
    print(cmd)
    print("stata_app_id")
    print(stata_app_id)
    os.system(cmd)

class StataHelpCommand(sublime_plugin.TextCommand):
  def run(self,edit):
    self.view.run_command("expand_selection", {"to": "word"})
    sel = self.view.sel()[0]
    help_word = self.view.substr(sel)
    version, stata_app_id = get_stata_version()
    cmd = """osascript<< END
     tell application id "{0}"
      activate
      DoCommandAsync "help {1}" with addToReview
     end tell
     tell application "{2}"
      activate
     end tell
     END""".format(stata_app_id,help_word,"Viewer")
    os.system(cmd)
class StataBrowse(sublime_plugin.TextCommand):
  def run(self,edit):
    self.view.run_command("expand_selection", {"to": "word"})
    sel = self.view.sel()[0]
    varlist = self.view.substr(sel)
    version, stata_app_id = get_stata_version()
    cmd = """osascript<< END
     tell application id "{0}"
      activate
      DoCommandAsync "browse {1}" with addToReview
     end tell
     tell application "{2}"
      activate
     end tell
     END""".format(stata_app_id,varlist,"Viewer")
    os.system(cmd)
class InsertDatetimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel();
        for s in sel:
            self.view.replace(edit, s, time.ctime())
